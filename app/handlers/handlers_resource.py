from datetime import timedelta

import kopf

from app.api import TwingateAPIClient
from app.crds import ResourceSpec
from app.handlers.base import fail, success


@kopf.on.create("twingateresource")
def twingate_resource_create(body, labels, spec, memo, logger, patch, **kwargs):
    logger.info("Got a create request: %s. Labels: %s", spec, labels)
    resource = ResourceSpec(**spec)
    client = TwingateAPIClient(memo.twingate_settings, logger=logger)
    labels = memo.twingate_settings.default_resource_tags | dict(labels)
    graphql_arguments = resource.to_graphql_arguments(labels=labels, exclude={"id"})

    # Support importing existing resources - if `id` already exist we assume it's already created
    if resource.id:
        resource = client.resource_update(**graphql_arguments)
        kopf.info(body, reason="Success", message=f"Imported {resource.id}")
        return success(
            twingate_id=resource.id,
            created_at=resource.created_at.isoformat(),
            updated_at=resource.updated_at.isoformat(),
            message="Resource id already present - assuming an import of an existing resource.",
        )

    resource = client.resource_create(**graphql_arguments)
    patch.spec["id"] = resource.id
    kopf.info(body, reason="Success", message=f"Created on Twingate as {resource.id}")
    return success(
        twingate_id=resource.id,
        created_at=resource.created_at.isoformat(),
        updated_at=resource.updated_at.isoformat(),
    )


@kopf.on.update("twingateresource")
def twingate_resource_update(labels, spec, diff, status, memo, logger, **kwargs):
    logger.info(
        "Got TwingateResource update request: %s. Labels: %s. Diff: %s. Status: %s.",
        spec,
        labels,
        diff,
        status,
    )
    crd = ResourceSpec(**spec)
    labels = memo.twingate_settings.default_resource_tags | dict(labels)
    graphql_arguments = crd.to_graphql_arguments(labels=labels)

    if not crd.id:
        return fail(error="Resource ID is missing in the spec")

    # Check if just "id" was added - means `create` just ran
    if len(diff) == 1 and diff[0][:3] == ("add", ("id",), None):
        return success(twingate_id=crd.id, message="No update required")

    logger.info("Updating resource %s", crd.id)
    client = TwingateAPIClient(memo.twingate_settings, logger=logger)
    resource = client.resource_update(**graphql_arguments)
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


@kopf.timer(
    "twingateresource", interval=timedelta(hours=10).seconds, initial_delay=60, idle=60
)
def twingate_resource_sync(labels, spec, status, memo, logger, patch, **kwargs):
    crd = ResourceSpec(**spec)
    labels = memo.twingate_settings.default_resource_tags | dict(labels)
    if resource_id := crd.id:
        logger.info("Checking resource %s is up to date...", resource_id)
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        if resource := client.get_resource(resource_id):
            logger.info("Got resource %s", resource)
            if not (
                resource.is_matching_spec(crd) and resource.is_matching_labels(labels)
            ):
                logger.info("Resource %s is out of date, updating...", resource_id)
                client.resource_update(**crd.to_graphql_arguments(labels=labels))
        else:
            # Resource was deleted, recreate it
            logger.info("Resource %s was deleted, recreating...", resource_id)
            resource = client.resource_create(
                **crd.to_graphql_arguments(labels=labels, exclude={"id"})
            )
            patch.spec["id"] = resource.id
            return success(
                twingate_id=resource.id,
                created_at=resource.created_at.isoformat(),
                updated_at=resource.updated_at.isoformat(),
            )

    return None
