from gql import GraphQLRequest
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel

from app.api.protocol import TwingateClientProtocol


class RemoteNetwork(BaseModel):
    id: str
    name: str

    @staticmethod
    def get_graphql_fragment():
        return """
            fragment RemoteNetworkFields on RemoteNetwork {
                id
                name
            }
        """


_RN_FRAGMENT = RemoteNetwork.get_graphql_fragment()

QUERY_GET_RN_BY_NAME = (
    _RN_FRAGMENT
    + """
    query GetRemoteNetworkByName($name: String!) {
      rn: remoteNetwork(name: $name) {
        ...RemoteNetworkFields
      }
    }
"""
)


class TwingateRemoteNetworksAPIs:
    def get_remote_network_by_name(
        self: TwingateClientProtocol, name: str
    ) -> RemoteNetwork | None:
        try:
            result = self.execute_gql(
                GraphQLRequest(QUERY_GET_RN_BY_NAME, variable_values={"name": name})
            )
            return RemoteNetwork(**result["rn"]) if result["rn"] else None
        except TransportQueryError:
            self.logger.exception("Failed to get remote network")
            return None
