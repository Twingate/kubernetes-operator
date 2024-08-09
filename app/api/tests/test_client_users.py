import json

import responses


class TestTwingateUserAPIs:
    def test_get_ids_for_emails_success(self, test_url, api_client, mocked_responses):
        success_response = json.dumps(
            {
                "data": {
                    "users": {
                        "pageInfo": {"endCursor": "cursor", "hasNextPage": False},
                        "edges": [
                            {"node": {"id": "test-id", "email": "test@example.com"}}
                        ],
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
                    {"variables": {"emails": ["test@example.com"]}}, strict_match=False
                )
            ],
        )
        result = api_client.get_group_id("test")
        assert result == "test-id"
