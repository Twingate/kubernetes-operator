import subprocess

import pytest

from tests_integration.utils import kubectl_create, kubectl_delete


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


def test_service_ref_required(unique_resource_name):
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
    assert "spec.serviceRef: Required" in stderr


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
