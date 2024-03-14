import json

import responses


class TestTwingateGroupsAPIs:
    def test_get_group_id_success(self, test_url, api_client, mocked_responses):
        success_response = json.dumps(
            {
                "data": {
                    "groups": {"edges": [{"node": {"id": "test-id", "name": "test"}}]}
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
        result = api_client.get_group_id("test")
        assert result == "test-id"

    def test_get_group_id_not_found_returns_none(
        self, test_url, api_client, mocked_responses
    ):
        success_response = json.dumps({"data": {"groups": {"edges": []}}})

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
        result = api_client.get_group_id("test")
        assert result is None
