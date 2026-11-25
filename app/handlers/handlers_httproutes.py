"""Expose an HTTPRoute through Twingate by annotating it ``resource.twingate.com``.

The generated Network TwingateResource points at the address of the route's
parent Gateway and uses the route's hostname as its alias. The Twingate Client
keeps the hostname for the Host header and SNI, so the Gateway routes and
terminates TLS as it would for any other client. Its ports are the ports of the
Gateway listeners the route attaches to.

The route handler reads the Gateway when the route changes; the Gateway watcher
applies later changes to the Gateway's address and listeners.
"""

import ipaddress
from collections.abc import Mapping
from typing import NamedTuple, cast

import kopf
import kubernetes
from kopf import Body

from app.crds import ResourceType
from app.handlers.annotated_resources import (
    ANNOTATION,
    create_or_update_twingate_resource,
    delete_twingate_resource,
    extra_annotations_spec,
    k8s_get_twingate_resource,
)

GATEWAY_API_GROUP = "gateway.networking.k8s.io"
GATEWAY_API_VERSION = "v1"

HOSTNAME_ANNOTATION = "resource.twingate.com/hostname"
PARENT_GATEWAY_ANNOTATION = "resource.twingate.com/parentGateway"
ALIAS_ANNOTATION = "resource.twingate.com/alias"

# HTTPRoutes only attach to listeners of these protocols.
HTTP_LISTENER_PROTOCOLS = frozenset({"HTTP", "HTTPS"})
# Gateway address types the Twingate backend can dial; `type` defaults to IPAddress.
SUPPORTED_GATEWAY_ADDRESS_TYPES = frozenset({"IPAddress", "Hostname"})
GATEWAY_RETRY_DELAY = 30
# The TwingateResource fields the Gateway watcher keeps in step with the Gateway.
GATEWAY_SYNCED_FIELDS = ("address", "protocols")
# Attempts to sync a route when its TwingateResource is written concurrently.
GATEWAY_SYNC_ATTEMPTS = 3


def httproute_resource_name(route_name: str) -> str:
    # Services generate "<name>-resource"; a distinct suffix keeps a Service and an
    # HTTPRoute that share a name from overwriting each other's TwingateResource.
    return f"{route_name}-httproute-resource"


def hostname_matches(pattern: str, hostname: str) -> bool:
    """Match a hostname against a Gateway API hostname.

    A ``*.`` prefix is a suffix match: ``*.example.com`` matches ``a.example.com``
    and ``a.b.example.com``, but not ``example.com``.
    """
    if pattern.startswith("*."):
        return hostname.endswith(pattern[1:])
    return hostname == pattern


def select_hostname(route_body: Body) -> str:
    route_name = route_body.meta.name
    hostnames: list[str] = route_body.spec.get("hostnames") or []

    if hostname := route_body.metadata.annotations.get(HOSTNAME_ANNOTATION):
        if "*" in hostname:
            raise kopf.PermanentError(
                f"{HOSTNAME_ANNOTATION} annotation must not contain a wildcard."
            )
        # A route without hostnames accepts any host its listeners accept; the
        # listener hostnames are checked when picking ports.
        if hostnames and not any(hostname_matches(p, hostname) for p in hostnames):
            raise kopf.PermanentError(
                f"{HOSTNAME_ANNOTATION} annotation ({hostname}) must match one of the "
                f"HTTPRoute {route_name} hostnames {hostnames}."
            )
        return hostname

    if len(hostnames) != 1 or "*" in hostnames[0]:
        raise kopf.PermanentError(
            f"{HOSTNAME_ANNOTATION} annotation is required unless the HTTPRoute "
            f"{route_name} has exactly one hostname without a wildcard."
        )
    return hostnames[0]


def gateway_parent_refs(
    route_body: Body, namespace: str
) -> dict[tuple[str, str], list[Mapping]]:
    """The route's parentRefs to Gateways, by the Gateway's namespace and name."""
    refs_by_gateway: dict[tuple[str, str], list[Mapping]] = {}
    for ref in route_body.spec.get("parentRefs") or []:
        if (
            ref.get("group", GATEWAY_API_GROUP) != GATEWAY_API_GROUP
            or ref.get("kind", "Gateway") != "Gateway"
        ):
            continue
        key = (ref.get("namespace") or namespace, ref["name"])
        refs_by_gateway.setdefault(key, []).append(ref)
    return refs_by_gateway


