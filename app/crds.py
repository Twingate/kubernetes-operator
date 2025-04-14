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

from app.settings import get_settings
from app.version_policy_providers import get_provider

K8sObject = MutableMapping[Any, Any]
OptionalK8sObject = K8sObject | None

logger = logging.getLogger(__name__)


class K8sMetadata(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, extra="allow", alias_generator=to_camel
    )

    uid: str
    name: str
    namespace: str
    labels: dict[str, str] = {}

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


class _KubernetesObjectRef(BaseModel):
    name: str
    namespace: str = Field(default="default")


# region TwingateResourceCRD


class ProtocolPolicy(str, Enum):
    ALLOW_ALL = "ALLOW_ALL"
    RESTRICTED = "RESTRICTED"


class ProtocolRange(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    start: int = Field(ge=1, le=65535)
    end: int = Field(ge=1, le=65535)

    @model_validator(mode="after")
    def check_ports(self):
        if self.start > self.end:
            raise ValueError("Start port value must be less or equal to end port value")

        return self


class ResourceProtocol(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    policy: ProtocolPolicy = ProtocolPolicy.ALLOW_ALL
    ports: list[ProtocolRange] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_policy_ports(self):
        if self.policy == ProtocolPolicy.ALLOW_ALL and self.ports:
            raise ValueError("ports can't be set if policy is ALLOW_ALL")

        return self


class ResourceProtocols(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    allow_icmp: bool | None = True
    tcp: ResourceProtocol = Field(default_factory=ResourceProtocol)
    udp: ResourceProtocol = Field(default_factory=ResourceProtocol)


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
    protocols: ResourceProtocols = Field(default_factory=ResourceProtocols)
    sync_labels: bool = True

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


class PrincipalTypeEnum(str, Enum):
    Group = "group"
    ServiceAccount = "serviceAccount"


class _PrincipalExternalRef(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    type: PrincipalTypeEnum
    name: str


class ResourceAccessSpec(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    resource_ref: _KubernetesObjectRef
    principal_id: str | None = None
    group_ref: _KubernetesObjectRef | None = None
    principal_external_ref: _PrincipalExternalRef | None = None
    security_policy_id: str | None = None

    @model_validator(mode="after")
    def validate_target_ref_exists(self):
        if self.principal_id or self.group_ref or self.principal_external_ref:
            return self

        raise ValueError("Missing principal_id, group_ref or principal_external_ref")

    @property
    def resource_ref_fullname(self) -> str:
        return f"{self.resource_ref.namespace}/{self.resource_ref.name}"

    def _get_ref_object(
        self, plural_type: str, namespace: str, name: str
    ) -> OptionalK8sObject:
        log_prefix = (
            f"ResourceAccessCRD._get_ref_object({plural_type}, {namespace}, {name}):"
        )
        try:
            kapi = kubernetes.client.CustomObjectsApi()
            response = kapi.get_namespaced_custom_object(
                "twingate.com",
                "v1beta",
                namespace,
                plural_type,
                name,
            )
            logger.info(
                "%s got %s",
                log_prefix,
                response,
            )
            return response
        except kubernetes.client.exceptions.ApiException as api_ex:
            if api_ex.status == 404:
                logger.warning("%s resource not found.", log_prefix)
            else:
                logger.exception("%s failed", log_prefix)

            return None

    def get_resource_ref_object(self) -> OptionalK8sObject:
        return self._get_ref_object(
            "twingateresources", self.resource_ref.namespace, self.resource_ref.name
        )

    def get_group_ref_object(self) -> OptionalK8sObject:
        if not self.group_ref:
            return None

        return self._get_ref_object(
            "twingategroups", self.group_ref.namespace, self.group_ref.name
        )

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


class ConnectorImagePolicyProvidersEnum(str, Enum):
    dockerhub = "dockerhub"
    google = "google"


class ConnectorImagePolicy(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel, extra="allow"
    )

    provider: ConnectorImagePolicyProvidersEnum = (
        ConnectorImagePolicyProvidersEnum.dockerhub
    )
    repository: str = "twingate/connector"
    schedule: str = "0 0 * * *"
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
        try:
            croniter(v)
            return v
        except ValueError as vex:
            raise ValueError("Invalid schedule value") from vex

    def get_next_date_iso8601(self) -> str:
        next_date = croniter(self.schedule, pendulum.now("UTC"), datetime).get_next()
        return pendulum.instance(next_date).to_iso8601_string()

    def get_image(self) -> str:
        provider = get_provider(self.provider.value, repository=self.repository)
        if tag := provider.get_latest(
            self.version, allow_prerelease=self.allow_prerelease
        ):
            return f"{self.repository}:{tag}"

        raise ValueError(
            f"Could not find valid tag for '{self.version}' at '{self.repository}'"
        )


class ConnectorImage(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel, extra="allow"
    )

    repository: str = "twingate/connector"
    tag: str = "1"

    def __str__(self):
        return f"{self.repository}:{self.tag}"


class ConnectorSpec(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel, extra="allow"
    )

    id: str | None = None
    name: str | None = None
    log_level: int = 3
    log_analytics: bool = True
    has_status_notifications_enabled: bool = True
    image: ConnectorImage | None = None
    image_policy: ConnectorImagePolicy | None = None
    container_extra: dict[str, Any] = {}
    pod_extra: dict[str, Any] = {}
    pod_annotations: dict[str, Any] = {}
    pod_labels: dict[str, Any] = {}
    sidecar_containers: list[dict[str, Any]] = []

    remote_network_id: str = Field(
        default_factory=lambda: get_settings().remote_network_id
    )

    @model_validator(mode="after")
    def validate_image_or_image_policy(self):
        if self.image or self.image_policy:
            return self

        # Default to having `image`
        return self.model_copy(update=dict(image=ConnectorImage()))

    def get_image(self) -> str:
        if image := self.image:
            return str(image)

        if image_policy := self.image_policy:
            return image_policy.get_image()

        # Impossible to get here because of our model validator
        raise ValueError("Invalid ConnectorSpec")  # pragma: no cover


class TwingateConnectorCRD(BaseK8sModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    spec: ConnectorSpec


# endregion

# region TwingateGroup


class GroupSpec(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    id: str | None = None
    name: str


class TwingateGroupCRD(BaseK8sModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True, extra="allow")

    spec: GroupSpec


# endregion
