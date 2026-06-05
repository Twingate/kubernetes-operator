from datetime import datetime
from typing import Any

import kopf
import kubernetes.client
from pydantic import BaseModel, ConfigDict, Field


def k8s_get_custom_object(
    plural: str,
    namespace: str,
    name: str,
    kapi: kubernetes.client.CustomObjectsApi | None = None,
) -> dict | None:
    kapi = kapi or kubernetes.client.CustomObjectsApi()
    try:
        return kapi.get_namespaced_custom_object(
            "twingate.com", "v1beta", namespace, plural, name
        )
    except kubernetes.client.exceptions.ApiException as ex:
        if ex.status == 404:
            return None
        raise


def resolve_ref_to_backend_id(
    plural: str, namespace: str, name: str, *, delay: int = 30
) -> str:
    """Resolve a reference to another Twingate CRD into its backend ``spec.id``.

    Raises ``kopf.TemporaryError`` (so the handler retries) when the referenced
    object does not exist yet or has not finished syncing to the backend.
    """
    obj = k8s_get_custom_object(plural, namespace, name)
    if obj is None:
        raise kopf.TemporaryError(
            f"Referenced {plural} '{name}' in namespace '{namespace}' not found.",
            delay=delay,
        )

    if backend_id := obj.get("spec", {}).get("id"):
        return backend_id

    raise kopf.TemporaryError(
        f"Referenced {plural} '{name}' in namespace '{namespace}' "
        "has not synced to Twingate yet.",
        delay=delay,
    )


class _HandlerResult(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    ts: datetime = Field(default_factory=datetime.now)
    success: bool


class _HandlerSuccess(_HandlerResult):
    def __init__(self, **data: Any) -> None:
        super().__init__(success=True, **data)


class _HandlerFailure(_HandlerResult):
    def __init__(self, **data: Any) -> None:
        super().__init__(success=False, **data)


def fail(**data: Any) -> dict:
    return _HandlerFailure(**data).model_dump(mode="json")


def success(**data: Any) -> dict:
    return _HandlerSuccess(**data).model_dump(mode="json")
