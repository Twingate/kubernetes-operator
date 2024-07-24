import kopf

from app.api import TwingateAPIClient
from app.crds import GroupStatusUserID, TwingateGroupCRD


@kopf.on.resume("twingategroup")
@kopf.on.create("twingategroup")
@kopf.on.update("twingategroup")
def twingate_group_reconciler(body, spec, namespace, meta, logger, memo, patch, **_):
    logger.info("twingate_group_reconciler: %s", spec)
    settings = memo.twingate_settings
    client = TwingateAPIClient(settings)

    crd = TwingateGroupCRD(**body)
    user_ids = crd.status.user_ids if crd.status else []
    if not crd.is_user_ids_cache_valid:
        logger.info("User IDs cache is invalid, fetching from Twingate")
        kopf.info(body, reason="User IDs cache is invalid, fetching from Twingate")

        email_to_id = client.get_ids_for_emails(crd.spec.members_email)
        user_ids = [
            GroupStatusUserID(id=id, email=email) for email, id in email_to_id.items()
        ]
        user_ids.extend([GroupStatusUserID(id=uid) for uid in crd.spec.members_ids])
        patch.status["user_ids"] = [ui.model_dump() for ui in user_ids]
        patch.status["user_ids_hash"] = crd.spec.members_hash

    if crd.spec.id:
        logger.info(
            "Updating group with name='%s', securityPolicyId='%s', userIds='%s'"
        )
        client.group_update(crd.spec, user_ids=[u.id for u in user_ids])

        # TODO: Group might have been deleted - remove id and fail to retry the handler

    else:
        logger.info(
            "Creating group with name='%s', securityPolicyId='%s', userIds='%s'",
            crd.spec.name,
            crd.spec.security_policy_id,
            [u.id for u in user_ids],
        )
        group_id = client.group_create(crd.spec, user_ids=[u.id for u in user_ids])
        patch.spec["id"] = group_id

    return {"message": "Group reconciled"}


@kopf.on.delete("twingategroup")
def twingate_group_delete(spec, status, memo, logger, **kwargs):
    logger.info("Got a delete request: %s. Status: %s", spec, status)
    if not status:
        return

    if group_id := spec.get("id"):
        logger.info("Deleting group %s", group_id)
        client = TwingateAPIClient(memo.twingate_settings)
        client.group_delete(group_id)
