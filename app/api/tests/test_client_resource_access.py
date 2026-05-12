from datetime import datetime, timezone

import orjson as json
import pytest
import responses

from app.api.client import GraphQLMutationError
from app.crds import AccessApprovalMode, AccessMode, AccessPolicyInput


class TestResourceAccessAPIs:
    def test_resource_access_add_success(self, test_url, api_client, mocked_responses):
        resource_id = "test-resource"
        principal_id = "test-principal"
        security_policy_id = "test-security-policy"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": security_policy_id,
                    "expiresAt": None,
                    "accessPolicy": None,
                    "approvalMode": None,
                }
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

    def test_resource_access_add_success_without_policy(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": None,
                    "expiresAt": None,
                    "accessPolicy": None,
                    "approvalMode": None,
                }
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
            security_policy_id=None,
        )

    def test_resource_access_add_failure(self, test_url, api_client, mocked_responses):
        resource_id = "test-resource"
        principal_id = "test-principal"
        security_policy_id = "test-security-policy"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": security_policy_id,
                    "expiresAt": None,
                    "accessPolicy": None,
                    "approvalMode": None,
                }
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
            GraphQLMutationError, match=r"resourceAccessAdd mutation failed."
        ):
            api_client.resource_access_add(
                resource_id=resource_id,
                principal_id=principal_id,
                security_policy_id=security_policy_id,
            )

    def test_resource_access_add_with_expires_at(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"
        expires_at = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": None,
                    "expiresAt": "2026-12-31T23:59:59Z",
                    "accessPolicy": None,
                    "approvalMode": None,
                }
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
            expires_at=expires_at,
        )

    def test_resource_access_add_with_access_policy(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"
        access_policy = AccessPolicyInput(
            mode=AccessMode.AUTO_LOCK, duration_seconds=3600
        )

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": None,
                    "expiresAt": None,
                    "accessPolicy": {
                        "mode": "AUTO_LOCK",
                        "durationSeconds": 3600,
                    },
                    "approvalMode": None,
                }
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
            access_policy=access_policy,
        )

    def test_resource_access_add_with_approval_mode(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": None,
                    "expiresAt": None,
                    "accessPolicy": None,
                    "approvalMode": "AUTOMATIC",
                }
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
            approval_mode=AccessApprovalMode.AUTOMATIC,
        )

    def test_resource_access_add_omitted_fields_serialize_as_null(
        self, test_url, api_client, mocked_responses
    ):
        resource_id = "test-resource"
        principal_id = "test-principal"

        expected_variables = {
            "resourceId": resource_id,
            "access": [
                {
                    "principalId": principal_id,
                    "securityPolicyId": None,
                    "expiresAt": None,
                    "accessPolicy": None,
                    "approvalMode": None,
                }
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
            resource_id=resource_id, principal_id=principal_id
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
            GraphQLMutationError, match=r"resourceAccessRemove mutation failed."
        ):
            api_client.resource_access_remove(
                resource_id=resource_id, principal_id=principal_id
            )
