import orjson as json
import pytest
import responses
from pydantic_core._pydantic_core import ValidationError

from app.api.client import GraphQLMutationError
from app.api.client_resources import Resource
from app.crds import K8sMetadata, ResourceSpec


@pytest.fixture
def mock_resource_data():
    return {
        "id": "1",
        "name": "My K8S Resource",
        "createdAt": "2021-08-18T15:00:00.000Z",
        "updatedAt": "2021-08-18T15:00:00.000Z",
        "alias": "my-k8s-resource",
        "isVisible": True,
        "isBrowserShortcutEnabled": False,
        "address": {"type": "DNS", "value": "my-k8s-resource.default.cluster.local"},
        "remoteNetwork": {"id": "rn1"},
        "securityPolicy": {"id": "sp1"},
        "tags": [{"key": "env", "value": "dev"}],
    }


class TestResourceModel:
    def test_construction(self, mock_resource_data):
        r = Resource(**mock_resource_data)
        for key in ["id", "name", "alias"]:
            assert getattr(r, key) == mock_resource_data[key], f"Failed for key: {key}"

        assert r.address.type == mock_resource_data["address"]["type"]
        assert r.address.value == mock_resource_data["address"]["value"]

    def test_construction_succeeds_with_no_security_policy(self, mock_resource_data):
        mock_resource_data["securityPolicy"] = None
        r = Resource(**mock_resource_data)
        for key in ["id", "name", "alias"]:
            assert getattr(r, key) == mock_resource_data[key], f"Failed for key: {key}"

    def test_construction_ignores_extra_params(self, mock_resource_data):
        mock_resource_data["extra"] = "extra"

        r = Resource(**mock_resource_data)
        for key in ["id", "name", "alias"]:
            assert getattr(r, key) == mock_resource_data[key], f"Failed for key: {key}"

        assert r.address.type == mock_resource_data["address"]["type"]
        assert r.address.value == mock_resource_data["address"]["value"]

    def test_construction_fails_on_missing_params(self, mock_resource_data):
        del mock_resource_data["name"]
        with pytest.raises(ValidationError):
            Resource(**mock_resource_data)

    def test_construction_fails_on_invalid_address_type(self, mock_resource_data):
        mock_resource_data["address"]["type"] = "invalid"
        with pytest.raises(ValidationError):
            Resource(**mock_resource_data)

    def test_is_matching_spec(self, resource_factory):
        r = resource_factory()
        crd = r.to_spec()
        assert r.is_matching_spec(crd)

        r1 = Resource(**r.model_dump())
        r1.alias = r.alias + "1"
        assert not r1.is_matching_spec(crd)

    def test_is_matching_case_protocols(self):
        resource = Resource(
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


class TestResourceFactory:
    def test_name_is_used_for_address(self, resource_factory):
        r = resource_factory()
        assert r.name in r.address.value


class TestTwingateResourceAPIs:
    def test_get_resource_with_valid_id_succeeds(
        self, test_url, api_client, resource_factory, mocked_responses
    ):
        resource = resource_factory()

        success_response = json.dumps({"data": {"resource": resource.model_dump()}})

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

    def test_get_resource_with_invalid_id_returns_none(
        self, test_url, api_client, resource_factory, mocked_responses
    ):
        resource = resource_factory()

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
        result = api_client.get_resource(resource.id)
        assert result is None

    def test_resource_create(
        self, test_url, api_client, resource_factory, mocked_responses
    ):
        resource = resource_factory()
        crd = resource.to_spec(id=None)
        k8s_metadata = K8sMetadata(
            name="my-resource",
            namespace="default",
            uid="ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
            labels=resource.to_metadata_labels(),
        )
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
                    {"variables": crd.model_dump(exclude=["id"], by_alias=True)},
                    strict_match=False,
                )
            ],
        )
        result = api_client.resource_create(crd, k8s_metadata)
        assert result == resource

    def test_resource_create_failure(
        self, test_url, api_client, resource_factory, mocked_responses
    ):
        resource = resource_factory()
        crd = resource.to_spec(id=None)
        k8s_metadata = K8sMetadata(
            name="my-resource",
            namespace="default",
            uid="ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
            labels=resource.to_metadata_labels(),
        )
        success_response = json.dumps(
            {"data": {"resourceCreate": {"ok": False, "error": "some error"}}}
        )

        mocked_responses.post(
            test_url,
            status=200,
            body=success_response,
            match=[
                responses.matchers.json_params_matcher(
                    {"variables": crd.model_dump(exclude=["id"], by_alias=True)},
                    strict_match=False,
                )
            ],
        )
        with pytest.raises(
            GraphQLMutationError, match="resourceCreate mutation failed."
        ):
            api_client.resource_create(crd, k8s_metadata)

    def test_resource_update(
        self, test_url, api_client, resource_factory, mocked_responses
    ):
        resource = resource_factory()
        crd = resource.to_spec()
        k8s_metadata = K8sMetadata(
            name="my-resource",
            namespace="default",
            uid="ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
            labels=resource.to_metadata_labels(),
        )
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
                    {"variables": crd.model_dump(by_alias=True)}, strict_match=False
                )
            ],
        )
        result = api_client.resource_update(crd, k8s_metadata)
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
            GraphQLMutationError, match="resourceDelete mutation failed."
        ):
            api_client.resource_delete("some-id")
