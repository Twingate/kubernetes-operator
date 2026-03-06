from unittest.mock import MagicMock, patch

import kopf
import pytest

from app.api.exceptions import GraphQLMutationError
from app.api.tests.factories import BASE64_OF_VALID_CA_CERT, VALID_CA_CERT
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
def mock_api_client():
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
                new=BASE64_OF_VALID_CA_CERT,
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.kubernetes_resource_update_ca_cert.assert_called_once_with(
            id=resource_spec.id,
            name=resource_spec.name,
            address=resource_spec.address,
            remote_network_id=resource_spec.remote_network_id,
            certificate_authority_cert=VALID_CA_CERT,
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
        mock_api_client.kubernetes_resource_update_ca_cert.side_effect = [
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
                new=BASE64_OF_VALID_CA_CERT,
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        assert mock_api_client.kubernetes_resource_update_ca_cert.call_count == 3

    def test_skip_update_with_non_indexed_secret(self, mock_api_client, mock_memo):
        mock_index = {}

        twingate_resource_tls_secret_update(
            namespace="default",
            name="unrelated-secret",
            diff=[],
            new=BASE64_OF_VALID_CA_CERT,
            memo=mock_memo,
            logger=MagicMock(),
            twingate_resource_secret_index=mock_index,
        )

        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

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
                new=BASE64_OF_VALID_CA_CERT,
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

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
                new=BASE64_OF_VALID_CA_CERT,
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_raise_permanent_error_on_invalid_cert(self, mock_api_client, mock_memo):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        with pytest.raises(
            kopf.PermanentError, match=r"Secret my-tls-secret ca.crt is invalid."
        ):
            twingate_resource_tls_secret_update(
                namespace="default",
                name="my-tls-secret",
                diff=[],
                new="invalid",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()
