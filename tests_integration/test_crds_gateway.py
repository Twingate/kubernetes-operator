import subprocess

import pytest

from tests_integration.utils import (
    kubectl_apply,
    kubectl_create,
    kubectl_delete,
    kubectl_get,
)


def test_success(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateGateway
        metadata:
          name: {unique_resource_name}
        spec:
          serviceRef:
            name: my-gateway-svc
            port: 443
          x509CertificateAuthorityRef:
            name: my-ca
    """)

    assert result.returncode == 0
    kubectl_delete("tggw", unique_resource_name)


def test_spec_is_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec: Required value" in stderr


def test_remote_network_id(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateGateway
        metadata:
          name: {unique_resource_name}
        spec:
          remoteNetworkId: "UmVtb3RlTmV0d29yazoxMjMK"
          serviceRef:
            name: my-gateway-svc
            port: 443
          x509CertificateAuthorityRef:
            name: my-ca
    """)

    assert result.returncode == 0

    data = kubectl_get("tggw", unique_resource_name)
    assert data["spec"]["remoteNetworkId"] == "UmVtb3RlTmV0d29yazoxMjMK"

    kubectl_delete("tggw", unique_resource_name)


def test_remote_network_id_invalid_pattern(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              remoteNetworkId: "not valid!"
              serviceRef:
                name: my-gateway-svc
                port: 443
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.remoteNetworkId in body should match" in stderr


def test_remote_network_id_is_immutable(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateGateway
        metadata:
          name: {unique_resource_name}
        spec:
          remoteNetworkId: "UmVtb3RlTmV0d29yazoxMjMK"
          serviceRef:
            name: my-gateway-svc
            port: 443
          x509CertificateAuthorityRef:
            name: my-ca
    """)
    assert result.returncode == 0

    try:
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_apply(f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateGateway
                metadata:
                  name: {unique_resource_name}
                spec:
                  remoteNetworkId: "UmVtb3RlTmV0d29yazo0NTYK"
                  serviceRef:
                    name: my-gateway-svc
                    port: 443
                  x509CertificateAuthorityRef:
                    name: my-ca
            """)

        stderr = ex.value.stderr.decode()
        assert "remoteNetworkId is immutable once set" in stderr
    finally:
        kubectl_delete("tggw", unique_resource_name)


def test_service_ref_or_address_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "exactly one of serviceRef or address must be set" in stderr


def test_service_ref_and_address_mutually_exclusive(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              serviceRef:
                name: my-gateway-svc
                port: 443
              address:
                host: gateway.corp.internal
                port: 8443
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "exactly one of serviceRef or address must be set" in stderr


def test_service_ref_name_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              serviceRef:
                port: 443
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.serviceRef.name: Required" in stderr


def test_service_ref_port_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              serviceRef:
                name: my-gateway-svc
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.serviceRef.port: Required" in stderr


@pytest.mark.parametrize("port", [0, 65536])
def test_service_ref_port_out_of_range(unique_resource_name, port):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              serviceRef:
                name: my-gateway-svc
                port: {port}
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.serviceRef.port" in stderr


@pytest.mark.parametrize(
    ("host", "port"),
    [
        ("gateway.corp.internal", 8443),
        ("10.0.0.1", 1),
        ("gateway.corp.internal", 65535),
    ],
)
def test_address(unique_resource_name, host, port):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateGateway
        metadata:
          name: {unique_resource_name}
        spec:
          address:
            host: "{host}"
            port: {port}
          x509CertificateAuthorityRef:
            name: my-ca
    """)

    assert result.returncode == 0

    data = kubectl_get("tggw", unique_resource_name)
    assert data["spec"]["address"] == {"host": host, "port": port}

    kubectl_delete("tggw", unique_resource_name)


@pytest.mark.parametrize(
    ("address", "error"),
    [
        ("{port: 443}", "spec.address.host: Required"),
        (
            '{host: "", port: 443}',
            "spec.address.host in body should be at least 1 chars long",
        ),
        ("{host: gateway.corp.internal}", "spec.address.port: Required"),
    ],
)
def test_address_field_invalid(unique_resource_name, address, error):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              address: {address}
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert error in stderr


@pytest.mark.parametrize("port", [0, 65536])
def test_address_port_out_of_range(unique_resource_name, port):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              address:
                host: gateway.corp.internal
                port: {port}
              x509CertificateAuthorityRef:
                name: my-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.address.port" in stderr


def test_ca_ref_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              serviceRef:
                name: my-gateway-svc
                port: 443
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.x509CertificateAuthorityRef: Required" in stderr


def test_ca_ref_name_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              serviceRef:
                name: my-gateway-svc
                port: 443
              x509CertificateAuthorityRef: {{}}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.x509CertificateAuthorityRef.name: Required" in stderr
