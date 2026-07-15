from unittest.mock import MagicMock, patch

import orjson as json
import pytest
import responses
from gql.transport.exceptions import TransportQueryError
from pydantic_core._pydantic_core import ValidationError

from app.api.client import GraphQLMutationError
from app.api.client_resources import (
    BaseResource,
    Diff,
    NetworkResource,
    ResourceGateway,
    ResourceProtocol,
    ResourceProtocols,
)
from app.crds import ProtocolPolicy, ResourceSpec, ResourceType


@pytest.fixture
def mock_resource_data():
    return {
        "id": "1",
        "name": "My K8S Resource",
        "createdAt": "2021-08-18T15:00:00.000Z",
        "updatedAt": "2021-08-18T15:00:00.000Z",
        "alias": "my-k8s-resource",
        "isVisible": True,
        "address": {"type": "DNS", "value": "my-k8s-resource.default.cluster.local"},
        "remoteNetwork": {"id": "rn1"},
        "securityPolicy": {"id": "sp1"},
        "tags": [{"key": "env", "value": "dev"}],
    }


class TestBaseResourceModel:
    def test_construction(self, mock_resource_data):
        r = BaseResource(**mock_resource_data)
        for key in ["id", "name", "alias"]:
            assert getattr(r, key) == mock_resource_data[key], f"Failed for key: {key}"

        assert r.address.type == mock_resource_data["address"]["type"]
        assert r.address.value == mock_resource_data["address"]["value"]

    def test_construction_succeeds_with_no_security_policy(self, mock_resource_data):
        mock_resource_data["securityPolicy"] = None
        r = BaseResource(**mock_resource_data)
        for key in ["id", "name", "alias"]:
            assert getattr(r, key) == mock_resource_data[key], f"Failed for key: {key}"

    def test_construction_ignores_extra_params(self, mock_resource_data):
        mock_resource_data["extra"] = "extra"

        r = BaseResource(**mock_resource_data)
        for key in ["id", "name", "alias"]:
            assert getattr(r, key) == mock_resource_data[key], f"Failed for key: {key}"

        assert r.address.type == mock_resource_data["address"]["type"]
        assert r.address.value == mock_resource_data["address"]["value"]

    def test_construction_fails_on_missing_params(self, mock_resource_data):
        del mock_resource_data["name"]
        with pytest.raises(ValidationError):
            BaseResource(**mock_resource_data)

    def test_construction_fails_on_invalid_address_type(self, mock_resource_data):
        mock_resource_data["address"]["type"] = "invalid"
        with pytest.raises(ValidationError):
            BaseResource(**mock_resource_data)

    def test_get_spec_diff_with_no_diff(self, mock_resource_data):
        resource = BaseResource(**mock_resource_data)
        crd = ResourceSpec(**resource.to_spec_dict())

        assert resource.get_spec_diff(crd) == {}

    def test_get_spec_diff(self, mock_resource_data):
        resource = BaseResource(**mock_resource_data)
        crd_protocols = ResourceProtocols(
            tcp=ResourceProtocol(policy=ProtocolPolicy.RESTRICTED)
        ).model_dump()
        crd = ResourceSpec(
            name="new-name",
            address="new-address.internal",
            is_visible=False,
            alias="new-alias.internal",
            protocols=crd_protocols,
            remote_network_id="new-rn-id",
            security_policy_id="new-sp-id",
        )

        assert resource.get_spec_diff(crd) == {
            "name": Diff(remote="My K8S Resource", local="new-name"),
            "address": Diff(
                remote="my-k8s-resource.default.cluster.local",
                local="new-address.internal",
            ),
            "is_visible": Diff(remote=True, local=False),
            "alias": Diff(remote="my-k8s-resource", local="new-alias.internal"),
            "protocols": Diff(
                remote=resource.protocols.model_dump(), local=crd_protocols
            ),
            "remote_network_id": Diff(remote="rn1", local="new-rn-id"),
            "security_policy_id": Diff(remote="sp1", local="new-sp-id"),
        }

    def test_get_spec_diff_with_empty_security_policy(self, mock_resource_data):
        resource = BaseResource(**mock_resource_data)
        crd = ResourceSpec(**resource.to_spec_dict() | {"security_policy_id": None})

        assert resource.get_spec_diff(crd) == {
            "security_policy_id": Diff(remote=resource.security_policy.id, local=None)
        }

    def test_get_labels_diff(self, mock_resource_data):
        r = BaseResource(**mock_resource_data)
        crd_labels = {"env": "dev"}

        assert r.get_labels_diff(crd_labels) == {}

        updated_crd_labels = {"env": "prod"}

        assert r.get_labels_diff(updated_crd_labels) == {
            "tags": Diff(remote=crd_labels, local=updated_crd_labels)
        }


