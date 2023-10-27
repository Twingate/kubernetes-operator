import logging
from collections.abc import MutableMapping
from typing import Any

import kubernetes.client
from pydantic import BaseModel, ConfigDict, Field

from app.settings import get_settings

K8sObject = MutableMapping[Any, Any]
OptionalK8sObject = K8sObject | None


class K8sMetadata(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    uid: str
    name: str
    namespace: str

    @property
    def owner_reference_object(self) -> dict:
        return {
            "apiVersion": "twingate.com/v1",
            "kind": "TwingateResource",
            "name": self.name,
            "uid": self.uid,
        }


class BaseK8sModel(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    api_version: str = Field(alias="apiVersion")
    kind: str
    metadata: K8sMetadata
    status: dict[str, Any] | None = None


# region TwingateResourceCRD


class ResourceSpec(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    id: str | None = None
    name: str
    address: str
    alias: str | None = None
    remote_network_id: str = Field(
        alias="remoteNetworkId",
        default_factory=lambda: get_settings().remote_network_id,
    )
    security_policy_id: str | None = Field(alias="securityPolicyId", default=None)


class TwingateResourceCRD(BaseK8sModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    spec: ResourceSpec


# endregion

# region TwingateResourceAccessCRD


class _ResourceRef(BaseModel):
    name: str
    namespace: str = Field(default="default")


class ResourceAccessSpec(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resource_ref: _ResourceRef = Field(alias="resourceRef")
    principal_id: str = Field(alias="principalId")
    security_policy_id: str | None = Field(alias="securityPolicyId", default=None)

    @property
    def resource_ref_fullname(self) -> str:
        return f"{self.resource_ref.namespace}/{self.resource_ref.name}"

    def get_resource_ref_object(self) -> OptionalK8sObject:
        try:
            kapi = kubernetes.client.CustomObjectsApi()
            response = kapi.get_namespaced_custom_object(
                "twingate.com",
                "v1",
                self.resource_ref.namespace,
                "twingateresources",
                self.resource_ref.name,
            )
            logging.info("ResourceAccessCRD.get_resource_ref_object got: %s", response)
            return response
        except kubernetes.client.exceptions.ApiException as api_ex:
            if api_ex.status == 404:
                logging.warning(
                    "ResourceAccessCRD.get_resource_ref_object: resource not found."
                )
            else:
                logging.exception("ResourceAccessCRD.get_resource_ref_object failed")

            return None

    def get_resource(self) -> TwingateResourceCRD | None:
        resource_ref_object = self.get_resource_ref_object()
        if not resource_ref_object:
            return None

        resource = ResourceSpec(**resource_ref_object.pop("spec"))
        metadata = K8sMetadata(**resource_ref_object.pop("metadata"))
        return TwingateResourceCRD(
            metadata=metadata, spec=resource, **resource_ref_object
        )


class TwingateResourceAccessCRD(BaseK8sModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    spec: ResourceAccessSpec


# endregion
