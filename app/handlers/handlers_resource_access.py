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
    create_status: dict | None,
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
        # Once `twingate_resource_access_change` ran and we have the principal_id
        # we dont use it and do not re-query the API
        if principal_id_already_fetched := create_status and create_status.get(
            "principal_id"
        ):
            return principal_id_already_fetched

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


def check_status_created(status: dict | None) -> dict | None:
    if (
        create_status := status
        # kopf 1.44 types the decorated handler as ChangingFn for mypy, but at
        # runtime it's the plain function, so __name__ (the handler id) is valid.
        and status.get(twingate_resource_access_change.__name__, {})  # type: ignore[attr-defined]
    ) and create_status["success"]:
        return create_status

    return None


def _reconcile_resource_access(body, namespace, spec, status, memo, logger) -> dict:
    creation_status = check_status_created(status)

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
        principal_id = get_principal_id(access_crd, creation_status, client, namespace)
        client.resource_access_add(
            resource_id,
            principal_id,
            access_crd.security_policy_id,
            expires_at=access_crd.expires_at,
            access_policy=access_crd.access_policy,
            approval_mode=access_crd.approval_mode,
        )

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


@kopf.on.create("twingateresourceaccess")
@kopf.on.update("twingateresourceaccess", field="spec")
def twingate_resource_access_change(
    body, namespace, spec, memo, logger, status, **kwargs
):
    logger.info("Got a TwingateResourceAccess create request: %s", spec)
    return _reconcile_resource_access(body, namespace, spec, status, memo, logger)


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
    body, namespace, spec, memo, logger, status, **kwargs
):
    # Allow the reconciler to be temporarily disabled because tenants with large numbers of
    # resource access CRD objects can generate many write operations and get throttled. We currently
    # don't have a way to diff the resource access CRD and make writes optional.
    if not to_bool(ENABLE_RESOURCE_ACCESS_RECONCILER):
        return None

    return _reconcile_resource_access(body, namespace, spec, status, memo, logger)


@kopf.on.delete("twingateresourceaccess")
def twingate_resource_access_delete(namespace, spec, status, memo, logger, **kwargs):
    logger.info("Got a TwingateResourceAccess delete request: %s", spec)
    creation_status = check_status_created(status)
    if not creation_status:
        return

    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource(namespace)
    if resource_id := resource_crd and resource_crd.spec.id:
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        principal_id = get_principal_id(access_crd, creation_status, client, namespace)
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

    _reconcile_access_refs(
        access_refs, f"Resource {name}", "resource_id", new, memo, logger
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

    _reconcile_access_refs(
        access_refs, f"Group {name}", "principal_id", new, memo, logger
    )


def _reconcile_access_refs(
    access_refs, trigger: str, status_id_field: str, new_id: str, memo, logger
) -> None:
    """Reconcile each TwingateResourceAccess binding named in access_refs."""
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

        # Skip bindings already on the new ID so a retry, or an ID change only some
        # bindings were waiting on, doesn't re-write the ones that are current.
        creation_status = check_status_created(ra_obj.get("status"))
        if creation_status and creation_status.get(status_id_field) == new_id:
            continue

        logger.info(
            "%s ID changed, reconciling resource access %s/%s.",
            trigger,
            ra_namespace,
            ra_name,
        )
        try:
            result = _reconcile_resource_access(
                ra_obj,
                ra_namespace,
                ra_obj["spec"],
                ra_obj.get("status"),
                memo,
                logger,
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
        except Exception:
            logger.exception(
                "Failed to reconcile resource access %s/%s after %s ID change",
                ra_namespace,
                ra_name,
                trigger,
            )
            continue

        # These handlers fire on the referenced object, so Kopf won't persist the result
        # onto the binding for us; record it ourselves, otherwise the stored IDs (and the
        # status printer columns) would keep showing stale values.
        if result and result.get("success"):
            k8s_patch_twingate_custom_object(
                "twingateresourceaccesses",
                ra_namespace,
                ra_name,
                SimpleNamespace(
                    spec={},
                    status={twingate_resource_access_change.__name__: result},  # type: ignore[attr-defined]
                ),
            )

    if retry_exc is not None:
        raise retry_exc
