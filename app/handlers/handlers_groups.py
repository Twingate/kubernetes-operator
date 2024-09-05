from datetime import timedelta

import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import TwingateGroupCRD
from app.handlers import fail, success


@kopf.on.resume("twingategroup")
@kopf.on.create("twingategroup")
@kopf.on.update("twingategroup")
def twingate_group_create_update(body, spec, logger, memo, patch, **kwargs):
    logger.info("twingate_group_reconciler: %s", spec)
    settings = memo.twingate_settings
    client = TwingateAPIClient(settings)

    if diff := kwargs.get("diff"):
        logger.info("Diff: %s", diff)
        # If ID changed from `None to value we just created it no need to update
        # diff is `(('add', ('spec', 'id'), None, 'R3JvdXA6MjAxNjc4OQ=='),)`
        if (
            len(diff) == 1
            and diff[0][0] == "add"
            and diff[0][1] == ("spec", "id")
            and diff[0][2] is None
        ):
            return success()

    crd = TwingateGroupCRD(**body)
    if crd.spec.id:
        logger.info("Updating group with name='%s'", crd.spec.name)
        try:
            client.group_update(crd.spec)
        except GraphQLMutationError as gqlerr:
            logger.error("Failed to update group: %s", gqlerr)
            if "does not exist" in gqlerr.message:
                patch.spec["id"] = None
            return fail(error=gqlerr.message)
    else:
        logger.info(
            "Creating group with name='%s'",
            crd.spec.name,
        )
        group_id = client.group_create(crd.spec)
        patch.spec["id"] = group_id

    return success()


@kopf.timer(
    "twingategroup", interval=timedelta(hours=10).seconds, initial_delay=60, idle=60
)
def twingate_group_reconciler(body, spec, logger, memo, patch, **_):
    return twingate_group_create_update(body, spec, logger, memo, patch)


@kopf.on.delete("twingategroup")
def twingate_group_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    if group_id := spec.get("id"):
        logger.info("Deleting group %s", group_id)
        client = TwingateAPIClient(memo.twingate_settings)
        client.group_delete(group_id)
