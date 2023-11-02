import logging

from gql import gql
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.api.protocol import TwingateClientProtocol


class ConnectorTokens(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    access_token: str
    refresh_token: str


class Connector(BaseModel):
    model_config = ConfigDict(
        frozen=True, populate_by_name=True, alias_generator=to_camel
    )

    id: str
    name: str

    @staticmethod
    def get_graphql_fragment():
        return """
            fragment ConnectorFields on Connector {
                id
                name
            }
        """


_CONNECTOR_FRAGMENT = Connector.get_graphql_fragment()

QUERY_GET_CONNECTOR = gql(
    _CONNECTOR_FRAGMENT
    + """
    query GetConnector($id: ID!) {
      connector(id: $id) {
        ...ConnectorFields
      }
    }
"""
)

MUT_CREATE_CONNECTOR = gql(
    _CONNECTOR_FRAGMENT
    + """
mutation CreateConnector($name: String, $remoteNetworkId: ID!) {
  connectorCreate(name: $name, remoteNetworkId: $remoteNetworkId) {
    ok
    error
    entity {
      ...ConnectorFields
    }
  }
}
"""
)

MUT_CONNECTOR_GENERATE_TOKENS = gql(
    """
mutation GenerateConnectorTokens($connectorId: ID!) {
    connectorGenerateTokens(connectorId: $connectorId) {
        ok
        error
        connectorTokens {
            accessToken
            refreshToken
        }
    }
}
"""
)

MUT_DELETE_CONNECTOR = gql(
    """
mutation DeleteResource($id: ID!) {
    resourceDelete(id: $id) {
        ok
        error
    }
}
"""
)


class TwingateConnectorsAPI:
    def get_connector(
        self: TwingateClientProtocol, connector_id: str
    ) -> Connector | None:
        try:
            result = self.execute_gql(
                QUERY_GET_CONNECTOR, variable_values={"id": connector_id}
            )
            return Connector(**result["connector"]) if result["connector"] else None
        except TransportQueryError:
            logging.exception("Failed to get connector")
            return None

    def connector_create(
        self: TwingateClientProtocol, name: str | None, remote_network_id: str
    ) -> Connector | None:
        result = self.execute_mutation(
            "connectorCreate",
            MUT_CREATE_CONNECTOR,
            variable_values={"name": name, "remoteNetworkId": remote_network_id},
        )

        if bool(result["ok"]):
            connector = result["entity"]
            return Connector(**connector)

        logging.error("Failed to create connector %s: %s", name, result["error"])
        return None

    def connector_generate_tokens(
        self: TwingateClientProtocol, connector_id: str
    ) -> ConnectorTokens | None:
        result = self.execute_mutation(
            "connectorGenerateTokens",
            MUT_CONNECTOR_GENERATE_TOKENS,
            variable_values={"connectorId": connector_id},
        )

        if bool(result["ok"]):
            tokens = result["connectorTokens"]
            return ConnectorTokens(**tokens)

        logging.error(
            "Failed to generate tokens for connector %s: %s",
            connector_id,
            result["error"],
        )
        return None

    def connector_delete(self: TwingateClientProtocol, connector_id: str) -> bool:
        try:
            result = self.execute_mutation(
                "connectorDelete",
                MUT_DELETE_CONNECTOR,
                variable_values={"id": connector_id},
            )

            return bool(result["ok"])
        except AttributeError:
            return False
