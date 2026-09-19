from unittest.mock import patch

import kopf
import pytest
from pydantic import ValidationError

from app.api.tests.factories import VALID_CA_CERT
from app.crds import (
    CACertificateReferenceKind,
    CertificateAuthoritySpec,
    CertificateAuthorityType,
    TwingateCertificateAuthorityCRD,
)


@pytest.fixture
def sample_ca_object():
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateCertificateAuthority",
        "metadata": {
            "name": "my-ca",
            "namespace": "default",
            "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        },
        "spec": {
            "name": "My CA",
            "secretRef": {"name": "gateway-tls"},
        },
    }


def test_ca_secret_ref_deserialization(sample_ca_object):
    ca = TwingateCertificateAuthorityCRD(**sample_ca_object)

    assert ca.metadata.name == "my-ca"
    assert ca.spec.name == "My CA"
    assert ca.spec.type == CertificateAuthorityType.X509
    assert ca.spec.secret_ref.name == "gateway-tls"
    assert ca.spec.secret_ref.namespace is None
    assert ca.spec.secret_ref.resolve_namespace("default") == "default"
    assert ca.spec.config_map_ref is None


def test_ca_type_defaults_to_x509():
    spec = CertificateAuthoritySpec(name="My CA", secret_ref={"name": "gateway-tls"})
    assert spec.type == CertificateAuthorityType.X509


def test_ca_rejects_ssh_type():
    # SSH is not supported yet; only X509 is accepted.
    with pytest.raises(ValidationError, match="type"):
        CertificateAuthoritySpec(
            name="My CA", type="SSH", secret_ref={"name": "gateway-tls"}
        )


def test_ca_rejects_invalid_type():
    with pytest.raises(ValidationError, match="type"):
        CertificateAuthoritySpec(
            name="My CA", type="bogus", secret_ref={"name": "gateway-tls"}
        )


def test_ca_name_required():
    with pytest.raises(ValidationError, match="name"):
        CertificateAuthoritySpec(secret_ref={"name": "gateway-tls"})


def test_ca_config_map_ref_deserialization(sample_ca_object):
    sample_ca_object["spec"] = {
        "name": "My CA",
        "configMapRef": {"name": "gateway-ca", "namespace": "ca-ns"},
    }

    ca = TwingateCertificateAuthorityCRD(**sample_ca_object)

    assert ca.spec.secret_ref is None
    assert ca.spec.config_map_ref.name == "gateway-ca"
    assert ca.spec.config_map_ref.resolve_namespace("default") == "ca-ns"


def test_ca_certificate_reference_required():
    with pytest.raises(
        ValidationError, match="Exactly one of secretRef or configMapRef must be set"
    ):
        CertificateAuthoritySpec(name="My CA")


def test_ca_rejects_both_secret_ref_and_config_map_ref():
    with pytest.raises(
        ValidationError, match="Exactly one of secretRef or configMapRef must be set"
    ):
        CertificateAuthoritySpec(
            name="My CA",
            secret_ref={"name": "gateway-tls"},
            config_map_ref={"name": "gateway-ca"},
        )


def test_ca_certificate_ref_is_the_configured_reference():
    secret_spec = CertificateAuthoritySpec(
        name="My CA", secret_ref={"name": "gateway-tls"}
    )
    config_map_spec = CertificateAuthoritySpec(
        name="My CA", config_map_ref={"name": "gateway-ca"}
    )

    assert secret_spec.certificate_ref == (
        CACertificateReferenceKind.SECRET,
        secret_spec.secret_ref,
    )
    assert config_map_spec.certificate_ref == (
        CACertificateReferenceKind.CONFIG_MAP,
        config_map_spec.config_map_ref,
    )


@patch("app.crds.k8s_read_namespaced_secret")
def test_get_certificate_reads_cert_from_secret(read_secret_mock, k8s_secret_mock):
    read_secret_mock.return_value = k8s_secret_mock
    spec = CertificateAuthoritySpec(name="My CA", secret_ref={"name": "gateway-tls"})

    # secretRef omits namespace, so it resolves to the CA's own namespace.
    assert spec.get_certificate("myns") == VALID_CA_CERT
    read_secret_mock.assert_called_once_with("myns", "gateway-tls")


@patch("app.crds.k8s_read_namespaced_secret")
def test_get_certificate_uses_secret_ref_namespace_when_set(
    read_secret_mock, k8s_secret_mock
):
    read_secret_mock.return_value = k8s_secret_mock
    spec = CertificateAuthoritySpec(
        name="My CA", secret_ref={"name": "gateway-tls", "namespace": "secrets-ns"}
    )

    assert spec.get_certificate("myns") == VALID_CA_CERT
    read_secret_mock.assert_called_once_with("secrets-ns", "gateway-tls")


