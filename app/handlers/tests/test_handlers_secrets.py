from unittest.mock import MagicMock, call, patch

import pytest
from gql.transport.exceptions import TransportQueryError

from app.api.exceptions import GraphQLMutationError
from app.api.tests.factories import (
    BASE64_OF_VALID_CA_CERT,
    VALID_CA_CERT,
    VALID_CA_CERT_1,
)
from app.crds import ResourceType
from app.handlers.handlers_secrets import twingate_tls_secret_update
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


class TestTwingateTlsSecretEvent:
    def test_update_resource_when_secret_change(
        self, mock_api_client, mock_memo, kubernetes_resource_factory
    ):
        resource_obj = sample_resource_obj(resource_id="1", resource_name="my-resource")
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        mock_api_client.get_resource.return_value = kubernetes_resource_factory(
            id="1", certificate_authority_cert=VALID_CA_CERT_1
        )

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=resource_obj,
        ):
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_called_once_with("1")
        mock_api_client.kubernetes_resource_update_ca_cert.assert_called_once_with(
            id="1",
            certificate_authority_cert=VALID_CA_CERT,
        )

    def test_update_multiple_resources_referencing_same_secret(
        self, mock_api_client, mock_memo, kubernetes_resource_factory
    ):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "resource-1"},
                {"namespace": "default", "name": "resource-2"},
                {"namespace": "default", "name": "resource-3"},
            ]
        }

        def get_resource_crd(_namespace, name):
            if name == "resource-1":
                return sample_resource_obj("resource-id-1", "resource-1")
            if name == "resource-2":
                return sample_resource_obj("resource-id-2", "resource-2")
            if name == "resource-3":
                return sample_resource_obj("resource-id-3", "resource-3")
            return None

        # Should continue updating other resources even if API request fails
        mock_api_client.get_resource.side_effect = [
            kubernetes_resource_factory(
                id="resource-id-1", certificate_authority_cert=VALID_CA_CERT_1
            ),
            kubernetes_resource_factory(
                id="resource-id-2", certificate_authority_cert=VALID_CA_CERT_1
            ),
            TransportQueryError("Failed to get resource"),
        ]
        mock_api_client.kubernetes_resource_update_ca_cert.side_effect = [
            MagicMock(),
            GraphQLMutationError("kubernetesResourceUpdate", "API error"),
            MagicMock(),
        ]

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            side_effect=get_resource_crd,
        ):
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_has_calls(
            [call("resource-id-1"), call("resource-id-2"), call("resource-id-3")],
            any_order=True,
        )
        mock_api_client.kubernetes_resource_update_ca_cert.assert_has_calls(
            [
                call(id="resource-id-1", certificate_authority_cert=VALID_CA_CERT),
                call(id="resource-id-2", certificate_authority_cert=VALID_CA_CERT),
            ],
            any_order=True,
        )

    @pytest.mark.parametrize("event_type", ["ADDED", "DELETED", None])
    def test_skip_update_on_non_modified_events(
        self, event_type, mock_api_client, mock_memo
    ):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        twingate_tls_secret_update(
            event={"type": event_type},
            body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
            namespace="default",
            name="my-tls-secret",
            memo=mock_memo,
            logger=MagicMock(),
            twingate_resource_secret_index=mock_index,
        )

        mock_api_client.get_resource.assert_not_called()
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    @pytest.mark.parametrize("secret_data", [{}, {"ca.crt": ""}, {"ca.crt": None}])
    def test_skip_update_on_empty_ca_cert(
        self, secret_data, mock_api_client, mock_memo
    ):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        twingate_tls_secret_update(
            event={"type": "MODIFIED"},
            body={"data": secret_data},
            namespace="default",
            name="my-tls-secret",
            memo=mock_memo,
            logger=MagicMock(),
            twingate_resource_secret_index=mock_index,
        )

        mock_api_client.get_resource.assert_not_called()
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_with_non_indexed_secret(self, mock_api_client, mock_memo):
        twingate_tls_secret_update(
            event={"type": "MODIFIED"},
            body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
            namespace="default",
            name="unrelated-secret",
            memo=mock_memo,
            logger=MagicMock(),
            twingate_resource_secret_index={},
        )

        mock_api_client.get_resource.assert_not_called()
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_on_invalid_cert(self, mock_api_client, mock_memo):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        twingate_tls_secret_update(
            event={"type": "MODIFIED"},
            body={"data": {"ca.crt": "invalid"}},
            namespace="default",
            name="my-tls-secret",
            memo=mock_memo,
            logger=MagicMock(),
            twingate_resource_secret_index=mock_index,
        )

        mock_api_client.get_resource.assert_not_called()
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_on_non_existent_resource(self, mock_api_client, mock_memo):
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "deleted-resource"}
            ]
        }

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=None,
        ):
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_not_called()
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_resource_without_id(self, mock_api_client, mock_memo):
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
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_not_called()
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_on_deleted_resource(self, mock_api_client, mock_memo):
        resource_obj = sample_resource_obj(resource_id="1", resource_name="my-resource")
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        mock_api_client.get_resource.return_value = None

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=resource_obj,
        ):
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_called_once_with("1")
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_on_network_resource(
        self, mock_api_client, mock_memo, network_resource_factory
    ):
        resource_obj = sample_resource_obj(resource_id="1", resource_name="my-resource")
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        mock_api_client.get_resource.return_value = network_resource_factory()

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=resource_obj,
        ):
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_called_once_with("1")
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()

    def test_skip_update_when_cert_unchanged(
        self, mock_api_client, mock_memo, kubernetes_resource_factory
    ):
        resource_obj = sample_resource_obj(resource_id="1", resource_name="my-resource")
        mock_index = {
            ("default", "my-tls-secret"): [
                {"namespace": "default", "name": "my-resource"}
            ]
        }

        mock_api_client.get_resource.return_value = kubernetes_resource_factory(
            certificate_authority_cert=VALID_CA_CERT
        )

        with patch(
            "app.handlers.handlers_secrets.k8s_get_twingate_resource",
            return_value=resource_obj,
        ):
            twingate_tls_secret_update(
                event={"type": "MODIFIED"},
                body={"data": {"ca.crt": BASE64_OF_VALID_CA_CERT}},
                namespace="default",
                name="my-tls-secret",
                memo=mock_memo,
                logger=MagicMock(),
                twingate_resource_secret_index=mock_index,
            )

        mock_api_client.get_resource.assert_called_once_with("1")
        mock_api_client.kubernetes_resource_update_ca_cert.assert_not_called()
