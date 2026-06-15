import os
from datetime import timedelta

import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import CertificateAuthoritySpec
from app.handlers.base import success


def _reconcile_certificate_authority(body, spec, logger, memo, patch):
    ca_spec = CertificateAuthoritySpec(**spec)

    client = TwingateAPIClient(memo.twingate_settings, logger=logger)

    # Already registered and still present on the backend - nothing to do.
    # NOTE: the backend has no CA update mutation, so a rotated cert / renamed CA
    # is reconciled by re-creating it (a new Twingate ID), not by updating in place.
    if ca_spec.id and client.get_certificate_authority(ca_spec.id):
        return success(twingate_id=ca_spec.id)

    certificate = ca_spec.get_certificate()
    if certificate is None:
        raise kopf.TemporaryError(
            f"ca.crt not found yet in Secret "
            f"'{ca_spec.secret_ref.namespace}/{ca_spec.secret_ref.name}'.",
            delay=30,
        )

    ca = client.x509_certificate_authority_create(
        name=ca_spec.name, certificate=certificate
    )
    patch.spec["id"] = ca.id
    kopf.info(
        body,
        reason="Success",
        message=f"Created Certificate Authority on Twingate as {ca.id}",
    )
    return success(twingate_id=ca.id)


@kopf.on.resume("twingatecertificateauthority")
@kopf.on.create("twingatecertificateauthority")
def twingate_certificate_authority_create(body, spec, logger, memo, patch, **_):
    logger.info("twingate_certificate_authority_create: %s", spec)
    return _reconcile_certificate_authority(body, spec, logger, memo, patch)


CA_RECONCILER_INTERVAL = int(os.environ.get("CA_RECONCILER_INTERVAL", timedelta(hours=10).seconds))  # fmt: skip
CA_RECONCILER_INIT_DELAY = int(os.environ.get("CA_RECONCILER_INIT_DELAY", 60))  # fmt: skip
CA_RECONCILER_IDLE = int(os.environ.get("CA_RECONCILER_IDLE", 60))  # fmt: skip


@kopf.timer(
    "twingatecertificateauthority",
    interval=CA_RECONCILER_INTERVAL,
    initial_delay=CA_RECONCILER_INIT_DELAY,
    idle=CA_RECONCILER_IDLE,
)
def twingate_certificate_authority_reconciler(body, spec, logger, memo, patch, **_):
    return _reconcile_certificate_authority(body, spec, logger, memo, patch)


@kopf.on.delete("twingatecertificateauthority")
def twingate_certificate_authority_delete(spec, status, memo, logger, **_):
    logger.info("twingate_certificate_authority_delete: %s. Status: %s", spec, status)
    if not status:
        return

    if ca_id := spec.get("id"):
        client = TwingateAPIClient(memo.twingate_settings, logger=logger)
        try:
            client.x509_certificate_authority_delete(ca_id)
        except GraphQLMutationError as gqlerr:
            # GC teardown order is not guaranteed: the CA may still be referenced
            # by a Gateway that hasn't been deleted yet. Retry so the CA is removed
            # once its Gateway is gone, instead of leaking it.
            if "in use" in gqlerr.message:
                raise kopf.TemporaryError(
                    "Certificate authority still in use, retrying.", delay=30
                ) from gqlerr
            logger.warning("Ignoring certificate authority delete error: %s", gqlerr)
