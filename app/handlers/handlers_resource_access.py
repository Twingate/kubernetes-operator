from collections.abc import MutableMapping
from datetime import timedelta
from typing import Any

import kopf

from app.api.client import GraphQLMutationError, TwingateAPIClient
from app.crds import PrincipalTypeEnum, ResourceAccessSpec
from app.handlers.base import fail, success

K8sObject = MutableMapping[Any, Any]


def get_principal_id(
    access_crd: ResourceAccessSpec,
    twingate_resource_access_create: dict | None,
    client: TwingateAPIClient,
) -> str:
    if principal_id := access_crd.principal_id:
        return principal_id

    if ref := access_crd.principal_external_ref:
        # Once `twingate_resource_access_create` ran and we have the principal_id
        # we dont use it and do not re-query the API
        if twingate_resource_access_create:
            return twingate_resource_access_create["principal_id"]

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
        twingate_resource_access_create := status
        and status.get("twingate_resource_access_create", {})
    ) and twingate_resource_access_create["ok"]:
        return twingate_resource_access_create

    return None


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
        client = TwingateAPIClient(memo.twingate_settings)
        principal_id = get_principal_id(access_crd, None, client)
        client.resource_access_add(
            resource_id, principal_id, access_crd.security_policy_id
        )

        kopf.info(
            body,
            reason="Success",
            message=f"Added access to {resource_crd.spec.id}<>{principal_id}",
        )
        patch.metadata["ownerReferences"] = [
            resource_crd.metadata.owner_reference_object
        ]
        return success(principal_id=principal_id, resource_id=resource_id)
    except GraphQLMutationError as mex:
        kopf.exception(
            body, reason="Failure", message=f"{mex.mutation_name} failed: {mex.error}"
        )
        return fail(error=mex.error)


@kopf.on.update("twingateresourceaccess", field="spec")
def twingate_resource_access_update(spec, diff, status, memo, logger, **kwargs):
    logger.info(
        "Got TwingateResourceAccess update request: %s. Diff: %s. Status: %s.",
        spec,
        diff,
        status,
    )
    creation_status = check_status_created(status)
    if not creation_status:
        # Object didn't go through create yet?   wait...
        raise kopf.TemporaryError("Resource not yet created, retrying...", delay=15)

    # Note that both principalId/principalExternalRef and resourceRef are immutable so only securityPolicyId could
    # change in this case we just need to call api_client.resource_access_add with the new value
    access_crd = ResourceAccessSpec(**spec)
    if resource_crd := access_crd.get_resource():
        try:
            client = TwingateAPIClient(memo.twingate_settings)
            principal_id = get_principal_id(access_crd, creation_status, client)
            client.resource_access_add(
                resource_crd.spec.id,
                principal_id,
                access_crd.security_policy_id,
            )
            return success()
        except GraphQLMutationError as mex:
            return fail(error=mex.error)

    return fail(error=f"Resource {access_crd.resource_ref_fullname} not found")


@kopf.on.delete("twingateresourceaccess")
def twingate_resource_access_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a TwingateResourceAccess delete request: %s", spec)
    creation_status = check_status_created(status)
    if not creation_status:
        return

    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource()
    if resource_id := resource_crd and resource_crd.spec.id:
        client = TwingateAPIClient(memo.twingate_settings)
        principal_id = get_principal_id(access_crd, client)
        client.resource_access_remove(resource_id, creation_status, principal_id)


@kopf.timer(
    "twingateresourceaccess",
    interval=timedelta(hours=10).seconds,
    initial_delay=60,
    idle=60,
)
def twingate_resource_access_sync(body, spec, status, memo, logger, **kwargs):
    creation_status = check_status_created(status)
    if not creation_status:
        return success(status="Skipped as creation didn't run yet.")

    access_crd = ResourceAccessSpec(**spec)
    resource_crd = access_crd.get_resource()
    if not resource_crd:
        err = f"Resource {access_crd.resource_ref_fullname} not found"
        logger.warning(err)
        kopf.warn(body, reason="ResourceNotFound", message=err)
        return fail(error=err)

    if not resource_crd.spec.id:
        return success(status="Skipped as resource not yet created")

    # Migrate old creation_status objects

    try:
        client = TwingateAPIClient(memo.twingate_settings)
        principal_id = get_principal_id(access_crd, creation_status, client)

        client.resource_access_add(
            resource_crd.spec.id, principal_id, access_crd.security_policy_id
        )

        status["twingate_resource_access_create"]["principal_id"] = principal_id
        status["twingate_resource_access_create"]["resource_id"] = resource_crd.spec.id
        return success(principal_id=principal_id, resource_id=resource_crd.spec.id)
    except GraphQLMutationError as mex:
        kopf.exception(
            body, reason="Failure", message=f"{mex.mutation_name} failed: {mex.error}"
        )
        return fail(error=mex.error)
