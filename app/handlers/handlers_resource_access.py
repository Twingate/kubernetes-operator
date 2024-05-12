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
    create_status: dict | None,
    client: TwingateAPIClient,
) -> str:
    if principal_id := access_crd.principal_id:
        return principal_id

    if ref := access_crd.principal_external_ref:
        # Once `twingate_resource_access_changed` ran and we have the principal_id
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
        and status.get(twingate_resource_access_sync.__name__, {})
    ) and create_status["success"]:
        return create_status

    return None


@kopf.on.create("twingateresourceaccess")
@kopf.on.update("twingateresourceaccess", field="spec")
def twingate_resource_access_changed(body, spec, memo, logger, patch, status, **kwargs):
    logger.info("Got a TwingateResourceAccess create request: %s", spec)
    creation_status = check_status_created(status)

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
        principal_id = get_principal_id(access_crd, creation_status, client)
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


@kopf.timer(
    "twingateresourceaccess",
    interval=timedelta(hours=10).seconds,
    initial_delay=60,
    idle=60,
)
def twingate_resource_access_sync(body, spec, memo, logger, patch, status, **kwargs):
    return twingate_resource_access_changed(
        body, spec, memo, logger, patch, status, **kwargs
    )


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
        principal_id = get_principal_id(access_crd, creation_status, client)
        client.resource_access_remove(resource_id, principal_id)
