import subprocess

import pytest

from tests_integration.utils import kubectl_create, kubectl_delete


@pytest.mark.integration()
class TestResourceCRD:
    def test_browser_shortcut_false_allows_wildcard_address(self, unique_resource_name):
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
        kubectl_delete(f"tgr/{unique_resource_name}")

    def test_browser_shortcut_cant_have_wildcard_address(self, unique_resource_name):
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

    def test_protocols_tcp_allowall_cant_specify_ports(self, unique_resource_name):
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
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

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
        kubectl_delete(f"tgr/{unique_resource_name}")

    def test_protocols_udp_allowall_cant_specify_ports(self, unique_resource_name):
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
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

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
        kubectl_delete(f"tgr/{unique_resource_name}")

    def test_protocols_tcp_restricted_must_specify_ports(self, unique_resource_name):
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
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

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
        kubectl_delete(f"tgr/{unique_resource_name}")

    def test_protocols_udp_restricted_must_specify_ports(self, unique_resource_name):
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
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

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
        kubectl_delete(f"tgr/{unique_resource_name}")

    def test_protocols_tcp_restricted_port_values_must_be_valid(
        self, unique_resource_name
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
                                - start: -1
                                  end: 10
            """
            )

        stderr = ex.value.stderr.decode()
        assert "Invalid value: -1" in stderr

    def test_protocols_tcp_restricted_port_values_start_must_be_lte_end(
        self, unique_resource_name
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

    def test_protocols_udp_restricted_port_values_must_be_valid(
        self, unique_resource_name
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
                                - start: 1
                                  end: 1000000000
            """
            )

        stderr = ex.value.stderr.decode()
        assert "Invalid value: 1000000000" in stderr, stderr

    def test_protocols_udp_restricted_port_values_start_must_be_lte_end(
        self, unique_resource_name
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
