from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client_certificate_authorities import CertificateAuthority
from app.api.exceptions import GraphQLMutationError
from app.handlers.handlers_certificate_authorities import (
    twingate_ca_config_map_update,
    twingate_ca_source_index,
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


def secret_spec(*, with_id=False):
    spec = {"name": "My CA", "secretRef": {"name": "gateway-tls"}}
    if with_id:
        spec["id"] = "ca-id"
    return spec


def config_map_spec(*, with_id=False):
    spec = {"name": "My CA", "configMapRef": {"name": "gateway-ca"}}
    if with_id:
        spec["id"] = "ca-id"
    return spec


def _call_create(spec):
    patch_mock = MagicMock()
    patch_mock.spec = {}
    result = twingate_certificate_authority_create(
        "", "default", spec, MagicMock(), MagicMock(), patch_mock
    )
    return result, patch_mock


class TestCertificateAuthorityCreateHandler:
    def test_create_from_secret(
        self,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="new-ca-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(secret_spec())

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

        result, patch_mock = _call_create(secret_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "ca-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_create.assert_not_called()
        mock_api_client.x509_certificate_authority_delete.assert_not_called()
        assert patch_mock.spec == {}

    def test_recreate_when_backend_deleted(
        self,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        # spec.id is set but the backend CA is gone - recreate, nothing to delete.
        mock_api_client.get_x509_certificate_authority.return_value = None
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(secret_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "recreated-id", "ts": ANY}
        # Backend CA already gone - no name collision, so keep the clean name.
        mock_api_client.x509_certificate_authority_create.assert_called_once_with(
            name="My CA", certificate=mock_get_certificate.return_value
        )
        mock_api_client.x509_certificate_authority_delete.assert_not_called()
        assert patch_mock.spec == {"id": "recreated-id"}

    def test_recreate_on_fingerprint_drift(
        self,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        # Cert rotated: backend fingerprint differs - recreate, then best-effort
        # delete the orphaned old CA.
        mock_api_client.get_x509_certificate_authority.return_value = (
            CertificateAuthority(id="ca-id", name="My CA", fingerprint="OLD:FP")
        )
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="recreated-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(secret_spec(with_id=True))

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
        self,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
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

        result, patch_mock = _call_create(secret_spec(with_id=True))

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
            _call_create(secret_spec())

    def test_create_from_config_map_ref(
        self,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="new-ca-id", name="My CA", fingerprint="AB:CD")
        )

        result, patch_mock = _call_create(config_map_spec())

        assert result == {"success": True, "twingate_id": "new-ca-id", "ts": ANY}
        mock_get_certificate.assert_called_once_with("default")
        mock_api_client.x509_certificate_authority_create.assert_called_once_with(
            name="My CA", certificate=mock_get_certificate.return_value
        )
        assert patch_mock.spec == {"id": "new-ca-id"}

    def test_missing_certificate_raises_temporary_error(
        self, mock_api_client, mock_get_certificate
    ):
        mock_get_certificate.return_value = None

        with pytest.raises(kopf.TemporaryError, match="Secret 'default/gateway-tls'"):
            _call_create(secret_spec())

        mock_api_client.x509_certificate_authority_create.assert_not_called()

    def test_missing_config_map_certificate_raises_temporary_error(
        self, mock_api_client, mock_get_certificate
    ):
        mock_get_certificate.return_value = None

        with pytest.raises(kopf.TemporaryError, match="ConfigMap 'default/gateway-ca'"):
            _call_create(config_map_spec())

        mock_api_client.x509_certificate_authority_create.assert_not_called()


class TestCertificateAuthorityReconciler:
    def test_reconciler_delegates_to_shared_reconcile(
        self,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
    ):
        mock_api_client.x509_certificate_authority_create.return_value = (
            CertificateAuthority(id="new-ca-id", name="My CA", fingerprint="AB:CD")
        )
        patch_mock = MagicMock()
        patch_mock.spec = {}

        result = twingate_certificate_authority_reconciler(
            "", "default", secret_spec(), MagicMock(), MagicMock(), patch_mock
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
        _call_delete(secret_spec(with_id=True), _STATUS)
        mock_api_client.x509_certificate_authority_delete.assert_called_once_with(
            "ca-id"
        )

    def test_delete_without_status_does_nothing(self, mock_api_client):
        _call_delete(secret_spec(with_id=True), {})
        mock_api_client.x509_certificate_authority_delete.assert_not_called()

    def test_delete_without_id_does_nothing(self, mock_api_client):
        _call_delete(secret_spec(), {"foo": "bar"})
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
                secret_spec(with_id=True),
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

        _call_delete(secret_spec(with_id=True), _STATUS)

    def test_delete_other_error_propagates(self, mock_api_client):
        # An unexpected backend error propagates so kopf retries (matching the other
        # delete handlers); the client already swallows already-deleted CAs.
        mock_api_client.x509_certificate_authority_delete.side_effect = (
            GraphQLMutationError("DeleteX509CertificateAuthority", "boom")
        )

        with pytest.raises(GraphQLMutationError, match="boom"):
            _call_delete(secret_spec(with_id=True), _STATUS)


class TestCertificateAuthoritySourceIndex:
    def test_maps_secret_to_ca(self):
        result = twingate_ca_source_index(
            namespace="default", name="my-ca", spec=secret_spec()
        )
        assert result == {
            ("Secret", "default", "gateway-tls"): {
                "namespace": "default",
                "name": "my-ca",
            }
        }

    def test_maps_config_map_to_ca(self):
        result = twingate_ca_source_index(
            namespace="default", name="my-ca", spec=config_map_spec()
        )
        assert result == {
            ("ConfigMap", "default", "gateway-ca"): {
                "namespace": "default",
                "name": "my-ca",
            }
        }

    def test_uses_ref_namespace_when_set(self):
        result = twingate_ca_source_index(
            namespace="ns1",
            name="my-ca",
            spec={"name": "My CA", "configMapRef": {"name": "ca", "namespace": "ns2"}},
        )
        assert result == {
            ("ConfigMap", "ns2", "ca"): {"namespace": "ns1", "name": "my-ca"}
        }

    def test_none_without_source(self):
        assert (
            twingate_ca_source_index(
                namespace="default", name="my-ca", spec={"name": "My CA"}
            )
            is None
        )
        assert (
            twingate_ca_source_index(namespace="default", name="my-ca", spec={}) is None
        )


# The Secret and ConfigMap watchers share reconcile_cas_referencing; run the same
# scenarios through each.
CA_SOURCES = [
    SimpleNamespace(
        kind="Secret",
        name="gateway-tls",
        handler=twingate_ca_tls_secret_update,
        spec=secret_spec,
    ),
    SimpleNamespace(
        kind="ConfigMap",
        name="gateway-ca",
        handler=twingate_ca_config_map_update,
        spec=config_map_spec,
    ),
]


@pytest.mark.parametrize("source", CA_SOURCES, ids=lambda s: s.kind)
@patch("app.handlers.handlers_certificate_authorities.k8s_patch_twingate_custom_object")
@patch("app.handlers.handlers_certificate_authorities.k8s_get_twingate_custom_object")
class TestCertificateAuthoritySourceWatch:
    @staticmethod
    def _index(source, refs=None, kind=None):
        key = (kind or source.kind, "default", source.name)
        return {
            key: refs
            if refs is not None
            else [{"namespace": "default", "name": "my-ca"}]
        }

    @staticmethod
    def _call(source, index, event_type="MODIFIED"):
        source.handler(
            event={"type": event_type},
            namespace="default",
            name=source.name,
            memo=MagicMock(),
            logger=MagicMock(),
            twingate_ca_source_index=index,
        )

    def test_reconciles_referenced_cas_on_drift(
        self,
        mock_get_obj,
        mock_patch_obj,
        kopf_info_mock,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
        source,
    ):
        # Two CAs reference the same object - the handler must reconcile both, not
        # just the first ref.
        mock_get_obj.side_effect = [
            {
                "metadata": {"namespace": "default", "name": name},
                "spec": source.spec(with_id=True),
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
            source,
            self._index(
                source,
                [
                    {"namespace": "default", "name": "my-ca"},
                    {"namespace": "default", "name": "my-ca-2"},
                ],
            ),
        )

        assert mock_get_obj.call_count == 2
        assert mock_api_client.x509_certificate_authority_create.call_count == 2
        assert mock_patch_obj.call_count == 2
        for call in mock_patch_obj.call_args_list:
            plural, _ns, _name, shim = call.args
            assert plural == "twingatecertificateauthorities"
            assert shim.spec == {"id": "recreated-id"}

    def test_skips_non_modified_events(
        self, mock_get_obj, mock_patch_obj, mock_api_client, source
    ):
        # E.g. every namespace has a kube-root-ca.crt ConfigMap with data.ca.crt; only
        # MODIFIED events for objects a CA references do any work.
        self._call(source, self._index(source), event_type="ADDED")
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_unreferenced_object(
        self, mock_get_obj, mock_patch_obj, mock_api_client, source
    ):
        self._call(source, {})
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_same_named_object_of_other_kind(
        self, mock_get_obj, mock_patch_obj, mock_api_client, source
    ):
        # A CA reading from a same-named object of the other kind must not be
        # reconciled - the index key carries the kind.
        other_kind = "ConfigMap" if source.kind == "Secret" else "Secret"
        self._call(source, self._index(source, kind=other_kind))
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_when_ca_object_missing(
        self, mock_get_obj, mock_patch_obj, mock_api_client, source
    ):
        # The CA CR is gone (e.g. deleted) - nothing to reconcile or persist.
        mock_get_obj.return_value = None

        self._call(source, self._index(source))

        mock_api_client.x509_certificate_authority_create.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_continues_on_reconcile_failure(
        self,
        mock_get_obj,
        mock_patch_obj,
        mock_api_client,
        mock_get_certificate,
        mock_fingerprint,
        source,
    ):
        # Reconcile blows up (cert not ready yet) - the error is logged and the
        # patch is not persisted.
        mock_get_obj.return_value = {
            "metadata": {"namespace": "default", "name": "my-ca"},
            "spec": source.spec(),
        }
        mock_get_certificate.return_value = None

        self._call(source, self._index(source))

        mock_patch_obj.assert_not_called()
