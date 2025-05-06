import kubernetes
import pytest

from app.utils_k8s import k8s_read_namespaced_pod


def test_k8s_read_namespaced_pod_handles_404_returns_none(k8s_core_client_mock):
    k8s_core_client_mock.read_namespaced_pod.side_effect = (
        kubernetes.client.exceptions.ApiException(status=404)
    )
    assert k8s_read_namespaced_pod("default", "test") is None


def test_k8s_read_namespaced_reraises_non_404_exceptions(k8s_core_client_mock):
    k8s_core_client_mock.read_namespaced_pod.side_effect = (
        kubernetes.client.exceptions.ApiException(status=500)
    )
    with pytest.raises(kubernetes.client.exceptions.ApiException):
        k8s_read_namespaced_pod("default", "test")
