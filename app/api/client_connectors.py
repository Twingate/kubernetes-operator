from gql import gql
from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.api.exceptions import GraphQLMutationError
from app.api.protocol import TwingateClientProtocol
from app.crds import ConnectorSpec


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
    has_status_notifications_enabled: bool = True

    @staticmethod
    def get_graphql_fragment():
        return """
            fragment ConnectorFields on Connector {
                id
                name
                hasStatusNotificationsEnabled
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
mutation CreateConnector($name: String, $hasStatusNotificationsEnabled: Boolean!, $remoteNetworkId: ID!) {
  connectorCreate(name: $name, hasStatusNotificationsEnabled: $hasStatusNotificationsEnabled, remoteNetworkId: $remoteNetworkId) {
    ok
    error
    entity {
      ...ConnectorFields
    }
  }
}
"""
)

MUT_UPDATE_CONNECTOR = gql(
    _CONNECTOR_FRAGMENT
    + """
mutation UpdateConnector($id: ID!, $name: String!, $hasStatusNotificationsEnabled: Boolean!) {
  connectorUpdate(id: $id, name: $name, hasStatusNotificationsEnabled: $hasStatusNotificationsEnabled) {
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
mutation DeleteConnector($id: ID!) {
    connectorDelete(id: $id) {
        ok
        error
    }
}
"""
)


class TwingateConnectorAPI:
    def get_connector(
        self: TwingateClientProtocol, connector_id: str
    ) -> Connector | None:
        try:
            result = self.execute_gql(
                QUERY_GET_CONNECTOR, variable_values={"id": connector_id}
            )
            return Connector(**result["connector"]) if result["connector"] else None
        except TransportQueryError:
            self.logger.exception("Failed to get connector")
            return None

    def connector_create(
        self: TwingateClientProtocol, connector: ConnectorSpec
    ) -> Connector:
        result = self.execute_mutation(
            "connectorCreate",
            MUT_CREATE_CONNECTOR,
            variable_values={
                "name": connector.name,
                "remoteNetworkId": connector.remote_network_id,
                "hasStatusNotificationsEnabled": connector.has_status_notifications_enabled,
            },
        )

        return Connector(**result["entity"])

    def connector_update(
        self: TwingateClientProtocol, connector: ConnectorSpec
    ) -> Connector:
        result = self.execute_mutation(
            "connectorUpdate",
            MUT_UPDATE_CONNECTOR,
            variable_values={
                "id": connector.id,
                "name": connector.name,
                "hasStatusNotificationsEnabled": connector.has_status_notifications_enabled,
            },
        )

        return Connector(**result["entity"])

    def connector_generate_tokens(
        self: TwingateClientProtocol, connector_id: str
    ) -> ConnectorTokens:
        result = self.execute_mutation(
            "connectorGenerateTokens",
            MUT_CONNECTOR_GENERATE_TOKENS,
            variable_values={"connectorId": connector_id},
        )

        tokens = result["connectorTokens"]
        return ConnectorTokens(**tokens)

    def connector_delete(self: TwingateClientProtocol, connector_id: str) -> bool:
        try:
            result = self.execute_mutation(
                "connectorDelete",
                MUT_DELETE_CONNECTOR,
                variable_values={"id": connector_id},
            )
            return bool(result["ok"])
        except GraphQLMutationError as gql_err:
            if "does not exist" in gql_err.error:
                return True

            raise
        except TransportQueryError:
            return False
