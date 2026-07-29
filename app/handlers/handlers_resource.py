import os
from datetime import timedelta

import kopf

from app.api import TwingateAPIClient
from app.crds import ResourceSpec, ResourceType, TwingateGatewayCRD
from app.handlers.base import fail, success
from app.utils_k8s import k8s_get_twingate_custom_object


def _repair_missing_gateway_ref(name, namespace, spec, patch, logger) -> bool:
    """Bind a Kubernetes Resource that the v2 upgrade left without a ``gatewayRef``.

    Resources generated from a Service's annotations predate ``gatewayRef``, and Helm 3
    cannot fill it in on upgrade: it adopts the object once the ownership annotations
    are present but never patches custom resources the way it does built-in types
    (helm/helm#11650), so no later revision recovers the field either. Server-side apply
    (Helm 4, Argo CD) does write it, so this only repairs the objects left behind by
    clients that don't.

    Returns True when a repair was staged on ``patch``.
    """
    if spec.get("type") != ResourceType.KUBERNETES or spec.get("gatewayRef"):
        return False

    # The Gateway chart renders the Service and the TwingateGateway from one name
    # helper, and the operator appended `-resource` when it generated this Resource
    # from that Service, so dropping the suffix gives the Gateway's name.
    gateway_name = name.removesuffix("-resource")
    if gateway_name == name:
        return False

    gateway = k8s_get_twingate_custom_object(
        TwingateGatewayCRD.PLURAL, namespace, gateway_name
    )
    if gateway is None:
        raise kopf.TemporaryError(
            f"Kubernetes Resource '{name}' has no gatewayRef and TwingateGateway "
            f"'{gateway_name}' does not exist yet.",
            delay=30,
        )

    # Only adopt a Gateway whose serviceRef points at the Service this Resource was
    # generated from, so a same-named but unrelated Gateway can't capture the access.
    if gateway.get("spec", {}).get("serviceRef", {}).get("name") != gateway_name:
        raise kopf.PermanentError(
            f"TwingateGateway '{gateway_name}' does not reference Service "
            f"'{gateway_name}'; set gatewayRef on '{name}' explicitly."
        )

    logger.info("Binding Resource %s to TwingateGateway %s", name, gateway_name)
    patch.spec["gatewayRef"] = {"name": gateway_name, "namespace": namespace}
    return True


def _release_service_ownership(meta, spec, patch, logger):
    """Drop the Service owner reference from a chart-declared Kubernetes Resource.

    From v2 the Gateway chart declares the Resource the operator once generated from a
    Service's annotations, so two owners claim one object: deleting the Service garbage
    collects something the chart still declares, Helm or Argo CD applies it back without
    a ``spec.id``, and the operator registers a second backend Resource.

    v2 no longer generates a Kubernetes Resource from Service annotations, so only that
    pre-v2 object matches. Network and WebApp Resources it still generates keep their
    owner reference, since garbage collection is their only cleanup path.
    """
    if spec.get("type") != ResourceType.KUBERNETES:
        return

    owner_references = meta.get("ownerReferences") or []
    remaining = [ref for ref in owner_references if ref.get("kind") != "Service"]
    if len(remaining) == len(owner_references):
        return

    logger.info("Releasing Service ownership of Resource %s", meta.get("name"))
    patch.meta["ownerReferences"] = remaining


@kopf.on.create("twingateresource")
def twingate_resource_create(
    body, namespace, labels, spec, memo, logger, patch, **kwargs
):
    logger.info("Got a create request: %s. Labels: %s", spec, labels)
    resource = ResourceSpec(**spec)
    client = TwingateAPIClient(memo.twingate_settings, logger=logger)
    labels = memo.twingate_settings.default_resource_tags | dict(labels)
    graphql_arguments = resource.to_graphql_arguments(
        labels=labels, owner_namespace=namespace, exclude={"id"}
    )

    # Support importing existing resources - if `id` already exist we assume it's already created
    if resource.id:
        resource = client.resource_update(
            id=resource.id, resource_type=resource.type, **graphql_arguments
        )
        kopf.info(body, reason="Success", message=f"Imported {resource.id}")
        return success(
            twingate_id=resource.id,
            created_at=resource.created_at.isoformat(),
            updated_at=resource.updated_at.isoformat(),
            message="Resource id already present - assuming an import of an existing resource.",
        )

    resource = client.resource_create(resource_type=resource.type, **graphql_arguments)
    patch.spec["id"] = resource.id
    kopf.info(body, reason="Success", message=f"Created on Twingate as {resource.id}")
    return success(
        twingate_id=resource.id,
        created_at=resource.created_at.isoformat(),
        updated_at=resource.updated_at.isoformat(),
    )


