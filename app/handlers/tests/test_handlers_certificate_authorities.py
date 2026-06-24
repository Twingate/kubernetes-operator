from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client_certificate_authorities import CertificateAuthority
from app.api.exceptions import GraphQLMutationError
from app.handlers.handlers_certificate_authorities import (
    twingate_ca_secret_index,
    twingate_ca_tls_secret_update,
    twingate_certificate_authority_create,
    twingate_certificate_authority_delete,
    twingate_certificate_authority_reconciler,
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


@pytest.fixture
def mock_fingerprint():
    with patch(
        "app.handlers.handlers_certificate_authorities.x509_sha256_fingerprint"
    ) as m:
        m.return_value = "AB:CD"
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
    def test_create(
        self, kopf_info_mock, mock_api_client, mock_get_certificate, mock_fingerprint
    ):
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="new-ca-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(_spec())

        assert result == {"success": True, "twingate_id": "new-ca-id", "ts": ANY}
        # First create uses the clean name (no timestamp suffix).
        mock_api_client.x509_certificate_authority_create.assert_called_once_with(
            name="My CA", certificate=mock_get_certificate.return_value
        )
        assert patch_mock.spec == {"id": "new-ca-id"}

    def test_already_registered_is_noop(
        self, mock_api_client, mock_get_certificate, mock_fingerprint
    ):
        # Backend CA exists with the same fingerprint - nothing to do.
        mock_api_client.get_x509_certificate_authority.return_value = (
            CertificateAuthority(id="ca-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "ca-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_create.assert_not_called()
        mock_api_client.x509_certificate_authority_delete.assert_not_called()
        assert patch_mock.spec == {}

    def test_recreate_when_backend_deleted(
        self, kopf_info_mock, mock_api_client, mock_get_certificate, mock_fingerprint
    ):
        # spec.id is set but the backend CA is gone - recreate, nothing to delete.
        mock_api_client.get_x509_certificate_authority.return_value = None
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "recreated-id", "ts": ANY}
        # Backend CA already gone - no name collision, so keep the clean name.
        mock_api_client.x509_certificate_authority_create.assert_called_once_with(
            name="My CA", certificate=mock_get_certificate.return_value
        )
        mock_api_client.x509_certificate_authority_delete.assert_not_called()
        assert patch_mock.spec == {"id": "recreated-id"}

    def test_recreate_on_fingerprint_drift(
        self, kopf_info_mock, mock_api_client, mock_get_certificate, mock_fingerprint
    ):
        # Cert rotated: backend fingerprint differs - recreate, then best-effort
        # delete the orphaned old CA.
        mock_api_client.get_x509_certificate_authority.return_value = (
            CertificateAuthority(id="ca-id", name="My CA", fingerprint="OLD:FP")
        )
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "recreated-id", "ts": ANY}
        # Old CA still holds the name - the re-create gets a timestamp suffix.
        call = mock_api_client.x509_certificate_authority_create.call_args
        assert call.kwargs["name"].startswith("My CA (")
        assert call.kwargs["certificate"] == mock_get_certificate.return_value
        mock_api_client.x509_certificate_authority_delete.assert_called_once_with(
            "ca-id"
        )
        assert patch_mock.spec == {"id": "recreated-id"}

    def test_recreate_on_drift_swallows_in_use_delete_error(
        self, kopf_info_mock, mock_api_client, mock_get_certificate, mock_fingerprint
    ):
        # The orphaned CA is still gateway-referenced, so the backend rejects the
        # delete. The re-create still succeeds.
        mock_api_client.get_x509_certificate_authority.return_value = (
            CertificateAuthority(id="ca-id", name="My CA", fingerprint="OLD:FP")
        )
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA", fingerprint="AB:CD")
        )
        mock_api_client.x509_certificate_authority_delete.side_effect = (
            GraphQLMutationError(
                "DeleteX509CertificateAuthority",
                "This CA is currently in use and cannot be deleted.",
            )
        )

        result, patch_mock = _call_create(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "recreated-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_delete.assert_called_once_with(
            "ca-id"
        )
        assert patch_mock.spec == {"id": "recreated-id"}

    def test_create_failure_propagates(
        self,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        # GraphQL errors propagate so Kopf retries (bounded by the handler
        # timeout), consistent with the resource handlers - the handler no longer
        # swallows them into a fail() result.
        mock_api_client.x509_certificate_authority_create.side_effect = (
            GraphQLMutationError("CreateX509CertificateAuthority", "boom")
        )

        with pytest.raises(GraphQLMutationError, match="boom"):
            _call_create(_spec())

    def test_missing_certificate_raises_temporary_error(
        self, mock_api_client, mock_get_certificate
    ):
        mock_get_certificate.return_value = None

        with pytest.raises(kopf.TemporaryError):
            _call_create(_spec())

        mock_api_client.x509_certificate_authority_create.assert_not_called()


class TestCertificateAuthorityReconciler:
    def test_reconciler_delegates_to_shared_reconcile(
        self, kopf_info_mock, mock_api_client, mock_get_certificate, mock_fingerprint
    ):
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="new-ca-id", name="My CA", fingerprint="AB:CD")
        )
        patch_mock = MagicMock()
        patch_mock.spec = {}

        result = twingate_certificate_authority_reconciler(
            "", _spec(), MagicMock(), MagicMock(), patch_mock
        )

        assert result == {"success": True, "twingate_id": "new-ca-id", "ts": ANY}
        assert patch_mock.spec == {"id": "new-ca-id"}


