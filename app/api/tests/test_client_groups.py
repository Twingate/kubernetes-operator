import json

import pytest
import responses

from app.api.exceptions import GraphQLMutationError
from app.crds import GroupSpec


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

    def test_group_create(self, test_url, api_client, mocked_responses):
        name = "my group name"
        success_response = json.dumps(
            {
                "data": {
                    "groupCreate": {
                        "ok": True,
                        "entity": {"id": "test-id", "name": name},
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
                    {"variables": {"name": name, "userIds": []}}, strict_match=False
                )
            ],
        )
        result = api_client.group_create(GroupSpec(name=name))
        assert result == "test-id"

    def test_group_create_failure(self, test_url, api_client, mocked_responses):
        name = "my group name"
        failed_response = json.dumps(
            {
                "data": {
                    "groupCreate": {
                        "ok": False,
                        "error": "some error",
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
                    {"variables": {"name": name, "userIds": []}}, strict_match=False
                )
            ],
        )
        with pytest.raises(GraphQLMutationError, match="groupCreate mutation failed."):
            api_client.group_create(GroupSpec(name=name))

    def test_group_update(self, test_url, api_client, mocked_responses):
        name = "my group name"
        success_response = json.dumps(
            {
                "data": {
                    "groupUpdate": {
                        "ok": True,
                        "entity": {"id": "test-id", "name": name},
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
                    {"variables": {"id": "test-id", "name": name, "userIds": []}},
                    strict_match=False,
                )
            ],
        )
        result = api_client.group_update(GroupSpec(id="test-id", name=name))
        assert result == "test-id"

    def test_group_update_failure(self, test_url, api_client, mocked_responses):
        name = "my group name"
        success_response = json.dumps(
            {
                "data": {
                    "groupUpdate": {
                        "ok": False,
                        "error": "some error",
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
                    {"variables": {"id": "test-id", "name": name, "userIds": []}},
                    strict_match=False,
                )
            ],
        )
        with pytest.raises(GraphQLMutationError, match="groupUpdate mutation failed."):
            api_client.group_update(GroupSpec(id="test-id", name=name))

    def test_group_delete(self, test_url, api_client, mocked_responses):
        success_response = json.dumps({"data": {"groupDelete": {"ok": True}}})

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "test-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.group_delete("test-id")
        assert result is True

    def test_group_delete_with_invalid_id_returns_false(
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
                "groupDelete": null
              }
            }
        """

        mocked_responses.post(
            test_url,
            status=200,
            body=failed_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "test-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.group_delete("test-id")
        assert result is False

    def test_group_delete_raises_if_unknown_error(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "groupDelete": {
                        "ok": False,
                        "error": "Something unknown happened...",
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
        with pytest.raises(GraphQLMutationError, match="groupDelete mutation failed."):
            api_client.group_delete("some-id")