def select_parent_gateway(
    route_body: Body, namespace: str
) -> tuple[str, str, list[Mapping]]:
    """Return the namespace, name and the route's parentRefs of its parent Gateway."""
    route_name = route_body.meta.name
    refs_by_gateway = gateway_parent_refs(route_body, namespace)

    if selected := route_body.metadata.annotations.get(PARENT_GATEWAY_ANNOTATION):
        gateway_namespace, _, gateway_name = selected.rpartition("/")
        key = (gateway_namespace or namespace, gateway_name)
        if key not in refs_by_gateway:
            raise kopf.PermanentError(
                f"{PARENT_GATEWAY_ANNOTATION} annotation ({selected}) must name a "
                f"Gateway in the HTTPRoute {route_name} parentRefs."
            )
        return key[0], key[1], refs_by_gateway[key]

    if len(refs_by_gateway) != 1:
        raise kopf.PermanentError(
            f"{PARENT_GATEWAY_ANNOTATION} annotation is required unless the HTTPRoute "
            f"{route_name} has exactly one parent Gateway."
        )
    ((gateway_namespace, gateway_name), refs) = next(iter(refs_by_gateway.items()))
    return gateway_namespace, gateway_name, refs


def k8s_get_gateway(
    namespace: str, name: str, kapi: kubernetes.client.CustomObjectsApi
) -> dict:
    try:
        return cast(
            dict,
            kapi.get_namespaced_custom_object(
                GATEWAY_API_GROUP, GATEWAY_API_VERSION, namespace, "gateways", name
            ),
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            raise kopf.TemporaryError(
                f"Gateway {namespace}/{name} not found.", delay=GATEWAY_RETRY_DELAY
            ) from ex
        raise


def is_ipv6(value: str) -> bool:
    try:
        return ipaddress.ip_address(value).version == 6
    except ValueError:
        return False


def gateway_address(gateway: Mapping) -> str:
    for address in gateway.get("status", {}).get("addresses") or []:
        if address.get("type", "IPAddress") not in SUPPORTED_GATEWAY_ADDRESS_TYPES:
            continue
        # The Twingate backend accepts a DNS name or an IPv4 address.
        if is_ipv6(value := address["value"]):
            continue
        return cast(str, value)

    meta = gateway["metadata"]
    raise kopf.TemporaryError(
        f"Gateway {meta['namespace']}/{meta['name']} has no IPv4 or hostname address "
        "in status.addresses yet.",
        delay=GATEWAY_RETRY_DELAY,
    )


def listener_accepts(listener: Mapping, hostname: str) -> bool:
    # A listener without a hostname accepts every hostname.
    listener_hostname = listener.get("hostname")
    return not listener_hostname or hostname_matches(listener_hostname, hostname)


def listener_selected_by(listener: Mapping, ref: Mapping) -> bool:
    section_name, port = ref.get("sectionName"), ref.get("port")
    return section_name in (None, listener["name"]) and port in (None, listener["port"])


def gateway_listener_ports(
    gateway: Mapping, parent_refs: list[Mapping], hostname: str, route_name: str
) -> list[int]:
    """Ports of the HTTP(S) listeners the route attaches to that accept ``hostname``."""
    ports = {
        listener["port"]
        for listener in gateway.get("spec", {}).get("listeners") or []
        if listener.get("protocol") in HTTP_LISTENER_PROTOCOLS
        and listener_accepts(listener, hostname)
        and any(listener_selected_by(listener, ref) for ref in parent_refs)
    }
    if not ports:
        meta = gateway["metadata"]
        raise kopf.PermanentError(
            f"Gateway {meta['namespace']}/{meta['name']} has no HTTP or HTTPS listener "
            f"for {hostname} that the HTTPRoute {route_name} attaches to."
        )
    return sorted(ports)


class RouteTarget(NamedTuple):
    """What an annotated HTTPRoute exposes, resolved from the route alone."""

    hostname: str
    extra_spec: dict
    gateway_namespace: str
    gateway_name: str
    parent_refs: list[Mapping]


def resolve_route(route_body: Body, namespace: str) -> RouteTarget:
    meta = route_body.metadata

    if ALIAS_ANNOTATION in meta.annotations:
        raise kopf.PermanentError(
            f"{ALIAS_ANNOTATION} annotation is not supported on HTTPRoutes: the alias "
            f"is the route's hostname, which {HOSTNAME_ANNOTATION} selects."
        )

    extra_spec = extra_annotations_spec(meta.annotations)
    if (resource_type := extra_spec.get("type")) not in (None, ResourceType.NETWORK):
        raise kopf.PermanentError(
            f"Unsupported resource type {resource_type!r} for HTTPRoutes; must be "
            f"{ResourceType.NETWORK.value!r}."
        )

    hostname = select_hostname(route_body)
    gateway_namespace, gateway_name, parent_refs = select_parent_gateway(
        route_body, namespace
    )
    return RouteTarget(
        hostname, extra_spec, gateway_namespace, gateway_name, parent_refs
    )


def twingate_resource_for_gateway(
    route_body: Body, target: RouteTarget, gateway: Mapping
) -> dict:
    route_name = route_body.meta.name
    resource_object_name = httproute_resource_name(route_name)
    ports = gateway_listener_ports(
        gateway, target.parent_refs, target.hostname, route_name
    )

    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResource",
        "metadata": {
            "name": resource_object_name,
            "labels": dict(route_body.metadata.labels),
        },
        "spec": {
            "name": resource_object_name,
            "address": gateway_address(gateway),
            "alias": target.hostname,
            **target.extra_spec,
            "protocols": {
                "allowIcmp": False,
                "tcp": {
                    "policy": "RESTRICTED",
                    "ports": [{"start": port, "end": port} for port in ports],
                },
                "udp": {"policy": "RESTRICTED", "ports": []},
            },
        },
    }


