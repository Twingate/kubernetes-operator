import os
from collections.abc import MutableMapping
from datetime import timedelta
from types import SimpleNamespace
from typing import Any

import kopf

from app.api.client import GraphQLMutationError, TwingateAPIClient
from app.crds import PrincipalTypeEnum, ResourceAccessSpec
from app.handlers.base import fail, success
from app.utils import to_bool
from app.utils_k8s import (
    k8s_get_twingate_custom_object,
    k8s_patch_twingate_custom_object,
)

K8sObject = MutableMapping[Any, Any]


def get_principal_id(
    access_crd: ResourceAccessSpec,
    status: dict | None,
    client: TwingateAPIClient,
    owner_namespace: str,
) -> str:
    if principal_id := access_crd.principal_id:
        return principal_id

    if group_ref_object := access_crd.get_group_ref_object(owner_namespace):
        group_spec = group_ref_object["spec"]
        if group_id := group_spec.get("id"):
            return group_id

        raise kopf.TemporaryError(
            "TwingateGroup object doesn't have an id yet. retrying...", delay=15
        )

    if ref := access_crd.principal_external_ref:
        # Once `twingate_resource_access_change` ran and we have the principal_id we reuse it
        # and do not re-query the API.
        if principal_id := fetched_principal_id(status):
            return principal_id

        if ref.type == PrincipalTypeEnum.Group:
            principal_id = client.get_group_id(ref.name)
        elif ref.type == PrincipalTypeEnum.ServiceAccount:
            principal_id = client.get_service_account_id(ref.name)
        else:
            raise ValueError(f"Unknown principal type: {ref.type}")

        if not principal_id:
            raise ValueError(f"Principal {ref.type} {ref.name} not found.")

        return principal_id

    raise ValueError("Missing principal_id or principal_external_ref")


def fetched_principal_id(status: dict | None) -> str | None:
    handler_values = (status or {}).get(twingate_resource_access_change.__name__) or {}  # type: ignore[attr-defined]
    if not handler_values.get("success"):
        return None

    return get_recorded_access(status)["principalId"]


def get_recorded_access(status: dict | None) -> dict[str, str | None]:
    """Return the resource and principal IDs recorded for the access grant."""
    status = status or {}
    # Fall back to where the IDs were recorded before they moved to the status root:
    # Kopf replaces the whole handler result each run, so a failed reconcile loses them.
    handler_values = status.get(twingate_resource_access_change.__name__) or {}  # type: ignore[attr-defined]
    return {
        "resourceId": status.get("resourceId") or handler_values.get("resource_id"),
        "principalId": status.get("principalId") or handler_values.get("principal_id"),
    }


def reconcile_resource_access(
    body, namespace, spec, status, memo, logger, patch
) -> dict:
    recorded_access = get_recorded_access(status)

    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource(namespace)
    if not resource_crd:
        err = f"Resource {access_crd.resource_ref.fullname(namespace)} not found"
        kopf.warn(body, reason="ResourceNotFound", message=err)
        raise kopf.TemporaryError(err, delay=15)

    if not resource_crd.spec.id:
        raise kopf.TemporaryError("Resource not yet created, retrying...", delay=15)

    resource_id = resource_crd.spec.id
    try:
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        principal_id = get_principal_id(access_crd, status, client, namespace)
        # Delete before adding so that a failure leaves less access than intended.
        delete_old_access(client, recorded_access, resource_id, principal_id, logger)
        client.resource_access_add(
            resource_id,
            principal_id,
            access_crd.security_policy_id,
            expires_at=access_crd.expires_at,
            access_policy=access_crd.access_policy,
            approval_mode=access_crd.approval_mode,
        )

        # Recorded only after the grant lands: a failed add has to leave the pair granted
        # earlier in the status so the next reconcile still takes it away.
        patch.status["resourceId"] = resource_id
        patch.status["principalId"] = principal_id

        kopf.info(
            body,
            reason="Success",
            message=f"Added access to {resource_crd.spec.id}<>{principal_id}",
        )
        return success(principal_id=principal_id, resource_id=resource_id)
    except GraphQLMutationError as mex:
        kopf.exception(
            body, reason="Failure", message=f"{mex.mutation_name} failed: {mex.error}"
        )
        return fail(error=mex.error)


