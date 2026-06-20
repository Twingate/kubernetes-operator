from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import kopf
import kubernetes
import pytest

from app.utils_k8s import (
    k8s_delete_pod,
    k8s_get_twingate_custom_object,
    k8s_patch_twingate_custom_object,
    k8s_read_namespaced_deployment,
    k8s_read_namespaced_pod,
    k8s_read_namespaced_secret,
    resolve_ref_to_twingate_id,
    resolve_service_address,
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


class TestReadNamespacedSecret:
    def test_handles_404_returns_none(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_secret.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        assert k8s_read_namespaced_secret("default", "test") is None

    def test_reraises_non_404_exceptions(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_secret.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )
        with pytest.raises(kubernetes.client.exceptions.ApiException):
            k8s_read_namespaced_secret("default", "test")


class TestGetTwingateCustomObject:
    def test_get_twingate_custom_object_returns_object(self):
        kapi = MagicMock()
        kapi.get_namespaced_custom_object.return_value = {"spec": {"id": "ca-1"}}

        result = k8s_get_twingate_custom_object(
            "twingatecertificateauthorities", "default", "my-ca", kapi=kapi
        )

        assert result == {"spec": {"id": "ca-1"}}
        kapi.get_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingatecertificateauthorities",
            "my-ca",
        )

    def test_get_twingate_custom_object_returns_none_on_404(self):
        kapi = MagicMock()
        kapi.get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )

        assert (
            k8s_get_twingate_custom_object("plural", "default", "name", kapi=kapi)
            is None
        )

    def test_get_twingate_custom_object_reraises_non_404(self):
        kapi = MagicMock()
        kapi.get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )

        with pytest.raises(kubernetes.client.exceptions.ApiException):
            k8s_get_twingate_custom_object("plural", "default", "name", kapi=kapi)

    @patch("app.utils_k8s.kubernetes.client.CustomObjectsApi")
    def test_get_twingate_custom_object_defaults_api_client(self, custom_api_mock):
        custom_api_mock.return_value.get_namespaced_custom_object.return_value = {
            "a": 1
        }

        result = k8s_get_twingate_custom_object("plural", "default", "name")

        assert result == {"a": 1}
        custom_api_mock.assert_called_once()


class TestPatchTwingateCustomObject:
    def test_patches_spec_and_status_together(self):
        kapi = MagicMock()
        patch = SimpleNamespace(spec={"id": "ca-1"}, status={"ok": True})

        k8s_patch_twingate_custom_object(
            "twingatecertificateauthorities", "default", "my-ca", patch, kapi=kapi
        )

        kapi.patch_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingatecertificateauthorities",
            "my-ca",
            {"spec": {"id": "ca-1"}, "status": {"ok": True}},
        )

    def test_no_op_when_empty(self):
        kapi = MagicMock()
        patch = SimpleNamespace(spec={}, status={})

        k8s_patch_twingate_custom_object("plural", "default", "name", patch, kapi=kapi)

        kapi.patch_namespaced_custom_object.assert_not_called()


class TestResolveRefToTwingateId:
    @patch("app.utils_k8s.k8s_get_twingate_custom_object")
    def test_resolve_ref_returns_twingate_id(self, get_obj_mock):
        get_obj_mock.return_value = {"spec": {"id": "ca-backend-id"}}

        result = resolve_ref_to_twingate_id(
            "twingatecertificateauthorities", "default", "my-ca"
        )

        assert result == "ca-backend-id"
        get_obj_mock.assert_called_once_with(
            "twingatecertificateauthorities", "default", "my-ca"
        )

    @patch("app.utils_k8s.k8s_get_twingate_custom_object")
    def test_resolve_ref_missing_object_raises_temporary_error(self, get_obj_mock):
        get_obj_mock.return_value = None

        with pytest.raises(kopf.TemporaryError):
            resolve_ref_to_twingate_id(
                "twingatecertificateauthorities", "default", "my-ca"
            )

    @patch("app.utils_k8s.k8s_get_twingate_custom_object")
    def test_resolve_ref_not_synced_raises_temporary_error(self, get_obj_mock):
        # Object exists but has not been assigned a backend id yet.
        get_obj_mock.return_value = {"spec": {}}

        with pytest.raises(kopf.TemporaryError):
            resolve_ref_to_twingate_id(
                "twingatecertificateauthorities", "default", "my-ca"
            )


def _service(service_type: str, ingress: list | None = None) -> MagicMock:
    service = MagicMock()
    service.spec.type = service_type
    if ingress is None:
        service.status.load_balancer.ingress = None
    else:
        service.status.load_balancer.ingress = ingress
    return service


class TestResolveServiceAddress:
    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_cluster_ip_resolves_to_dns_name(self, core_api_mock):
        core_api_mock.return_value.read_namespaced_service.return_value = _service(
            "ClusterIP"
        )

        address = resolve_service_address("twingate", "gateway", 443)

        assert address == "gateway.twingate.svc.cluster.local:443"

    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_node_port_resolves_to_dns_name(self, core_api_mock):
        core_api_mock.return_value.read_namespaced_service.return_value = _service(
            "NodePort"
        )

        address = resolve_service_address("twingate", "gateway", 443)

        assert address == "gateway.twingate.svc.cluster.local:443"

    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_unsupported_service_type_raises_permanent_error(self, core_api_mock):
        core_api_mock.return_value.read_namespaced_service.return_value = _service(
            "ExternalName"
        )

        with pytest.raises(kopf.PermanentError):
            resolve_service_address("twingate", "gateway", 443)

    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_load_balancer_resolves_to_ip(self, core_api_mock):
        ingress = [MagicMock(ip="203.0.113.10", hostname=None)]
        core_api_mock.return_value.read_namespaced_service.return_value = _service(
            "LoadBalancer", ingress
        )

        address = resolve_service_address("twingate", "gateway", 8443)

        assert address == "203.0.113.10:8443"

    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_load_balancer_resolves_to_hostname(self, core_api_mock):
        ingress = [MagicMock(ip=None, hostname="lb.example.com")]
        core_api_mock.return_value.read_namespaced_service.return_value = _service(
            "LoadBalancer", ingress
        )

        address = resolve_service_address("twingate", "gateway", 443)

        assert address == "lb.example.com:443"

    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_load_balancer_not_ready_raises_temporary_error(self, core_api_mock):
        core_api_mock.return_value.read_namespaced_service.return_value = _service(
            "LoadBalancer", ingress=[]
        )

        with pytest.raises(kopf.TemporaryError):
            resolve_service_address("twingate", "gateway", 443)

    @patch("app.utils_k8s.kubernetes.client.CoreV1Api")
    def test_missing_service_raises_temporary_error(self, core_api_mock):
        core_api_mock.return_value.read_namespaced_service.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )

        with pytest.raises(kopf.TemporaryError):
            resolve_service_address("twingate", "gateway", 443)
