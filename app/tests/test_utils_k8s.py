import kopf
import kubernetes
import pytest

from app.api.tests.factories import BASE64_OF_VALID_CA_CERT
from app.utils_k8s import (
    get_ca_cert,
    k8s_delete_pod,
    k8s_get_secret,
    k8s_read_namespaced_deployment,
    k8s_read_namespaced_pod,
)


class TestReadNamespacedPod:
    def test_handles_404_returns_none(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_pod.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        assert k8s_read_namespaced_pod("default", "test") is None

    def test_reraises_non_404_exceptions(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_pod.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )
        with pytest.raises(kubernetes.client.exceptions.ApiException):
            k8s_read_namespaced_pod("default", "test")


class TestDeletePod:
    def test_calls_patch_when_force(self, k8s_core_client_mock):
        k8s_core_client_mock.patch_namespaced_pod.return_value = None
        k8s_core_client_mock.delete_namespaced_pod.return_value = None

        k8s_delete_pod("default", "test", force=True)

        k8s_core_client_mock.patch_namespaced_pod.assert_called_once()
        k8s_core_client_mock.delete_namespaced_pod.assert_called_once()

    def test_calls_only_delete_when_not_force(self, k8s_core_client_mock):
        k8s_core_client_mock.patch_namespaced_pod.return_value = None
        k8s_core_client_mock.delete_namespaced_pod.return_value = None

        k8s_delete_pod("default", "test", force=False)

        k8s_core_client_mock.patch_namespaced_pod.assert_not_called()
        k8s_core_client_mock.delete_namespaced_pod.assert_called_once()


class TestReadNamespacedDeployment:
    def test_handles_404_returns_none(self, k8s_apps_client_mock):
        k8s_apps_client_mock.read_namespaced_deployment.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        assert k8s_read_namespaced_deployment("default", "test") is None

    def test_reraises_non_404_exceptions(self, k8s_apps_client_mock):
        k8s_apps_client_mock.read_namespaced_deployment.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )
        with pytest.raises(kubernetes.client.exceptions.ApiException):
            k8s_read_namespaced_deployment("default", "test")


class TestK8sGetTLSSecret:
    def test_handles_404_returns_none(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_secret.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        assert k8s_get_secret("default", "test") is None

    def test_reraises_non_404_exceptions(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_secret.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )
        with pytest.raises(kubernetes.client.exceptions.ApiException):
            k8s_get_secret("default", "test")


class TestGetCACert:
    def test_get_ca_cert(self, k8s_tls_secret_mock):
        assert get_ca_cert(k8s_tls_secret_mock) == BASE64_OF_VALID_CA_CERT

    def test_get_ca_cert_with_invalid_secret_type(self, k8s_tls_secret_mock):
        k8s_tls_secret_mock.type = "kubernetes.io/token"

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls type is invalid.",
        ):
            get_ca_cert(k8s_tls_secret_mock)

    def test_get_ca_cert_with_missing_ca_cert(self, k8s_tls_secret_mock):
        k8s_tls_secret_mock.data = {}

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls is missing ca.crt.",
        ):
            get_ca_cert(k8s_tls_secret_mock)

    def test_get_ca_cert_with_invalid_ca_cert(self, k8s_tls_secret_mock):
        k8s_tls_secret_mock.data["ca.crt"] = (
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tIE1JSUZmakNDQTJhZ0F3SUJBZ0lVQk50IC0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0="
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls ca.crt is invalid.",
        ):
            get_ca_cert(k8s_tls_secret_mock)
