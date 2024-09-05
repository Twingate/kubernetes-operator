import logging

from gql import gql
from gql.transport.exceptions import TransportQueryError

from app.api.exceptions import GraphQLMutationError
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
    mutation CreateGroup($name: String!, $userIds: [ID]) {
      groupCreate(
        name: $name
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

MUT_GROUP_UPDATE = gql(
    _GROUP_FRAGMENT
    + """
    mutation UpdateGroup($id: ID!, $name: String!, $userIds: [ID]) {
        groupUpdate(
            id: $id,
            name: $name
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

MUT_DELETE_GROUP = gql("""
mutation DeleteGroup($id: ID!) {
    groupDelete(id: $id) {
        ok
        error
    }
}
""")


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

    def group_create(
        self: TwingateClientProtocol,
        group: GroupSpec,
        user_ids: list[str] | None = None,
    ) -> str:
        user_ids = user_ids or []
        result = self.execute_mutation(
            "groupCreate",
            MUT_GROUP_CREATE,
            variable_values={
                "name": group.name,
                "userIds": user_ids,
            },
        )
        return result["entity"]["id"]

    def group_update(
        self: TwingateClientProtocol,
        group: GroupSpec,
        user_ids: list[str] | None = None,
    ) -> str:
        user_ids = user_ids or []
        result = self.execute_mutation(
            "groupUpdate",
            MUT_GROUP_UPDATE,
            variable_values={
                "id": group.id,
                "name": group.name,
                "userIds": user_ids,
            },
        )
        return result["entity"]["id"]

    def group_delete(self: TwingateClientProtocol, group_id: str):
        try:
            result = self.execute_mutation(
                "groupDelete",
                MUT_DELETE_GROUP,
                variable_values={"id": group_id},
            )

            return bool(result["ok"])
        except GraphQLMutationError as gql_err:
            if "does not exist" in gql_err.error:
                return True

            raise
        except TransportQueryError:
            return False
