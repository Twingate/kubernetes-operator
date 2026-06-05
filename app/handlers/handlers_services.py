from collections.abc import Callable
from enum import StrEnum
from typing import cast

import kopf
import kubernetes
from kopf import Body, Status

from app.crds import ResourceType
from app.handlers.base import k8s_get_custom_object
from app.utils import to_bool

GATEWAY_ANNOTATION = "gateway.twingate.com"
GATEWAY_TLS_SECRET_ANNOTATION = "gateway.twingate.com/tlsSecret"  # noqa: S105


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
    spec = service_body.spec
    status = service_body.status
    service_name = cast(str, service_body.meta.name)
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

    if result["spec"].get("type") == ResourceType.KUBERNETES:
        if not (secret_name := meta.annotations.get(TLS_OBJECT_ANNOTATION)):
            raise kopf.PermanentError(
                f"{TLS_OBJECT_ANNOTATION} annotation is not provided."
            )

        host = (
            get_load_balancer_address(status, service_name)
            if spec["type"] == ServiceType.LOAD_BALANCER
            else f"{service_name}.{namespace}.svc.cluster.local"
        )
        result["spec"] |= {
            "address": "kubernetes.default.svc.cluster.local",
            "proxy": {
                "address": f"{host}:443",
                "certificateAuthorityCertSecretRef": {
                    "name": secret_name,
                    "namespace": namespace,
                },
            },
        }

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


def _gateway_address(service_body: Body, namespace: str) -> str:
    service_name = cast(str, service_body.meta.name)
    spec = service_body.spec
    status = service_body.status
    host = (
        get_load_balancer_address(status, service_name)
        if spec["type"] == ServiceType.LOAD_BALANCER
        else f"{service_name}.{namespace}.svc.cluster.local"
    )
    return f"{host}:443"


def service_to_certificate_authority(
    service_body: Body, namespace: str, secret_name: str
) -> dict:
    service_name = cast(str, service_body.meta.name)
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateCertificateAuthority",
        "metadata": {
            "name": f"{service_name}-ca",
            "labels": dict(service_body.metadata.labels),
        },
        "spec": {
            "name": f"{service_name}-ca",
            "secretRef": {"name": secret_name, "namespace": namespace},
        },
    }


def service_to_gateway(service_body: Body, namespace: str) -> dict:
    service_name = cast(str, service_body.meta.name)
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateGateway",
        "metadata": {
            "name": f"{service_name}-gateway",
            "labels": dict(service_body.metadata.labels),
        },
        "spec": {
            "address": _gateway_address(service_body, namespace),
            "x509CertificateAuthorityRef": {
                "name": f"{service_name}-ca",
                "namespace": namespace,
            },
        },
    }


def service_to_gateway_resource(service_body: Body, namespace: str) -> dict:
    """Build the in-cluster Kubernetes TwingateResource bound to the Gateway.

    Unlike the legacy proxy-based flow, the resource points at the cluster API
    server and references the gateway via `gatewayRef`. Only name/alias/etc. come
    from the `resource.twingate.com/*` annotations - the type, address and gateway
    binding are supplied here.
    """
    meta = service_body.metadata
    spec = service_body.spec
    service_name = cast(str, service_body.meta.name)
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
            "address": "kubernetes.default.svc.cluster.local",
            "type": ResourceType.KUBERNETES.value,
            "gatewayRef": {"name": f"{service_name}-gateway", "namespace": namespace},
        },
    }

    for key, convert_f in ALLOWED_EXTRA_ANNOTATIONS:
        # `type` is forced to Kubernetes; `isBrowserShortcutEnabled` is not allowed
        # on Kubernetes resources, so neither is taken from annotations here.
        if key in ("type", "isBrowserShortcutEnabled"):
            continue
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


