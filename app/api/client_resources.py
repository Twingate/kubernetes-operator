import logging
from datetime import datetime
from typing import Any, Literal

from gql import gql
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel, ConfigDict, Field

from app.api.protocol import TwingateClientProtocol
from app.crds import ResourceSpec


class ResourceAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Literal["IP", "DNS"]
    value: str


class ResourceRemoteNetwork(BaseModel):
    id: str


class ResourceSecurityPolicy(BaseModel):
    id: str


class Resource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    address: ResourceAddress
    alias: str | None = None
    remote_network: ResourceRemoteNetwork = Field(alias="remoteNetwork")
    security_policy: ResourceSecurityPolicy | None = Field(
        alias="securityPolicy", default=None
    )

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
                remoteNetwork { id }
                securityPolicy { id }
            }
        """

    def is_matching_spec(self, crd: ResourceSpec) -> bool:
        return (
            self.name == crd.name
            and self.address.value == crd.address
            and self.alias == crd.alias
            and self.remote_network.id == crd.remote_network_id
            and (self.security_policy and self.security_policy.id)
            == crd.security_policy_id
        )

    def to_spec(self, **overrides: Any) -> ResourceSpec:
        data = dict(
            id=self.id,
            name=self.name,
            address=self.address.value,
            alias=self.alias,
            remote_network_id=self.remote_network.id,
            security_policy_id=self.security_policy.id
            if self.security_policy
            else None,
        )
        data.update(overrides)
        return ResourceSpec(**data)  # type: ignore


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
    mutation CreateResource($name: String!, $address: String!, $alias: String, $remoteNetworkId: ID!, $securityPolicyId: ID) {
        resourceCreate(name: $name, address: $address, alias: $alias, remoteNetworkId: $remoteNetworkId, securityPolicyId: $securityPolicyId) {
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
    mutation UpdateResource($id: ID!, $name: String!, $address: String, $alias: String, $remoteNetworkId: ID!, $securityPolicyId: ID) {
        resourceUpdate(id: $id, name: $name, address: $address, alias: $alias, remoteNetworkId: $remoteNetworkId, securityPolicyId: $securityPolicyId) {
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
            logging.exception("Failed to get resource")
            return None

    def resource_create(
        self: TwingateClientProtocol, resource: ResourceSpec
    ) -> Resource | None:
        result = self.execute_mutation(
            "resourceCreate",
            MUT_CREATE_RESOURCE,
            variable_values={
                "name": resource.name,
                "address": resource.address,
                "alias": resource.alias,
                "remoteNetworkId": resource.remote_network_id,
                "securityPolicyId": resource.security_policy_id,
            },
        )

        return Resource(**result["entity"])

    def resource_update(
        self: TwingateClientProtocol, resource: ResourceSpec
    ) -> Resource | None:
        result = self.execute_mutation(
            "resourceUpdate",
            MUT_UPDATE_RESOURCE,
            variable_values={
                "id": resource.id,
                "name": resource.name,
                "address": resource.address,
                "alias": resource.alias,
                "remoteNetworkId": resource.remote_network_id,
                "securityPolicyId": resource.security_policy_id,
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
        except AttributeError:
            return False