def delete_old_access(
    client: TwingateAPIClient,
    recorded_access: dict[str, str | None],
    resource_id: str,
    principal_id: str,
    logger,
) -> None:
    old_resource_id = recorded_access["resourceId"]
    old_principal_id = recorded_access["principalId"]
    if not old_resource_id or not old_principal_id:
        return

    if (old_resource_id, old_principal_id) == (resource_id, principal_id):
        return

    logger.info("Deleting old access %s<>%s", old_resource_id, old_principal_id)
    client.resource_access_remove(old_resource_id, old_principal_id)


@kopf.on.create("twingateresourceaccess")
@kopf.on.update("twingateresourceaccess", field="spec")
def twingate_resource_access_change(
    body, namespace, spec, memo, logger, status, patch, **kwargs
):
    logger.info("Got a TwingateResourceAccess create request: %s", spec)
    return reconcile_resource_access(body, namespace, spec, status, memo, logger, patch)


def get_unmigrated_recorded_ids(status: dict | None) -> dict[str, str]:
    """Return the recorded IDs the handler's values carry and the status root does not."""
    status = status or {}
    handler_values = status.get(twingate_resource_access_change.__name__) or {}  # type: ignore[attr-defined]
    # Skip an ID already at the root: it came from a later reconcile than the handler's.
    return {
        root_field: handler_values[handler_field]
        for root_field, handler_field in (
            ("resourceId", "resource_id"),
            ("principalId", "principal_id"),
        )
        if handler_values.get(handler_field) and not status.get(root_field)
    }


def has_unmigrated_recorded_access(status, **_) -> bool:
    return bool(get_unmigrated_recorded_ids(status))


@kopf.on.resume("twingateresourceaccess", when=has_unmigrated_recorded_access)
def twingate_resource_access_migrate_status(status, patch, logger, **_):
    """Copy IDs recorded by earlier operator versions to the root of the status."""
    patch.status.update(get_unmigrated_recorded_ids(status))
    logger.info("Migrated the recorded access IDs to the root of the status: %s", patch.status)  # fmt: skip


ENABLE_RESOURCE_ACCESS_RECONCILER = os.environ.get(
    "ENABLE_RESOURCE_ACCESS_RECONCILER", True
)


@kopf.timer(
    "twingateresourceaccess",
    interval=timedelta(hours=10).seconds,
    initial_delay=60,
    idle=60,
)
def twingate_resource_access_sync(
    body, namespace, spec, memo, logger, patch, status, **kwargs
):
    # Allow the reconciler to be temporarily disabled because tenants with large numbers of
    # resource access CRD objects can generate many write operations and get throttled. We currently
    # don't have a way to diff the resource access CRD and make writes optional.
    if not to_bool(ENABLE_RESOURCE_ACCESS_RECONCILER):
        return None

    return reconcile_resource_access(body, namespace, spec, status, memo, logger, patch)


@kopf.on.delete("twingateresourceaccess")
def twingate_resource_access_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a TwingateResourceAccess delete request: %s", spec)
    recorded_access = get_recorded_access(status)
    resource_id = recorded_access["resourceId"]
    principal_id = recorded_access["principalId"]
    if not (resource_id and principal_id):
        return

    client = TwingateAPIClient(memo.twingate_settings, logger=logger)
    client.resource_access_remove(resource_id, principal_id)


@kopf.index("twingateresourceaccess")
def twingate_resource_access_by_resource(namespace, name, spec, **_):
    resource_ref = spec.get("resourceRef", {})
    resource_name = resource_ref.get("name")
    resource_namespace = resource_ref.get("namespace") or namespace

    if not resource_name:
        return None

    return {
        (resource_namespace, resource_name): {
            "namespace": namespace,
            "name": name,
        },
    }


@kopf.index("twingateresourceaccess")
def twingate_resource_access_by_group(namespace, name, spec, **_):
    group_ref = spec.get("groupRef", {})
    group_name = group_ref.get("name")
    group_namespace = group_ref.get("namespace") or namespace

    if not group_name:
        return None

    return {
        (group_namespace, group_name): {
            "namespace": namespace,
            "name": name,
        },
    }


# Bound retries so a binding stuck on a never-ready reference eventually fails instead of
# retrying forever; the timer reconciler still recovers it if the reference is later fixed.
RESOURCE_ACCESS_HANDLER_TIMEOUT = int(os.environ.get("RESOURCE_ACCESS_HANDLER_TIMEOUT", timedelta(minutes=5).seconds))  # fmt: skip