def _create_or_replace_custom_object(
    kapi: kubernetes.client.CustomObjectsApi,
    namespace: str,
    plural: str,
    subobject: dict,
) -> None:
    """Create the custom object, or replace it in place preserving its backend id."""
    name = subobject["metadata"]["name"]
    if existing := k8s_get_custom_object(plural, namespace, name, kapi):
        if existing_id := existing.get("spec", {}).get("id"):
            subobject["spec"]["id"] = existing_id
        existing["spec"] = subobject["spec"]
        existing["metadata"]["labels"] = subobject["metadata"].get("labels", {})
        kapi.replace_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, plural, name, existing
        )
    else:
        kapi.create_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, plural, subobject
        )


def _find_owned_twingate_resource(
    kapi: kubernetes.client.CustomObjectsApi, namespace: str, service_uid: str
) -> dict | None:
    objs = kapi.list_namespaced_custom_object(
        "twingate.com", "v1beta", namespace, "twingateresources"
    )
    for obj in objs.get("items", []):
        owner_refs = obj.get("metadata", {}).get("ownerReferences", [])
        if any(ref.get("uid") == service_uid for ref in owner_refs):
            return obj
    return None


def _migrate_or_create_gateway_resource(
    kapi: kubernetes.client.CustomObjectsApi,
    namespace: str,
    service_body: Body,
    resource_subobject: dict,
    logger,
) -> None:
    """Bind the in-cluster Kubernetes resource to the Gateway.

    If a TwingateResource owned by this Service already exists (the legacy
    proxy-based resource), migrate it IN PLACE: reuse its `spec.id` and rewrite
    its spec to use `gatewayRef`, so the backend entity - and its access grants -
    are preserved. Otherwise create a new resource.
    """
    service_uid = cast(str, service_body.meta.uid)
    existing = _find_owned_twingate_resource(kapi, namespace, service_uid)
    if existing is None:
        # Fall back to the deterministic name the legacy flow used.
        existing = k8s_get_twingate_resource(
            namespace, resource_subobject["metadata"]["name"], kapi
        )

    if existing is None:
        kapi.create_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", resource_subobject
        )
        return

    existing_type = existing.get("spec", {}).get("type", ResourceType.NETWORK.value)
    if existing_type != ResourceType.KUBERNETES.value:
        # Resource type is immutable on the backend; refuse to clobber a
        # non-Kubernetes resource the Service happens to own.
        raise kopf.PermanentError(
            f"Cannot migrate owned TwingateResource of type '{existing_type}' to a "
            "gateway-managed Kubernetes resource."
        )

    name = existing["metadata"]["name"]
    if existing_id := existing.get("spec", {}).get("id"):
        # Preserve the backend id so access grants ride along.
        resource_subobject["spec"]["id"] = existing_id
    existing["spec"] = resource_subobject["spec"]
    existing["metadata"]["labels"] = resource_subobject["metadata"].get("labels", {})
    kapi.replace_namespaced_custom_object(
        "twingate.com", "v1beta", namespace, "twingateresources", name, existing
    )
    logger.info("Migrated TwingateResource %s to gatewayRef in place", name)


@kopf.on.resume("service", annotations={GATEWAY_ANNOTATION: "true"})
@kopf.on.create("service", annotations={GATEWAY_ANNOTATION: "true"})
@kopf.on.update("service", annotations={GATEWAY_ANNOTATION: "true"})
def twingate_gateway_service_create(body, spec, namespace, meta, logger, reason, **_):
    logger.info("twingate_gateway_service_create: %s", body)

    if not (secret_name := meta.annotations.get(GATEWAY_TLS_SECRET_ANNOTATION)):
        raise kopf.PermanentError(
            f"{GATEWAY_TLS_SECRET_ANNOTATION} annotation is not provided."
        )

    kapi = kubernetes.client.CustomObjectsApi()

    # The annotated Service IS the gateway: derive the CA and Gateway from it.
    ca_subobject = service_to_certificate_authority(body, namespace, secret_name)
    kopf.adopt(ca_subobject, owner=body, strict=True, forced=True)
    _create_or_replace_custom_object(
        kapi, namespace, "twingatecertificateauthorities", ca_subobject
    )

    gateway_subobject = service_to_gateway(body, namespace)
    kopf.adopt(gateway_subobject, owner=body, strict=True, forced=True)
    _create_or_replace_custom_object(
        kapi, namespace, "twingategateways", gateway_subobject
    )

    # Optionally expose the in-cluster API server as a Kubernetes resource bound
    # to this gateway, migrating any legacy proxy-based resource in place.
    if meta.annotations.get("resource.twingate.com") == "true":
        resource_subobject = service_to_gateway_resource(body, namespace)
        kopf.adopt(resource_subobject, owner=body, strict=True, forced=True)
        _migrate_or_create_gateway_resource(
            kapi, namespace, body, resource_subobject, logger
        )

    kopf.info(
        body,
        reason=f"twingate_gateway_service_create ({reason.value})",
        message=f"Reconciled gateway for Service {body.meta.name}",
    )


