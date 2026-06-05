from gql import GraphQLRequest
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel

from app.api.exceptions import GraphQLMutationError
from app.api.protocol import TwingateClientProtocol


class Gateway(BaseModel):
    id: str
    address: str


_GATEWAY_FRAGMENT = """
    fragment GatewayFields on Gateway {
        id
        address
    }
"""

QUERY_GET_GATEWAY = (
    _GATEWAY_FRAGMENT
    + """
    query GetGateway($id: ID!) {
      gateway(id: $id) {
        ...GatewayFields
      }
    }
"""
)

MUT_CREATE_GATEWAY = (
    _GATEWAY_FRAGMENT
    + """
    mutation CreateGateway($address: String!, $remoteNetworkId: ID!, $x509CAId: ID!) {
      gatewayCreate(
        address: $address
        remoteNetworkId: $remoteNetworkId
        x509CAId: $x509CAId
      ) {
        ok
        error
        entity {
          ...GatewayFields
        }
      }
    }
"""
)

MUT_UPDATE_GATEWAY = (
    _GATEWAY_FRAGMENT
    + """
    mutation UpdateGateway(
        $id: ID!
        $remoteNetworkId: ID!
        $address: String
        $x509CAId: ID
    ) {
      gatewayUpdate(
        id: $id
        remoteNetworkId: $remoteNetworkId
        address: $address
        x509CAId: $x509CAId
      ) {
        ok
        error
        entity {
          ...GatewayFields
        }
      }
    }
"""
)

MUT_DELETE_GATEWAY = """
    mutation DeleteGateway($id: ID!) {
      gatewayDelete(id: $id) {
        ok
        error
      }
    }
"""


class TwingateGatewayAPIs:
    def get_gateway(self: TwingateClientProtocol, gateway_id: str) -> Gateway | None:
        try:
            result = self.execute_gql(
                GraphQLRequest(QUERY_GET_GATEWAY, variable_values={"id": gateway_id})
            )
            return Gateway(**result["gateway"]) if result["gateway"] else None
        except (TransportQueryError, KeyError):
            self.logger.exception("Failed to get gateway")
            return None

    def gateway_create(
        self: TwingateClientProtocol,
        *,
        address: str,
        remote_network_id: str,
        x509_ca_id: str,
    ) -> Gateway:
        result = self.execute_mutation(
            "gatewayCreate",
            GraphQLRequest(
                MUT_CREATE_GATEWAY,
                variable_values={
                    "address": address,
                    "remoteNetworkId": remote_network_id,
                    "x509CAId": x509_ca_id,
                },
            ),
        )
        return Gateway(**result["entity"])

    def gateway_update(
        self: TwingateClientProtocol,
        *,
        gateway_id: str,
        remote_network_id: str,
        address: str | None = None,
        x509_ca_id: str | None = None,
    ) -> Gateway:
        result = self.execute_mutation(
            "gatewayUpdate",
            GraphQLRequest(
                MUT_UPDATE_GATEWAY,
                variable_values={
                    "id": gateway_id,
                    "remoteNetworkId": remote_network_id,
                    "address": address,
                    "x509CAId": x509_ca_id,
                },
            ),
        )
        return Gateway(**result["entity"])

    def gateway_delete(self: TwingateClientProtocol, gateway_id: str) -> bool:
        try:
            result = self.execute_mutation(
                "gatewayDelete",
                GraphQLRequest(MUT_DELETE_GATEWAY, variable_values={"id": gateway_id}),
            )
            return bool(result["ok"])
        except GraphQLMutationError:
            raise
        except TransportQueryError:
            return False
