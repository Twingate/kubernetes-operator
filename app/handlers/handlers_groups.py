import os
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
        # If ID changed from `None` to value we just created it no need to update
        # diff is `(('add', ('spec', 'id'), None, 'R3JvdXA6MjAxNjc4OQ=='),)`
        # fmt: off
        if len(diff) == 1 and diff[0][:3] == ("add", ("spec", "id",), None):
            return success()
        # fmt: on

    crd = TwingateGroupCRD(**body)
    group_id = crd.spec.id
    if group_id:
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

    return success(
        twingate_id=group_id,
    )


GROUP_RECONCILER_INTERVAL = int(os.environ.get("GROUP_RECONCILER_INTERVAL", timedelta(hours=10).seconds))  # fmt: skip
GROUP_RECONCILER_INIT_DELAY = int(os.environ.get("GROUP_RECONCILER_INIT_DELAY", 60))  # fmt: skip


@kopf.timer(
    "twingategroup",
    interval=GROUP_RECONCILER_INTERVAL,
    initial_delay=GROUP_RECONCILER_INIT_DELAY,
    idle=60,
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
