import os
from datetime import timedelta
from types import SimpleNamespace

import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import GatewaySpec, TwingateCertificateAuthorityCRD, TwingateGatewayCRD
from app.handlers.base import fail, success
from app.handlers.handlers_certificate_authorities import try_delete_ca
from app.utils_k8s import (
    k8s_get_twingate_custom_object,
    k8s_patch_twingate_custom_object,
    resolve_ref_to_twingate_id,
    resolve_service_address,
)


def _reconcile_gateway(body, spec, logger, memo, patch, status=None):
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
        TwingateCertificateAuthorityCRD.PLURAL,
        gw_spec.x509_certificate_authority_ref.namespace,
        gw_spec.x509_certificate_authority_ref.name,
    )
    patch.status["address"] = address
    patch.status["x509CaId"] = x509_ca_id

    if gw_spec.id and client.get_gateway(gw_spec.id) is not None:
        logger.info("Updating gateway %s", gw_spec.id)
        client.gateway_update(
            gateway_id=gw_spec.id,
            remote_network_id=settings.remote_network_id,
            address=address,
            x509_ca_id=x509_ca_id,
        )
        old_x509_ca_id = (status or {}).get("x509CaId")
        if old_x509_ca_id and old_x509_ca_id != x509_ca_id:
            try_delete_ca(client, old_x509_ca_id, logger)
        return success(twingate_id=gw_spec.id)

    if gw_spec.id:
        logger.info("Gateway %s was deleted, recreating...", gw_spec.id)
    else:
        logger.info("Creating gateway")
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
GATEWAY_HANDLER_TIMEOUT = int(os.environ.get("GATEWAY_HANDLER_TIMEOUT", timedelta(minutes=5).seconds))  # fmt: skip


@kopf.on.resume(TwingateGatewayCRD.PLURAL, timeout=GATEWAY_HANDLER_TIMEOUT)
@kopf.on.create(TwingateGatewayCRD.PLURAL, timeout=GATEWAY_HANDLER_TIMEOUT)
@kopf.on.update(
    TwingateGatewayCRD.PLURAL, field="spec", timeout=GATEWAY_HANDLER_TIMEOUT
)
def twingate_gateway_create_update(
    body, spec, logger, memo, patch, status=None, **kwargs
):
    logger.info("twingate_gateway_create_update: %s", spec)

    # If ID changed from `None` to a value we just created it - no need to
    # immediately update. The update handler uses `field="spec"`, so the diff
    # is scoped relative to `spec` (path is `("id",)`, not `("spec", "id")`).
    diff = kwargs.get("diff")
    # fmt: off
    if diff and len(diff) == 1 and diff[0][:3] == ("add", ("id",), None):
        return success(twingate_id=spec["id"], message="No update required")
    # fmt: on

    try:
        return _reconcile_gateway(body, spec, logger, memo, patch, status=status)
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
    TwingateGatewayCRD.PLURAL,
    interval=GATEWAY_RECONCILER_INTERVAL,
    initial_delay=GATEWAY_RECONCILER_INIT_DELAY,
    idle=GATEWAY_RECONCILER_IDLE,
)
def twingate_gateway_reconciler(body, spec, logger, memo, patch, status=None, **_):
    return _reconcile_gateway(body, spec, logger, memo, patch, status=status)


@kopf.on.delete(  # type: ignore[arg-type]
    TwingateGatewayCRD.PLURAL, timeout=GATEWAY_HANDLER_TIMEOUT
)
def twingate_gateway_delete(
    namespace, name, spec, status, memo, logger, twingate_resource_gateway_index, **_
):
    logger.info("twingate_gateway_delete: %s. Status: %s", spec, status)
    if not status:
        return

    if gateway_id := spec.get("id"):
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        try:
            client.gateway_delete(gateway_id)
        except GraphQLMutationError as gqlerr:
            # Surface unexpected errors so kopf retries them (the client already
            # treats an already-deleted Gateway as success).
            if "being used" not in gqlerr.message:
                raise
            # Still referenced (GC order isn't guaranteed). Retry while a Resource in
            # this cluster references it; otherwise the ref is stale or managed
            # elsewhere and won't clear by waiting, so leave it for later cleanup.
            if twingate_resource_gateway_index.get((namespace, name)):
                raise kopf.TemporaryError(
                    "Gateway still in use by a Resource, retrying.",
                    delay=5,
                ) from gqlerr
            logger.info(
                "Gateway still in use but unreferenced in this cluster; "
                "leaving it for later cleanup."
            )


@kopf.index(TwingateGatewayCRD.PLURAL)
def twingate_gateway_ca_index(namespace, name, spec, **_):
    ca_ref = spec.get("x509CertificateAuthorityRef", {})
    ca_name = ca_ref.get("name")
    ca_namespace = ca_ref.get("namespace") or namespace

    if not ca_name:
        return None

    return {
        (ca_namespace, ca_name): {
            "namespace": namespace,
            "name": name,
        },
    }


@kopf.on.field(  # type: ignore[arg-type]
    TwingateCertificateAuthorityCRD.PLURAL,
    field="spec.id",
    timeout=GATEWAY_HANDLER_TIMEOUT,
)
def twingate_ca_id_changed(
    namespace, name, new, memo, logger, twingate_gateway_ca_index, **_
):
    """Reconcile Gateways referencing a CA whose backend ID changed.

    Gateways resolve the CA ref to its ``spec.id`` at reconcile time, so a recreated
    CA (new id) is pushed to its Gateways promptly instead of waiting for the Gateway
    timer (which stays as a backstop). Also re-drives Gateways that were blocked on a
    not-yet-synced CA.
    """
    if not new:
        return

    gateway_refs = twingate_gateway_ca_index.get((namespace, name), [])
    if not gateway_refs:
        return

    # Re-raise after attempting every Gateway so Kopf retries, without letting one
    # not-yet-ready Gateway starve the others.
    retry_exc: kopf.TemporaryError | None = None

    for gateway_ref in gateway_refs:
        gw_namespace = gateway_ref["namespace"]
        gw_name = gateway_ref["name"]
        gw_obj = k8s_get_twingate_custom_object(
            TwingateGatewayCRD.PLURAL, gw_namespace, gw_name
        )
        if not gw_obj:
            continue

        logger.info(
            "Certificate authority %s id changed, reconciling gateway %s/%s.",
            name,
            gw_namespace,
            gw_name,
        )
        patch = SimpleNamespace(spec={}, status={})
        try:
            _reconcile_gateway(
                gw_obj,
                gw_obj["spec"],
                logger,
                memo,
                patch,
                status=gw_obj.get("status"),
            )
        except kopf.TemporaryError as err:
            # Service not ready yet - retry the event.
            logger.warning(
                "Gateway %s/%s not ready after CA change, will retry: %s",
                gw_namespace,
                gw_name,
                err,
            )
            retry_exc = err
            continue
        except Exception:
            # Non-transient: log and let the Gateway timer be the backstop.
            logger.exception(
                "Failed to reconcile gateway %s/%s after CA change",
                gw_namespace,
                gw_name,
            )
            continue

        # Persist the patch so the Gateway's resolved status (address, x509CaId)
        # and any new backend ID (spec.id) are saved back to the CR.
        k8s_patch_twingate_custom_object(
            TwingateGatewayCRD.PLURAL, gw_namespace, gw_name, patch
        )

    if retry_exc is not None:
        raise retry_exc
