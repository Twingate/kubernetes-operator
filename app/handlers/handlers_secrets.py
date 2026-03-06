import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import ResourceSpec
from app.handlers.handlers_services import k8s_get_twingate_resource


def update_twingate_resource(resource_ref, memo, logger):
    twingate_resource = k8s_get_twingate_resource(
        resource_ref["namespace"], resource_ref["name"]
    )
    if not twingate_resource:
        return

    crd = ResourceSpec(**twingate_resource["spec"])
    if not crd.id:
        return

    labels = memo.twingate_settings.default_resource_tags | twingate_resource[
        "metadata"
    ].get("labels", {})

    try:
        logger.info("Updating resource %s", crd.id)
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        resource = client.resource_update(
            resource_type=crd.type,
            **crd.to_graphql_arguments(labels=labels),
        )
        logger.info("Got resource %s", resource)
    except GraphQLMutationError:
        logger.exception("Failed to update resource %s after secret changed", crd.id)


@kopf.on.update("", "v1", "secrets", field=("data", "ca.crt"))  # type: ignore[arg-type]
def twingate_resource_tls_secret_update(
    namespace, name, diff, memo, logger, twingate_resource_secret_index, **_
):
    logger.info("Secret %s ca.crt changed. Diff: %s", name, diff)

    twingate_resource_refs = twingate_resource_secret_index.get((namespace, name), [])
    if not twingate_resource_refs:
        return

    for resource_ref in twingate_resource_refs:
        update_twingate_resource(resource_ref, memo, logger)