class TestNetworkResourceModel:
    def test_get_spec_diff_when_no_diff(self, network_resource_factory):
        resource = network_resource_factory()
        crd = resource.to_spec()

        assert resource.get_spec_diff(crd) == {}

    def test_get_spec_diff_with_is_browser_shortcut_enabled(
        self, network_resource_factory
    ):
        resource = network_resource_factory(is_browser_shortcut_enabled=False)
        crd = resource.to_spec(is_browser_shortcut_enabled=True)

        assert resource.get_spec_diff(crd) == {
            "is_browser_shortcut_enabled": Diff(remote=False, local=True)
        }

    def test_is_matching_case_protocols(self):
        resource = NetworkResource(
            **{  # noqa: PIE804
                "id": "UmVzb3VyY2U6MTI3NTIxMw==",
                "name": "My K8S Resource",
                "createdAt": "2024-02-15T01:13:51.059028+00:00",
                "updatedAt": "2024-02-15T01:20:24.242272+00:00",
                "address": {"type": "DNS", "value": "my.default.cluster.local"},
                "alias": "mine.local",
                "isVisible": True,
                "isBrowserShortcutEnabled": False,
                "remoteNetwork": {"id": "UmVtb3RlTmV0d29yazo5Njc0OTU="},
                "securityPolicy": None,
                "protocols": {
                    "allowIcmp": True,
                    "tcp": {"policy": "ALLOW_ALL", "ports": []},
                    "udp": {"policy": "ALLOW_ALL", "ports": []},
                },
                "tags": [
                    {"key": "env", "value": "dev"},
                ],
            }
        )

        crd = ResourceSpec(
            **{  # noqa: PIE804
                "address": "my.default.cluster.local",
                "alias": "mine.local",
                "id": "UmVzb3VyY2U6MTI3NTIxMw==",
                "isBrowserShortcutEnabled": False,
                "isVisible": True,
                "name": "My K8S Resource",
                "remoteNetworkId": "UmVtb3RlTmV0d29yazo5Njc0OTU=",
                "tags": [
                    {"key": "env", "value": "dev"},
                ],
            }
        )

        assert resource.get_spec_diff(crd) == {}


class TestKubernetesResourceModel:
    def test_get_spec_diff_when_in_sync(self, kubernetes_resource_factory):
        resource = kubernetes_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(gateway_ref={"name": "my-gateway"})

        with patch(
            "app.api.client_resources.resolve_ref_to_twingate_id",
            return_value="gw-1",
        ) as resolve_mock:
            assert resource.get_spec_diff(crd) == {}

        resolve_mock.assert_called_once_with(
            "twingategateways", "default", "my-gateway"
        )

    def test_get_spec_diff_for_gateway_drift(self, kubernetes_resource_factory):
        resource = kubernetes_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(gateway_ref={"name": "my-gateway"})

        with patch(
            "app.api.client_resources.resolve_ref_to_twingate_id",
            return_value="gw-2",
        ):
            assert resource.get_spec_diff(crd) == {
                "gateway_id": Diff(remote="gw-1", local="gw-2"),
            }


