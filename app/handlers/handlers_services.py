from collections.abc import Callable

import kopf
import kubernetes
from kopf import Body

from app.handlers import success
from app.utils import to_bool


def k8s_get_twingate_resource(
    namespace: str, name: str, kapi: kubernetes.client.CustomObjectsApi | None = None
) -> dict | None:
    kapi = kapi or kubernetes.client.CustomObjectsApi()
    try:
        return kapi.get_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", name
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


ALLOWED_EXTRA_ANNOTATIONS: list[tuple[str, Callable]] = [
    ("name", str),
    ("alias", str),
    ("isBrowserShortcutEnabled", to_bool),
    ("securityPolicyId", str),
    ("isVisible", to_bool),
]


def service_to_twingate_resource(service_body: Body, namespace: str) -> dict:
    meta = service_body.metadata
    spec = service_body.spec
    service_name = service_body.meta.name
    resource_object_name = f"{service_name}-resource"

    result: dict = {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResource",
        "metadata": {
            "name": resource_object_name,
            "labels": dict(meta.labels),
        },
        "spec": {
            "name": resource_object_name,
            "address": f"{service_name}.{namespace}.svc.cluster.local",
        },
    }

    for key, convert_f in ALLOWED_EXTRA_ANNOTATIONS:
        # TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
        if value := meta.annotations.get(f"twingate.com/resource-{key}"):
            result["spec"][key] = convert_f(value)
        if value := meta.annotations.get(f"resource.twingate.com/{key}"):
            result["spec"][key] = convert_f(value)

    protocols: dict = {
        "allowIcmp": False,
        "tcp": {"policy": "RESTRICTED", "ports": []},
        "udp": {"policy": "RESTRICTED", "ports": []},
    }
    for port_obj in spec.get("ports", []):
        port = port_obj["port"]
        if port_obj["protocol"] == "TCP":
            protocols["tcp"]["ports"].append({"start": port, "end": port})
        elif port_obj["protocol"] == "UDP":
            protocols["udp"]["ports"].append({"start": port, "end": port})

    result["spec"]["protocols"] = protocols

    return result


# TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
@kopf.on.resume("service", annotations={"twingate.com/resource": "true"})
@kopf.on.create("service", annotations={"twingate.com/resource": "true"})
@kopf.on.update("service", annotations={"twingate.com/resource": "true"})
@kopf.on.resume("service", annotations={"resource.twingate.com": "true"})
@kopf.on.create("service", annotations={"resource.twingate.com": "true"})
@kopf.on.update("service", annotations={"resource.twingate.com": "true"})
def twingate_service_create(body, spec, namespace, meta, logger, **_):
    logger.info("twingate_service_create: %s", spec)

    resource_subobject = service_to_twingate_resource(body, namespace)
    kopf.adopt(resource_subobject)

    resource_object_name = resource_subobject["metadata"]["name"]

    kapi = kubernetes.client.CustomObjectsApi()
    if existing_resource_object := k8s_get_twingate_resource(
        namespace, resource_object_name, kapi
    ):
        logger.info("TwingateResource already exists: %s", existing_resource_object)
        existing_resource_object["spec"] = {
            "id": existing_resource_object["spec"]["id"],
            **resource_subobject["spec"],
        }
        existing_resource_object["metadata"]["labels"] = resource_subobject["metadata"][
            "labels"
        ]
        kapi.replace_namespaced_custom_object(
            "twingate.com",
            "v1beta",
            namespace,
            "twingateresources",
            resource_object_name,
            existing_resource_object,
        )
    else:
        api_response = kapi.create_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", resource_subobject
        )
        logger.info("create_namespaced_custom_object response: %s", api_response)

    return success(
        message=f"Created TwingateResource {resource_subobject['spec']['name']}"
    )


@kopf.on.update("service", annotations={"resource.twingate.com": "false"})
@kopf.on.update("service", annotations={"resource.twingate.com": kopf.ABSENT})
def twingate_service_annotation_removed(body, spec, namespace, meta, logger, **_):
    logger.info("twingate_service_annotation_removed: %s", spec)

    resource_object_name = f"{body.meta.name}-resource"

    kapi = kubernetes.client.CustomObjectsApi()
    if existing_resource_object := k8s_get_twingate_resource(
        namespace, resource_object_name, kapi
    ):
        logger.info("Deleting TwingateResource: %s", existing_resource_object)
        kapi.delete_namespaced_custom_object(
            "twingate.com",
            "v1beta",
            namespace,
            "twingateresources",
            resource_object_name,
        )
        return success(message=f"Deleted TwingateResource {resource_object_name}")

    return success(message=f"TwingateResource {resource_object_name} does not exist")
