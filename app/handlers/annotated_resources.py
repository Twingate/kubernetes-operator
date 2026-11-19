"""TwingateResources generated from objects annotated ``resource.twingate.com``.

The Service and HTTPRoute handlers each map their object to a TwingateResource
manifest; these helpers create, update and delete that TwingateResource.
"""

from collections.abc import Callable, Mapping
from typing import cast

import kopf
import kubernetes
from kopf import Body

from app.crds import ResourceType
from app.utils import to_bool

ANNOTATION = "resource.twingate.com"

ALLOWED_EXTRA_ANNOTATIONS: list[tuple[str, Callable]] = [
    ("name", str),
    ("alias", str),
    ("isBrowserShortcutEnabled", to_bool),
    ("securityPolicyId", str),
    ("isVisible", to_bool),
    ("syncLabels", to_bool),
    ("type", str),
]


def k8s_get_twingate_resource(
    namespace: str, name: str, kapi: kubernetes.client.CustomObjectsApi | None = None
) -> dict | None:
    kapi = kapi or kubernetes.client.CustomObjectsApi()
    try:
        return cast(
            dict,
            kapi.get_namespaced_custom_object(
                "twingate.com", "v1beta", namespace, "twingateresources", name
            ),
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


def extra_annotations_spec(annotations: Mapping[str, str]) -> dict:
    """TwingateResource spec fields set by ``resource.twingate.com/<field>``."""
    return {
        key: convert_f(value)
        for key, convert_f in ALLOWED_EXTRA_ANNOTATIONS
        if (value := annotations.get(f"{ANNOTATION}/{key}"))
    }


def create_or_update_twingate_resource(
    kapi: kubernetes.client.CustomObjectsApi,
    owner_body: Body,
    namespace: str,
    resource_subobject: dict,
    *,
    existing_resource_object: dict | None,
    handler: str,
    reason: kopf.Reason,
    logger,
) -> None:
    """Create the TwingateResource owned by ``owner_body``, or update it in place.

    ``existing_resource_object`` is the TwingateResource as the caller read it. The
    update replaces it at that ``resourceVersion``, so a concurrent write in between
    fails with a 409 Conflict instead of being overwritten.
    """
    kopf.adopt(resource_subobject, owner=owner_body)

    resource_object_name = resource_subobject["metadata"]["name"]

    if existing_resource_object:
        delete_if_resource_type_changes(
            kapi,
            namespace,
            existing_resource_object,
            resource_subobject,
            owner_body,
            logger,
            handler=handler,
        )

        logger.info("TwingateResource already exists: %s", existing_resource_object)
        existing_resource_object["spec"] = {
            "id": existing_resource_object["spec"]["id"],
            **resource_subobject["spec"],
        }
        existing_resource_object["metadata"]["labels"] = resource_subobject["metadata"][
            "labels"
        ]
        kapi.replace_namespaced_custom_object(
            "twingate.com",
            "v1beta",
            namespace,
            "twingateresources",
            resource_object_name,
            existing_resource_object,
        )
        kopf.info(
            owner_body,
            reason=f"{handler} ({reason.value})",
            message=f"Updated TwingateResource {resource_object_name}",
        )
    else:
        api_response = kapi.create_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, "twingateresources", resource_subobject
        )
        logger.info("create_namespaced_custom_object response: %s", api_response)
        kopf.info(
            owner_body,
            reason=f"{handler} ({reason.value})",
            message=f"Created TwingateResource {resource_object_name}",
        )


def delete_if_resource_type_changes(
    kapi: kubernetes.client.CustomObjectsApi,
    namespace: str,
    existing_resource_object: dict,
    new_resource_object: dict,
    owner_body: Body,
    logger,
    *,
    handler: str,
) -> None:
    """Delete a generated TwingateResource whose type no longer matches its owner.

    ``spec.type`` is immutable, so the type change is applied by deleting the Resource
    and raising ``kopf.TemporaryError`` so a later retry registers the replacement.
    """
    resource_object_name = existing_resource_object["metadata"]["name"]
    existing_type = existing_resource_object["spec"].get("type", ResourceType.NETWORK)
    new_type = new_resource_object["spec"].get("type", ResourceType.NETWORK)
    if existing_type == new_type:
        return

    logger.info(
        "Deleting TwingateResource %s to recreate it as %s",
        resource_object_name,
        new_type,
    )
    kapi.delete_namespaced_custom_object(
        "twingate.com", "v1beta", namespace, "twingateresources", resource_object_name
    )
    kopf.warn(
        owner_body,
        reason=handler,
        message=f"Recreating TwingateResource {resource_object_name} as {new_type}: "
        "the Twingate Resource is deprovisioned and recreated with a new ID, and group "
        "access is re-granted on the next TwingateResourceAccess reconcile",
    )
    raise kopf.TemporaryError(
        f"Deleting TwingateResource {resource_object_name} to recreate it as "
        f"{new_type}.",
        delay=5,
    )


def delete_twingate_resource(
    kapi: kubernetes.client.CustomObjectsApi,
    owner_body: Body,
    namespace: str,
    resource_object_name: str,
    *,
    handler: str,
    logger,
) -> None:
    logger.info("Deleting TwingateResource: %s", resource_object_name)
    kapi.delete_namespaced_custom_object(
        "twingate.com", "v1beta", namespace, "twingateresources", resource_object_name
    )
    kopf.info(
        owner_body,
        reason=handler,
        message=f"Deleted TwingateResource {resource_object_name}",
    )
