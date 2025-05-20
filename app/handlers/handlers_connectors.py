import os

import kopf
import kubernetes.client
import pendulum
from kubernetes.client.models import V1ObjectMeta

from app.api import TwingateAPIClient
from app.crds import TwingateConnectorCRD
from app.handlers.base import fail, success
from app.settings import get_version
from app.utils_k8s import (
    k8s_delete_pod,
    k8s_read_namespaced_deployment,
    k8s_read_namespaced_pod,
)

ANNOTATION_LAST_VERSION_CHECK = "twingate.com/last-version-check"
ANNOTATION_NEXT_VERSION_CHECK = "twingate.com/next-version-check"


def get_connector_deployment(
    crd: TwingateConnectorCRD, tenant_url: str, image: str
) -> kubernetes.client.V1Deployment:
    spec = crd.spec
    name = crd.metadata.name

    connector_env_vars = []
    if spec.image_policy:
        connector_env_vars = [
            {
                "name": "TWINGATE_LABEL_VERSION_POLICY_SCHEDULE",
                "value": spec.image_policy.schedule,
            },
            {
                "name": "TWINGATE_LABEL_VERSION_POLICY_SPEC",
                "value": spec.image_policy.version,
            },
        ]

    if spec.log_analytics:
        connector_env_vars.append(
            {
                "name": "TWINGATE_LOG_ANALYTICS",
                "value": "v2",
            }
        )

    container_extra = spec.container_extra
    extra_env = container_extra.pop("env", [])
    extra_env_from = container_extra.pop("envFrom", [])

    pod_extra = spec.pod_extra
    extra_volumes = pod_extra.pop("volumes", [])
    extra_volume_mounts = container_extra.pop("volumeMounts", [])

    # fmt: off
    pod_annotations = spec.pod_annotations
    pod_selector_labels = {
        "app.kubernetes.io/name": "TwingateConnector",
        "app.kubernetes.io/instance": name,
    }
    pod_labels = spec.pod_labels | pod_selector_labels

    deployment_spec = {
        "replicas": 1,
        "selector": {
            "matchLabels": pod_selector_labels,
        },
        "strategy": {
            "type": "Recreate",
        },
        "template": {
            "metadata": {
                "annotations": pod_annotations,
                "labels": pod_labels,
            },
            "spec": {
                "containers": [
                    {
                        "env": [
                            {"name": "TWINGATE_LABEL_DEPLOYED_BY", "value": "operator"},
                            {"name": "TWINGATE_LABEL_OPERATOR_VERSION", "value": get_version()},
                            {"name": "TWINGATE_URL", "value": tenant_url},
                            {"name": "TWINGATE_LOG_LEVEL", "value": str(spec.log_level)},
                            *connector_env_vars,
                            *extra_env
                        ],
                        "envFrom": [{"secretRef": {"name": name, "optional": False}}, *extra_env_from],
                        "image": image,
                        "imagePullPolicy": "Always",
                        "name": "connector",
                        "securityContext": {
                            "allowPrivilegeEscalation": False,
                            "capabilities": {
                                "drop": ["ALL"],
                            },
                            "runAsNonRoot": True,
                            "runAsUser": 65532,
                            "seccompProfile": {
                                "type": "RuntimeDefault"
                            },
                            "readOnlyRootFilesystem": True,
                        },
                        "readinessProbe": {
                            "exec": {
                                "command": ["/connectorctl", "health"]
                            },
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5,
                        },
                        "livenessProbe": {
                            "exec": {
                                "command": ["/connectorctl", "health"]
                            },
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5,
                        },
                        "volumeMounts": [
                            {
                                "name": "twingate-socket",
                                "mountPath": "/var/run/twingate",
                            },
                            *extra_volume_mounts
                        ],
                        **container_extra,
                    },
                    *spec.sidecar_containers,
                ],
                "volumes": [{"name": "twingate-socket", "emptyDir": {}}, *extra_volumes],
                **spec.pod_extra,
            },
        },
    }

    deployment_meta = V1ObjectMeta(annotations=pod_annotations, labels=pod_labels)

    # fmt: on
    return kubernetes.client.V1Deployment(
        spec=deployment_spec, metadata=deployment_meta
    )


