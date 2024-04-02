from datetime import timedelta

import kopf

from app.api import TwingateAPIClient
from app.crds import ResourceSpec
from app.handlers.base import fail, success


@kopf.on.create("twingateresource")
def twingate_resource_create(body, spec, memo, logger, patch, **kwargs):
    logger.info("Got a create request: %s", spec)
    resource = ResourceSpec(**spec)
    resource = TwingateAPIClient(memo.twingate_settings).resource_create(resource)
    patch.spec["id"] = resource.id
    kopf.info(body, reason="Success", message=f"Created on Twingate as {resource.id}")
    return success(
        twingate_id=resource.id,
        created_at=resource.created_at.isoformat(),
        updated_at=resource.updated_at.isoformat(),
    )


@kopf.on.update("twingateresource", field="spec")
def twingate_resource_update(spec, diff, status, memo, logger, **kwargs):
    logger.info(
        "Got TwingateResource update request: %s. Diff: %s. Status: %s.",
        spec,
        diff,
        status,
    )

    crd = ResourceSpec(**spec)
    if not crd.id:
        return fail(error="Resource ID is missing in the spec")

    # Check if just "id" was added - means `create` just ran
    if len(diff) == 1 and diff[0][:3] == ("add", ("id",), None):
        return success(twingate_id=crd.id, message="No update required")

    logger.info("Updating resource %s", crd.id)
    client = TwingateAPIClient(memo.twingate_settings)
    resource = client.resource_update(crd)
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
        client = TwingateAPIClient(memo.twingate_settings)
        client.resource_delete(resource_id)


@kopf.timer(
    "twingateresource", interval=timedelta(hours=10).seconds, initial_delay=60, idle=60
)
def twingate_resource_sync(spec, status, memo, logger, patch, **kwargs):
    crd = ResourceSpec(**spec)

    if resource_id := crd.id:
        logger.info("Checking resource %s is up to date...", resource_id)
        client = TwingateAPIClient(memo.twingate_settings)
        if resource := client.get_resource(resource_id):
            logger.info("Got resource %s", resource)
            if not resource.is_matching_spec(crd):
                logger.info("Resource %s is out of date, updating...", resource_id)
                client.resource_update(crd)
        else:
            # Resource was deleted, recreate it
            logger.info("Resource %s was deleted, recreating...", resource_id)
            crd_withoput_id = crd.model_copy(update={"id": None})
            resource = client.resource_create(crd_withoput_id)
            patch.spec["id"] = resource.id
            return success(
                twingate_id=resource.id,
                created_at=resource.created_at.isoformat(),
                updated_at=resource.updated_at.isoformat(),
            )

    return None