def httproute_to_twingate_resource(
    route_body: Body,
    namespace: str,
    kapi: kubernetes.client.CustomObjectsApi | None = None,
) -> dict:
    kapi = kapi or kubernetes.client.CustomObjectsApi()
    target = resolve_route(route_body, namespace)
    gateway = k8s_get_gateway(target.gateway_namespace, target.gateway_name, kapi)
    return twingate_resource_for_gateway(route_body, target, gateway)


@kopf.on.resume(
    GATEWAY_API_GROUP,
    GATEWAY_API_VERSION,
    "httproutes",
    annotations={ANNOTATION: "true"},
)
@kopf.on.create(
    GATEWAY_API_GROUP,
    GATEWAY_API_VERSION,
    "httproutes",
    annotations={ANNOTATION: "true"},
)
@kopf.on.update(
    GATEWAY_API_GROUP,
    GATEWAY_API_VERSION,
    "httproutes",
    annotations={ANNOTATION: "true"},
)
def twingate_httproute_create(body, namespace, logger, reason, **_):
    logger.info("twingate_httproute_create: %s", body)

    kapi = kubernetes.client.CustomObjectsApi()
    # Read the TwingateResource before the Gateway. If the Gateway watcher updates
    # it in between, replacing it at this resourceVersion fails with a 409 and Kopf
    # retries with the new Gateway, instead of writing back the old address.
    existing_resource_object = k8s_get_twingate_resource(
        namespace, httproute_resource_name(body.meta.name), kapi
    )
    resource_subobject = httproute_to_twingate_resource(body, namespace, kapi)
    create_or_update_twingate_resource(
        kapi,
        body,
        namespace,
        resource_subobject,
        existing_resource_object=existing_resource_object,
        handler="twingate_httproute_create",
        reason=reason,
        logger=logger,
    )


@kopf.index(
    GATEWAY_API_GROUP,
    GATEWAY_API_VERSION,
    "httproutes",
    annotations={ANNOTATION: "true"},
)
def httproutes_by_gateway(body, namespace, **_) -> dict[tuple[str, str], Body]:
    """Index annotated HTTPRoutes by each of their parent Gateways.

    Kopf drops a route from the index once it loses the annotation or is deleted.
    """
    return dict.fromkeys(gateway_parent_refs(body, namespace), body)