def get_connector_secret(
    access_token: str, refresh_token: str
) -> kubernetes.client.V1Secret:
    return kubernetes.client.V1Secret(
        immutable=True,
        string_data={
            "TWINGATE_ACCESS_TOKEN": access_token,
            "TWINGATE_REFRESH_TOKEN": refresh_token,
        },
    )


def delete_pre_deployment_pod_if_exists(
    namespace: str, name: str, kapi: kubernetes.client.CoreV1Api | None = None
):
    """Delete the pod if it exists. This is used to delete the old pod that was used before we switched to using Deployment objects."""
    if k8s_read_namespaced_pod(namespace, name, kapi=kapi):
        k8s_delete_pod(namespace, name, kapi=kapi, force=True)


def create_or_replace_deployment(
    body: kopf.Body,
    namespace: str,
    connector: TwingateConnectorCRD,
    tenant_url: str,
    *,
    kapi: kubernetes.client.AppsV1Api = None,
):
    kapi = kapi or kubernetes.client.AppsV1Api()
    expected_image = connector.spec.get_image()
    deployment = get_connector_deployment(connector, tenant_url, expected_image)
    kopf.adopt(deployment, owner=body, strict=True, forced=True)

    k8s_deployment = k8s_read_namespaced_deployment(
        namespace, connector.metadata.name, kapi_apps=kapi
    )
    if not k8s_deployment:
        kapi.create_namespaced_deployment(namespace, body=deployment)
        kopf.info(
            body,
            reason="Deployment created",
            message=f"Created connector deployment {namespace}/{connector.metadata.name} with image {expected_image}",
        )
        return

    kapi.replace_namespaced_deployment(
        connector.metadata.name, namespace, body=deployment
    )
    kopf.info(
        body,
        reason="Deployment patched",
        message=f"Updated deployment {namespace}/{connector.metadata.name} successfully",
    )


@kopf.on.resume("twingateconnector")
def twingate_connector_resume(body, namespace, **_):
    crd = TwingateConnectorCRD(**body)
    delete_pre_deployment_pod_if_exists(namespace, crd.metadata.name)
    return success(twingate_id=crd.spec.id)


@kopf.on.create("twingateconnector")
def twingate_connector_create(body, memo, logger, namespace, patch, **_):
    settings = memo.twingate_settings
    client = TwingateAPIClient(settings, logger=logger)

    logger.info("Got twingateconnector create request: %s", body)
    crd = TwingateConnectorCRD(**body)

    if not crd.spec.id:
        connector = client.connector_create(crd.spec)
        patch.spec["id"] = connector.id
        patch.spec["name"] = connector.name
    else:
        connector = client.get_connector(crd.spec.id)

    logger.info("connector: %s", connector)
    tokens = client.connector_generate_tokens(connector.id)

    secret = get_connector_secret(tokens.access_token, tokens.refresh_token)
    kopf.adopt([secret], owner=body, strict=True, forced=True)

    kapi = kubernetes.client.CoreV1Api()
    kapi.create_namespaced_secret(namespace=namespace, body=secret)

    return success(twingate_id=connector.id)


