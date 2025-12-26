import base64
from unittest.mock import MagicMock

import orjson as json
import pytest
import responses
from cryptography import x509
from gql.transport.exceptions import TransportQueryError
from pydantic_core._pydantic_core import ValidationError

from app.api.client import GraphQLMutationError
from app.api.client_resources import (
    BaseResource,
    NetworkResource,
    ResourceProtocol,
    ResourceProtocols,
)
from app.api.tests.factories import VALID_CA_CERT, VALID_CA_CERT_1
from app.crds import ProtocolPolicy, ResourceProxy, ResourceSpec, ResourceType


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
            "name": ("My K8S Resource", "new-name"),
            "address": (
                "my-k8s-resource.default.cluster.local",
                "new-address.internal",
            ),
            "is_visible": (True, False),
            "alias": ("my-k8s-resource", "new-alias.internal"),
            "protocols": (resource.protocols.model_dump(), crd_protocols),
            "remote_network_id": ("rn1", "new-rn-id"),
            "security_policy_id": ("sp1", "new-sp-id"),
        }

    def test_get_spec_diff_with_empty_security_policy(self, mock_resource_data):
        resource = BaseResource(**mock_resource_data)
        crd = ResourceSpec(**resource.to_spec_dict() | {"security_policy_id": None})

        assert resource.get_spec_diff(crd) == {
            "security_policy_id": (resource.security_policy.id, None)
        }

    def test_get_labels_diff(self, mock_resource_data):
        r = BaseResource(**mock_resource_data)
        crd_labels = {"env": "dev"}

        assert r.get_labels_diff(crd_labels) == {}

        updated_crd_labels = {"env": "prod"}

        assert r.get_labels_diff(updated_crd_labels) == {
            "tags": (crd_labels, updated_crd_labels)
        }