_STATUS = {"twingate_certificate_authority_create": {"success": True}}


def _call_delete(spec, status, *, gateway_index=None):
    twingate_certificate_authority_delete(
        namespace="default",
        name="my-ca",
        spec=spec,
        status=status,
        memo=MagicMock(),
        logger=MagicMock(),
        twingate_gateway_ca_index=gateway_index or {},
    )


class TestCertificateAuthorityDeleteHandler:
    def test_delete(self, mock_api_client):
        _call_delete(_spec(with_id=True), _STATUS)
        mock_api_client.x509_certificate_authority_delete.assert_called_once_with(
            "ca-id"
        )

    def test_delete_without_status_does_nothing(self, mock_api_client):
        _call_delete(_spec(with_id=True), {})
        mock_api_client.x509_certificate_authority_delete.assert_not_called()

    def test_delete_without_id_does_nothing(self, mock_api_client):
        _call_delete(_spec(), {"foo": "bar"})
        mock_api_client.x509_certificate_authority_delete.assert_not_called()

    def test_delete_in_use_retries_while_referenced(self, mock_api_client):
        # A Gateway in this cluster still references the CA: retry until the Gateway
        # is gone and the CA is freed (bounded by the handler timeout).
        mock_api_client.x509_certificate_authority_delete.side_effect = (
            GraphQLMutationError(
                "DeleteX509CertificateAuthority", "CA is in use by a gateway"
            )
        )

        with pytest.raises(kopf.TemporaryError):
            _call_delete(
                _spec(with_id=True),
                _STATUS,
                gateway_index={
                    ("default", "my-ca"): [{"namespace": "default", "name": "gw"}]
                },
            )

    def test_delete_in_use_gives_up_when_unreferenced(self, mock_api_client):
        # No in-cluster Gateway references the CA (stale ref, or another cluster's
        # Gateway holds it): nothing to wait for, give up.
        mock_api_client.x509_certificate_authority_delete.side_effect = (
            GraphQLMutationError(
                "DeleteX509CertificateAuthority", "CA is in use by a gateway"
            )
        )

        _call_delete(_spec(with_id=True), _STATUS)

    def test_delete_other_error_propagates(self, mock_api_client):
        # An unexpected backend error propagates so kopf retries (matching the other
        # delete handlers); the client already swallows already-deleted CAs.
        mock_api_client.x509_certificate_authority_delete.side_effect = (
            GraphQLMutationError("DeleteX509CertificateAuthority", "boom")
        )

        with pytest.raises(GraphQLMutationError, match="boom"):
            _call_delete(_spec(with_id=True), _STATUS)