@kopf.on.update("twingateconnector", field=["spec"])
def twingate_connector_update(body, memo, logger, new, diff, status, namespace, patch, **_):
    logger.info(
        "Got TwingateConnector update request: %s. Diff: %s. Status: %s.",
        new,
        diff,
        status,
    )

    settings = memo.twingate_settings
    client = TwingateAPIClient(settings, logger=logger)

    crd = TwingateConnectorCRD(**body)
    # diff example: (('add', ('name',), None, 'whispering-petrel'), ('add', ('id',), None, 'Q29ubmVjdG9yOjEwMzkyMTI='))
    # but name could be missing
    if len(diff) == 1 and diff[0][:3] == ("add", ("id",), None):
        return success(twingate_id=crd.spec.id, message="No update required")

    if len(diff) == 2:
        diffs = [d[:3] for d in diff]
        if ("add", ("name",), None) in diffs and ("add", ("id",), None) in diffs:
            return success(twingate_id=crd.spec.id, message="No update required")

    if not crd.spec.id:
        return fail(error="Update called before Connector has an ID")

    updated_connector = client.connector_update(crd.spec)
    
    # If the connector doesn't exist anymore, reset the ID and create it again
    if updated_connector is None:
        logger.info(
            "Connector with id %s no longer exists. Recreating...",
            crd.spec.id
        )
        # Reset the ID in the patch
        patch.spec["id"] = None
        
        # Create a new connector
        new_connector = client.connector_create(crd.spec)
        patch.spec["id"] = new_connector.id
        
        # Generate tokens for the new connector
        tokens = client.connector_generate_tokens(new_connector.id)
        
        # Create or replace the secret
        secret = get_connector_secret(tokens.access_token, tokens.refresh_token)
        kopf.adopt([secret], owner=body, strict=True, forced=True)
        
        kapi = kubernetes.client.CoreV1Api()
        secret_name = crd.metadata.name
        
        try:
            kapi.delete_namespaced_secret(name=secret_name, namespace=namespace)
        except kubernetes.client.exceptions.ApiException as e:
            if e.status != 404:  # Only re-raise if not a "not found" error
                raise
        
        kapi.create_namespaced_secret(namespace=namespace, body=secret)
        
        create_or_replace_deployment(body, namespace, crd, memo.twingate_settings.full_url)
        
        return success(twingate_id=new_connector.id, message="Connector was recreated")

    create_or_replace_deployment(body, namespace, crd, memo.twingate_settings.full_url)

    return success(twingate_id=updated_connector.id)


@kopf.on.delete("twingateconnector")
def twingate_connector_delete(spec, meta, status, namespace, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    client = TwingateAPIClient(memo.twingate_settings, logger=logger)

    if connector_id := spec.get("id"):
        logger.info("Deleting connector %s", connector_id)
        client.connector_delete(connector_id)


CONNECTOR_RECONCILER_INTERVAL = int(os.environ.get("CONNECTOR_RECONCILER_INTERVAL", "5"))  # fmt: skip
CONNECTOR_RECONCILER_INIT_DELAY = int(os.environ.get("CONNECTOR_RECONCILER_INIT_DELAY", "5"))  # fmt: skip


@kopf.timer(
    "twingateconnector",
    interval=CONNECTOR_RECONCILER_INTERVAL,
    initial_delay=CONNECTOR_RECONCILER_INIT_DELAY,
)
def twingate_connector_pod_reconciler(
    body, meta, status, namespace, patch, memo, logger, **_
):
    logger.info("twingate_connector_reconciler: %s", body)
    if not (status and "twingate_connector_create" in status):
        raise kopf.TemporaryError("TwingateConnector not ready.", delay=1)

    crd = TwingateConnectorCRD(**body)

    kapi_apps = kubernetes.client.AppsV1Api()
    k8s_deployment = k8s_read_namespaced_deployment(
        namespace, crd.metadata.name, kapi_apps=kapi_apps
    )
    k8s_pod = k8s_deployment.spec.template if k8s_deployment else None
    k8s_pod_image = k8s_pod.spec.containers[0].image if k8s_pod else None

    if crd.spec.image:
        # If we're on a fixed-image policy, image updates are handled by `twingate_connector_update`.
        # Here we only check for a drift (someone edited the deployment manually)
        if k8s_pod_image != crd.spec.image:
            logger.warning(
                "Detected a drift between the Deployment image (%s) and the CRD image (%s)",
                k8s_pod_image,
                crd.spec.image,
            )
            create_or_replace_deployment(
                body, namespace, crd, memo.twingate_settings.full_url, kapi=kapi_apps
            )
    elif crd.spec.image_policy:
        now = pendulum.now("UTC").start_of("minute")
        next_check_at = pendulum.parse(
            meta.annotations.get(ANNOTATION_NEXT_VERSION_CHECK, "0001-01-01 00:00:00")
        )

        if now >= next_check_at:
            patch.meta["annotations"] = {
                ANNOTATION_LAST_VERSION_CHECK: now.to_iso8601_string(),
                ANNOTATION_NEXT_VERSION_CHECK: crd.spec.image_policy.get_next_date_iso8601(),
            }
            create_or_replace_deployment(
                body, namespace, crd, memo.twingate_settings.full_url, kapi=kapi_apps
            )

    return success()