@patch("app.crds.k8s_read_namespaced_secret")
def test_get_certificate_returns_none_when_secret_missing(read_secret_mock):
    read_secret_mock.return_value = None
    spec = CertificateAuthoritySpec(name="My CA", secret_ref={"name": "gateway-tls"})

    assert spec.get_certificate("default") is None


@patch("app.crds.k8s_read_namespaced_config_map")
def test_get_certificate_reads_cert_from_config_map(
    read_config_map_mock, k8s_configmap_mock
):
    read_config_map_mock.return_value = k8s_configmap_mock
    spec = CertificateAuthoritySpec(name="My CA", config_map_ref={"name": "gateway-ca"})

    # configMapRef omits namespace, so it resolves to the CA's own namespace.
    assert spec.get_certificate("myns") == VALID_CA_CERT
    read_config_map_mock.assert_called_once_with("myns", "gateway-ca")


@patch("app.crds.k8s_read_namespaced_config_map")
def test_get_certificate_uses_config_map_ref_namespace_when_set(
    read_config_map_mock, k8s_configmap_mock
):
    read_config_map_mock.return_value = k8s_configmap_mock
    spec = CertificateAuthoritySpec(
        name="My CA", config_map_ref={"name": "gateway-ca", "namespace": "ca-ns"}
    )

    assert spec.get_certificate("myns") == VALID_CA_CERT
    read_config_map_mock.assert_called_once_with("ca-ns", "gateway-ca")


@patch("app.crds.k8s_read_namespaced_config_map")
def test_get_certificate_returns_none_when_config_map_missing(read_config_map_mock):
    read_config_map_mock.return_value = None
    spec = CertificateAuthoritySpec(name="My CA", config_map_ref={"name": "gateway-ca"})

    assert spec.get_certificate("default") is None


class TestReadCACertFromSecret:
    def test_read_ca_cert_from_secret(self, k8s_secret_mock):
        assert (
            CertificateAuthoritySpec.read_certificate_authority_cert_from_secret(
                k8s_secret_mock
            )
            == VALID_CA_CERT
        )

    def test_read_ca_cert_from_secret_with_missing_ca_cert(self, k8s_secret_mock):
        k8s_secret_mock.data = {}

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls is missing ca.crt.",
        ):
            CertificateAuthoritySpec.read_certificate_authority_cert_from_secret(
                k8s_secret_mock
            )

    def test_read_ca_cert_from_secret_with_invalid_ca_cert(self, k8s_secret_mock):
        k8s_secret_mock.data["ca.crt"] = (
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tIE1JSUZmakNDQTJhZ0F3SUJBZ0lVQk50IC0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0="
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls ca.crt is invalid.",
        ):
            CertificateAuthoritySpec.read_certificate_authority_cert_from_secret(
                k8s_secret_mock
            )


class TestReadCACertFromConfigMap:
    def test_read_ca_cert_from_config_map(self, k8s_configmap_mock):
        assert (
            CertificateAuthoritySpec.read_certificate_authority_cert_from_config_map(
                k8s_configmap_mock
            )
            == VALID_CA_CERT
        )

    def test_read_ca_cert_from_config_map_with_missing_ca_cert(
        self, k8s_configmap_mock
    ):
        k8s_configmap_mock.data = {}

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes ConfigMap object: gateway-ca is missing ca.crt.",
        ):
            CertificateAuthoritySpec.read_certificate_authority_cert_from_config_map(
                k8s_configmap_mock
            )

    def test_read_ca_cert_from_config_map_without_data(self, k8s_configmap_mock):
        # A ConfigMap holding only `binaryData` has `data` unset (None).
        k8s_configmap_mock.data = None

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes ConfigMap object: gateway-ca is missing ca.crt.",
        ):
            CertificateAuthoritySpec.read_certificate_authority_cert_from_config_map(
                k8s_configmap_mock
            )

    def test_read_ca_cert_from_config_map_with_invalid_ca_cert(
        self, k8s_configmap_mock
    ):
        k8s_configmap_mock.data["ca.crt"] = (
            "-----BEGIN CERTIFICATE----- not a cert -----END CERTIFICATE-----"
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes ConfigMap object: gateway-ca ca.crt is invalid.",
        ):
            CertificateAuthoritySpec.read_certificate_authority_cert_from_config_map(
                k8s_configmap_mock
            )
