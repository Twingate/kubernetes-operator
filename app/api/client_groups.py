import logging

from gql import gql
from gql.transport.exceptions import TransportQueryError

QUERY_GET_GROUP_ID_BY_NAME = gql(
    """
    query GetGroupByName($name: String!) {
      groups(filter: {name: {eq: $name}}) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
"""
)


class TwingateGroupsAPIs:
    def get_group_id(self, group_name: str) -> str | None:
        try:
            result = self.execute_gql(
                QUERY_GET_GROUP_ID_BY_NAME, variable_values={"name": group_name}
            )
            return result["groups"]["edges"][0]["node"]["id"]
        except (TransportQueryError, IndexError, KeyError):
            logging.exception("Failed to get resource")
            return None
