import json

import pytest
import responses

from app.api.exceptions import GraphQLMutationError

ADDRESS = "gateway.twingate.svc.cluster.local:443"
REMOTE_NETWORK_ID = "UmVtb3RlTmV0d29yazoxMjMK"
X509_CA_ID = "ca-id"


class TestTwingateGatewayAPIs:
    def test_get_gateway_success(self, test_url, api_client, mocked_responses):
        success_response = json.dumps(
            {"data": {"gateway": {"id": "gw-id", "address": ADDRESS}}}
        )
        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "gw-id"}}, strict_match=False
                )
            ],
        )
        result = api_client.get_gateway("gw-id")
        assert result is not None
        assert result.id == "gw-id"
        assert result.address == ADDRESS

    def test_get_gateway_not_found_returns_none(
        self, test_url, api_client, mocked_responses
    ):
        mocked_responses.post(
            test_url, status=200, body=json.dumps({"data": {"gateway": None}})
        )
        assert api_client.get_gateway("gw-id") is None

    def test_get_gateway_transport_error_returns_none(
        self, test_url, api_client, mocked_responses
    ):
        errors_response = json.dumps({"errors": [{"message": "Transport error"}]})
        mocked_responses.post(
            test_url,
            status=200,
            body=errors_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "gw-id"}}, strict_match=False
                )
            ],
        )
        assert api_client.get_gateway("gw-id") is None

    def test_gateway_create(self, test_url, api_client, mocked_responses):
        success_response = json.dumps(
            {
                "data": {
                    "gatewayCreate": {
                        "ok": True,
                        "entity": {"id": "gw-id", "address": ADDRESS},
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
                        "variables": {
                            "address": ADDRESS,
                            "remoteNetworkId": REMOTE_NETWORK_ID,
                            "x509CAId": X509_CA_ID,
                        }
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.gateway_create(
            address=ADDRESS,
            remote_network_id=REMOTE_NETWORK_ID,
            x509_ca_id=X509_CA_ID,
        )
        assert result.id == "gw-id"

    def test_gateway_create_failure(self, test_url, api_client, mocked_responses):
        failed_response = json.dumps(
            {"data": {"gatewayCreate": {"ok": False, "error": "some error"}}}
        )
        mocked_responses.post(test_url, status=200, body=failed_response)
        with pytest.raises(
            GraphQLMutationError, match=r"gatewayCreate mutation failed - some error"
        ):
            api_client.gateway_create(
                address=ADDRESS,
                remote_network_id=REMOTE_NETWORK_ID,
                x509_ca_id=X509_CA_ID,
            )

    def test_gateway_update(self, test_url, api_client, mocked_responses):
        success_response = json.dumps(
            {
                "data": {
                    "gatewayUpdate": {
                        "ok": True,
                        "entity": {"id": "gw-id", "address": ADDRESS},
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
                        "variables": {
                            "id": "gw-id",
                            "remoteNetworkId": REMOTE_NETWORK_ID,
                            "address": ADDRESS,
                            "x509CAId": X509_CA_ID,
                        }
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.gateway_update(
            gateway_id="gw-id",
            remote_network_id=REMOTE_NETWORK_ID,
            address=ADDRESS,
            x509_ca_id=X509_CA_ID,
        )
        assert result.id == "gw-id"

    def test_gateway_delete(self, test_url, api_client, mocked_responses):
        mocked_responses.post(
            test_url,
            status=200,
            body=json.dumps({"data": {"gatewayDelete": {"ok": True}}}),
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "gw-id"}}, strict_match=False
                )
            ],
        )
        assert api_client.gateway_delete("gw-id") is True

    def test_gateway_delete_raises_on_error(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "gatewayDelete": {
                        "ok": False,
                        "error": "Cannot delete. This Gateway is being used by Resource.",
                    }
                }
            }
        )
        mocked_responses.post(test_url, status=200, body=failed_response)
        with pytest.raises(
            GraphQLMutationError, match=r"gatewayDelete mutation failed - .*being used"
        ):
            api_client.gateway_delete("gw-id")

    def test_gateway_delete_already_deleted_returns_true(
        self, test_url, api_client, mocked_responses
    ):
        # The backend reports the entity is already gone - treat as success so
        # finalizer teardown completes instead of getting stuck.
        failed_response = json.dumps(
            {
                "data": {
                    "gatewayDelete": {
                        "ok": False,
                        "error": "Gateway does not exist.",
                    }
                }
            }
        )
        mocked_responses.post(test_url, status=200, body=failed_response)
        assert api_client.gateway_delete("gw-id") is True

    def test_gateway_delete_transport_error_returns_false(
        self, test_url, api_client, mocked_responses
    ):
        errors_response = json.dumps({"errors": [{"message": "Transport error"}]})
        mocked_responses.post(
            test_url,
            status=200,
            body=errors_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": "gw-id"}}, strict_match=False
                )
            ],
        )
        assert api_client.gateway_delete("gw-id") is False