@kopf.on.field(  # type: ignore[arg-type]
    "twingateresource", field="spec.id", timeout=RESOURCE_ACCESS_HANDLER_TIMEOUT
)
def twingate_resource_id_changed(
    namespace, name, new, memo, logger, twingate_resource_access_by_resource, **_
):
    """Reconcile bindings whose `resourceRef` points at a Resource with a new ID."""
    if not new:
        return

    access_refs = twingate_resource_access_by_resource.get((namespace, name), [])
    if not access_refs:
        return

    reconcile_access_refs(
        access_refs, f"Resource {name}", "resourceId", new, memo, logger
    )


@kopf.on.field(  # type: ignore[arg-type]
    "twingategroup", field="spec.id", timeout=RESOURCE_ACCESS_HANDLER_TIMEOUT
)
def twingate_group_id_changed(
    namespace, name, new, memo, logger, twingate_resource_access_by_group, **_
):
    """Reconcile bindings whose `groupRef` points at a Group with a new ID."""
    if not new:
        return

    access_refs = twingate_resource_access_by_group.get((namespace, name), [])
    if not access_refs:
        return

    reconcile_access_refs(
        access_refs, f"Group {name}", "principalId", new, memo, logger
    )


def reconcile_access_refs(
    access_refs, trigger: str, recorded_id_field: str, new_id: str, memo, logger
) -> None:
    # Re-raise after attempting every binding so Kopf retries, without letting one
    # not-yet-ready binding starve the others.
    retry_exc: kopf.TemporaryError | None = None

    for access_ref in access_refs:
        ra_namespace = access_ref["namespace"]
        ra_name = access_ref["name"]
        ra_obj = k8s_get_twingate_custom_object(
            "twingateresourceaccesses", ra_namespace, ra_name
        )
        if not ra_obj:
            continue

        recorded_id = get_recorded_access(ra_obj.get("status"))[recorded_id_field]
        # A binding that was never granted is driven by its own create handler, which keeps
        # retrying until the reference syncs; granting it here too would double the writes.
        if not recorded_id:
            continue

        # Skip bindings already on the new ID so a retry, or an ID change only some
        # bindings were waiting on, doesn't re-write the ones that are current.
        if recorded_id == new_id:
            continue

        logger.info(
            "%s ID changed, reconciling resource access %s/%s.",
            trigger,
            ra_namespace,
            ra_name,
        )
        patch = SimpleNamespace(spec={}, status={})
        try:
            result = reconcile_resource_access(
                ra_obj,
                ra_namespace,
                ra_obj["spec"],
                ra_obj.get("status"),
                memo,
                logger,
                patch,
            )

            # Kopf patches the object the handler is bound to, not the binding.
            k8s_patch_twingate_custom_object(
                "twingateresourceaccesses", ra_namespace, ra_name, patch
            )
        except kopf.TemporaryError as err:
            logger.warning(
                "Resource access %s/%s not ready after %s ID change, will retry: %s",
                ra_namespace,
                ra_name,
                trigger,
                err,
            )
            retry_exc = err
            continue
        except kopf.PermanentError:
            logger.exception(
                "Failed to reconcile resource access %s/%s after %s ID change",
                ra_namespace,
                ra_name,
                trigger,
            )
            continue
        except Exception as err:
            # Unknown failures are retried too: a failure part-way through leaves the
            # binding without the access it already revoked.
            logger.exception(
                "Failed to reconcile resource access %s/%s after %s ID change, will retry",
                ra_namespace,
                ra_name,
                trigger,
            )
            retry_exc = kopf.TemporaryError(
                f"Reconciling resource access {ra_namespace}/{ra_name} after the {trigger} "
                f"ID change failed, will retry: {err}",
                delay=15,
            )
            continue

        if not result["success"]:
            # A rejected mutation is recorded rather than raised, and the old access is
            # already gone by then, so ask for a retry instead of leaving the binding
            # without access until the sync timer.
            retry_exc = kopf.TemporaryError(
                f"Reconciling resource access {ra_namespace}/{ra_name} after the {trigger} "
                f"ID change failed, will retry: {result['error']}",
                delay=15,
            )

    if retry_exc is not None:
        raise retry_exc
