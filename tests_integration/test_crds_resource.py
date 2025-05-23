import subprocess

import pytest

from tests_integration.utils import (
    kubectl_apply,
    kubectl_create,
    kubectl_delete,
)


def test_browser_shortcut_false_allows_wildcard_address(unique_resource_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "*.default.cluster.local"
            isBrowserShortcutEnabled: false
    """
    )

    assert result.returncode == 0
    kubectl_delete("tgr", unique_resource_name)


def test_browser_shortcut_cant_have_wildcard_address(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "*.default.cluster.local"
                isBrowserShortcutEnabled: true
        """
        )

    stderr = ex.value.stderr.decode()
    assert (
        "if isBrowserShortcutEnabled is set to true, then address can't be wildcard"
        in stderr
    )

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo?.default.cluster.local"
                isBrowserShortcutEnabled: true
        """
        )

    stderr = ex.value.stderr.decode()
    assert (
        "if isBrowserShortcutEnabled is set to true, then address can't be wildcard"
        in stderr
    )


def test_protocols_tcp_allowall_cant_specify_ports(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    tcp:
                        policy: ALLOW_ALL
                        ports:
                            - start: 80
                              end: 80
        """
        )

    stderr = ex.value.stderr.decode()
    assert "Can't specify port ranges for ALLOW_ALL policy." in stderr

    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "*.default.cluster.local"
            protocols:
                tcp:
                    policy: ALLOW_ALL
    """
    )

    assert result.returncode == 0, result.value.stderr.decode()
    kubectl_delete("tgr", unique_resource_name)


def test_protocols_udp_allowall_cant_specify_ports(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    udp:
                        policy: ALLOW_ALL
                        ports:
                            - start: 80
                              end: 80
        """
        )

    stderr = ex.value.stderr.decode()
    assert "Can't specify port ranges for ALLOW_ALL policy." in stderr

    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "*.default.cluster.local"
            protocols:
                udp:
                    policy: ALLOW_ALL
    """
    )

    assert result.returncode == 0, result.value.stderr.decode()
    kubectl_delete("tgr", unique_resource_name)


def test_protocols_tcp_restricted(unique_resource_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "foo.default.cluster.local"
            protocols:
                tcp:
                    policy: RESTRICTED
    """
    )

    assert result.returncode == 0, result.value.stderr.decode()
    kubectl_delete("tgr", unique_resource_name)

    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "foo.default.cluster.local"
            protocols:
                tcp:
                    policy: RESTRICTED
                    ports:
                        - start: 80
                          end: 80
    """
    )

    assert result.returncode == 0, result.value.stderr.decode()
    kubectl_delete("tgr", unique_resource_name)


def test_protocols_udp_restricted(unique_resource_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "foo.default.cluster.local"
            protocols:
                udp:
                    policy: RESTRICTED
    """
    )

    assert result.returncode == 0, result.value.stderr.decode()
    kubectl_delete("tgr", unique_resource_name)

    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
            name: {unique_resource_name}
        spec:
            name: My K8S Resource
            address: "foo.default.cluster.local"
            protocols:
                udp:
                    policy: RESTRICTED
                    ports:
                        - start: 80
                          end: 80
    """
    )

    assert result.returncode == 0, result.value.stderr.decode()
    kubectl_delete("tgr", unique_resource_name)


def test_protocols_tcp_restricted_port_values_must_be_valid(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    tcp:
                        policy: RESTRICTED
                        ports:
                            - start: -1
                              end: 10
        """
        )

    stderr = ex.value.stderr.decode()
    assert "Invalid value: -1" in stderr


def test_protocols_tcp_restricted_port_values_start_must_be_lte_end(
    unique_resource_name,
):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    tcp:
                        policy: RESTRICTED
                        ports:
                            - start: 8080
                              end: 7080
        """
        )

    stderr = ex.value.stderr.decode()
    assert "Start port value must be less or equal to end port value" in stderr


def test_protocols_udp_restricted_port_values_must_be_valid(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    tcp:
                        policy: RESTRICTED
                        ports:
                            - start: 1
                              end: 1000000000
        """
        )

    stderr = ex.value.stderr.decode()
    assert "Invalid value: 1000000000" in stderr, stderr


def test_protocols_udp_restricted_port_values_start_must_be_lte_end(
    unique_resource_name,
):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    udp:
                        policy: RESTRICTED
                        ports:
                            - start: 8080
                              end: 7080
        """
        )

    stderr = ex.value.stderr.decode()
    assert "Start port value must be less or equal to end port value" in stderr


def test_resource_type_is_immutable(unique_resource_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: "foo.default.cluster.local"
          type: Network
        """
    )
    assert result.returncode == 0

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_apply(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Resource
              address: "foo.default.cluster.local"
              type: Kubernetes
              proxy:
                address: "my-proxy.default.cluster.local"
                certificateAuthorityCert: "base64-encoded-cert"
            """
        )

    stderr = ex.value.stderr.decode()
    assert "Resource type is immutable" in stderr

    kubectl_delete("tgr", unique_resource_name)


def test_network_resource_cannot_have_proxy_object(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Resource
              address: "foo.default.cluster.local"
              type: Network
              proxy:
                address: "my-proxy.default.cluster.local"
                certificateAuthorityCert: "base64-encoded-cert"
            """
        )

    stderr = ex.value.stderr.decode()
    assert "proxy should be set for Kubernetes Resource" in stderr


def test_kubernetes_resource_must_have_proxy_object(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Resource
              address: "foo.default.cluster.local"
              type: Kubernetes
            """
        )

    stderr = ex.value.stderr.decode()
    assert "proxy should be set for Kubernetes Resource" in stderr


def test_kubernetes_resource_cannot_have_browser_shortcut(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Resource
              address: "foo.default.cluster.local"
              isBrowserShortcutEnabled: true
              type: Kubernetes
              proxy:
                address: "my-proxy.default.cluster.local"
                certificateAuthorityCert: "base64-encoded-cert"
            """
        )

    stderr = ex.value.stderr.decode()
    assert (
        "isBrowserShortcutEnabled cannot be set to true for Kubernetes Resource"
        in stderr
    )