class TestWebAppResourceModel:
    def test_get_spec_diff_when_no_diff(self, web_app_resource_factory):
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(gateway_ref={"name": "my-gateway"})

        with patch(
            "app.api.client_resources.resolve_ref_to_twingate_id", return_value="gw-1"
        ):
            assert resource.get_spec_diff(crd) == {}

    def test_get_spec_diff_for_gateway_drift(self, web_app_resource_factory):
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(gateway_ref={"name": "my-gateway"})

        with patch(
            "app.api.client_resources.resolve_ref_to_twingate_id", return_value="gw-2"
        ):
            assert resource.get_spec_diff(crd) == {
                "gateway_id": Diff(remote="gw-1", local="gw-2"),
            }

    def test_get_spec_diff_for_port_drift(self, web_app_resource_factory):
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(
            gateway_ref={"name": "my-gateway"},
            downstream={"port": 8443},
            upstream={"port": 9090},
        )

        with patch(
            "app.api.client_resources.resolve_ref_to_twingate_id", return_value="gw-1"
        ):
            assert resource.get_spec_diff(crd) == {
                "downstream": Diff(remote=resource.downstream.port, local=8443),
                "upstream": Diff(remote=resource.upstream.port, local=9090),
            }

    def test_get_spec_diff_ignores_protocols(self, web_app_resource_factory):
        # WebApp is not port-based; protocols are not sent on update, so they must
        # not appear in the diff even when the CRD sets non-default protocols.
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(
            gateway_ref={"name": "my-gateway"},
            protocols=ResourceProtocols(
                tcp=ResourceProtocol(policy=ProtocolPolicy.RESTRICTED)
            ).model_dump(),
        )

        with patch(
            "app.api.client_resources.resolve_ref_to_twingate_id", return_value="gw-1"
        ):
            assert resource.get_spec_diff(crd) == {}


class TestResourceFactory:
    def test_name_is_used_for_address(self, base_resource_factory):
        r = base_resource_factory()
        assert r.name in r.address.value


