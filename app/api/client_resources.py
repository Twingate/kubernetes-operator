import base64
from datetime import datetime
from typing import Any, Literal, NamedTuple

from cryptography import x509
from gql import GraphQLRequest
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.api.exceptions import GraphQLMutationError
from app.api.protocol import TwingateClientProtocol
from app.crds import ProtocolPolicy, ResourceProxy, ResourceSpec, ResourceType


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


class Diff(NamedTuple):
    remote: Any
    local: Any


class BaseResource(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    address: ResourceAddress
    is_visible: bool
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
            fragment BaseResourceFields on Resource {
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

    def get_spec_diff(self, crd: ResourceSpec) -> dict[str, Diff]:
        diff = {}
        if self.name != crd.name:
            diff["name"] = Diff(remote=self.name, local=crd.name)

        if self.address.value != crd.address:
            diff["address"] = Diff(remote=self.address.value, local=crd.address)

        if self.alias != crd.alias:
            diff["alias"] = Diff(remote=self.alias, local=crd.alias)

        if self.is_visible != crd.is_visible:
            diff["is_visible"] = Diff(remote=self.is_visible, local=crd.is_visible)

        self_protocols = self.protocols.model_dump() if self.protocols else None
        crd_protocols = crd.protocols.model_dump() if crd.protocols else None
        if self_protocols != crd_protocols:
            diff["protocols"] = Diff(remote=self_protocols, local=crd_protocols)

        if self.remote_network.id != crd.remote_network_id:
            diff["remote_network_id"] = Diff(
                remote=self.remote_network.id, local=crd.remote_network_id
            )

        security_policy_id = self.security_policy and self.security_policy.id
        if security_policy_id != crd.security_policy_id:
            diff["security_policy_id"] = Diff(
                remote=security_policy_id, local=crd.security_policy_id
            )

        return diff

    def to_spec_dict(self) -> dict[str, Any]:
        data = self.model_dump(
            include={
                "id",
                "name",
                "alias",
                "is_visible",
                "protocols",
                "tags",
            }
        )
        data["address"] = self.address.value
        data["remote_network_id"] = self.remote_network.id
        data["security_policy_id"] = (
            self.security_policy.id if self.security_policy else None
        )
        return data

    def get_labels_diff(self, crd_labels: dict[str, str]) -> dict[str, Diff]:
        diff = {}

        metadata_labels = self.to_metadata_labels()
        if metadata_labels != crd_labels:
            diff["tags"] = Diff(remote=metadata_labels, local=crd_labels)

        return diff

    def to_metadata_labels(self) -> dict[str, str]:
        return {tag.key: tag.value for tag in self.tags}


class NetworkResource(BaseResource):
    is_browser_shortcut_enabled: bool

    @staticmethod
    def get_graphql_fragment():
        return (
            BaseResource.get_graphql_fragment()
            + """
            fragment NetworkResourceFields on NetworkResource {
                ...BaseResourceFields
                isBrowserShortcutEnabled
            }
            """
        )

    def get_spec_diff(self, crd: ResourceSpec) -> dict[str, Diff]:
        diff = super().get_spec_diff(crd)
        if self.is_browser_shortcut_enabled != crd.is_browser_shortcut_enabled:
            diff["is_browser_shortcut_enabled"] = Diff(
                remote=self.is_browser_shortcut_enabled,
                local=crd.is_browser_shortcut_enabled,
            )

        return diff

    def to_spec(self, **overrides: Any) -> ResourceSpec:
        data: dict[str, Any] = (
            {
                "type": ResourceType.NETWORK,
                "is_browser_shortcut_enabled": self.is_browser_shortcut_enabled,
            }
            | super().to_spec_dict()
            | overrides
        )

        return ResourceSpec(**data)


class KubernetesResource(BaseResource):
    proxy_address: str
    certificate_authority_cert: str

    @staticmethod
    def get_graphql_fragment():
        return (
            BaseResource.get_graphql_fragment()
            + """
            fragment KubernetesResourceFields on KubernetesResource {
                ...BaseResourceFields
                proxyAddress
                certificateAuthorityCert
            }
            """
        )

    @property
    def x509_ca_cert(self) -> x509.Certificate:
        return x509.load_pem_x509_certificate(self.certificate_authority_cert.encode())

    def get_spec_diff(self, crd: ResourceSpec) -> dict[str, Diff]:
        diff = super().get_spec_diff(crd)
        crd_proxy_address = crd.proxy and crd.proxy.address
        if self.proxy_address != crd_proxy_address:
            diff["proxy_address"] = Diff(
                remote=self.proxy_address, local=crd_proxy_address
            )

        crd_ca_cert = crd.proxy and crd.proxy.x509_ca_cert
        if self.x509_ca_cert != crd_ca_cert:
            diff["certificate_authority_cert"] = Diff(
                remote=self.x509_ca_cert,
                local=crd_ca_cert,
            )

        return diff

    def to_spec(self, **overrides: Any) -> ResourceSpec:
        data: dict[str, Any] = (
            {
                "type": ResourceType.KUBERNETES,
                "proxy": ResourceProxy(
                    address=self.proxy_address,
                    certificate_authority_cert=base64.b64encode(
                        self.certificate_authority_cert.encode()
                    ).decode(),
                ),
            }
            | super().to_spec_dict()
            | overrides
        )
        return ResourceSpec(**data)


# fmt:off

_NETWORK_RESOURCE_FRAGMENT = NetworkResource.get_graphql_fragment()
_KUBERNETES_RESOURCE_FRAGMENT = KubernetesResource.get_graphql_fragment()

QUERY_GET_RESOURCE = BaseResource.get_graphql_fragment() + """
    query GetResource($id: ID!) {
        resource(id: $id) {
            __typename
            ...BaseResourceFields
            ... on NetworkResource {
                isBrowserShortcutEnabled
            }
            ... on KubernetesResource {
                proxyAddress
                certificateAuthorityCert
            }
        }
    }
"""

# region Resource Create Mutations

MUT_CREATE_RESOURCE = _NETWORK_RESOURCE_FRAGMENT + """
    mutation CreateNetworkResource(
        $name: String!
        $address: String!
        $alias: String
        $isVisible: Boolean
        $isBrowserShortcutEnabled: Boolean
        $protocols: ProtocolsInput
        $remoteNetworkId: ID!
        $securityPolicyId: ID
        $tags: [TagInput!]
    ) {
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
              ...NetworkResourceFields
            }
        }
    }
"""

MUT_CREATE_KUBERNETES_RESOURCE = _KUBERNETES_RESOURCE_FRAGMENT + """
    mutation CreateKubernetesResource(
        $name: String!
        $address: String!
        $alias: String
        $isVisible: Boolean
        $protocols: ProtocolsInput
        $remoteNetworkId: ID!
        $securityPolicyId: ID
        $tags: [TagInput!]
        $proxyAddress: String!
        $certificateAuthorityCert: String!
    ) {
        kubernetesResourceCreate(
            name: $name
            address: $address
            alias: $alias
            isVisible: $isVisible
            protocols: $protocols
            remoteNetworkId: $remoteNetworkId
            securityPolicyId: $securityPolicyId
            tags: $tags
            proxyAddress: $proxyAddress
            certificateAuthorityCert: $certificateAuthorityCert
        ) {
            ok
            error
            entity {
              ...KubernetesResourceFields
            }
        }
    }
"""


# endregion

# region Resource Update Mutations

MUT_UPDATE_NETWORK_RESOURCE = _NETWORK_RESOURCE_FRAGMENT + """
    mutation UpdateNetworkResource(
        $id: ID!
        $name: String!
        $address: String!
        $alias: String
        $isVisible: Boolean
        $isBrowserShortcutEnabled: Boolean
        $protocols: ProtocolsInput
        $remoteNetworkId: ID!
        $securityPolicyId: ID
        $tags: [TagInput!]
    ) {
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
                ...NetworkResourceFields
            }
        }
    }
"""

MUT_UPDATE_KUBERNETES_RESOURCE = _KUBERNETES_RESOURCE_FRAGMENT + """
    mutation UpdateKubernetesResource(
        $id: ID!
        $name: String!
        $address: String!
        $alias: String
        $isVisible: Boolean
        $protocols: ProtocolsInput
        $remoteNetworkId: ID!
        $securityPolicyId: ID
        $tags: [TagInput!]
        $proxyAddress: String
        $certificateAuthorityCert: String
    ) {
        kubernetesResourceUpdate(
            id: $id,
            name: $name
            address: $address
            alias: $alias
            isVisible: $isVisible
            protocols: $protocols
            remoteNetworkId: $remoteNetworkId
            securityPolicyId: $securityPolicyId
            tags: $tags
            proxyAddress: $proxyAddress
            certificateAuthorityCert: $certificateAuthorityCert
        ) {
            ok
            error
            entity {
                ...KubernetesResourceFields
            }
        }
    }
"""

# endregion



MUT_DELETE_RESOURCE = """
    mutation DeleteResource($id: ID!) {
        resourceDelete(id: $id) {
            ok
            error
        }
    }
"""


# fmt:on


class TwingateResourceAPIs:
    def get_resource(
        self: TwingateClientProtocol, resource_id: str
    ) -> NetworkResource | KubernetesResource | None:
        try:
            result = self.execute_gql(
                GraphQLRequest(QUERY_GET_RESOURCE, variable_values={"id": resource_id})
            )
            if not result["resource"]:
                return None

            resource_type = result["resource"]["__typename"]
            match resource_type:
                case "NetworkResource":
                    return NetworkResource(**result["resource"])
                case "KubernetesResource":
                    return KubernetesResource(**result["resource"])
                case _:
                    raise ValueError(f"Invalid Resource Type: {resource_type}")
        except TransportQueryError:
            self.logger.exception("Failed to get resource")
            raise

    def resource_create(
        self: TwingateClientProtocol, resource_type: ResourceType, **graphql_arguments
    ) -> NetworkResource | KubernetesResource:
        if resource_type == ResourceType.KUBERNETES:
            return self.kubernetes_resource_create(**graphql_arguments)  # type: ignore[attr-defined]

        return self.network_resource_create(**graphql_arguments)  # type: ignore[attr-defined]

    def network_resource_create(
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
    ) -> NetworkResource:
        result = self.execute_mutation(
            "resourceCreate",
            GraphQLRequest(
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
            ),
        )
        return NetworkResource(**result["entity"])

    def kubernetes_resource_create(
        self: TwingateClientProtocol,
        *,
        name: str,
        address: str,
        alias: str | None,
        is_visible: bool,
        remote_network_id: str,
        security_policy_id: str | None,
        protocols: dict[str, Any],
        tags: list[dict[str, str]],
        proxy_address: str,
        certificate_authority_cert: str,
    ) -> KubernetesResource:
        result = self.execute_mutation(
            "kubernetesResourceCreate",
            GraphQLRequest(
                MUT_CREATE_KUBERNETES_RESOURCE,
                variable_values={
                    "name": name,
                    "address": address,
                    "alias": alias,
                    "isVisible": is_visible,
                    "remoteNetworkId": remote_network_id,
                    "securityPolicyId": security_policy_id,
                    "protocols": protocols,
                    "tags": tags,
                    "proxyAddress": proxy_address,
                    "certificateAuthorityCert": certificate_authority_cert,
                },
            ),
        )
        return KubernetesResource(**result["entity"])

    def resource_update(
        self: TwingateClientProtocol,
        id: str,
        resource_type: ResourceType,
        **graphql_arguments,
    ) -> NetworkResource | KubernetesResource | None:
        if resource_type == ResourceType.KUBERNETES:
            return self.kubernetes_resource_update(id=id, **graphql_arguments)  # type: ignore[attr-defined]

        return self.network_resource_update(id=id, **graphql_arguments)  # type: ignore[attr-defined]

    def network_resource_update(
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
    ) -> NetworkResource | None:
        result = self.execute_mutation(
            "resourceUpdate",
            GraphQLRequest(
                MUT_UPDATE_NETWORK_RESOURCE,
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
            ),
        )
        return NetworkResource(**result["entity"])

    def kubernetes_resource_update(
        self: TwingateClientProtocol,
        *,
        id: str,
        name: str,
        address: str,
        alias: str | None,
        is_visible: bool,
        remote_network_id: str,
        security_policy_id: str | None,
        protocols: dict[str, Any],
        tags: list[dict[str, str]],
        proxy_address: str,
        certificate_authority_cert: str,
    ) -> KubernetesResource | None:
        result = self.execute_mutation(
            "kubernetesResourceUpdate",
            GraphQLRequest(
                MUT_UPDATE_KUBERNETES_RESOURCE,
                variable_values={
                    "id": id,
                    "name": name,
                    "address": address,
                    "alias": alias,
                    "isVisible": is_visible,
                    "remoteNetworkId": remote_network_id,
                    "securityPolicyId": security_policy_id,
                    "protocols": protocols,
                    "tags": tags,
                    "proxyAddress": proxy_address,
                    "certificateAuthorityCert": certificate_authority_cert,
                },
            ),
        )
        return KubernetesResource(**result["entity"])

    def resource_delete(self: TwingateClientProtocol, resource_id: str) -> bool:
        try:
            result = self.execute_mutation(
                "resourceDelete",
                GraphQLRequest(
                    MUT_DELETE_RESOURCE,
                    variable_values={"id": resource_id},
                ),
            )

            return bool(result["ok"])
        except GraphQLMutationError as gql_err:
            if "does not exist" in gql_err.error:
                return True

            raise
        except TransportQueryError:
            return False
