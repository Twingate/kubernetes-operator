import kopf
import kubernetes.client

from app.settings import get_settings, get_version

def get_connector_pod(url: str, access_token: str, refresh_token: str) -> kubernetes.client.V1Pod:
    operator_settings = get_settings()
    # fmt: off
    pod_spec = {
        "containers": [
            {
                "env": [
                    {"name": "TWINGATE_LABEL_DEPLOYED_BY", "value": "operator"},
                    {"name": "TWINGATE_LABEL_OPERATOR_VERSION", "value": get_version()},
                    {"name": "TWINGATE_URL", "value": url},
                    {"name": "TWINGATE_LOG_LEVEL", "value": "7"},
                    {"name": "TWINGATE_ACCESS_TOKEN", "value": access_token},
                    {"name": "TWINGATE_REFRESH_TOKEN", "value": refresh_token},
                ],
                "image": "twingate/connector:1",
                "imagePullPolicy": "Always",
                "name": "connector",
                "resources": {
                    "requests": {
                        "cpu": "50m",
                        "memory": "100M"
                    }
                },
            }
        ],
    }
    # fmt: on
    return kubernetes.client.V1Pod(spec=pod_spec)


@kopf.on.create("twingateconnector")
def twingate_connector_create(body, spec, memo, logger, namespace, **_):
    logger.info("Got connectorcreate request: %s", body)

    pod = get_connector_pod(memo.twingate_settings.full_url, spec["accessToken"], spec["refreshToken"])
    kopf.adopt(pod, owner=body, strict=True, forced=True)
    kopf.label(pod, {"operator.twingate.com/owner": "connector"})

    kapi = kubernetes.client.CoreV1Api()
    kapi.create_namespaced_pod(namespace=namespace, body=pod)


@kopf.on.delete("", "v1", "pods", labels={"operator.twingate.com/owner": "connector"})
def twingate_connector_pod_deleted(body, spec, meta, logger, namespace, **_):
    logger.info("twingate_connector_pod_deleted: %s", body)

    owners = meta["ownerReferences"]
    connector_owner = next((o for o in owners if o["kind"] == "TwingateConnector"), None)
    if not connector_owner:
        return

    kapi = kubernetes.client.CustomObjectsApi()
    response = kapi.get_namespaced_custom_object(
        "twingate.com",
        connector_owner["apiVersion"],
        namespace,
        "twingateconnector",
        connector_owner["name"],
    )


    pod = kubernetes.client.V1Pod(spec={
        "containers": spec["containers"],
    })
    # logger.info("pod!: %s", pod)
    kapi = kubernetes.client.CoreV1Api()
    result = kapi.create_namespaced_pod(namespace=namespace, body=dict(**body))
    logger.info("result: %s", result)