class TestCertificateAuthoritySecretIndex:
    def test_maps_secret_to_ca(self):
        result = twingate_ca_secret_index(
            namespace="default", name="my-ca", spec=_spec()
        )
        assert result == {
            ("default", "gateway-tls"): {"namespace": "default", "name": "my-ca"}
        }

    def test_uses_secret_namespace_when_set(self):
        result = twingate_ca_secret_index(
            namespace="ns1",
            name="my-ca",
            spec={"name": "My CA", "secretRef": {"name": "tls", "namespace": "ns2"}},
        )
        assert result == {("ns2", "tls"): {"namespace": "ns1", "name": "my-ca"}}

    def test_none_without_secret_name(self):
        assert (
            twingate_ca_secret_index(namespace="default", name="my-ca", spec={}) is None
        )


@patch("app.handlers.handlers_certificate_authorities.k8s_patch_twingate_custom_object")
@patch("app.handlers.handlers_certificate_authorities.k8s_get_twingate_custom_object")
class TestCertificateAuthoritySecretWatch:
    @staticmethod
    def _index(refs=None):
        key = ("default", "gateway-tls")
        return {
            key: refs
            if refs is not None
            else [{"namespace": "default", "name": "my-ca"}]
        }

    def _call(self, index, event_type="MODIFIED"):
        twingate_ca_tls_secret_update(
            event={"type": event_type},
            namespace="default",
            name="gateway-tls",
            memo=MagicMock(),
            logger=MagicMock(),
            twingate_ca_secret_index=index,
        )

    def test_reconciles_referenced_ca_on_drift(
        self,
        mock_get_obj,
        mock_patch_obj,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        # Two CAs reference the same Secret - the handler must reconcile both, not
        # just the first ref.
        mock_get_obj.side_effect = [
            {
                "metadata": {"namespace": "default", "name": name},
                "spec": {
                    "name": "My CA",
                    "secretRef": {"name": "gateway-tls"},
                    "id": "ca-id",
                },
            }
            for name in ("my-ca", "my-ca-2")
        ]
        mock_api_client.get_x509_certificate_authority.return_value = (
            CertificateAuthority(id="ca-id", name="My CA", fingerprint="OLD:FP")
        )
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA", fingerprint="AB:CD")
        )

        self._call(
            self._index(
                [
                    {"namespace": "default", "name": "my-ca"},
                    {"namespace": "default", "name": "my-ca-2"},
                ]
            )
        )

        assert mock_get_obj.call_count == 2
        assert mock_api_client.x509_certificate_authority_create.call_count == 2
        assert mock_patch_obj.call_count == 2
        for call in mock_patch_obj.call_args_list:
            plural, _ns, _name, shim = call.args
            assert plural == "twingatecertificateauthorities"
            assert shim.spec == {"id": "recreated-id"}

    def test_skips_non_modified_events(
        self, mock_get_obj, mock_patch_obj, mock_api_client
    ):
        self._call(self._index(), event_type="ADDED")
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_unreferenced_secret(
        self, mock_get_obj, mock_patch_obj, mock_api_client
    ):
        self._call({})
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_when_ca_object_missing(
        self, mock_get_obj, mock_patch_obj, mock_api_client
    ):
        # The CA CR is gone (e.g. deleted) - nothing to reconcile or persist.
        mock_get_obj.return_value = None

        self._call(self._index())

        mock_api_client.x509_certificate_authority_create.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_continues_on_reconcile_failure(
        self,
        mock_get_obj,
        mock_patch_obj,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        # Reconcile blows up (cert not ready yet) - the error is logged and the
        # patch is not persisted.
        mock_get_obj.return_value = {
            "metadata": {"namespace": "default", "name": "my-ca"},
            "spec": {"name": "My CA", "secretRef": {"name": "gateway-tls"}},
        }
        mock_get_certificate.return_value = None

        self._call(self._index())

        mock_patch_obj.assert_not_called()
