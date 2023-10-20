import kopf

from app.crds import ResourceSpec
from app.handlers.base import success


@kopf.on.create("twingateresource")
def twingate_resource_create(body, spec, memo, logger, patch, **kwargs):
    logger.info("Got a create request: %s", spec)
    resource = ResourceSpec(**spec)
    resource = memo.twingate_client.resource_create(resource)
    patch.spec["id"] = resource.id
    kopf.info(body, reason="Success", message=f"Created on Twingate as {resource.id}")
    return success(
        twingate_id=resource.id,
        created_at=resource.created_at.isoformat(),
        updated_at=resource.updated_at.isoformat(),
    )


@kopf.on.update("twingateresource")
def twingate_resource_update(old, new, diff, status, memo, logger, **kwargs):
    # status looks like  {'twingate_resource_create': {'twingate_id': 'UmVzb3VyY2U6ODcyNDY2'}}
    logger.info("Got an update request: %s. Diff: %s. Status: %s.", new, diff, status)
    crd = ResourceSpec(**new["spec"])
    if crd.id:
        logger.info("Updating resource %s", crd.id)
        resource = memo.twingate_client.resource_update(crd)
        logger.info("Got resource %s", resource)
        return success(
            twingate_id=resource.id,
            created_at=resource.created_at.isoformat(),
            updated_at=resource.updated_at.isoformat(),
        )


@kopf.on.delete("twingateresource")
def twingate_resource_delete(spec, status, memo, logger, **kwargs):
    # status looks like {'twingate_resource_create': {'twingate_id': 'UmVzb3VyY2U6ODcyNDYz'}}
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    if resource_id := spec.get("id"):
        logger.info("Deleting resource %s", resource_id)
        memo.twingate_client.resource_delete(resource_id)


@kopf.timer("twingateresource", interval=60 * 5, initial_delay=60, idle=60)
def twingate_resource_sync(spec, status, memo, logger, patch, **kwargs):
    crd = ResourceSpec(**spec)

    if resource_id := crd.id:
        logger.info("Checking resource %s is up to date...", resource_id)
        if resource := memo.twingate_client.get_resource(resource_id):
            logger.info("Got resource %s", resource)
            if not resource.is_matching_spec(crd):
                logger.info("Resource %s is out of date, updating...", resource_id)
                memo.twingate_client.resource_update(crd)
        else:
            # Resource was deleted, recreate it
            logger.info("Resource %s was deleted, recreating...", resource_id)
            crd_withoput_id = crd.model_copy(update={"id": None})
            resource = memo.twingate_client.resource_create(crd_withoput_id)
            patch.spec["id"] = resource.id
            return success(
                twingate_id=resource.id,
                created_at=resource.created_at.isoformat(),
                updated_at=resource.updated_at.isoformat(),
            )
