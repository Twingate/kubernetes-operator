from gql import gql
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel, ConfigDict, Field

from app.api.exceptions import GraphQLMutationError
from app.api.protocol import TwingateClientProtocol


class AccessInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    principal_id: str = Field(alias="principalId")
    security_policy_id: str | None = Field(alias="securityPolicyId")


# fmt:off

MUT_RESOURCE_ADD_ACCESS = gql( """
    mutation ResourceAccessAdd($resourceId: ID!, $access: [AccessInput!]!) {
      resourceAccessAdd(resourceId: $resourceId, access: $access) {
        ok
        error
      }
    }
""")

MUT_RESOURCE_REMOVE_ACCESS = gql("""
    mutation ResourceAccessRemove($resourceId: ID!, $principalId: ID!) {
      resourceAccessRemove(resourceId: $resourceId, principalIds: [$principalId]) {
        ok
        error
      }
    }
""")

# fmt:on


class TwingateResourceAccessAPIs:
    def resource_access_add(
        self: TwingateClientProtocol,
        resource_id: str,
        principal_id: str,
        security_policy_id: str | None,
    ) -> bool:
        access = AccessInput(
            principal_id=principal_id, security_policy_id=security_policy_id
        )
        access_list = [access.model_dump(by_alias=True)]
        result = self.execute_mutation(
            "resourceAccessAdd",
            MUT_RESOURCE_ADD_ACCESS,
            variable_values={"resourceId": resource_id, "access": access_list},
        )
        return result["ok"]

    def resource_access_remove(
        self: TwingateClientProtocol, resource_id: str, principal_id: str
    ):
        try:
            result = self.execute_mutation(
                "resourceAccessRemove",
                MUT_RESOURCE_REMOVE_ACCESS,
                variable_values={
                    "resourceId": resource_id,
                    "principalId": principal_id,
                },
            )
            return result["ok"]
        except GraphQLMutationError as gql_err:
            if "does not exist" in gql_err.error:
                return True

            raise
        except TransportQueryError:
            return False
