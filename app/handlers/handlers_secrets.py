import base64

import kopf
from gql.transport.exceptions import TransportQueryError

from app.api import TwingateAPIClient
from app.api.client_resources import KubernetesResource
from app.api.exceptions import GraphQLMutationError
from app.crds import ResourceSpec
from app.handlers.handlers_services import k8s_get_twingate_resource
from app.utils import validate_pem_x509_certificate


@kopf.on.event("", "v1", "secrets", field="type", value="kubernetes.io/tls")  # type: ignore[arg-type]
def twingate_tls_secret_update(
    event, body, namespace, name, memo, logger, twingate_resource_secret_index, **_
):
    if event.get("type") != "MODIFIED":
        return

    logger.info("Secret %s content is modified. Body: %s", name, body)

    ca_crt_b64 = body.get("data", {}).get("ca.crt")
    if not ca_crt_b64:
        return

    twingate_resource_refs = twingate_resource_secret_index.get((namespace, name), [])
    if not twingate_resource_refs:
        logger.info(
            "Secret %s is not referenced by any TwingateResource, skipping update.",
            name,
        )
        return

    try:
        local_ca_cert = base64.b64decode(ca_crt_b64).decode()
        validate_pem_x509_certificate(local_ca_cert)
    except ValueError:
        logger.error("Secret %s ca.crt is invalid, skipping update.", name)
        return

    client = TwingateAPIClient(memo.twingate_settings, logger=logger)

    for resource_ref in twingate_resource_refs:
        twingate_resource = k8s_get_twingate_resource(
            resource_ref["namespace"], resource_ref["name"]
        )
        if not twingate_resource:
            continue

        crd = ResourceSpec(**twingate_resource["spec"])
        if not crd.id:
            continue

        try:
            remote_resource = client.get_resource(crd.id)
            if not isinstance(remote_resource, KubernetesResource):
                continue

            if remote_resource.certificate_authority_cert == local_ca_cert:
                logger.info(
                    "Secret %s ca.crt is unchanged for resource %s, skipping update.",
                    name,
                    crd.id,
                )
                continue

            logger.info("Updating resource %s", crd.id)
            resource = client.kubernetes_resource_update_ca_cert(
                id=crd.id,
                name=crd.name,
                address=crd.address,
                remote_network_id=crd.remote_network_id,
                certificate_authority_cert=local_ca_cert,
            )
            logger.info("Got resource %s", resource)
        except GraphQLMutationError:
            logger.exception(
                "Failed to update resource %s after secret changed", crd.id
            )
        except TransportQueryError:
            logger.exception("Failed to get resource %s after secret changed", crd.id)
