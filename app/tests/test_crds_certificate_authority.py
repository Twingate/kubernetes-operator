from unittest.mock import patch

import kopf
import pytest
from pydantic import ValidationError

from app.api.tests.factories import VALID_CA_CERT
from app.crds import (
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


def test_ca_deserialization(sample_ca_object):
    ca = TwingateCertificateAuthorityCRD(**sample_ca_object)

    assert ca.metadata.name == "my-ca"
    assert ca.spec.name == "My CA"
    assert ca.spec.type == CertificateAuthorityType.X509
    assert ca.spec.secret_ref.name == "gateway-tls"
    assert ca.spec.secret_ref.namespace == "default"


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


def test_ca_secret_ref_required():
    with pytest.raises(ValidationError, match="secretRef"):
        CertificateAuthoritySpec(name="My CA")


def test_ca_name_required():
    with pytest.raises(ValidationError, match="name"):
        CertificateAuthoritySpec(secret_ref={"name": "gateway-tls"})


@patch("app.crds.k8s_read_namespaced_secret")
def test_get_certificate_reads_cert_from_secret(read_secret_mock, k8s_secret_mock):
    read_secret_mock.return_value = k8s_secret_mock
    spec = CertificateAuthoritySpec(name="My CA", secret_ref={"name": "gateway-tls"})

    assert spec.get_certificate_from_secret() == VALID_CA_CERT
    read_secret_mock.assert_called_once_with("default", "gateway-tls")


@patch("app.crds.k8s_read_namespaced_secret")
def test_get_certificate_returns_none_when_secret_missing(read_secret_mock):
    read_secret_mock.return_value = None
    spec = CertificateAuthoritySpec(name="My CA", secret_ref={"name": "gateway-tls"})

    assert spec.get_certificate_from_secret() is None


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
