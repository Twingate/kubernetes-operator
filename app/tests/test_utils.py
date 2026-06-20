import pytest

from app.api.tests.factories import BASE64_OF_VALID_CA_CERT, VALID_CA_CERT
from app.utils import (
    to_bool,
    validate_pem_x509_certificate,
    x509_sha256_fingerprint,
)


class TestToBool:
    def test_unhashable(self):
        """Fails if value is unhashable."""
        with pytest.raises(ValueError, match=r"Cannot convert value to bool"):
            to_bool([])

    def test_truthy(self):
        """Fails if truthy values are incorrectly converted."""
        assert to_bool("t")
        assert to_bool("yes")
        assert to_bool("on")

    def test_falsy(self):
        """Fails if falsy values are incorrectly converted."""
        assert not to_bool("f")
        assert not to_bool("no")
        assert not to_bool("off")


class TestValidatePemX509Certificate:
    def test_valid_cert(self):
        try:
            validate_pem_x509_certificate(VALID_CA_CERT)
        except ValueError:
            pytest.fail("Failed to validate valid cert")

    def test_invalid_cert(self):
        with pytest.raises(ValueError, match=r"Invalid certificate"):
            validate_pem_x509_certificate(BASE64_OF_VALID_CA_CERT)

        with pytest.raises(ValueError, match=r"Invalid certificate"):
            validate_pem_x509_certificate(
                VALID_CA_CERT[len("-----BEGIN CERTIFICATE-----") :]
            )

        with pytest.raises(ValueError, match=r"Invalid certificate"):
            validate_pem_x509_certificate(
                VALID_CA_CERT[: -len("-----END CERTIFICATE-----")]
            )

        with pytest.raises(ValueError, match=r"Invalid certificate"):
            validate_pem_x509_certificate(
                """-----BEGIN CERTIFICATE-----
                MIIFfjCCA2agAwIBAgIUBNt
                -----END CERTIFICATE-----"""
            )


class TestX509Sha256Fingerprint:
    def test_fingerprint(self):
        assert x509_sha256_fingerprint(VALID_CA_CERT) == (
            "C3:FA:A1:49:4F:74:57:1E:85:E3:91:7C:55:58:62:DB:"
            "88:F8:74:CC:0F:6A:91:85:7C:BD:60:3B:93:43:80:E3"
        )