# Kopf injects indices by name, but its WatchingFn protocol only lists its own kwargs.
@kopf.on.event(GATEWAY_API_GROUP, GATEWAY_API_VERSION, "gateways")  # type: ignore[arg-type]
def twingate_httproute_gateway_event(
    event,
    namespace,
    name,
    body,
    logger,
    httproutes_by_gateway: kopf.Index[tuple[str, str], Body],
    **_,
):
    """Apply a Gateway's address and listeners to its annotated HTTPRoutes.

    An event handler, so the operator writes nothing to Gateways. Every event is
    compared against the TwingateResources, so repeats and the initial listing at
    startup are no-ops. A deleted Gateway leaves its routes' TwingateResources as
    they are, so recreating the Gateway doesn't deprovision them.
    """
    if event["type"] == "DELETED":
        return

    kapi = kubernetes.client.CustomObjectsApi()
    for route_body in httproutes_by_gateway.get((namespace, name), []):
        sync_httproute_with_gateway(kapi, route_body, body, logger)


def sync_httproute_with_gateway(
    kapi: kubernetes.client.CustomObjectsApi,
    route_body: Body,
    gateway: Body,
    logger,
) -> None:
    # HTTPRoutes are namespaced, so the namespace is always set.
    route_namespace = cast(str, route_body.meta.namespace)
    route_name = route_body.meta.name
    gateway_ref = f"{gateway.meta.namespace}/{gateway.meta.name}"

    try:
        target = resolve_route(route_body, route_namespace)
        if (target.gateway_namespace, target.gateway_name) != (
            gateway.meta.namespace,
            gateway.meta.name,
        ):
            # Another of its parent Gateways serves the route.
            return
        resource_subobject = twingate_resource_for_gateway(route_body, target, gateway)
    except kopf.TemporaryError as ex:
        # E.g. no address yet: the Gateway's next status update comes back here.
        logger.info("Not syncing HTTPRoute %s/%s: %s", route_namespace, route_name, ex)
        return
    except kopf.PermanentError as ex:
        kopf.warn(
            route_body, reason="twingate_httproute_gateway_event", message=str(ex)
        )
        return

    resource_object_name = resource_subobject["metadata"]["name"]
    for _ in range(GATEWAY_SYNC_ATTEMPTS):
        existing_resource_object = k8s_get_twingate_resource(
            route_namespace, resource_object_name, kapi
        )
        try:
            if existing_resource_object is None:
                create_or_update_twingate_resource(
                    kapi,
                    route_body,
                    route_namespace,
                    resource_subobject,
                    existing_resource_object=None,
                    handler="twingate_httproute_gateway_event",
                    reason=kopf.Reason.CREATE,
                    logger=logger,
                )
                return

            synced = {
                field: resource_subobject["spec"][field]
                for field in GATEWAY_SYNCED_FIELDS
            }
            if all(
                existing_resource_object["spec"].get(field) == value
                for field, value in synced.items()
            ):
                return

            # Only the Gateway-derived fields: the route handler owns the rest.
            existing_resource_object["spec"] |= synced
            kapi.replace_namespaced_custom_object(
                "twingate.com",
                "v1beta",
                route_namespace,
                "twingateresources",
                resource_object_name,
                existing_resource_object,
            )
            kopf.info(
                route_body,
                reason="twingate_httproute_gateway_event",
                message=f"Updated TwingateResource {resource_object_name} from "
                f"Gateway {gateway_ref}",
            )
            return
        except kubernetes.client.exceptions.ApiException as ex:
            # 409: the route handler wrote it in between. Read it again and compare.
            if ex.status != 409:
                raise

    logger.warning(
        "Gave up syncing TwingateResource %s/%s with Gateway %s after %d conflicts",
        route_namespace,
        resource_object_name,
        gateway_ref,
        GATEWAY_SYNC_ATTEMPTS,
    )


# Use Tuple for the field to properly escape dots in the annotation key.
@kopf.on.update(
    GATEWAY_API_GROUP,
    GATEWAY_API_VERSION,
    "httproutes",
    field=("metadata", "annotations", ANNOTATION),
    old="true",
)
def twingate_httproute_annotation_removed(body, namespace, logger, **_):
    logger.info("twingate_httproute_annotation_removed: %s", body.meta.name)

    resource_object_name = httproute_resource_name(body.meta.name)

    kapi = kubernetes.client.CustomObjectsApi()
    if k8s_get_twingate_resource(namespace, resource_object_name, kapi):
        delete_twingate_resource(
            kapi,
            body,
            namespace,
            resource_object_name,
            handler="twingate_httproute_annotation_removed",
            logger=logger,
        )
        return

    kopf.info(
        body,
        reason="twingate_httproute_annotation_removed",
        message=f"TwingateResource {resource_object_name} does not exist",
    )
