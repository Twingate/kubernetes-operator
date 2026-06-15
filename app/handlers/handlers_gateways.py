import os
from datetime import timedelta

import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import GatewaySpec
from app.handlers.base import fail, success
from app.utils_k8s import resolve_ref_to_twingate_id, resolve_service_address


def _reconcile_gateway(body, spec, logger, memo, patch):
    gw_spec = GatewaySpec(**spec)
    settings = memo.twingate_settings
    client = TwingateAPIClient(settings, logger=logger)

    # Resolve both references before mutating status so a TemporaryError from
    # either resolver doesn't leave status advertising an address for a Gateway
    # that was never created/updated.
    address = resolve_service_address(
        gw_spec.service_ref.namespace,
        gw_spec.service_ref.name,
        gw_spec.service_ref.port,
    )
    x509_ca_id = resolve_ref_to_twingate_id(
        "twingatecertificateauthorities",
        gw_spec.x509_certificate_authority_ref.namespace,
        gw_spec.x509_certificate_authority_ref.name,
    )
    patch.status["address"] = address

    if gw_spec.id:
        if client.get_gateway(gw_spec.id) is None:
            # Backend entity was deleted out from under us - recreate it.
            gateway = client.gateway_create(
                address=address,
                remote_network_id=settings.remote_network_id,
                x509_ca_id=x509_ca_id,
            )
            patch.spec["id"] = gateway.id
            kopf.info(body, reason="Success", message=f"Recreated as {gateway.id}")
            return success(twingate_id=gateway.id)

        client.gateway_update(
            gateway_id=gw_spec.id,
            remote_network_id=settings.remote_network_id,
            address=address,
            x509_ca_id=x509_ca_id,
        )
        return success(twingate_id=gw_spec.id)

    gateway = client.gateway_create(
        address=address,
        remote_network_id=settings.remote_network_id,
        x509_ca_id=x509_ca_id,
    )
    patch.spec["id"] = gateway.id
    kopf.info(
        body, reason="Success", message=f"Created Gateway on Twingate as {gateway.id}"
    )
    return success(twingate_id=gateway.id)


# Bound retries so a bad ref (e.g. a typo) eventually fails instead of retrying
# forever; the timer reconciler still recovers it if the ref is later fixed.
GATEWAY_HANDLER_TIMEOUT = int(os.environ.get("GATEWAY_HANDLER_TIMEOUT", timedelta(minutes=10).seconds))  # fmt: skip


@kopf.on.resume("twingategateway", timeout=GATEWAY_HANDLER_TIMEOUT)
@kopf.on.create("twingategateway", timeout=GATEWAY_HANDLER_TIMEOUT)
@kopf.on.update("twingategateway", field="spec", timeout=GATEWAY_HANDLER_TIMEOUT)
def twingate_gateway_create_update(body, spec, logger, memo, patch, **kwargs):
    logger.info("twingate_gateway_create_update: %s", spec)

    # If ID changed from `None` to a value we just created it - no need to
    # immediately update. The update handler uses `field="spec"`, so the diff
    # is scoped relative to `spec` (path is `("id",)`, not `("spec", "id")`).
    diff = kwargs.get("diff")
    # fmt: off
    if diff and len(diff) == 1 and diff[0][:3] == ("add", ("id",), None):
        return success()
    # fmt: on

    try:
        return _reconcile_gateway(body, spec, logger, memo, patch)
    except GraphQLMutationError as gqlerr:
        logger.error("Failed to reconcile gateway: %s", gqlerr)
        kopf.exception(body, reason="Failed to reconcile gateway", exc=gqlerr)
        if "does not exist" in gqlerr.message:
            patch.spec["id"] = None
        return fail(error=gqlerr.message)


GATEWAY_RECONCILER_INTERVAL = int(os.environ.get("GATEWAY_RECONCILER_INTERVAL", timedelta(hours=10).seconds))  # fmt: skip
GATEWAY_RECONCILER_INIT_DELAY = int(os.environ.get("GATEWAY_RECONCILER_INIT_DELAY", 60))  # fmt: skip
GATEWAY_RECONCILER_IDLE = int(os.environ.get("GATEWAY_RECONCILER_IDLE", 60))  # fmt: skip


@kopf.timer(
    "twingategateway",
    interval=GATEWAY_RECONCILER_INTERVAL,
    initial_delay=GATEWAY_RECONCILER_INIT_DELAY,
    idle=GATEWAY_RECONCILER_IDLE,
)
def twingate_gateway_reconciler(body, spec, logger, memo, patch, **_):
    return _reconcile_gateway(body, spec, logger, memo, patch)


@kopf.on.delete("twingategateway")
def twingate_gateway_delete(spec, status, memo, logger, **_):
    logger.info("twingate_gateway_delete: %s. Status: %s", spec, status)
    if not status:
        return

    if gateway_id := spec.get("id"):
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        try:
            if not client.gateway_delete(gateway_id):
                # Transport/API error - retry so we don't leak the backend Gateway.
                raise kopf.TemporaryError(
                    "Failed to delete gateway, retrying.", delay=30
                )
        except GraphQLMutationError as gqlerr:
            # Retry while the Gateway is still referenced by a Resource (GC order
            # is not guaranteed) rather than leaking the backend entity.
            if "being used" in gqlerr.message:
                raise kopf.TemporaryError(
                    "Gateway still in use, retrying.", delay=5
                ) from gqlerr
            logger.warning("Ignoring gateway delete error: %s", gqlerr)
