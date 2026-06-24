import os
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import CertificateAuthoritySpec, TwingateCertificateAuthorityCRD
from app.handlers.base import success
from app.utils import x509_sha256_fingerprint
from app.utils_k8s import (
    k8s_get_twingate_custom_object,
    k8s_patch_twingate_custom_object,
)


def try_delete_ca(client, ca_id, logger):
    """Best-effort delete of a backend CA.

    The backend only deletes a CA once no Gateway references it, so this is a no-op
    left for a later reconcile while the CA is still in use.
    """
    try:
        client.x509_certificate_authority_delete(ca_id)
        logger.info("Deleted certificate authority %s", ca_id)
    except GraphQLMutationError as gqlerr:
        if "in use" in gqlerr.message:
            logger.info(
                "Certificate authority %s still in use; leaving it for later cleanup.",
                ca_id,
            )
        else:
            logger.warning(
                "Ignoring certificate authority %s delete error: %s", ca_id, gqlerr
            )


def _reconcile_certificate_authority(body, spec, logger, memo, patch):
    ca_spec = CertificateAuthoritySpec(**spec)

    client = TwingateAPIClient(memo.twingate_settings, logger=logger)

    certificate = ca_spec.get_certificate()
    if certificate is None:
        raise kopf.TemporaryError(
            f"ca.crt not found yet in Secret "
            f"'{ca_spec.secret_ref.namespace}/{ca_spec.secret_ref.name}'.",
            delay=30,
        )

    desired_fingerprint = x509_sha256_fingerprint(certificate)

    # The backend has no CA update mutation, so reconciliation re-creates the CA
    # when its certificate changes (a new fingerprint -> a new Twingate ID) rather
    # than updating in place. `name` is only used when creating and is immutable.
    old_id = ca_spec.id
    backend = client.get_certificate_authority(old_id) if old_id else None
    if backend and backend.fingerprint == desired_fingerprint:
        return success(twingate_id=old_id)

    name = ca_spec.name
    if backend is not None:
        # The old CA still holds `ca_spec.name` until it is removed, and the backend
        # rejects duplicate names - so suffix this re-create's name.
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        name = f"{ca_spec.name} ({timestamp})"

    ca = client.x509_certificate_authority_create(name=name, certificate=certificate)

    patch.spec["id"] = ca.id

    if old_id and backend is not None:
        try_delete_ca(client, old_id, logger)

    kopf.info(
        body,
        reason="Success",
        message=f"Created Certificate Authority on Twingate as {ca.id}",
    )
    return success(twingate_id=ca.id)


# Bound retries so a misspelled secretRef eventually fails instead of retrying
# forever; the timer reconciler still recovers it if the ref is later fixed.
CA_HANDLER_TIMEOUT = int(os.environ.get("CA_HANDLER_TIMEOUT", timedelta(minutes=5).seconds))  # fmt: skip


@kopf.on.resume(TwingateCertificateAuthorityCRD.PLURAL, timeout=CA_HANDLER_TIMEOUT)
@kopf.on.create(TwingateCertificateAuthorityCRD.PLURAL, timeout=CA_HANDLER_TIMEOUT)
def twingate_certificate_authority_create(body, spec, logger, memo, patch, **_):
    logger.info("twingate_certificate_authority_create: %s", spec)
    return _reconcile_certificate_authority(body, spec, logger, memo, patch)


CA_RECONCILER_INTERVAL = int(os.environ.get("CA_RECONCILER_INTERVAL", timedelta(hours=10).seconds))  # fmt: skip
CA_RECONCILER_INIT_DELAY = int(os.environ.get("CA_RECONCILER_INIT_DELAY", 60))  # fmt: skip
CA_RECONCILER_IDLE = int(os.environ.get("CA_RECONCILER_IDLE", 60))  # fmt: skip


@kopf.timer(
    TwingateCertificateAuthorityCRD.PLURAL,
    interval=CA_RECONCILER_INTERVAL,
    initial_delay=CA_RECONCILER_INIT_DELAY,
    idle=CA_RECONCILER_IDLE,
)
def twingate_certificate_authority_reconciler(body, spec, logger, memo, patch, **_):
    return _reconcile_certificate_authority(body, spec, logger, memo, patch)


@kopf.on.delete(  # type: ignore[arg-type]
    TwingateCertificateAuthorityCRD.PLURAL, timeout=CA_HANDLER_TIMEOUT
)
def twingate_certificate_authority_delete(
    namespace, name, spec, status, memo, logger, twingate_gateway_ca_index, **_
):
    logger.info("twingate_certificate_authority_delete: %s. Status: %s", spec, status)
    if not status:
        return

    if ca_id := spec.get("id"):
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        try:
            client.x509_certificate_authority_delete(ca_id)
        except GraphQLMutationError as gqlerr:
            # Surface unexpected errors so kopf retries them (the client already
            # treats an already-deleted CA as success).
            if "in use" not in gqlerr.message:
                raise
            # Still referenced (GC order isn't guaranteed). Retry while a Gateway in
            # this cluster references it; otherwise the ref is stale or managed
            # elsewhere and won't clear by waiting, so leave it for later cleanup.
            if twingate_gateway_ca_index.get((namespace, name)):
                raise kopf.TemporaryError(
                    "Certificate authority still in use by a Gateway, retrying.",
                    delay=5,
                ) from gqlerr
            logger.info(
                "Certificate authority still in use but unreferenced in this "
                "cluster; leaving it for later cleanup."
            )


@kopf.index(TwingateCertificateAuthorityCRD.PLURAL)
def twingate_ca_secret_index(namespace, name, spec, **_):
    secret_ref = spec.get("secretRef", {})
    secret_name = secret_ref.get("name")
    secret_namespace = secret_ref.get("namespace") or namespace

    if not secret_name:
        return None

    return {
        (secret_namespace, secret_name): {
            "namespace": namespace,
            "name": name,
        },
    }


@kopf.on.event("", "v1", "secrets", field=("data", "ca.crt"))  # type: ignore[arg-type]
def twingate_ca_tls_secret_update(
    event, namespace, name, memo, logger, twingate_ca_secret_index, **_
):
    if event.get("type") != "MODIFIED":
        return

    ca_refs = twingate_ca_secret_index.get((namespace, name), [])
    if not ca_refs:
        return

    for ca_ref in ca_refs:
        ca_namespace = ca_ref["namespace"]
        ca_name = ca_ref["name"]
        ca_obj = k8s_get_twingate_custom_object(
            TwingateCertificateAuthorityCRD.PLURAL, ca_namespace, ca_name
        )
        if not ca_obj:
            continue

        logger.info(
            "Secret %s changed, reconciling certificate authority %s/%s.",
            name,
            ca_namespace,
            ca_name,
        )
        patch = SimpleNamespace(spec={}, status={})
        try:
            _reconcile_certificate_authority(
                ca_obj, ca_obj["spec"], logger, memo, patch
            )
        except Exception:
            logger.exception(
                "Failed to reconcile certificate authority %s/%s after secret change",
                ca_namespace,
                ca_name,
            )
            continue

        # Persist the patch so a re-created CA's new backend ID (spec.id) is
        # saved back to the CR.
        k8s_patch_twingate_custom_object(
            TwingateCertificateAuthorityCRD.PLURAL, ca_namespace, ca_name, patch
        )
