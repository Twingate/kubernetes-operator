import pytest
from pydantic import ValidationError

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


def test_ca_accepts_ssh_type():
    spec = CertificateAuthoritySpec(
        name="My CA", type="SSH", secret_ref={"name": "gateway-tls"}
    )
    assert spec.type == CertificateAuthorityType.SSH


def test_ca_rejects_invalid_type():
    with pytest.raises(ValidationError):
        CertificateAuthoritySpec(
            name="My CA", type="bogus", secret_ref={"name": "gateway-tls"}
        )


def test_ca_secret_ref_required():
    with pytest.raises(ValidationError):
        CertificateAuthoritySpec(name="My CA")


def test_ca_name_required():
    with pytest.raises(ValidationError):
        CertificateAuthoritySpec(secret_ref={"name": "gateway-tls"})