class TestNetworkResourceModel:
    def test_get_spec_diff_no_diff(self, network_resource_factory):
        resource = network_resource_factory()
        crd = resource.to_spec()

        assert resource.get_spec_diff(crd) == {}

    def test_get_spec_diff_with_is_browser_shortcut_enabled(
        self, network_resource_factory
    ):
        resource = network_resource_factory(is_browser_shortcut_enabled=False)
        crd = resource.to_spec(is_browser_shortcut_enabled=True)

        assert resource.get_spec_diff(crd) == {
            "is_browser_shortcut_enabled": (False, True)
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
    def test_get_spec_diff_no_diff(self, kubernetes_resource_factory):
        resource = kubernetes_resource_factory()
        crd = resource.to_spec()

        assert resource.get_spec_diff(crd) == {}

    def test_get_spec_diff_with_kubernetes_resource(self, kubernetes_resource_factory):
        resource = kubernetes_resource_factory()
        crd = resource.to_spec(
            proxy=ResourceProxy(
                address="proxy.kubernetes.cluster.local",
                certificate_authority_cert=base64.b64encode(
                    VALID_CA_CERT_1.encode()
                ).decode(),
            )
        )

        assert resource.get_spec_diff(crd) == {
            "proxy_address": (resource.proxy_address, "proxy.kubernetes.cluster.local"),
            "certificate_authority_cert": (
                resource.x509_ca_cert,
                x509.load_pem_x509_certificate(VALID_CA_CERT_1.encode()),
            ),
        }

    def test_get_spec_diff_with_empty_proxy(self, kubernetes_resource_factory):
        resource = kubernetes_resource_factory()
        crd = resource.to_spec(proxy=None)

        assert resource.get_spec_diff(crd) == {
            "proxy_address": (resource.proxy_address, None),
            "certificate_authority_cert": (resource.x509_ca_cert, None),
        }

    def test_get_spec_diff_with_equivalent_certificate(
        self, kubernetes_resource_factory
    ):
        resource = kubernetes_resource_factory(certificate_authority_cert=VALID_CA_CERT)
        crd = resource.to_spec()

        # This x509 cert is the same as VALID_CA_CERT but formatted differently in PEM.
        resource.certificate_authority_cert = "-----BEGIN CERTIFICATE-----\nMIIFfzCCA2egAwIBAgIVALoOJAoSP1m81BQ3DAjRHcYXrLR8MA0GCSqGSIb3DQEB\nCwUAMHcxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDTzEQMA4GA1UEBxMHQm91bGRl\ncjESMBAGA1UEChMJSnVtcENsb3VkMRkwFwYDVQQLExBKdW1wQ2xvdWRTQU1MSWRQ\nMRowGAYDVQQDExFKdW1wQ2xvdWRTQU1MVXNlcjAeFw0yMTExMjkwMTAyMTRaFw0y\nNjExMjkwMTAyMTRaMHcxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDTzEQMA4GA1UE\nBxMHQm91bGRlcjESMBAGA1UEChMJSnVtcENsb3VkMRkwFwYDVQQLExBKdW1wQ2xv\ndWRTQU1MSWRQMRowGAYDVQQDExFKdW1wQ2xvdWRTQU1MVXNlcjCCAiIwDQYJKoZI\nhvcNAQEBBQADggIPADCCAgoCggIBALc6KJOG3Nm02vHfvoaWkr0sR94HOVwiK79j\ndxP4saCi5hL7Fj2EnEmz73BH/BxBFQ/uHcRjMO9uLn6WRcT2P8WDMtyUuBSIUL4l\nLxoTOm0/37qrYYAHfbYJuPWAbvIxne2Ns0iXYFkgHSZ6DudZ37SSdXnPBuR6caey\nmbovrCHPbETb3SpgcVMuuuG1XhCTN0lZ/xrpB1G8HqL37xVCmJAzmBmUgYpu9+zH\n1uBPwUoWa8THelXrp2CUZ3mtwo0uKnfyXJcJyC5rJv0RLo4oJRetU3miTF7/trcX\nMhXGsosM/U/a5sn79Eh3vx+BJCDdrJte5z0WCCR+FcLYtE9iweWpIKh98746rUoS\n4rMHpUae0Ns6eSpU+OwImMw6oUCHO8+x1gkcVBG2tfD0mv7TIdW5ib6M9L9T63L1\n5qeke9APPcpG0vG5IxeGbClRcjE4usiTg+iK8+ACT7h2htScSGlPsI3Dbln9D4LX\nRKNHCcyBcpVOHI06Z0D0hK7yclpiuILSHaTTCPl38xwUNFlJDqXjUvzLxM1sWzeb\nt4It3g886MkS4l0wZgaYHxmcmCdlJvyPqV8txgQZYBY3jT7EjgPFox4kLMVKA+jA\nzf9sHTh7zQnOgRE32rhj2NUAK3hBbHv1aOeUlhxSLDle7X6lXGxxHCvA3l1Npmo5\nA1OZhMBFAgMBAAGjAjAAMA0GCSqGSIb3DQEBCwUAA4ICAQCUIop2TSQJzsRhgwOG\nYkbpAblSjkNQ5TBZfrrZoFYOMA0ji62qlWD3C5OUaWQbBrvG/8LvCOXm4mPmp1e0\nJeli6DZBIn2Uo7ne29V+itvgB/du6+pkrIr0egAbkJfkS+f3lQjepjFakiQqK3YL\nJtXJUrKvwjWkdgTmWr8S1P9LX4fE4Rlr9i+pg6NVspSDezmDHg7jbgcq1tK8g3ra\nDpAM4LkyGJHCSE0tWmNDw6QKRb/ev6fBdz1UVTXaWZoA22rWcfMH35YwcCP5oXpi\nkISi+JmG6HojBs4ljpbZFYcRRu9P/i0mvpdJQtPRRnvNC5v5EwPuktE1Wi6qkp68\nN7j+QLl8jyaXLn6GHE6CjggE4YB8veqceLaDDYutxRjT77LhESxWN6XRBzhMcOrH\nFpNJQI1VlalABW2YjpJIPvo+iWlAZZx20k2+GFJVNiwe0Xzdyql1eGMxCkKpd5wB\nezJeBUurMQ+tqd+1dG10fEBL3gikBGlZLSWus3pFxSiwYzhSSoAqK9zF7T+A674p\n7EQB9fk8V4ZtR6Oo20R4NWOX4VrqszFcYaNJrpKuB8FaDvUqcE2aQ+vkYXfi0Fad\nLFmc7WeMePIMvkfinr9qEgYc+yq5Xa0WHb3Xe+1y7l0TKyuKHdBgHGJUBAbAEyau\n4UcIBjn1gX2YNQ/N1TRvqIbkcQ==\n-----END CERTIFICATE-----"

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
