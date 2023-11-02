import base64

import kopf
import kubernetes.client

from app.crds import ConnectorSpec, TwingateConnectorCRD
from app.settings import get_version


def get_connector_pod(
    name: str, url: str, spec: ConnectorSpec
) -> kubernetes.client.V1Pod:
    # fmt: off
    pod_spec = {
        "containers": [
            {
                "env": [
                    {"name": "TWINGATE_LABEL_DEPLOYED_BY", "value": "operator"},
                    {"name": "TWINGATE_LABEL_OPERATOR_VERSION", "value": get_version()},
                    {"name": "TWINGATE_URL", "value": url},
                    {"name": "TWINGATE_LOG_LEVEL", "value": "7"},
                ],
                "envFrom": [
                    {
                        "secretRef": {
                            "name": name,
                            "optional": False
                        }
                    }
                ],
                "image": "twingate/connector:1",
                "imagePullPolicy": "Always",
                "name": "connector",
                "securityContext": {
                    "allowPrivilegeEscalation": False
               },
                **spec.container_extra,
            }
        ],
        **spec.pod_extra,
    }
    # fmt: on
    return kubernetes.client.V1Pod(spec=pod_spec)


def get_connector_secret(
    access_token: str, refresh_token: str
) -> kubernetes.client.V1Secret:
    return kubernetes.client.V1Secret(
        immutable=True,
        data={
            "TWINGATE_ACCESS_TOKEN": base64.b64encode(
                access_token.encode("ascii")
            ).decode(),
            "TWINGATE_REFRESH_TOKEN": base64.b64encode(
                refresh_token.encode("ascii")
            ).decode(),
        },
    )


@kopf.on.create("twingateconnector")
def twingate_connector_create(body, spec, memo, logger, namespace, patch, **_):
    settings = memo.twingate_settings
    client = memo.twingate_client

    logger.info("Got connectorcreate request: %s", body)
    crd = TwingateConnectorCRD(**body)

    if not crd.spec.id:
        connector = client.connector_create(
            crd.spec.name, memo.twingate_settings.remote_network_id
        )
        patch.spec["id"] = connector.id
        patch.spec["name"] = connector.name
    else:
        connector = client.get_connector(crd.spec.id)

    logger.info("connector: %s", connector)
    tokens = client.connector_generate_tokens(connector.id)

    pod = get_connector_pod(crd.metadata.name, settings.full_url, crd.spec)
    secret = get_connector_secret(tokens.access_token, tokens.refresh_token)
    kopf.adopt([pod, secret], owner=body, strict=True, forced=True)
    kopf.label([pod, secret], {"twingate.com/owner": "connector"})

    kapi = kubernetes.client.CoreV1Api()
    kapi.create_namespaced_secret(namespace=namespace, body=secret)
    kapi.create_namespaced_pod(namespace=namespace, body=pod)


@kopf.on.delete("", "v1", "pods", labels={"twingate.com/owner": "connector"})
def twingate_connector_pod_deleted(body, spec, meta, logger, namespace, memo, **_):
    logger.info("twingate_connector_pod_deleted: %s", body)

    connector_owner = next(
        (o for o in meta["ownerReferences"] if o["kind"] == "TwingateConnector"), None
    )
    if not connector_owner:
        return None

    owner_group, owner_version = connector_owner["apiVersion"].split("/")

    try:
        kapi = kubernetes.client.CustomObjectsApi()
        response = kapi.get_namespaced_custom_object(
            owner_group,
            owner_version,
            namespace,
            "twingateconnectors",
            connector_owner["name"],
        )
        connector = TwingateConnectorCRD(**response)
        pod = get_connector_pod(memo.twingate_settings.full_url, connector.spec)
        kopf.adopt(pod, owner=response)
        kopf.label(pod, {"operator.twingate.com/owner": "connector"})

        # logger.info("pod!: %s", pod)
        kapi = kubernetes.client.CoreV1Api()
        result = kapi.create_namespaced_pod(namespace=namespace, body=pod)
        logger.info("result: %s", result)
    except kubernetes.client.exceptions.ApiException as api_ex:
        if api_ex.status == 404:
            logger.warning(
                "ResourceAccessCRD.get_resource_ref_object: resource not found."
            )
        else:
            logger.exception("ResourceAccessCRD.get_resource_ref_object failed")

        return None


@kopf.on.delete("twingateconnector")
def twingate_connector_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    if connector_id := spec.get("id"):
        logger.info("Deleting connector %s", connector_id)
        memo.twingate_client.connector_delete(connector_id)