import subprocess

import pytest

from tests_integration.utils import kubectl_create, kubectl_delete


def test_success(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateCertificateAuthority
        metadata:
          name: {unique_resource_name}
        spec:
          name: My CA
          secretRef:
            name: gateway-tls
    """)

    assert result.returncode == 0
    kubectl_delete("tgca", unique_resource_name)


def test_spec_is_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec: Required value" in stderr


def test_name_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              secretRef:
                name: gateway-tls
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.name: Required" in stderr


def test_secret_ref_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.secretRef: Required" in stderr


def test_invalid_type_rejected(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
              type: bogus
              secretRef:
                name: gateway-tls
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.type" in stderr


def test_secret_ref_name_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
              secretRef: {{}}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.secretRef.name: Required" in stderr
