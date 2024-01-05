import orjson as json
import pytest
import responses


@pytest.fixture()
def mock_resource_data():
    return {"id": "1", "name": "My Cluster"}


class TestTwingateResourceAPIs:
    def test_get_rn_with_valid_name_succeeds(
        self, test_url, api_client, mock_resource_data, mocked_responses
    ):
        success_response = json.dumps({"data": {"rn": mock_resource_data}})

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"name": "My Cluster"}}, strict_match=False
                )
            ],
        )
        result = api_client.get_remote_network_by_name("My Cluster")
        assert result.id == mock_resource_data["id"]
        assert result.name == mock_resource_data["name"]

    def test_get_rn_with_non_existing_name_returns_none(
        self, test_url, api_client, mock_resource_data, mocked_responses
    ):
        success_response = json.dumps({"data": {"rn": None}})

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"name": "My Cluster"}}, strict_match=False
                )
            ],
        )
        result = api_client.get_remote_network_by_name("My Cluster")
        assert result is None