@kopf.on.update("twingateresource")
def twingate_resource_update(
    name, namespace, meta, labels, spec, diff, status, memo, logger, patch, **kwargs
):
    logger.info(
        "Got TwingateResource update request: %s. Labels: %s. Diff: %s. Status: %s.",
        spec,
        labels,
        diff,
        status,
    )
    if _repair_missing_gateway_ref(name, namespace, spec, patch, logger):
        raise kopf.TemporaryError("Staged gatewayRef; reconciling on retry.", delay=5)

    _release_service_ownership(meta, spec, patch, logger)

    crd = ResourceSpec(**spec)
    labels = memo.twingate_settings.default_resource_tags | dict(labels)
    graphql_arguments = crd.to_graphql_arguments(
        labels=labels, owner_namespace=namespace
    )

    if not crd.id:
        return fail(error="Resource ID is missing in the spec")

    # We only care about `spec` or `labels` changes
    changed_fields = [".".join(d[1]) for d in diff]
    is_spec_changed = any(cf.startswith("spec.") for cf in changed_fields)
    is_labels_changed = any(cf.startswith("metadata.labels.") for cf in changed_fields)
    if not (is_spec_changed or is_labels_changed):
        logger.info("No relevant changes detected, skipping update.")
        return success(twingate_id=crd.id, message="No update required")

    # Check if just "spec.id" was added - means `create` just ran
    if len(diff) == 1 and diff[0][:3] == ("add", ("spec", "id"), None):
        return success(twingate_id=crd.id, message="No update required")

    logger.info("Updating resource %s", crd.id)
    client = TwingateAPIClient(memo.twingate_settings, logger=logger)
    resource = client.resource_update(resource_type=crd.type, **graphql_arguments)

    logger.info("Got resource %s", resource)
    return success(
        twingate_id=resource.id,
        created_at=resource.created_at.isoformat(),
        updated_at=resource.updated_at.isoformat(),
    )


@kopf.on.delete("twingateresource")
def twingate_resource_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    if resource_id := spec.get("id"):
        logger.info("Deleting resource %s", resource_id)
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        client.resource_delete(resource_id)


RESOURCE_RECONCILER_INTERVAL = int(os.environ.get("RESOURCE_RECONCILER_INTERVAL", timedelta(hours=10).seconds))  # fmt: skip
RESOURCE_RECONCILER_INIT_DELAY = int(os.environ.get("RESOURCE_RECONCILER_INIT_DELAY", 60))  # fmt: skip
RESOURCE_RECONCILER_IDLE = int(os.environ.get("RESOURCE_RECONCILER_IDLE", 60))  # fmt: skip


@kopf.timer(
    "twingateresource",
    interval=RESOURCE_RECONCILER_INTERVAL,
    initial_delay=RESOURCE_RECONCILER_INIT_DELAY,
    idle=RESOURCE_RECONCILER_IDLE,
)
def twingate_resource_sync(
    name, namespace, meta, labels, spec, status, memo, logger, patch, **kwargs
):
    if _repair_missing_gateway_ref(name, namespace, spec, patch, logger):
        raise kopf.TemporaryError("Staged gatewayRef; reconciling on retry.", delay=5)

    _release_service_ownership(meta, spec, patch, logger)

    crd = ResourceSpec(**spec)
    labels = memo.twingate_settings.default_resource_tags | dict(labels)
    if resource_id := crd.id:
        logger.info("Checking resource %s is up to date...", resource_id)
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        if resource := client.get_resource(resource_id):
            logger.info("Got resource %s", resource)
            diff = resource.get_spec_diff(
                crd, owner_namespace=namespace
            ) | resource.get_labels_diff(labels)
            if not diff:
                return success(twingate_id=resource_id, message="No update required")

            logger.info("Resource %s is out of date. Diff: %s", resource_id, diff)
            client.resource_update(
                resource_type=crd.type,
                **crd.to_graphql_arguments(labels=labels, owner_namespace=namespace),
            )

            return success(
                twingate_id=resource.id,
                created_at=resource.created_at.isoformat(),
                updated_at=resource.updated_at.isoformat(),
            )

        # Resource was deleted, recreate it
        logger.info("Resource %s was deleted, recreating...", resource_id)
        graphql_arguments = crd.to_graphql_arguments(
            labels=labels, owner_namespace=namespace, exclude={"id"}
        )
        resource = client.resource_create(resource_type=crd.type, **graphql_arguments)
        patch.spec["id"] = resource.id
        return success(
            twingate_id=resource.id,
            created_at=resource.created_at.isoformat(),
            updated_at=resource.updated_at.isoformat(),
        )

    return None


@kopf.index("twingateresource")
def twingate_resource_gateway_index(namespace, name, spec, **_):
    gw_ref = spec.get("gatewayRef", {})
    gw_name = gw_ref.get("name")
    gw_namespace = gw_ref.get("namespace") or namespace

    if not gw_name:
        return None

    return {
        (gw_namespace, gw_name): {
            "namespace": namespace,
            "name": name,
        },
    }
