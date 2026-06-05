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
          address: gateway.twingate.svc.cluster.local:443
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


def test_address_required(unique_resource_name):
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
    assert "spec.address: Required" in stderr


def test_ca_ref_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGateway
            metadata:
              name: {unique_resource_name}
            spec:
              address: gateway.twingate.svc.cluster.local:443
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
              address: gateway.twingate.svc.cluster.local:443
              x509CertificateAuthorityRef: {{}}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.x509CertificateAuthorityRef.name: Required" in stderr
