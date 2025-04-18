from datetime import datetime
from typing import Any, Literal

from gql import gql
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.api.exceptions import GraphQLMutationError
from app.api.protocol import TwingateClientProtocol
from app.crds import ProtocolPolicy, ResourceSpec


class ResourceAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Literal["IP", "DNS"]
    value: str


class ResourceRemoteNetwork(BaseModel):
    id: str


class ResourceSecurityPolicy(BaseModel):
    id: str


class ProtocoRange(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    start: int = Field(ge=0, le=65535)
    end: int = Field(ge=0, le=65535)


class ResourceProtocol(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    policy: ProtocolPolicy = ProtocolPolicy.ALLOW_ALL
    ports: list[ProtocoRange] = Field(default_factory=list)


class ResourceProtocols(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    allow_icmp: bool = True
    tcp: ResourceProtocol = Field(default_factory=ResourceProtocol)
    udp: ResourceProtocol = Field(default_factory=ResourceProtocol)


class Tag(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    key: str
    value: str


class Resource(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    address: ResourceAddress
    is_visible: bool
    is_browser_shortcut_enabled: bool
    remote_network: ResourceRemoteNetwork
    alias: str | None = None
    security_policy: ResourceSecurityPolicy | None = Field(
        alias="securityPolicy", default=None
    )
    protocols: ResourceProtocols = Field(default_factory=ResourceProtocols)
    tags: list[Tag]

    @staticmethod
    def get_graphql_fragment():
        return """
            fragment ResourceFields on Resource {
                id
                name
                createdAt
                updatedAt
                address {
                  type
                  value
                }
                alias
                isVisible
                isBrowserShortcutEnabled
                remoteNetwork { id }
                securityPolicy { id }
                protocols {
                    allowIcmp
                    tcp {
                        policy
                        ports {
                            start
                            end
                        }
                    }
                    udp {
                        policy
                        ports {
                            start
                            end
                        }
                    }
                }
                tags {
                    key
                    value
                }
            }
        """

    def is_matching_spec(self, crd: ResourceSpec) -> bool:
        self_protocols = self.protocols.model_dump() if self.protocols else None
        crd_protocols = crd.protocols.model_dump() if crd.protocols else None

        return (
            self.name == crd.name
            and self.address.value == crd.address
            and self.alias == crd.alias
            and self.is_visible == crd.is_visible
            and self.is_browser_shortcut_enabled == crd.is_browser_shortcut_enabled
            and self_protocols == crd_protocols
            and self.remote_network.id == crd.remote_network_id
            and (self.security_policy and self.security_policy.id)
            == crd.security_policy_id
        )

    def is_matching_labels(self, crd_labels: dict[str, str]) -> bool:
        return crd_labels == self.to_metadata_labels()

    def to_spec(self, **overrides: Any) -> ResourceSpec:
        data = self.model_dump(
            include={
                "id",
                "name",
                "alias",
                "is_visible",
                "is_browser_shortcut_enabled",
                "protocols",
                "tags",
            }
        )
        data["address"] = self.address.value
        data["remote_network_id"] = self.remote_network.id
        data["security_policy_id"] = (
            self.security_policy.id if self.security_policy else None
        )
        data.update(overrides)
        return ResourceSpec(**data)

    def to_metadata_labels(self) -> dict[str, str]:
        return {tag.key: tag.value for tag in self.tags}


# fmt:off

_RESOURCE_FRAGMENT = Resource.get_graphql_fragment()

QUERY_GET_RESOURCE = gql(_RESOURCE_FRAGMENT + """
    query GetResource($id: ID!) {
      resource(id: $id) {
        ...ResourceFields
      }
    }
"""
)

MUT_CREATE_RESOURCE = gql(_RESOURCE_FRAGMENT + """
    mutation CreateResource($name: String!, $address: String!, $alias: String, $isVisible: Boolean, $isBrowserShortcutEnabled: Boolean, $protocols: ProtocolsInput, $remoteNetworkId: ID!, $securityPolicyId: ID, $tags: [TagInput!]) {
      resourceCreate(
        name: $name
        address: $address
        alias: $alias
        isVisible: $isVisible
        isBrowserShortcutEnabled: $isBrowserShortcutEnabled
        protocols: $protocols
        remoteNetworkId: $remoteNetworkId
        securityPolicyId: $securityPolicyId
        tags: $tags
      ) {
        ok
        error
        entity {
          ...ResourceFields
        }
      }
    }
"""
)

MUT_UPDATE_RESOURCE = gql(_RESOURCE_FRAGMENT + """
    mutation UpdateResource($id: ID!, $name: String!, $address: String!, $alias: String, $isVisible: Boolean, $isBrowserShortcutEnabled: Boolean, $protocols: ProtocolsInput, $remoteNetworkId: ID!, $securityPolicyId: ID, $tags: [TagInput!]) {
        resourceUpdate(
            id: $id,
            name: $name
            address: $address
            alias: $alias
            isVisible: $isVisible
            isBrowserShortcutEnabled: $isBrowserShortcutEnabled
            protocols: $protocols
            remoteNetworkId: $remoteNetworkId
            securityPolicyId: $securityPolicyId
            tags: $tags
        ) {
            ok
            error
            entity {
                ...ResourceFields
            }
        }
    }
"""
)

MUT_DELETE_RESOURCE = gql("""
mutation DeleteResource($id: ID!) {
    resourceDelete(id: $id) {
        ok
        error
    }
}
"""
)

# fmt:on


class TwingateResourceAPIs:
    def get_resource(self: TwingateClientProtocol, resource_id: str) -> Resource | None:
        try:
            result = self.execute_gql(
                QUERY_GET_RESOURCE, variable_values={"id": resource_id}
            )
            return Resource(**result["resource"]) if result["resource"] else None
        except TransportQueryError:
            self.logger.exception("Failed to get resource")
            return None

    def resource_create(
        self: TwingateClientProtocol,
        *,
        name: str,
        address: str,
        alias: str | None,
        is_visible: bool,
        is_browser_shortcut_enabled: bool,
        remote_network_id: str,
        security_policy_id: str | None,
        protocols: dict[str, Any],
        tags: list[dict[str, str]],
    ) -> Resource:
        result = self.execute_mutation(
            "resourceCreate",
            MUT_CREATE_RESOURCE,
            variable_values={
                "name": name,
                "address": address,
                "alias": alias,
                "isVisible": is_visible,
                "isBrowserShortcutEnabled": is_browser_shortcut_enabled,
                "remoteNetworkId": remote_network_id,
                "securityPolicyId": security_policy_id,
                "protocols": protocols,
                "tags": tags,
            },
        )
        return Resource(**result["entity"])

    def resource_update(
        self: TwingateClientProtocol,
        *,
        id: str,
        name: str,
        address: str,
        alias: str | None,
        is_visible: bool,
        is_browser_shortcut_enabled: bool,
        remote_network_id: str,
        security_policy_id: str | None,
        protocols: dict[str, Any],
        tags: list[dict[str, str]],
    ) -> Resource | None:
        result = self.execute_mutation(
            "resourceUpdate",
            MUT_UPDATE_RESOURCE,
            variable_values={
                "id": id,
                "name": name,
                "address": address,
                "alias": alias,
                "isVisible": is_visible,
                "isBrowserShortcutEnabled": is_browser_shortcut_enabled,
                "remoteNetworkId": remote_network_id,
                "securityPolicyId": security_policy_id,
                "protocols": protocols,
                "tags": tags,
            },
        )
        return Resource(**result["entity"])

    def resource_delete(self: TwingateClientProtocol, resource_id: str) -> bool:
        try:
            result = self.execute_mutation(
                "resourceDelete",
                MUT_DELETE_RESOURCE,
                variable_values={"id": resource_id},
            )

            return bool(result["ok"])
        except GraphQLMutationError as gql_err:
            if "does not exist" in gql_err.error:
                return True

            raise
        except TransportQueryError:
            return False
