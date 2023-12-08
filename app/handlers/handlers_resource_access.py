from collections.abc import MutableMapping
from datetime import timedelta
from typing import Any

import kopf

from app.api.client import GraphQLMutationError
from app.crds import ResourceAccessSpec
from app.handlers.base import fail, success

K8sObject = MutableMapping[Any, Any]


@kopf.on.create("twingateresourceaccess")
def twingate_resource_access_create(body, spec, memo, logger, patch, **kwargs):
    logger.info("Got a TwingateResourceAccess create request: %s", spec)
    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource()
    if not resource_crd:
        err = f"Resource {access_crd.resource_ref_fullname} not found"
        kopf.warn(body, reason="ResourceNotFound", message=err)
        return {"success": False, "error": err}

    if not resource_crd.spec.id:
        raise kopf.TemporaryError("Resource not yet created, retrying...", delay=15)

    resource_id = resource_crd.spec.id
    try:
        memo.twingate_client.resource_access_add(
            resource_id, access_crd.principal_id, access_crd.security_policy_id
        )
        kopf.info(
            body,
            reason="Success",
            message=f"Added access to {spec.id}<>{access_crd.principal_id}",
        )
        patch.metadata["ownerReferences"] = [
            resource_crd.metadata.owner_reference_object
        ]
        return success()
    except GraphQLMutationError as mex:
        kopf.exception(
            body, reason="Failure", message=f"{mex.mutation_name} failed: {mex.error}"
        )
        return fail(error=mex.error)


@kopf.on.update("twingateresourceaccess")
def twingate_resource_access_update(new, diff, status, memo, logger, **kwargs):
    logger.info(
        "Got TwingateResourceAccess update request: %s. Diff: %s. Status: %s.",
        new,
        diff,
        status,
    )

    if not status.get("twingate_resource_access_create", {}).get("ok"):
        # Object didnt go through create yet?   wait...
        raise kopf.TemporaryError("Resource not yet created, retrying...", delay=15)

    # Note that both principalId and resourceRef are immutable so only securityPolicyId could change
    # in this case we just need to call api_client.resource_access_add with the new value
    access_crd = ResourceAccessSpec(**new["spec"])
    if resource_crd := access_crd.get_resource():
        try:
            memo.twingate_client.resource_access_add(
                resource_crd.spec.id,
                access_crd.principal_id,
                access_crd.security_policy_id,
            )
            return success()
        except GraphQLMutationError as mex:
            return fail(error=mex.error)

    return fail(error=f"Resource {access_crd.resource_ref_fullname} not found")


@kopf.on.delete("twingateresourceaccess")
def twingate_resource_access_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a TwingateResourceAccess delete request: %s", spec)
    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource()
    if resource_id := resource_crd and resource_crd.spec.id:
        memo.twingate_client.resource_access_remove(
            resource_id, access_crd.principal_id
        )


@kopf.timer(
    "twingateresourceaccess",
    interval=timedelta(hours=10).seconds,
    initial_delay=60,
    idle=60,
)
def twingate_resource_access_sync(body, spec, status, memo, logger, **kwargs):
    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource()
    if not resource_crd:
        err = f"Resource {access_crd.resource_ref_fullname} not found"
        logger.warning(err)
        kopf.warn(body, reason="ResourceNotFound", message=err)
        return fail(error=err)

    if not resource_crd.spec.id:
        return success(status="Skipped as resource not yet created")

    try:
        memo.twingate_client.resource_access_add(
            resource_crd.spec.id, access_crd.principal_id, access_crd.security_policy_id
        )
        return success()
    except GraphQLMutationError as mex:
        kopf.exception(
            body, reason="Failure", message=f"{mex.mutation_name} failed: {mex.error}"
        )
        return fail(error=mex.error)
