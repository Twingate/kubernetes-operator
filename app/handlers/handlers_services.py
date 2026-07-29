import json
from collections.abc import Callable
from enum import StrEnum

import kopf
import kubernetes
from kopf import Body, Status

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
TLS_OBJECT_ANNOTATION = "resource.twingate.com/tlsSecret"
GATEWAY_NAME_ANNOTATION = "resource.twingate.com/gatewayName"
GATEWAY_NAMESPACE_ANNOTATION = "resource.twingate.com/gatewayNamespace"
DOWNSTREAM_PORT_ANNOTATION = "resource.twingate.com/downstreamPort"
UPSTREAM_PORT_ANNOTATION = "resource.twingate.com/upstreamPort"
REQUEST_HEADER_REWRITES_ANNOTATION = "resource.twingate.com/requestHeaderRewrites"


# Metadata that lets Helm take over the generated Kubernetes Resource, which v2's Gateway
# chart declares under the same name. This operator has to write it while it is still the
# one running, since Helm checks ownership when the v2 chart is applied.
# TODO: Remove in v2, which declares and owns the Resource from the start.
HELM_OWNERSHIP_ANNOTATIONS = (
    "meta.helm.sh/release-name",
    "meta.helm.sh/release-namespace",
)
HELM_MANAGED_BY_LABEL = "app.kubernetes.io/managed-by"
# Labels identifying the chart revision that rendered the Service. They describe the
# Service rather than the Resource derived from it, and copying them makes the operator
# the owning field manager of values that go stale on the next chart bump, which then
# collides with Helm's server-side apply when it declares the same labels.
HELM_CHART_REVISION_LABELS = (
    "helm.sh/chart",
    "app.kubernetes.io/version",
)


def get_load_balancer_address(status: Status, service_name: str) -> str:
    if not (ingress := status.get("loadBalancer", {}).get("ingress")):
        raise kopf.TemporaryError(
            f"Kubernetes Service: {service_name} LoadBalancer is not ready.",
            delay=30,
        )

    ip = ingress[0].get("ip")
    hostname = ingress[0].get("hostname")
    if not ip and not hostname:
        raise kopf.TemporaryError(
            f"Kubernetes Service: {service_name} LoadBalancer is not ready.",
            delay=30,
        )

    return ip or hostname


class ServiceType(StrEnum):
    CLUSTER_IP = "ClusterIP"
    LOAD_BALANCER = "LoadBalancer"


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
        case ResourceType.KUBERNETES:
            result["spec"] |= _kubernetes_spec(service_body, namespace)
        case None | ResourceType.NETWORK:
            result["spec"]["protocols"] = _network_protocols(service_body)
        case unsupported:
            raise kopf.PermanentError(
                f"Unsupported resource type {unsupported!r}; "
                f"must be one of {[t.value for t in ResourceType]}."
            )

    # v2's Gateway chart declares the Kubernetes Resource itself, under the same name
    # this generates, and Helm refuses to take over an existing object that doesn't
    # already carry both annotations and the managed-by label. Propagate them from the
    # Helm-deployed Service so that upgrade doesn't fail on invalid ownership metadata.
    # The label is set explicitly rather than relied on from the Service, which need not
    # label itself even when Helm renders it.
    #
    # Only for the Kubernetes type: nothing else is handed over to Helm, and marking a
    # Resource as Helm-owned tells v2's operator to drop its Service owner reference,
    # which is the only thing that cleans up a Resource when its Service is deleted.
    if result["spec"].get("type") == ResourceType.KUBERNETES and all(
        key in meta.annotations for key in HELM_OWNERSHIP_ANNOTATIONS
    ):
        result["metadata"]["annotations"] = {
            key: meta.annotations[key] for key in HELM_OWNERSHIP_ANNOTATIONS
        }
        result["metadata"]["labels"][HELM_MANAGED_BY_LABEL] = "Helm"

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

    web_app_spec: dict = {
        "gatewayRef": {
            "name": gateway_name,
            "namespace": meta.annotations.get(GATEWAY_NAMESPACE_ANNOTATION, namespace),
        },
        "downstream": {"port": downstream},
        "upstream": {"port": upstream},
    }

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

        web_app_spec["requestHeaderRewrites"] = [
            {"name": name, "value": value} for name, value in parsed.items()
        ]

    return web_app_spec


def _kubernetes_spec(service_body: Body, namespace: str) -> dict:
    meta = service_body.metadata
    spec = service_body.spec
    status = service_body.status
    service_name = service_body.meta.name

    if not (secret_name := meta.annotations.get(TLS_OBJECT_ANNOTATION)):
        raise kopf.PermanentError(
            f"{TLS_OBJECT_ANNOTATION} annotation is not provided."
        )

    host = (
        get_load_balancer_address(status, service_name)
        if spec["type"] == ServiceType.LOAD_BALANCER
        else f"{service_name}.{namespace}.svc.cluster.local"
    )
    return {
        "address": "kubernetes.default.svc.cluster.local",
        "proxy": {
            "address": f"{host}:443",
            "certificateAuthorityCertSecretRef": {
                "name": secret_name,
                "namespace": namespace,
            },
        },
    }


# Only Network resources use port-based protocols. Kubernetes and WebApp resources
# configure upstream/downstream on the gateway instead.
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
    # Only the Kubernetes Resource is handed over to Helm, and only its labels collide
    # with Helm's server-side apply. Labels also become Twingate tags when syncLabels is
    # on, so dropping them from any other Resource would change its tags in Twingate.
    #
    # `kopf.adopt` copies the owner's labels onto the child, so this has to run after it
    # rather than while building the object, or the Service's copies come straight back.
    if resource_subobject["spec"].get("type") == ResourceType.KUBERNETES:
        for label in HELM_CHART_REVISION_LABELS:
            resource_subobject["metadata"]["labels"].pop(label, None)

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
        # Merge rather than replace: the existing object also carries kopf's own
        # annotations, and dropping those would lose its handler state.
        if helm_annotations := resource_subobject["metadata"].get("annotations"):
            existing_resource_object["metadata"]["annotations"] = (
                existing_resource_object["metadata"].get("annotations") or {}
            ) | helm_annotations
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
        # In v2 the Gateway chart drops these annotations and declares the
        # TwingateResource itself, so deleting here would deprovision the backend
        # Resource mid-upgrade. Leave it for the v2 chart to adopt. Deleting the Service
        # outright is unaffected: the owner reference still garbage-collects the object.
        #
        # v2 keeps this guard as a safety net. The annotations are expected to be removed
        # while this operator is still running, but if the removal is only observed after
        # the upgrade, the event lands on v2, which would then delete the Resource its
        # chart now owns.
        # TODO: Remove once no v1 operator is still running in the field, and in v3 at
        # the latest.
        if existing_resource_object["spec"].get("type") == ResourceType.KUBERNETES:
            logger.warning(
                "Not deleting TwingateResource %s: Kubernetes Resources are kept so the "
                "v2 Gateway chart can adopt them. Delete it explicitly to deprovision.",
                resource_object_name,
            )
            kopf.info(
                body,
                reason="twingate_service_annotation_removed",
                message=f"Kept Kubernetes TwingateResource {resource_object_name}; "
                "delete it explicitly to deprovision",
            )
            return

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
