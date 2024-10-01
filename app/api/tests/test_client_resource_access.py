import orjson as json
import pytest
import responses

from app.api.client import GraphQLMutationError


class TestResourceAccessAPIs:
    def test_resource_access_add_success(self, test_url, api_client, mocked_responses):
        resource_id = "test-resource"
        principal_id = "test-principal"
        security_policy_id = "test-security-policy"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {"principalId": principal_id, "securityPolicyId": security_policy_id}
            ],
        }

        mocked_responses.post(
            test_url,
            status=200,
            body=json.dumps({"data": {"resourceAccessAdd": {"ok": True}}}),
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": expected_variables}, strict_match=False
                )
            ],
        )

        assert api_client.resource_access_add(
            resource_id=resource_id,
            principal_id=principal_id,
            security_policy_id=security_policy_id,
        )

    def test_resource_access_add_failure(self, test_url, api_client, mocked_responses):
        resource_id = "test-resource"
        principal_id = "test-principal"
        security_policy_id = "test-security-policy"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {"principalId": principal_id, "securityPolicyId": security_policy_id}
            ],
        }

        mocked_responses.post(
            test_url,
            status=200,
            body=json.dumps({"data": {"resourceAccessAdd": {"ok": False}}}),
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": expected_variables}, strict_match=False
                )
            ],
        )

        with pytest.raises(
            GraphQLMutationError, match="resourceAccessAdd mutation failed."
        ):
            api_client.resource_access_add(
                resource_id=resource_id,
                principal_id=principal_id,
                security_policy_id=security_policy_id,
            )

    def test_resource_access_remove_success(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {"resourceId": resource_id, "principalId": principal_id}

        mocked_responses.post(
            test_url,
            status=200,
            body=json.dumps({"data": {"resourceAccessRemove": {"ok": True}}}),
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": expected_variables}, strict_match=False
                )
            ],
        )

        assert api_client.resource_access_remove(
            resource_id=resource_id, principal_id=principal_id
        )

    def test_resource_access_remove_invalid_id_returns_false(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {"resourceId": resource_id, "principalId": principal_id}

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
                "resourceAccessRemove": null
              }
            }
        """

        mocked_responses.post(
            test_url,
            status=200,
            body=failed_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": expected_variables}, strict_match=False
                )
            ],
        )

        result = api_client.resource_access_remove(
            resource_id=resource_id, principal_id=principal_id
        )
        assert result is False

    def test_resource_access_remove_already_deleted_returns_true(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {"resourceId": resource_id, "principalId": principal_id}

        mocked_responses.post(
            test_url,
            status=200,
            body=json.dumps(
                {
                    "data": {
                        "resourceAccessRemove": {
                            "ok": False,
                            "error": f"Resource with id '{resource_id}' does not exist",
                        }
                    }
                }
            ),
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": expected_variables}, strict_match=False
                )
            ],
        )

        result = api_client.resource_access_remove(
            resource_id=resource_id, principal_id=principal_id
        )
        assert result is True

    def test_resource_access_remove_raises_if_unknown_error(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {"resourceId": resource_id, "principalId": principal_id}

        mocked_responses.post(
            test_url,
            status=200,
            body=json.dumps(
                {
                    "data": {
                        "resourceAccessRemove": {
                            "ok": False,
                            "error": "Something unknown happened...",
                        }
                    }
                }
            ),
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": expected_variables}, strict_match=False
                )
            ],
        )

        with pytest.raises(
            GraphQLMutationError, match="resourceAccessRemove mutation failed."
        ):
            api_client.resource_access_remove(
                resource_id=resource_id, principal_id=principal_id
            )
