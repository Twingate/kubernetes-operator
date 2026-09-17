import subprocess

import pytest

from tests_integration.utils import kubectl_apply, kubectl_create, kubectl_delete


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


def test_success_with_config_map_ref(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateCertificateAuthority
        metadata:
          name: {unique_resource_name}
        spec:
          name: My CA
          configMapRef:
            name: gateway-ca
            namespace: other-ns
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


def test_certificate_source_required(unique_resource_name):
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
    assert "Exactly one of `secretRef` or `configMapRef` must be set." in stderr


def test_secret_ref_and_config_map_ref_are_specified(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
              secretRef:
                name: gateway-tls
              configMapRef:
                name: gateway-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "Exactly one of `secretRef` or `configMapRef` must be set." in stderr


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


def ca_manifest(name, ref_key, labels=""):
    """CA manifest reading `ca.crt` from ``ref_key`` (secretRef / configMapRef / None)."""
    source_names = {"secretRef": "gateway-tls", "configMapRef": "gateway-ca"}
    source = ""
    if ref_key is not None:
        source = f"""
          {ref_key}:
            name: {source_names[ref_key]}"""
    return f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateCertificateAuthority
        metadata:
          name: {name}{labels}
        spec:
          name: My CA{source}
    """


def test_update_keeping_certificate_source_is_accepted(unique_resource_name):
    # The transition rule must not reject updates that leave the source alone.
    result = kubectl_apply(ca_manifest(unique_resource_name, "configMapRef"))
    assert result.returncode == 0

    result = kubectl_apply(
        ca_manifest(
            unique_resource_name,
            "configMapRef",
            labels="""
          labels:
            updated: now""",
        )
    )
    assert result.returncode == 0

    kubectl_delete("tgca", unique_resource_name)


def test_secret_ref_is_immutable(unique_resource_name):
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

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_apply(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
              secretRef:
                name: other-tls
        """)

    stderr = ex.value.stderr.decode()
    assert "secretRef is immutable" in stderr

    kubectl_delete("tgca", unique_resource_name)


def test_config_map_ref_name_required(unique_resource_name):
    # An empty object still satisfies has(self.configMapRef), so the exactly-one
    # rule must not mask the nested required `name`.
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
              configMapRef: {{}}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.configMapRef.name: Required" in stderr


def test_config_map_ref_is_immutable(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateCertificateAuthority
        metadata:
          name: {unique_resource_name}
        spec:
          name: My CA
          configMapRef:
            name: gateway-ca
    """)
    assert result.returncode == 0

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_apply(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My CA
              configMapRef:
                name: other-ca
        """)

    stderr = ex.value.stderr.decode()
    assert "configMapRef is immutable" in stderr

    kubectl_delete("tgca", unique_resource_name)


@pytest.mark.parametrize(
    ("ref_key", "new_ref_key"),
    [
        ("secretRef", "configMapRef"),
        ("configMapRef", "secretRef"),
    ],
)
def test_certificate_source_cannot_change_after_creation(
    unique_resource_name, ref_key, new_ref_key
):
    result = kubectl_apply(ca_manifest(unique_resource_name, ref_key))
    assert result.returncode == 0

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_apply(ca_manifest(unique_resource_name, new_ref_key))

    stderr = ex.value.stderr.decode()
    assert "Cannot switch between `secretRef` and `configMapRef`." in stderr

    kubectl_delete("tgca", unique_resource_name)


def test_name_is_immutable(unique_resource_name):
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

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_apply(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateCertificateAuthority
            metadata:
              name: {unique_resource_name}
            spec:
              name: My Renamed CA
              secretRef:
                name: gateway-tls
        """)

    stderr = ex.value.stderr.decode()
    assert "name is immutable" in stderr

    kubectl_delete("tgca", unique_resource_name)
