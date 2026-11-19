import json
from enum import StrEnum

import kopf
import kubernetes
from kopf import Body

from app.crds import ResourceType, TLSClientMode, TLSServerMode
from app.handlers.annotated_resources import (
    ANNOTATION,
    create_or_update_twingate_resource,
    delete_twingate_resource,
    extra_annotations_spec,
    k8s_get_twingate_resource,
)

GATEWAY_NAME_ANNOTATION = "resource.twingate.com/gatewayName"
GATEWAY_NAMESPACE_ANNOTATION = "resource.twingate.com/gatewayNamespace"
DOWNSTREAM_PORT_ANNOTATION = "resource.twingate.com/downstreamPort"
DOWNSTREAM_TLS_MODE_ANNOTATION = "resource.twingate.com/downstreamTLSMode"
UPSTREAM_PORT_ANNOTATION = "resource.twingate.com/upstreamPort"
UPSTREAM_TLS_MODE_ANNOTATION = "resource.twingate.com/upstreamTLSMode"
REQUEST_HEADER_REWRITES_ANNOTATION = "resource.twingate.com/requestHeaderRewrites"


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

    result["spec"] |= extra_annotations_spec(meta.annotations)

    match result["spec"].get("type"):
        case ResourceType.WEB_APP:
            result["spec"] |= web_app_spec(service_body, namespace)
        case None | ResourceType.NETWORK:
            result["spec"]["protocols"] = network_protocols(service_body)
        case unsupported:
            raise kopf.PermanentError(
                f"Unsupported resource type {unsupported!r}; must be one of "
                f"{[ResourceType.NETWORK.value, ResourceType.WEB_APP.value]}."
            )

    return result


def web_app_spec(service_body: Body, namespace: str) -> dict:
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
        downstream = parse_port_annotation(DOWNSTREAM_PORT_ANNOTATION, downstream_port)
    else:
        downstream = default_service_port(
            tcp_ports, DOWNSTREAM_PORT_ANNOTATION, service_name
        )

    # upstream is the Service's target port, so an explicit value must match a port
    # the Service exposes; it defaults to the Service's port.
    if upstream_port := meta.annotations.get(UPSTREAM_PORT_ANNOTATION):
        upstream = parse_port_annotation(UPSTREAM_PORT_ANNOTATION, upstream_port)
        if upstream not in tcp_ports:
            raise kopf.PermanentError(
                f"{UPSTREAM_PORT_ANNOTATION} annotation ({upstream}) must match a "
                f"TCP port exposed by the Service {service_name}."
            )
    else:
        upstream = default_service_port(
            tcp_ports, UPSTREAM_PORT_ANNOTATION, service_name
        )

    result: dict = {
        "gatewayRef": {
            "name": gateway_name,
            "namespace": meta.annotations.get(GATEWAY_NAMESPACE_ANNOTATION, namespace),
        },
        "downstream": {"port": downstream},
        "upstream": {"port": upstream},
    }

    if downstream_tls_mode := meta.annotations.get(DOWNSTREAM_TLS_MODE_ANNOTATION):
        result["downstream"]["tlsMode"] = parse_tls_mode_annotation(
            DOWNSTREAM_TLS_MODE_ANNOTATION, downstream_tls_mode, TLSServerMode
        )

    if upstream_tls_mode := meta.annotations.get(UPSTREAM_TLS_MODE_ANNOTATION):
        result["upstream"]["tlsMode"] = parse_tls_mode_annotation(
            UPSTREAM_TLS_MODE_ANNOTATION, upstream_tls_mode, TLSClientMode
        )

    if rewrites := meta.annotations.get(REQUEST_HEADER_REWRITES_ANNOTATION):
        invalid_msg = (
            f"{REQUEST_HEADER_REWRITES_ANNOTATION} annotation must be a JSON "
            "object mapping header names to string values."
        )
        try:
            parsed = json.loads(rewrites)
        except json.JSONDecodeError as ex:
            raise kopf.PermanentError(invalid_msg) from ex

        if not isinstance(parsed, dict) or not all(
            isinstance(value, str) for value in parsed.values()
        ):
            raise kopf.PermanentError(invalid_msg)

        result["requestHeaderRewrites"] = [
            {"name": name, "value": value} for name, value in parsed.items()
        ]

    return result


# Only Network resources use port-based protocols. WebApp resources configure
# upstream/downstream on the gateway instead.
def network_protocols(service_body: Body) -> dict:
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


def default_service_port(
    tcp_ports: list[int], annotation: str, service_name: str
) -> int:
    if len(tcp_ports) != 1:
        raise kopf.PermanentError(
            f"{annotation} annotation is required for WebApp resources unless the "
            f"Service {service_name} exposes exactly one TCP port."
        )
    return tcp_ports[0]


def parse_port_annotation(annotation: str, value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise kopf.PermanentError(
            f"{annotation} annotation must be an integer."
        ) from None


def parse_tls_mode_annotation[T: StrEnum](
    annotation: str, value: str, mode_enum: type[T]
) -> T:
    try:
        return mode_enum(value)
    except ValueError:
        raise kopf.PermanentError(
            f"{annotation} annotation must be one of {[m.value for m in mode_enum]}."
        ) from None


@kopf.on.resume("service", annotations={ANNOTATION: "true"})
@kopf.on.create("service", annotations={ANNOTATION: "true"})
@kopf.on.update("service", annotations={ANNOTATION: "true"})
def twingate_service_create(body, spec, namespace, meta, logger, reason, **_):
    logger.info("twingate_service_create: %s", body)

    resource_subobject = service_to_twingate_resource(body, namespace)
    kapi = kubernetes.client.CustomObjectsApi()
    create_or_update_twingate_resource(
        kapi,
        body,
        namespace,
        resource_subobject,
        existing_resource_object=k8s_get_twingate_resource(
            namespace, resource_subobject["metadata"]["name"], kapi
        ),
        handler="twingate_service_create",
        reason=reason,
        logger=logger,
    )


# Use Tuple for the field to properly escape dots in the annotation key.
@kopf.on.update("service", field=("metadata", "annotations", ANNOTATION), old="true")
def twingate_service_annotation_removed(body, spec, namespace, meta, logger, **_):
    logger.info("twingate_service_annotation_removed: %s", spec)

    resource_object_name = f"{body.meta.name}-resource"

    kapi = kubernetes.client.CustomObjectsApi()
    if existing_resource_object := k8s_get_twingate_resource(
        namespace, resource_object_name, kapi
    ):
        # In v2 the Gateway chart drops these annotations and declares the
        # TwingateResource itself, so deleting here would deprovision the backend
        # Resource mid-upgrade. Leave it for the v2 chart to adopt. Deleting the Service
        # outright is unaffected: the owner reference still garbage-collects the object.
        if existing_resource_object["spec"].get("type") == ResourceType.KUBERNETES:
            logger.warning(
                "Not deleting TwingateResource %s: Kubernetes Resources are migrated to "
                "TwingateGateway in v2. Delete it explicitly to deprovision.",
                resource_object_name,
            )
            kopf.info(
                body,
                reason="twingate_service_annotation_removed",
                message=f"Kept Kubernetes TwingateResource {resource_object_name} "
                "for migration to TwingateGateway",
            )
            return

        delete_twingate_resource(
            kapi,
            body,
            namespace,
            resource_object_name,
            handler="twingate_service_annotation_removed",
            logger=logger,
        )
        return

    kopf.info(
        body,
        reason="twingate_service_annotation_removed",
        message=f"TwingateResource {resource_object_name} does not exist",
    )
