from unittest.mock import MagicMock

import orjson as json
import pytest
import responses
from gql.transport.exceptions import TransportQueryError
from pydantic_core._pydantic_core import ValidationError

from app.api.client import GraphQLMutationError
from app.api.client_resources import BaseResource, KubernetesResource, NetworkResource
from app.api.tests.factories import VALID_CA_CERT_1
from app.crds import ResourceSpec, ResourceType


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

    def test_is_matching_labels(self, mock_resource_data):
        r = BaseResource(**mock_resource_data)
        crd_labels = {"env": "dev"}

        assert r.is_matching_labels(crd_labels)


class TestNetworkResourceModel:
    def test_is_matching_spec(self, network_resource_factory):
        resource = network_resource_factory()
        crd = resource.to_spec()
        assert resource.is_matching_spec(crd)

        updated_resource = NetworkResource(**resource.model_dump())
        updated_resource.is_browser_shortcut_enabled = (
            not updated_resource.is_browser_shortcut_enabled
        )
        assert not updated_resource.is_matching_spec(crd)

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

        assert resource.is_matching_spec(crd)

    @pytest.mark.parametrize(
        ("field", "updated_value"),
        [
            ("proxy_address", "proxy.kubernetes.cluster.local"),
            ("certificate_authority_cert", VALID_CA_CERT_1),
        ],
    )
    def test_is_matching_spec_with_kubernetes_resource(
        self, kubernetes_resource_factory, field, updated_value
    ):
        resource = kubernetes_resource_factory()
        crd = resource.to_spec()
        assert resource.is_matching_spec(crd)

        updated_resource = KubernetesResource(**resource.model_dump())
        setattr(updated_resource, field, updated_value)
        assert not updated_resource.is_matching_spec(crd)


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
                            exclude=["id", "sync_labels", "type", "proxy"],
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
                            exclude=["id", "sync_labels", "type", "proxy"],
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
        resource = kubernetes_resource_factory()
        crd = resource.to_spec(id=None)
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
                    {
                        "variables": crd.model_dump(
                            exclude={
                                "id",
                                "is_browser_shortcut_enabled",
                                "sync_labels",
                                "type",
                                "proxy",
                            },
                            by_alias=True,
                        )
                        | {"tags": [tag.model_dump() for tag in resource.tags]}
                    },
                    strict_match=False,
                )
            ],
        )
        result = api_client.kubernetes_resource_create(
            **crd.to_graphql_arguments(
                labels=resource.to_metadata_labels(), exclude={"id"}
            )
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
                            exclude=["sync_labels", "type", "proxy"], by_alias=True
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
        resource = kubernetes_resource_factory()
        crd = resource.to_spec()

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
                    {
                        "variables": crd.model_dump(
                            exclude={
                                "is_browser_shortcut_enabled",
                                "sync_labels",
                                "type",
                                "proxy",
                            },
                            by_alias=True,
                        )
                        | {"tags": [tag.model_dump() for tag in resource.tags]}
                    },
                    strict_match=False,
                )
            ],
        )

        result = api_client.kubernetes_resource_update(
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
