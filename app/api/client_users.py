import logging
from collections.abc import Mapping

from gql import gql
from gql.transport.exceptions import TransportQueryError

from app.api.protocol import TwingateClientProtocol


class TwingateUserAPIs:
    def get_ids_for_emails(
        self: TwingateClientProtocol, emails: list[str]
    ) -> Mapping[str, str]:
        after = None
        result = {}
        while True:
            try:
                page = self.execute_gql(
                    gql("""
                    query GetUserIds($emails: [String!], $after: String, $first: Int = 100) {
                        users(filter: {email: {in: $emails}}, after: $after, first: $first) {
                            pageInfo { endCursor, hasNextPage }
                            edges { node { id, email } }
                        }
                    }
                    """),
                    variable_values={"emails": emails, "after": after},
                )
                users = page["users"]
                page_info = users["pageInfo"]
                for edge in users["edges"]:
                    result[edge["node"]["email"]] = edge["node"]["id"]

                if not page_info["hasNextPage"]:
                    break

                after = page_info["endCursor"]
            except (TransportQueryError, IndexError, KeyError) as ex:
                logging.exception("Failed to get user ids")
                raise ValueError(f"Failed to get user ids: {ex}") from ex

        return result
