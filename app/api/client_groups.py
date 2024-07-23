import logging

from gql import gql
from gql.transport.exceptions import TransportQueryError

from app.api.protocol import TwingateClientProtocol
from app.crds import GroupSpec

_GROUP_FRAGMENT = """
    fragment GroupFields on Group {
        id
        name
        createdAt
        updatedAt
    }
"""

QUERY_GET_GROUP_ID_BY_NAME = gql(
    _GROUP_FRAGMENT
    + """
    query GetGroupByName($name: String!) {
      groups(filter: {name: {eq: $name}}) {
        edges {
          node {
            ...GroupFields
          }
        }
      }
    }
"""
)

MUT_GROUP_CREATE = gql(
    _GROUP_FRAGMENT
    + """
    mutation CreateGroup($name: String!, $securityPolicyId: ID, $userIds: [ID]) {
      groupCreate(
        name: $name
        securityPolicyId: $securityPolicyId
        userIds: $userIds
      ) {
        ok
        error
        entity {
          ...GroupFields
        }
      }
    }
"""
)


class TwingateGroupAPIs:
    def get_group_id(self: TwingateClientProtocol, group_name: str) -> str | None:
        try:
            result = self.execute_gql(
                QUERY_GET_GROUP_ID_BY_NAME, variable_values={"name": group_name}
            )
            return result["groups"]["edges"][0]["node"]["id"]
        except (TransportQueryError, IndexError, KeyError):
            logging.exception("Failed to get resource")
            return None

    def group_create(self: TwingateClientProtocol, group: GroupSpec):
        member_emails = [v for v in group.members if "@" in v]
        member_ids = [v for v in group.members if "@" not in v]

        member_emails_ids = self.__get_user_ids(member_emails)
        member_ids.extend(member_emails_ids)

        result = self.execute_mutation(
            "groupCreate",
            MUT_GROUP_CREATE,
            variable_values={
                "name": group.name,
                "securityPolicyId": group.security_policy_id,
                "userIds": member_ids,
            },
        )
        return result["entity"]
