import kopf
import kubernetes.client

from app.settings import get_settings, get_version


@kopf.on.create("twingateconnector")
def twingate_connector_create(body, spec, memo, logger, patch, **_):
    logger.info("Got connectorcreate request: %s", body)

    operator_settings = get_settings()

    # fmt: off

    pod_spec = {
        "containers": [
            {
                "env": [
                    {"name": "TWINGATE_LABEL_DEPLOYED_BY", "value": "operator"},
                    {"name": "TWINGATE_LABEL_OPERATOR_VERSION", "value": get_version()},
                    {"name": "TWINGATE_URL", "value": f"https://{operator_settings.network}.{operator_settings.host}"},
                    {"name": "TWINGATE_LOG_LEVEL", "value": "7"},
                    {"name": "TWINGATE_ACCESS_TOKEN", "value": spec["accessToken"]},
                    {"name": "TWINGATE_REFRESH_TOKEN", "value": spec["refreshToken"]},
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

    pod = kubernetes.client.V1Pod(spec=pod_spec)
    kopf.adopt(pod, owner=body)

    kapi = kubernetes.client.CoreV1Api()
    kapi.create_namespaced_pod(namespace="default", body=pod)
