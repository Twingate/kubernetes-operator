from collections.abc import Callable

import kopf
import kubernetes
from kopf import Body

from app.crds import ResourceType
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
    ("syncLabels", to_bool),
    ("type", str),
]
GATEWAY_NAME_ANNOTATION = "resource.twingate.com/gatewayName"
GATEWAY_NAMESPACE_ANNOTATION = "resource.twingate.com/gatewayNamespace"
DOWNSTREAM_PORT_ANNOTATION = "resource.twingate.com/downstreamPort"
UPSTREAM_PORT_ANNOTATION = "resource.twingate.com/upstreamPort"


def service_to_twingate_resource(service_body: Body, namespace: str) -> dict:
    meta = service_body.metadata
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

    match result["spec"].get("type"):
        case ResourceType.WEB_APP:
            result["spec"] |= _web_app_spec(service_body, namespace)
        case None | ResourceType.NETWORK:
            result["spec"]["protocols"] = _network_protocols(service_body)
        case unsupported:
            raise kopf.PermanentError(
                f"Unsupported resource type {unsupported!r}; must be one of "
                f"{[ResourceType.NETWORK.value, ResourceType.WEB_APP.value]}."
            )

    return result


def _web_app_spec(service_body: Body, namespace: str) -> dict:
    meta = service_body.metadata
    spec = service_body.spec
    service_name = service_body.meta.name

    if not (gateway_name := meta.annotations.get(GATEWAY_NAME_ANNOTATION)):
        raise kopf.PermanentError(
            f"{GATEWAY_NAME_ANNOTATION} annotation is required for WebApp resources."
        )

    tcp_ports = [
        port_obj["port"]
        for port_obj in spec.get("ports", [])
        if port_obj.get("protocol", "TCP") == "TCP"
    ]

    # downstream is the client-facing port and is arbitrary, so an explicit value
    # is not constrained to the Service's ports; it defaults to the Service's port.
    if downstream_port := meta.annotations.get(DOWNSTREAM_PORT_ANNOTATION):
        downstream = _parse_port_annotation(DOWNSTREAM_PORT_ANNOTATION, downstream_port)
    else:
        downstream = _default_service_port(
            tcp_ports, DOWNSTREAM_PORT_ANNOTATION, service_name
        )

    # upstream is the Service's target port, so an explicit value must match a port
    # the Service exposes; it defaults to the Service's port.
    if upstream_port := meta.annotations.get(UPSTREAM_PORT_ANNOTATION):
        upstream = _parse_port_annotation(UPSTREAM_PORT_ANNOTATION, upstream_port)
        if upstream not in tcp_ports:
            raise kopf.PermanentError(
                f"{UPSTREAM_PORT_ANNOTATION} annotation ({upstream}) must match a "
                f"TCP port exposed by the Service {service_name}."
            )
    else:
        upstream = _default_service_port(
            tcp_ports, UPSTREAM_PORT_ANNOTATION, service_name
        )

    return {
        "gatewayRef": {
            "name": gateway_name,
            "namespace": meta.annotations.get(GATEWAY_NAMESPACE_ANNOTATION, namespace),
        },
        "downstream": {"port": downstream},
        "upstream": {"port": upstream},
    }


# Only Network resources use port-based protocols. WebApp resources configure
# upstream/downstream on the gateway instead.
def _network_protocols(service_body: Body) -> dict:
    protocols: dict = {
        "allowIcmp": False,
        "tcp": {"policy": "RESTRICTED", "ports": []},
        "udp": {"policy": "RESTRICTED", "ports": []},
    }
    for port_obj in service_body.spec.get("ports", []):
        port = port_obj["port"]
        protocol = port_obj.get("protocol", "TCP")
        if protocol == "TCP":
            protocols["tcp"]["ports"].append({"start": port, "end": port})
        elif protocol == "UDP":
            protocols["udp"]["ports"].append({"start": port, "end": port})
    return protocols


def _default_service_port(
    tcp_ports: list[int], annotation: str, service_name: str
) -> int:
    if len(tcp_ports) != 1:
        raise kopf.PermanentError(
            f"{annotation} annotation is required for WebApp resources unless the "
            f"Service {service_name} exposes exactly one TCP port."
        )
    return tcp_ports[0]


def _parse_port_annotation(annotation: str, value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise kopf.PermanentError(
            f"{annotation} annotation must be an integer."
        ) from None


# TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
@kopf.on.resume("service", annotations={"twingate.com/resource": "true"})
@kopf.on.create("service", annotations={"twingate.com/resource": "true"})
@kopf.on.update("service", annotations={"twingate.com/resource": "true"})
@kopf.on.resume("service", annotations={"resource.twingate.com": "true"})
@kopf.on.create("service", annotations={"resource.twingate.com": "true"})
@kopf.on.update("service", annotations={"resource.twingate.com": "true"})
def twingate_service_create(body, spec, namespace, meta, logger, reason, **_):
    logger.info("twingate_service_create: %s", body)

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
        kopf.info(
            body,
            reason=f"twingate_service_create ({reason.value})",
            message=f"Updated TwingateResource {resource_object_name}",
        )
    else:
        api_response = kapi.create_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", resource_subobject
        )
        logger.info("create_namespaced_custom_object response: %s", api_response)
        kopf.info(
            body,
            reason=f"twingate_service_create ({reason.value})",
            message=f"Created TwingateResource {resource_object_name}",
        )


# Use Tuple for the field to properly escape dots in the annotation key.
@kopf.on.update(
    "service", field=("metadata", "annotations", "twingate.com/resource"), old="true"
)
@kopf.on.update(
    "service", field=("metadata", "annotations", "resource.twingate.com"), old="true"
)
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
        kopf.info(
            body,
            reason="twingate_service_annotation_removed",
            message=f"Deleted TwingateResource {resource_object_name}",
        )
        return

    kopf.info(
        body,
        reason="twingate_service_annotation_removed",
        message=f"TwingateResource {resource_object_name} does not exist",
    )
