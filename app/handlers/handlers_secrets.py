import base64

import kopf

from app.api import TwingateAPIClient
from app.api.exceptions import GraphQLMutationError
from app.crds import ResourceSpec
from app.handlers.handlers_services import k8s_get_twingate_resource
from app.utils import validate_pem_x509_certificate


@kopf.on.update("", "v1", "secrets", field=("data", "ca.crt"))  # type: ignore[arg-type]
def twingate_resource_tls_secret_update(
    namespace, name, diff, new, memo, logger, twingate_resource_secret_index, **_
):
    logger.info("Secret %s ca.crt changed. Diff: %s", name, diff)

    twingate_resource_refs = twingate_resource_secret_index.get((namespace, name), [])
    if not twingate_resource_refs:
        return

    try:
        ca_cert = base64.b64decode(new).decode()
        validate_pem_x509_certificate(ca_cert)
    except ValueError as ex:
        raise kopf.PermanentError(f"Secret {name} ca.crt is invalid.") from ex

    for resource_ref in twingate_resource_refs:
        twingate_resource = k8s_get_twingate_resource(
            resource_ref["namespace"], resource_ref["name"]
        )
        if not twingate_resource:
            return

        crd = ResourceSpec(**twingate_resource["spec"])
        if not crd.id:
            return

        try:
            logger.info("Updating resource %s", crd.id)
            client = TwingateAPIClient(memo.twingate_settings, logger=logger)
            resource = client.kubernetes_resource_update_ca_cert(
                id=crd.id,
                name=crd.name,
                address=crd.address,
                remote_network_id=crd.remote_network_id,
                certificate_authority_cert=ca_cert,
            )
            logger.info("Got resource %s", resource)
        except GraphQLMutationError:
            logger.exception(
                "Failed to update resource %s after secret changed", crd.id
            )