# NOTE: every annotation filter excludes services that also carry
# `gateway.twingate.com`; those are handled by twingate_gateway_service_create
# (which owns the gateway-managed resource), so the legacy handler must defer to
# avoid fighting over / deleting the gateway-managed TwingateResource.
# TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
@kopf.on.resume("service", annotations={"twingate.com/resource": "true", GATEWAY_ANNOTATION: kopf.ABSENT})  # fmt: skip
@kopf.on.create("service", annotations={"twingate.com/resource": "true", GATEWAY_ANNOTATION: kopf.ABSENT})  # fmt: skip
@kopf.on.update("service", annotations={"twingate.com/resource": "true", GATEWAY_ANNOTATION: kopf.ABSENT})  # fmt: skip
@kopf.on.resume("service", annotations={"resource.twingate.com": "true", GATEWAY_ANNOTATION: kopf.ABSENT})  # fmt: skip
@kopf.on.create("service", annotations={"resource.twingate.com": "true", GATEWAY_ANNOTATION: kopf.ABSENT})  # fmt: skip
@kopf.on.update("service", annotations={"resource.twingate.com": "true", GATEWAY_ANNOTATION: kopf.ABSENT})  # fmt: skip
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
# The `gateway.twingate.com: kopf.ABSENT` guard prevents this handler from
# deleting the gateway-managed TwingateResource when `resource.twingate.com` is
# removed while `gateway.twingate.com` is still present.
@kopf.on.update(
    "service",
    field=("metadata", "annotations", "twingate.com/resource"),
    old="true",
    annotations={GATEWAY_ANNOTATION: kopf.ABSENT},
)
@kopf.on.update(
    "service",
    field=("metadata", "annotations", "resource.twingate.com"),
    old="true",
    annotations={GATEWAY_ANNOTATION: kopf.ABSENT},
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


def _delete_custom_object_if_exists(
    kapi: kubernetes.client.CustomObjectsApi,
    namespace: str,
    plural: str,
    name: str,
    logger,
) -> None:
    try:
        kapi.delete_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, plural, name
        )
        logger.info("Deleted %s/%s", plural, name)
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status != 404:
            raise


@kopf.on.update(
    "service", field=("metadata", "annotations", GATEWAY_ANNOTATION), old="true"
)
def twingate_gateway_service_removed(body, namespace, logger, **_):
    logger.info("twingate_gateway_service_removed: %s", body.meta.name)

    service_name = body.meta.name
    kapi = kubernetes.client.CustomObjectsApi()

    # Tear down in dependency order: resource -> gateway -> CA. Each CRD's own
    # delete handler performs the backend delete (retrying on "in use"), so the
    # ordering here just minimises avoidable retries.
    for plural, name in (
        ("twingateresources", f"{service_name}-resource"),
        ("twingategateways", f"{service_name}-gateway"),
        ("twingatecertificateauthorities", f"{service_name}-ca"),
    ):
        _delete_custom_object_if_exists(kapi, namespace, plural, name, logger)

    kopf.info(
        body,
        reason="twingate_gateway_service_removed",
        message=f"Tore down gateway resources for Service {service_name}",
    )
