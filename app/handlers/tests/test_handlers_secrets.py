from unittest.mock import MagicMock, patch

import pytest

from app.api.exceptions import GraphQLMutationError
from app.crds import ResourceSpec, ResourceType
from app.handlers.handlers_secrets import (
    twingate_resource_tls_secret_update,
)
from app.settings import TwingateOperatorSettings


@pytest.fixture
def mock_memo():
    return MagicMock(
        twingate_settings=TwingateOperatorSettings(
            network="slug",
            host="test.com",
            api_key="test_key",
            remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
        )
    )


@pytest.fixture
def mock_api_client(k8s_core_client_mock, k8s_secret_mock):
    k8s_core_client_mock.read_namespaced_secret.return_value = k8s_secret_mock
    api_client_instance = MagicMock()
    with patch(
        "app.handlers.handlers_secrets.TwingateAPIClient"
    ) as mock_secrets_client:
        mock_secrets_client.return_value = api_client_instance
        yield api_client_instance


def sample_resource_obj(resource_id, resource_name):
    return {
        "spec": {
            "id": resource_id,
            "name": resource_name,
            "address": "kubernetes.default.svc.cluster.local",
            "type": ResourceType.KUBERNETES,
            "proxy": {
                "address": "proxy.default.svc.cluster.local:443",
                "certificateAuthorityCertSecretRef": {
                    "name": "my-secret",
                    "namespace": "default",
                },
            },
        },
        "metadata": {"labels": {"env": "dev"}},
    }


class TestTwingateResourceTlsSecretUpdate:
    def test_update_resource_when_secret_change(self, mock_api_client, mock_memo):
        resource_obj = sample_resource_obj(resource_id="1", resource_name="my-resource")
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        resource_spec = ResourceSpec(**resource_obj["spec"])

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=resource_obj,
        ):
            twingate_resource_tls_secret_update(
                namespace="default",
                name="my-tls-secret",
                diff=[],
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.resource_update.assert_called_once_with(
            resource_type=ResourceType.KUBERNETES,
            **resource_spec.to_graphql_arguments(labels={"env": "dev"}),
        )

    def test_update_multiple_resources_referencing_same_secret(
        self, mock_api_client, mock_memo
    ):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "resource-1"},
                {"namespace": "default", "name": "resource-2"},
                {"namespace": "default", "name": "resource-3"},
            ]
        }

        def get_resource(_namespace, name):
            if name == "resource-1":
                return sample_resource_obj("resource-id-1", "resource-1")
            if name == "resource-2":
                return sample_resource_obj("resource-id-2", "resource-2")
            if name == "resource-3":
                return sample_resource_obj("resource-id-3", "resource-3")
            return None

        # Should continue updating other resources even if one update fails
        mock_api_client.resource_update.side_effect = [
            MagicMock(),
            GraphQLMutationError("kubernetesResourceUpdate", "API error"),
            MagicMock(),
        ]

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            side_effect=get_resource,
        ):
            twingate_resource_tls_secret_update(
                namespace="default",
                name="my-tls-secret",
                diff=[],
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        assert mock_api_client.resource_update.call_count == 3

    def test_skip_update_with_non_indexed_secret(self, mock_api_client, mock_memo):
        mock_index = {}

        twingate_resource_tls_secret_update(
            namespace="default",
            name="unrelated-secret",
            diff=[],
            memo=mock_memo,
            logger=MagicMock(),
            twingate_resource_secret_index=mock_index,
        )

        mock_api_client.resource_update.assert_not_called()

    def test_skip_non_existent_resource(self, mock_api_client, mock_memo):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "deleted-resource"}
            ]
        }

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=None,
        ):
            twingate_resource_tls_secret_update(
                namespace="default",
                name="my-tls-secret",
                diff=[],
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.resource_update.assert_not_called()

    def test_skip_resource_without_id(self, mock_api_client, mock_memo):
        resource_obj = sample_resource_obj("resource-id-1", "my-resource")
        resource_obj["spec"]["id"] = None

        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=resource_obj,
        ):
            twingate_resource_tls_secret_update(
                namespace="default",
                name="my-tls-secret",
                diff=[],
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.resource_update.assert_not_called()
