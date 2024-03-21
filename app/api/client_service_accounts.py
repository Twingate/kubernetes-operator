import logging

from gql import gql
from gql.transport.exceptions import TransportQueryError

from app.api.protocol import TwingateClientProtocol

QUERY_GET_SA_ID_BY_NAME = gql(
    """
    query GetGroupByName($name: String!) {
      serviceAccounts(filter: {name: {eq: $name}}) {
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


class TwingateServiceAccountAPIs:
    def get_service_account_id(
        self: TwingateClientProtocol, service_account_name: str
    ) -> str | None:
        try:
            result = self.execute_gql(
                QUERY_GET_SA_ID_BY_NAME, variable_values={"name": service_account_name}
            )
            return result["serviceAccounts"]["edges"][0]["node"]["id"]
        except (TransportQueryError, IndexError, KeyError):
            logging.exception("Failed to get resource")
            return None
