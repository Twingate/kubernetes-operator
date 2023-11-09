import logging
from collections.abc import MutableMapping
from datetime import datetime
from enum import Enum
from typing import Any

import kubernetes.client
import pendulum
from croniter import croniter
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel
from semantic_version import NpmSpec

from app.dockerhub import DockerhubVersionProvider
from app.settings import get_settings

K8sObject = MutableMapping[Any, Any]
OptionalK8sObject = K8sObject | None


class K8sMetadata(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, extra="allow", alias_generator=to_camel
    )

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
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, extra="allow", alias_generator=to_camel
    )

    api_version: str
    kind: str
    metadata: K8sMetadata
    status: dict[str, Any] | None = None


# region TwingateResourceCRD


class ProtocolPolicy(str, Enum):
    ALLOW_ALL = "ALLOW_ALL"
    RESTRICTED = "RESTRICTED"


class ProtocoRange(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    start: int = Field(ge=0, le=65535)
    end: int = Field(ge=0, le=65535)

    @model_validator(mode="after")
    def check_ports(self):
        if self.start > self.end:
            raise ValueError("Start port value must be less or equal to end port value")

        return self


class ResourceProtocol(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    policy: ProtocolPolicy
    ports: list[ProtocoRange] | None = None

    @model_validator(mode="after")
    def check_policy_ports(self):
        if self.policy == ProtocolPolicy.ALLOW_ALL and self.ports:
            raise ValueError("ports can't be set if policy is ALLOW_ALL")

        if self.policy == ProtocolPolicy.RESTRICTED and not self.ports:
            raise ValueError("ports must be set if policy is RESTRICTED")

        return self


class ResourceProtocols(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    allow_icmp: bool | None = None
    tcp: ResourceProtocol | None = None
    udp: ResourceProtocol | None = None


class ResourceSpec(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    id: str | None = None
    name: str
    address: str
    alias: str | None = None
    remote_network_id: str = Field(
        default_factory=lambda: get_settings().remote_network_id
    )
    security_policy_id: str | None = None
    is_visible: bool = True
    is_browser_shortcut_enabled: bool = True
    protocols: ResourceProtocols | None = None

    def __is_wildcard(self):
        return "*" in self.address or "?" in self.address

    @model_validator(mode="after")
    def check_address_if_is_browser_shortcut_enabled(self):
        if self.is_browser_shortcut_enabled and self.__is_wildcard():
            raise ValueError(
                "isBrowserShortcutEnabled can't be True for wildcard addresses"
            )

        return self


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
                "v1beta",
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

# region TwingateConnector


class ConnectorVersionPolicy(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel, extra="allow"
    )

    schedule: str | None = "0 0 * * *"
    version: str = "^1.0.0"
    allow_prerelease: bool = False

    @field_validator("version")
    @classmethod
    def check_valid_version_specifier(cls, v: str, info: ValidationInfo) -> str:
        try:
            NpmSpec(v)
        except ValueError as vex:
            raise ValueError("Invalid version specifier") from vex
        return v

    @field_validator("schedule")
    @classmethod
    def check_valid_crontab(cls, v: str, info: ValidationInfo) -> str:
        if v:
            try:
                croniter(v)
            except ValueError as vex:
                raise ValueError("Invalid schedule value") from vex
        return v

    def get_next_date_iso8601(self) -> str | None:
        if not self.schedule:
            return None

        next_date = croniter(self.schedule, pendulum.now("UTC")).get_next(datetime)
        return pendulum.instance(next_date).to_iso8601_string()


class ConnectorSpec(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel, extra="allow"
    )

    id: str | None = None
    name: str | None = None
    version_policy: ConnectorVersionPolicy = Field(
        default_factory=ConnectorVersionPolicy
    )
    container_extra: dict[str, Any] = {}
    pod_extra: dict[str, Any] = {}

    remote_network_id: str = Field(
        default_factory=lambda: get_settings().remote_network_id
    )

    def get_image_tag_by_policy(self) -> str:
        if tag := DockerhubVersionProvider().get_latest(
            self.version_policy.version,
            allow_prerelease=self.version_policy.allow_prerelease,
        ):
            return tag

        raise ValueError(
            f"Could not find valid tag for '{self.version_policy.version}'"
        )


class TwingateConnectorCRD(BaseK8sModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    spec: ConnectorSpec


# endregion
