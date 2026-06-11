from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client_certificate_authorities import CertificateAuthority
from app.api.exceptions import GraphQLMutationError
from app.handlers.handlers_certificate_authorities import (
    twingate_certificate_authority_create,
    twingate_certificate_authority_delete,
)


@pytest.fixture
def mock_api_client():
    with patch(
        "app.handlers.handlers_certificate_authorities.TwingateAPIClient"
    ) as mock_api_client:
        instance = MagicMock()
        mock_api_client.return_value = instance
        yield instance


@pytest.fixture
def mock_get_certificate():
    with patch("app.crds.CertificateAuthoritySpec.get_certificate") as m:
        m.return_value = "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
        yield m


def _spec(*, with_id=False):
    spec = {"name": "My CA", "secretRef": {"name": "gateway-tls"}}
    if with_id:
        spec["id"] = "ca-id"
    return spec


def _call_create(spec):
    patch_mock = MagicMock()
    patch_mock.spec = {}
    result = twingate_certificate_authority_create(
        "", spec, MagicMock(), MagicMock(), patch_mock
    )
    return result, patch_mock


class TestCertificateAuthorityCreateHandler:
    def test_create(self, kopf_info_mock, mock_api_client, mock_get_certificate):
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="new-ca-id", name="My CA")
        )

        result, patch_mock = _call_create(_spec())

        assert result == {"success": True, "twingate_id": "new-ca-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_create.assert_called_once_with(
            name="My CA", certificate=mock_get_certificate.return_value
        )
        assert patch_mock.spec == {"id": "new-ca-id"}

    def test_already_registered_is_noop(self, mock_api_client, mock_get_certificate):
        mock_api_client.get_certificate_authority.return_value = CertificateAuthority(
            id="ca-id", name="My CA"
        )

        result, patch_mock = _call_create(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "ca-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_create.assert_not_called()
        mock_get_certificate.assert_not_called()
        assert patch_mock.spec == {}

    def test_recreate_when_backend_deleted(
        self, kopf_info_mock, mock_api_client, mock_get_certificate
    ):
        # spec.id is set but the backend CA is gone (e.g. cert rotated) - recreate.
        mock_api_client.get_certificate_authority.return_value = None
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA")
        )

        result, patch_mock = _call_create(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "recreated-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_create.assert_called_once()
        assert patch_mock.spec == {"id": "recreated-id"}

    def test_missing_certificate_raises_temporary_error(
        self, mock_api_client, mock_get_certificate
    ):
        mock_get_certificate.return_value = None

        with pytest.raises(kopf.TemporaryError):
            _call_create(_spec())

        mock_api_client.x509_certificate_authority_create.assert_not_called()


class TestCertificateAuthorityDeleteHandler:
    def test_delete(self, mock_api_client):
        twingate_certificate_authority_delete(
            _spec(with_id=True),
            {"twingate_certificate_authority_create": {"success": True}},
            MagicMock(),
            MagicMock(),
        )
        mock_api_client.x509_certificate_authority_delete.assert_called_once_with(
            "ca-id"
        )

    def test_delete_without_status_does_nothing(self, mock_api_client):
        twingate_certificate_authority_delete(
            _spec(with_id=True), {}, MagicMock(), MagicMock()
        )
        mock_api_client.x509_certificate_authority_delete.assert_not_called()

    def test_delete_without_id_does_nothing(self, mock_api_client):
        twingate_certificate_authority_delete(
            _spec(), {"foo": "bar"}, MagicMock(), MagicMock()
        )
        mock_api_client.x509_certificate_authority_delete.assert_not_called()

    def test_delete_in_use_raises_temporary_error(self, mock_api_client):
        mock_api_client.x509_certificate_authority_delete.side_effect = (
            GraphQLMutationError(
                "DeleteX509CertificateAuthority", "CA is in use by a gateway"
            )
        )

        with pytest.raises(kopf.TemporaryError):
            twingate_certificate_authority_delete(
                _spec(with_id=True),
                {"twingate_certificate_authority_create": {"success": True}},
                MagicMock(),
                MagicMock(),
            )

    def test_delete_returns_false_raises_temporary_error(self, mock_api_client):
        # A False return (e.g. transport error) must retry, not leak the CA.
        mock_api_client.x509_certificate_authority_delete.return_value = False

        with pytest.raises(kopf.TemporaryError):
            twingate_certificate_authority_delete(
                _spec(with_id=True),
                {"twingate_certificate_authority_create": {"success": True}},
                MagicMock(),
                MagicMock(),
            )
