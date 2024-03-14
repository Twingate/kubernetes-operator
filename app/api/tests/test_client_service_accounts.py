import json

import responses


class TestTwingateServiceAccountAPIs:
    def test_get_service_account_id_success(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps(
            {
                "data": {
                    "serviceAccounts": {
                        "edges": [{"node": {"id": "test-id", "name": "test"}}]
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
                    {"variables": {"name": "test"}}, strict_match=False
                )
            ],
        )
        result = api_client.get_service_account_id("test")
        assert result == "test-id"

    def test_get_service_account_id_not_found_returns_none(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps({"data": {"serviceAccounts": {"edges": []}}})

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"name": "test"}}, strict_match=False
                )
            ],
        )
        result = api_client.get_service_account_id("test")
        assert result is None
