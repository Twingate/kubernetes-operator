import os

import kopf
import kubernetes.client
import pendulum
from kubernetes.client.models import V1ObjectMeta

from app.api import TwingateAPIClient
from app.crds import TwingateConnectorCRD
from app.handlers.base import fail, success
from app.settings import get_version

ANNOTATION_LAST_VERSION_CHECK = "twingate.com/last-version-check"
ANNOTATION_NEXT_VERSION_CHECK = "twingate.com/next-version-check"

ANNOTATION_POD_SPEC_VERSION = "twingate.com/connector-podspec-version"
ANNOTATION_POD_SPEC_VERSION_VALUE = "v1"


def get_connector_pod(
    crd: TwingateConnectorCRD, tenant_url: str, image: str
) -> kubernetes.client.V1Pod:
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

    # fmt: off
    pod_spec = {
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
               },
                **container_extra,
            },
            *spec.sidecar_containers,
        ],
        **spec.pod_extra,
    }
    pod_annotations = spec.pod_annotations | {ANNOTATION_POD_SPEC_VERSION: ANNOTATION_POD_SPEC_VERSION_VALUE}

    pod_meta = V1ObjectMeta(annotations=pod_annotations)

    # fmt: on
    return kubernetes.client.V1Pod(spec=pod_spec, metadata=pod_meta)


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


def k8s_read_namespaced_pod(
    namespace: str, name: str, kapi: kubernetes.client.CoreV1Api | None = None
) -> kubernetes.client.V1Pod | None:
    try:
        kapi = kapi or kubernetes.client.CoreV1Api()
        return kapi.read_namespaced_pod(name=name, namespace=namespace)
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


def k8s_force_delete_pod(
    namespace: str, name: str, kapi: kubernetes.client.CoreV1Api | None = None
):
    kapi = kapi or kubernetes.client.CoreV1Api()
    kapi.patch_namespaced_pod(name, namespace, body={"metadata": {"finalizers": None}})
    kapi.delete_namespaced_pod(
        name, namespace, body=kubernetes.client.V1DeleteOptions(grace_period_seconds=0)
    )


@kopf.on.create("twingateconnector")
def twingate_connector_create(body, memo, logger, namespace, patch, **_):
    settings = memo.twingate_settings
    client = TwingateAPIClient(settings)

    logger.info("Got twingateconnector create request: %s", body)
    crd = TwingateConnectorCRD(**body)
    connector_id = crd.spec.id

    if not crd.spec.id:
        connector = client.connector_create(crd.spec)
        connector_id = connector.id
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

    return success(twingate_id=connector_id)


@kopf.on.update("twingateconnector", field=["spec"])
def twingate_connector_update(body, memo, logger, new, diff, status, namespace, **_):
    logger.info(
        "Got TwingateConnector update request: %s. Diff: %s. Status: %s.",
        new,
        diff,
        status,
    )

    settings = memo.twingate_settings
    client = TwingateAPIClient(settings)

    crd = TwingateConnectorCRD(**body)
    # diff example: (('add', ('id',), None, 'Q29ubmVjdG9yOjUwNjE3NQ=='),)
    if len(diff) == 1 and diff[0][:3] == ("add", ("id",), None):
        return success(twingate_id=crd.spec.id, message="No update required")

    if not crd.spec.id:
        return fail(error="Update called before Connector has an ID")

    updated_connector = client.connector_update(crd.spec)

    kapi = kubernetes.client.CoreV1Api()
    kapi.delete_namespaced_pod(crd.metadata.name, namespace)

    return success(twingate_id=updated_connector.id)


@kopf.on.delete("twingateconnector")
def twingate_connector_delete(spec, meta, status, namespace, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    client = TwingateAPIClient(memo.twingate_settings)

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
    kapi = kubernetes.client.CoreV1Api()
    k8s_pod = k8s_read_namespaced_pod(namespace, crd.metadata.name, kapi=kapi)
    if k8s_pod and k8s_pod.status.phase != "Running":
        raise kopf.TemporaryError("Pod not running.", delay=1)

    # Migrate old pods
    pod_spec_version = (k8s_pod and k8s_pod.metadata.annotations or {}).get(
        ANNOTATION_POD_SPEC_VERSION
    )
    if k8s_pod and pod_spec_version != ANNOTATION_POD_SPEC_VERSION_VALUE:
        k8s_force_delete_pod(namespace, crd.metadata.name, kapi)
        return success(
            message=f"Pod spec version mismatch. Deleting pod {crd.metadata.name}."
        )

    image = k8s_pod.spec.containers[0].image if k8s_pod else None

    if crd.spec.image or not k8s_pod:
        image = crd.spec.get_image()
    elif crd.spec.image_policy:
        now = pendulum.now("UTC").start_of("minute")
        next_check_at = pendulum.parse(
            meta.annotations.get(ANNOTATION_NEXT_VERSION_CHECK, "0001-01-01 00:00:00")
        )

        if now >= next_check_at:
            image = crd.spec.get_image()
            patch.meta["annotations"] = {
                ANNOTATION_LAST_VERSION_CHECK: now.to_iso8601_string(),
                ANNOTATION_NEXT_VERSION_CHECK: crd.spec.image_policy.get_next_date_iso8601(),
            }

    if k8s_pod:
        # When pod exists, can only update the image or we get `Forbidden: pod updates may not change fields other than `spec.containers[*].image`
        current_image = k8s_pod.spec.containers[0].image
        if current_image != image:
            k8s_pod.spec.containers[0].image = image
            kapi.patch_namespaced_pod(meta.name, namespace, body=k8s_pod)
    else:
        pod = get_connector_pod(crd, memo.twingate_settings.full_url, image)
        kopf.adopt(pod, owner=body, strict=True, forced=True)
        kapi.create_namespaced_pod(namespace, body=pod)

    return success()