class TestTwingateResourceAPIs:
    def test_get_network_resource_with_valid_id_succeeds(
        self, test_url, api_client, network_resource_factory, mocked_responses
    ):
        resource = network_resource_factory()

        success_response = json.dumps(
            {
                "data": {
                    "resource": resource.model_dump()
                    | {"__typename": "NetworkResource"}
                }
            }
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": resource.id}}, strict_match=False
                )
            ],
        )
        result = api_client.get_resource(resource.id)
        assert result == resource

    def test_get_kubernetes_resource(
        self, test_url, api_client, kubernetes_resource_factory, mocked_responses
    ):
        resource = kubernetes_resource_factory()

        success_response = json.dumps(
            {
                "data": {
                    "resource": resource.model_dump()
                    | {"__typename": "KubernetesResource"}
                }
            }
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": resource.id}}, strict_match=False
                )
            ],
        )
        result = api_client.get_resource(resource.id)
        assert result == resource

    def test_get_invalid_resource(
        self, test_url, api_client, kubernetes_resource_factory, mocked_responses
    ):
        resource = kubernetes_resource_factory()

        success_response = json.dumps(
            {
                "data": {
                    "resource": resource.model_dump()
                    | {"__typename": "InvalidResource"}
                }
            }
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": resource.id}}, strict_match=False
                )
            ],
        )
        with pytest.raises(ValueError, match=r"Invalid Resource Type: InvalidResource"):
            api_client.get_resource(resource.id)

    def test_get_resource_with_invalid_b64_id_raises(
        self, test_url, api_client, network_resource_factory, mocked_responses
    ):
        resource = network_resource_factory()

        failed_response = """
        {
          "errors": [
            {
              "message": "{'id': ['Unable to parse global ID']}",
              "locations": [{"line": 2, "column": 3}],
              "path": ["resource"]
            }
          ],
          "data": {
            "resource": null
          }
        }
        """

        mocked_responses.post(test_url, status=200, body=failed_response)
        with pytest.raises(TransportQueryError):
            api_client.get_resource(resource.id)

    def test_resource_create_with_network_type(self, api_client):
        api_client.network_resource_create = MagicMock()
        api_client.kubernetes_resource_create = MagicMock()

        api_client.resource_create(resource_type=ResourceType.NETWORK, mock_argument=1)

        api_client.network_resource_create.assert_called_once_with(mock_argument=1)
        api_client.kubernetes_resource_create.assert_not_called()

    def test_resource_create_with_kubernetes_type(self, api_client):
        api_client.network_resource_create = MagicMock()
        api_client.kubernetes_resource_create = MagicMock()

        api_client.resource_create(
            resource_type=ResourceType.KUBERNETES, mock_argument=1
        )

        api_client.kubernetes_resource_create.assert_called_once_with(mock_argument=1)
        api_client.network_resource_create.assert_not_called()

    def test_resource_create_with_web_app_type(self, api_client):
        api_client.network_resource_create = MagicMock()
        api_client.web_app_resource_create = MagicMock()

        api_client.resource_create(resource_type=ResourceType.WEB_APP, mock_argument=1)

        api_client.web_app_resource_create.assert_called_once_with(mock_argument=1)
        api_client.network_resource_create.assert_not_called()

    def test_resource_update_with_web_app_type(self, api_client):
        api_client.network_resource_update = MagicMock()
        api_client.web_app_resource_update = MagicMock()

        api_client.resource_update(
            id="1", resource_type=ResourceType.WEB_APP, mock_argument=1
        )

        api_client.web_app_resource_update.assert_called_once_with(
            id="1", mock_argument=1
        )
        api_client.network_resource_update.assert_not_called()

    def test_resource_create_failure(
        self, test_url, api_client, network_resource_factory, mocked_responses
    ):
        resource = network_resource_factory()
        crd = resource.to_spec(id=None)
        success_response = json.dumps(
            {"data": {"resourceCreate": {"ok": False, "error": "some error"}}}
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "variables": crd.model_dump(
                            exclude=[
                                "id",
                                "sync_labels",
                                "type",
                                "gateway_ref",
                                "downstream",
                                "upstream",
                            ],
                            by_alias=True,
                        )
                    },
                    strict_match=False,
                )
            ],
        )
        with pytest.raises(
            GraphQLMutationError, match=r"resourceCreate mutation failed."
        ):
            api_client.resource_create(
                resource_type=ResourceType.NETWORK,
                **crd.to_graphql_arguments(
                    labels=resource.to_metadata_labels(), exclude={"id"}
                ),
            )

    def test_network_resource_create(
        self, test_url, api_client, network_resource_factory, mocked_responses
    ):
        resource = network_resource_factory()
        crd = resource.to_spec(id=None)
        success_response = json.dumps(
            {
                "data": {
                    "resourceCreate": {
                        "ok": True,
                        "entity": resource.model_dump(by_alias=True),
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
                        "variables": crd.model_dump(
                            exclude=[
                                "id",
                                "sync_labels",
                                "type",
                                "gateway_ref",
                                "downstream",
                                "upstream",
                            ],
                            by_alias=True,
                        )
                        | {"tags": [tag.model_dump() for tag in resource.tags]}
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.network_resource_create(
            **crd.to_graphql_arguments(
                labels=resource.to_metadata_labels(), exclude={"id"}
            ),
        )
        assert result == resource

    def test_kubernetes_resource_create(
        self, test_url, api_client, kubernetes_resource_factory, mocked_responses
    ):
        resource = kubernetes_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(id=None, gateway_ref={"name": "my-gateway"})
        success_response = json.dumps(
            {
                "data": {
                    "kubernetesResourceCreate": {
                        "ok": True,
                        "entity": resource.model_dump(by_alias=True),
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
                    {"variables": {"gatewayId": "gw-1"}},
                    strict_match=False,
                )
            ],
        )
        with patch(
            "app.crds.resolve_ref_to_twingate_id", return_value="gw-1"
        ) as resolve_mock:
            result = api_client.kubernetes_resource_create(
                **crd.to_graphql_arguments(
                    labels=resource.to_metadata_labels(), exclude={"id"}
                )
            )

        resolve_mock.assert_called_once_with(
            "twingategateways", "default", "my-gateway"
        )
        assert result == resource

    def test_resource_update_with_network_type(self, api_client):
        api_client.network_resource_update = MagicMock()
        api_client.kubernetes_resource_update = MagicMock()

        api_client.resource_update(
            id="1", resource_type=ResourceType.NETWORK, mock_argument=1
        )

        api_client.network_resource_update.assert_called_once_with(
            id="1", mock_argument=1
        )
        api_client.kubernetes_resource_update.assert_not_called()

    def test_resource_update_with_kubernetes_type(self, api_client):
        api_client.network_resource_update = MagicMock()
        api_client.kubernetes_resource_update = MagicMock()

        api_client.resource_update(
            id="1", resource_type=ResourceType.KUBERNETES, mock_argument=1
        )

        api_client.kubernetes_resource_update.assert_called_once_with(
            id="1", mock_argument=1
        )
        api_client.network_resource_update.assert_not_called()

    def test_network_resource_update(
        self, test_url, api_client, network_resource_factory, mocked_responses
    ):
        resource = network_resource_factory()
        crd = resource.to_spec()
        success_response = json.dumps(
            {
                "data": {
                    "resourceUpdate": {
                        "ok": True,
                        "entity": resource.model_dump(by_alias=True),
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
                        "variables": crd.model_dump(
                            exclude=[
                                "sync_labels",
                                "type",
                                "gateway_ref",
                                "downstream",
                                "upstream",
                            ],
                            by_alias=True,
                        )
                        | {"tags": [tag.model_dump() for tag in resource.tags]}
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.network_resource_update(
            **crd.to_graphql_arguments(labels=resource.to_metadata_labels())
        )
        assert result == resource

    def test_kubernetes_resource_update(
        self, test_url, api_client, kubernetes_resource_factory, mocked_responses
    ):
        resource = kubernetes_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(gateway_ref={"name": "my-gateway"})

        success_response = json.dumps(
            {
                "data": {
                    "kubernetesResourceUpdate": {
                        "ok": True,
                        "entity": resource.model_dump(by_alias=True),
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
                    {"variables": {"gatewayId": "gw-1"}},
                    strict_match=False,
                )
            ],
        )

        with patch(
            "app.crds.resolve_ref_to_twingate_id", return_value="gw-1"
        ) as resolve_mock:
            result = api_client.kubernetes_resource_update(
                **crd.to_graphql_arguments(labels=resource.to_metadata_labels())
            )

        resolve_mock.assert_called_once_with(
            "twingategateways", "default", "my-gateway"
        )
        assert result == resource

    def test_get_web_app_resource(
        self, test_url, api_client, web_app_resource_factory, mocked_responses
    ):
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))

        success_response = json.dumps(
            {
                "data": {
                    "resource": resource.model_dump(by_alias=True)
                    | {"__typename": "WebAppResource"}
                }
            }
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": {"id": resource.id}}, strict_match=False
                )
            ],
        )
        result = api_client.get_resource(resource.id)
        assert result == resource

    def test_web_app_resource_create(
        self, test_url, api_client, web_app_resource_factory, mocked_responses
    ):
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(
            id=None,
            gateway_ref={"name": "my-gateway"},
        )
        success_response = json.dumps(
            {
                "data": {
                    "webAppResourceCreate": {
                        "ok": True,
                        "entity": resource.model_dump(by_alias=True),
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
                            "gatewayId": "gw-1",
                            "downstream": {"port": resource.downstream.port},
                            "upstream": {"port": resource.upstream.port},
                        }
                    },
                    strict_match=False,
                )
            ],
        )
        with patch(
            "app.crds.resolve_ref_to_twingate_id", return_value="gw-1"
        ) as resolve_mock:
            result = api_client.web_app_resource_create(
                **crd.to_graphql_arguments(
                    labels=resource.to_metadata_labels(), exclude={"id"}
                )
            )

        resolve_mock.assert_called_once_with(
            "twingategateways", "default", "my-gateway"
        )
        assert result == resource

    def test_web_app_resource_update(
        self, test_url, api_client, web_app_resource_factory, mocked_responses
    ):
        resource = web_app_resource_factory(gateway=ResourceGateway(id="gw-1"))
        crd = resource.to_spec(gateway_ref={"name": "my-gateway"})
        success_response = json.dumps(
            {
                "data": {
                    "webAppResourceUpdate": {
                        "ok": True,
                        "entity": resource.model_dump(by_alias=True),
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
                    {"variables": {"gatewayId": "gw-1"}},
                    strict_match=False,
                )
            ],
        )
        with patch("app.crds.resolve_ref_to_twingate_id", return_value="gw-1"):
            result = api_client.web_app_resource_update(
                **crd.to_graphql_arguments(labels=resource.to_metadata_labels())
            )

        assert result == resource

    def test_resource_delete(self, test_url, api_client, mocked_responses):
        success_response = json.dumps({"data": {"resourceDelete": {"ok": True}}})

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
        result = api_client.resource_delete("some-id")
        assert result is True

    def test_resource_delete_with_invalid_id_returns_false(
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
                "resourceDelete": null
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
        result = api_client.resource_delete("some-id")
        assert result is False

    def test_resource_delete_with_id_already_deleted_returns_true(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "resourceDelete": {
                        "ok": False,
                        "error": "Resource with id 'some-id' does not exist",
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
        result = api_client.resource_delete("some-id")
        assert result is True

    def test_resource_delete_raises_if_unknown_error(
        self, test_url, api_client, mocked_responses
    ):
        failed_response = json.dumps(
            {
                "data": {
                    "resourceDelete": {
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
        with pytest.raises(
            GraphQLMutationError, match=r"resourceDelete mutation failed."
        ):
            api_client.resource_delete("some-id")
