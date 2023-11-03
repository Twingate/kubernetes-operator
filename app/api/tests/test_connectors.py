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


class TestTwingateConnectorsAPI:
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
        result = api_client.get_resource(connector.id)
        assert result is None

    def test_connector_create(
        self, test_url, api_client, connector_factory, mocked_responses
    ):
        connector = connector_factory()
        connector_spec = ConnectorSpec(**connector.dict(exclude=["id"]))

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
        connector_spec = ConnectorSpec(**connector.dict(exclude=["id"]))
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

    def test_resource_delete(self, test_url, api_client, mocked_responses):
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
