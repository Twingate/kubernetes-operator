import orjson as json
import pytest
import responses

from app.api.client import GraphQLMutationError
from app.api.client_connectors import Connector, ConnectorTokens
from app.crds import ConnectorSpec


class TestConnectorModel:
    def test_construction(self):
        c = Connector(id="id", name="name")
        assert c.id == "id"
        assert c.name == "name"


class TestConnectorTokens:
    def test_construction(self):
        c = ConnectorTokens(accessToken="at", refreshToken="rt")
        assert c.access_token == "at"  # noqa: S105 # nosec
        assert c.refresh_token == "rt"  # noqa: S105 # nosec


class TestTwingateConnectorAPI:
    def test_get_connector_with_valid_id_succeeds(
        self, test_url, api_client, connector_factory, mocked_responses
    ):
        connector = connector_factory()

        success_response = json.dumps({"data": {"connector": connector.model_dump()}})

        mocked_responses.post(test_url, status=200, body=success_response)

        assert connector == api_client.get_connector(connector.id)

    def test_get_connector_with_invalid_id_returns_none(
        self, test_url, api_client, connector_factory, mocked_responses
    ):
        connector = connector_factory()

        failed_response = """
        {
          "errors": [
            {
              "message": "{'id': ['Unable to parse global ID']}",
              "locations": [{"line": 2, "column": 3}],
              "path": ["connector"]
            }
          ],
          "data": {
            "connector": null
          }
        }
        """
        mocked_responses.post(test_url, status=200, body=failed_response)
        result = api_client.get_connector(connector.id)
        assert result is None

    def test_connector_create(
        self, test_url, api_client, connector_factory, mocked_responses
    ):
        connector = connector_factory()
        connector_spec = ConnectorSpec(**connector.model_dump(exclude=["id"]))

        success_response = json.dumps(
            {
                "data": {
                    "connectorCreate": {
                        "ok": True,
                        "entity": connector.model_dump(by_alias=True),
                    }
                }
            }
        )
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "variables": connector_spec.model_dump(
                            include=["name", "remote_network_id"], by_alias=True
                        )
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.connector_create(connector_spec)
        assert result == connector

    def test_connector_create_failure(
        self, test_url, api_client, connector_factory, mocked_responses
    ):
        connector = connector_factory()
        connector_spec = ConnectorSpec(**connector.model_dump(exclude=["id"]))
        success_response = json.dumps(
            {"data": {"connectorCreate": {"ok": False, "error": "some error"}}}
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "variables": connector_spec.model_dump(
                            include=["name", "remote_network_id"], by_alias=True
                        )
                    },
                    strict_match=False,
                )
            ],
        )
        with pytest.raises(
            GraphQLMutationError, match="connectorCreate mutation failed."
        ):
            api_client.connector_create(connector_spec)

    def test_connector_update(
        self, test_url, api_client, connector_factory, mocked_responses
    ):
        connector = connector_factory()
        connector_spec = ConnectorSpec(**connector.model_dump())

        success_response = json.dumps(
            {
                "data": {
                    "connectorUpdate": {
                        "ok": True,
                        "entity": connector.model_dump(by_alias=True),
                    }
                }
            }
        )
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "variables": connector_spec.model_dump(
                            include=["id", "name", "hasStatusNotificationsEnabled"],
                            by_alias=True,
                        )
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.connector_update(connector_spec)
        assert result == connector

    def test_connector_generate_tokens(self, test_url, api_client, mocked_responses):
        connector_id = "test-connector-id"
        success_response = json.dumps(
            {
                "data": {
                    "connectorGenerateTokens": {
                        "ok": True,
                        "connectorTokens": {
                            "accessToken": "test-access-token",
                            "refreshToken": "test-refresh-token",
                        },
                    }
                }
            }
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"connectorId": connector_id}}, strict_match=False
                )
            ],
        )

        tokens = api_client.connector_generate_tokens(connector_id)
        assert tokens.access_token == "test-access-token"  # noqa: S105 # nosec
        assert tokens.refresh_token == "test-refresh-token"  # noqa: S105 # nosec

    def test_connector_delete(self, test_url, api_client, mocked_responses):
        success_response = json.dumps({"data": {"connectorDelete": {"ok": True}}})

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "some-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.connector_delete("some-id")
        assert result is True

    def test_connector_delete_with_invalid_id_returns_false(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = """
                {
                  "errors": [
                    {
                      "message": "{'id': ['Unable to parse global ID']}",
                      "locations": [{"line": 2, "column": 3}],
                      "path": ["connector"]
                    }
                  ],
                  "data": {
                    "connectorDelete": null
                  }
                }
                """

        mocked_responses.post(
            test_url,
            status=200,
            body=failed_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "some-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.connector_delete("some-id")
        assert result is False

    def test_connector_delete_with_id_already_deleted_returns_true(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "connectorDelete": {
                        "ok": False,
                        "error": "Connector with id 'some-id' does not exist",
                    }
                }
            }
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=failed_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "some-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.connector_delete("some-id")
        assert result is True
