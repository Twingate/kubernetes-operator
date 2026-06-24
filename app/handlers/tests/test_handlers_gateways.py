from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client_gateways import Gateway
from app.api.exceptions import GraphQLMutationError
from app.handlers.handlers_gateways import (
    twingate_ca_id_changed,
    twingate_gateway_ca_index,
    twingate_gateway_create_update,
    twingate_gateway_delete,
    twingate_gateway_reconciler,
)


@pytest.fixture
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_gateways.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


@pytest.fixture
def mock_resolve_service_address():
    with patch("app.handlers.handlers_gateways.resolve_service_address") as m:
        m.return_value = "gateway.default.svc.cluster.local:443"
        yield m


@pytest.fixture
def mock_resolve_ref_to_twingate_id():
    with patch("app.handlers.handlers_gateways.resolve_ref_to_twingate_id") as m:
        m.return_value = "ca-backend-id"
        yield m


def _spec(*, with_id=False):
    spec = {
        "serviceRef": {"name": "my-gateway-svc", "port": 443},
        "x509CertificateAuthorityRef": {"name": "my-ca"},
    }
    if with_id:
        spec["id"] = "gateway-id"
    return spec


@pytest.fixture
def call_create_update(mock_resolve_service_address, mock_resolve_ref_to_twingate_id):
    def run(spec, *, diff=None, status=None):
        patch_mock = MagicMock()
        patch_mock.spec = {}
        patch_mock.status = {}
        result = twingate_gateway_create_update(
            "",
            spec,
            MagicMock(),
            MagicMock(),
            patch_mock,
            status=status,
            diff=diff,
        )
        return result, patch_mock

    return run


class TestGatewayCreateUpdateHandler:
    def test_create(self, kopf_info_mock, mock_api_client, call_create_update):
        gateway = Gateway(id="new-gateway-id", address="addr")
        mock_api_client.gateway_create.return_value = gateway

        result, patch_mock = call_create_update(_spec())

        assert result == {"success": True, "twingate_id": gateway.id, "ts": ANY}
        mock_api_client.gateway_create.assert_called_once_with(
            address="gateway.default.svc.cluster.local:443",
            remote_network_id=ANY,
            x509_ca_id="ca-backend-id",
        )
        mock_api_client.gateway_update.assert_not_called()
        assert patch_mock.spec == {"id": gateway.id}
        assert patch_mock.status == {
            "address": "gateway.default.svc.cluster.local:443",
            "x509CaId": "ca-backend-id",
        }

    def test_update_existing(self, mock_api_client, call_create_update):
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )

        result, patch_mock = call_create_update(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "gateway-id", "ts": ANY}
        mock_api_client.gateway_update.assert_called_once_with(
            gateway_id="gateway-id",
            remote_network_id=ANY,
            address="gateway.default.svc.cluster.local:443",
            x509_ca_id="ca-backend-id",
        )
        mock_api_client.gateway_create.assert_not_called()
        mock_api_client.x509_certificate_authority_delete.assert_not_called()
        assert patch_mock.spec == {}

    def test_update_swaps_ca_deletes_old(self, mock_api_client, call_create_update):
        # The Gateway moves off the old CA - the orphaned old CA is best-effort
        # deleted now rather than left to linger.
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )

        result, _patch_mock = call_create_update(
            _spec(with_id=True), status={"x509CaId": "old-ca-id"}
        )

        assert result == {"success": True, "twingate_id": "gateway-id", "ts": ANY}
        mock_api_client.x509_certificate_authority_delete.assert_called_once_with(
            "old-ca-id"
        )

    def test_update_same_ca_does_not_delete(self, mock_api_client, call_create_update):
        # CA unchanged (status already points at the resolved id) - nothing to reap.
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )

        call_create_update(_spec(with_id=True), status={"x509CaId": "ca-backend-id"})

        mock_api_client.x509_certificate_authority_delete.assert_not_called()

    def test_recreate_when_backend_deleted(
        self, kopf_info_mock, mock_api_client, call_create_update
    ):
        # spec.id is set but the backend entity is gone - recreate it.
        mock_api_client.get_gateway.return_value = None
        mock_api_client.gateway_create.return_value = Gateway(
            id="recreated-id", address="addr"
        )

        result, patch_mock = call_create_update(_spec(with_id=True))

        assert result == {"success": True, "twingate_id": "recreated-id", "ts": ANY}
        mock_api_client.gateway_create.assert_called_once()
        mock_api_client.gateway_update.assert_not_called()
        assert patch_mock.spec == {"id": "recreated-id"}

    def test_diff_only_id_added_skips(self, mock_api_client, call_create_update):
        result, patch_mock = call_create_update(
            _spec(with_id=True),
            diff=(("add", ("id",), None, "gateway-id"),),
        )

        assert result == {
            "success": True,
            "twingate_id": "gateway-id",
            "message": "No update required",
            "ts": ANY,
        }
        mock_api_client.gateway_create.assert_not_called()
        mock_api_client.gateway_update.assert_not_called()
        assert patch_mock.spec == {}

    def test_error_resets_id_when_backend_missing(
        self, kopf_exception_mock, mock_api_client, call_create_update
    ):
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )
        mock_api_client.gateway_update.side_effect = GraphQLMutationError(
            "UpdateGateway", "Gateway does not exist"
        )

        result, patch_mock = call_create_update(_spec(with_id=True))

        assert result["success"] is False
        assert patch_mock.spec == {"id": None}

    def test_error_keeps_id_otherwise(
        self, kopf_exception_mock, mock_api_client, call_create_update
    ):
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )
        mock_api_client.gateway_update.side_effect = GraphQLMutationError(
            "UpdateGateway", "something else broke"
        )

        result, patch_mock = call_create_update(_spec(with_id=True))

        assert result["success"] is False
        assert patch_mock.spec == {}


class TestGatewayReconciler:
    def test_reconciler_delegates_to_shared_reconcile(
        self,
        kopf_info_mock,
        mock_api_client,
        mock_resolve_service_address,
        mock_resolve_ref_to_twingate_id,
    ):
        mock_api_client.gateway_create.return_value = Gateway(
            id="new-gateway-id", address="addr"
        )
        patch_mock = MagicMock()
        patch_mock.spec = {}
        patch_mock.status = {}

        result = twingate_gateway_reconciler(
            "", _spec(), MagicMock(), MagicMock(), patch_mock
        )

        assert result == {"success": True, "twingate_id": "new-gateway-id", "ts": ANY}
        assert patch_mock.spec == {"id": "new-gateway-id"}


_STATUS = {"twingate_gateway_create_update": {"success": True}}


def _call_delete(spec, status, *, resource_index=None):
    twingate_gateway_delete(
        namespace="default",
        name="my-gw",
        spec=spec,
        status=status,
        memo=MagicMock(),
        logger=MagicMock(),
        twingate_resource_gateway_index=resource_index or {},
    )


class TestGatewayDeleteHandler:
    def test_delete(self, mock_api_client):
        _call_delete(_spec(with_id=True), _STATUS)
        mock_api_client.gateway_delete.assert_called_once_with("gateway-id")

    def test_delete_without_status_does_nothing(self, mock_api_client):
        _call_delete(_spec(with_id=True), {})
        mock_api_client.gateway_delete.assert_not_called()

    def test_delete_without_id_does_nothing(self, mock_api_client):
        _call_delete(_spec(), {"foo": "bar"})
        mock_api_client.gateway_delete.assert_not_called()

    def test_delete_in_use_retries_while_referenced(self, mock_api_client):
        # A Resource in this cluster still references the Gateway: retry until the
        # Resource is gone and the Gateway is freed (bounded by the handler timeout).
        mock_api_client.gateway_delete.side_effect = GraphQLMutationError(
            "DeleteGateway", "Gateway is being used by a resource"
        )

        with pytest.raises(kopf.TemporaryError):
            _call_delete(
                _spec(with_id=True),
                _STATUS,
                resource_index={
                    ("default", "my-gw"): [{"namespace": "default", "name": "res"}]
                },
            )

    def test_delete_in_use_gives_up_when_unreferenced(self, mock_api_client):
        # No in-cluster Resource references the Gateway (stale ref, or another
        # cluster's Resource holds it): nothing to wait for, give up.
        mock_api_client.gateway_delete.side_effect = GraphQLMutationError(
            "DeleteGateway", "Gateway is being used by a resource"
        )

        _call_delete(_spec(with_id=True), _STATUS)

    def test_delete_other_error_propagates(self, mock_api_client):
        # An unexpected backend error propagates so kopf retries (matching the other
        # delete handlers); the client already swallows already-deleted Gateways.
        mock_api_client.gateway_delete.side_effect = GraphQLMutationError(
            "DeleteGateway", "boom"
        )

        with pytest.raises(GraphQLMutationError, match="boom"):
            _call_delete(_spec(with_id=True), _STATUS)


class TestGatewayCaIndex:
    def test_maps_ca_to_gateway(self):
        result = twingate_gateway_ca_index(
            namespace="default", name="my-gw", spec=_spec()
        )
        assert result == {
            ("default", "my-ca"): {"namespace": "default", "name": "my-gw"}
        }

    def test_uses_ca_namespace_when_set(self):
        spec = _spec()
        spec["x509CertificateAuthorityRef"] = {"name": "my-ca", "namespace": "ns2"}
        result = twingate_gateway_ca_index(namespace="ns1", name="my-gw", spec=spec)
        assert result == {("ns2", "my-ca"): {"namespace": "ns1", "name": "my-gw"}}

    def test_none_without_ca_name(self):
        assert (
            twingate_gateway_ca_index(namespace="default", name="my-gw", spec={})
            is None
        )


@patch("app.handlers.handlers_gateways.k8s_patch_twingate_custom_object")
@patch("app.handlers.handlers_gateways.k8s_get_twingate_custom_object")
class TestGatewayCaIdChanged:
    @staticmethod
    def _index(refs=None):
        key = ("default", "my-ca")
        return {
            key: refs
            if refs is not None
            else [{"namespace": "default", "name": "my-gw"}]
        }

    def _call(self, index, new="ca-backend-id"):
        twingate_ca_id_changed(
            namespace="default",
            name="my-ca",
            new=new,
            memo=MagicMock(),
            logger=MagicMock(),
            twingate_gateway_ca_index=index,
        )

    def test_reconciles_referencing_gateway(
        self,
        mock_get_obj,
        mock_patch_obj,
        mock_api_client,
        mock_resolve_service_address,
        mock_resolve_ref_to_twingate_id,
    ):
        mock_get_obj.return_value = {
            "metadata": {"namespace": "default", "name": "my-gw"},
            "spec": {**_spec(with_id=True)},
        }
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )

        self._call(self._index())

        mock_api_client.gateway_update.assert_called_once()
        plural, _ns, _name, shim = mock_patch_obj.call_args.args
        assert plural == "twingategateways"
        assert shim.status["x509CaId"] == "ca-backend-id"

    def test_noop_when_id_unset(self, mock_get_obj, mock_patch_obj, mock_api_client):
        self._call(self._index(), new=None)
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_noop_without_referencing_gateways(
        self, mock_get_obj, mock_patch_obj, mock_api_client
    ):
        self._call({})
        mock_get_obj.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_when_gateway_object_missing(
        self, mock_get_obj, mock_patch_obj, mock_api_client
    ):
        # The Gateway CR is gone - nothing to reconcile or persist.
        mock_get_obj.return_value = None

        self._call(self._index())

        mock_api_client.gateway_update.assert_not_called()
        mock_api_client.gateway_create.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_reraises_temporary_error_for_retry(
        self,
        mock_get_obj,
        mock_patch_obj,
        mock_api_client,
        mock_resolve_service_address,
        mock_resolve_ref_to_twingate_id,
    ):
        # CA/service not ready - re-raise so Kopf retries; patch not persisted.
        mock_get_obj.return_value = {
            "metadata": {"namespace": "default", "name": "my-gw"},
            "spec": {**_spec(with_id=True)},
        }
        mock_resolve_service_address.side_effect = kopf.TemporaryError("not ready")

        with pytest.raises(kopf.TemporaryError):
            self._call(self._index())

        mock_patch_obj.assert_not_called()

    def test_continues_on_non_transient_failure(
        self,
        mock_get_obj,
        mock_patch_obj,
        mock_api_client,
        mock_resolve_service_address,
        mock_resolve_ref_to_twingate_id,
    ):
        # A non-transient error is logged and swallowed (timer is the backstop),
        # so the handler does not re-raise and the patch is not persisted.
        mock_get_obj.return_value = {
            "metadata": {"namespace": "default", "name": "my-gw"},
            "spec": {**_spec(with_id=True)},
        }
        mock_api_client.get_gateway.side_effect = GraphQLMutationError(
            "GetGateway", "boom"
        )

        self._call(self._index())

        mock_patch_obj.assert_not_called()

    def test_one_gateway_not_ready_does_not_starve_others(
        self,
        mock_get_obj,
        mock_patch_obj,
        mock_api_client,
        mock_resolve_service_address,
        mock_resolve_ref_to_twingate_id,
    ):
        # First Gateway is not ready, second reconciles fine: the ready one is still
        # persisted, and the handler re-raises so the stuck one is retried.
        refs = [
            {"namespace": "default", "name": "gw-not-ready"},
            {"namespace": "default", "name": "gw-ready"},
        ]
        mock_get_obj.side_effect = lambda _plural, _ns, gw_name: {
            "metadata": {"namespace": "default", "name": gw_name},
            "spec": {**_spec(with_id=True)},
        }
        mock_api_client.get_gateway.return_value = Gateway(
            id="gateway-id", address="old-addr"
        )
        mock_resolve_service_address.side_effect = [
            kopf.TemporaryError("not ready"),
            "gateway.default.svc.cluster.local:443",
        ]

        with pytest.raises(kopf.TemporaryError):
            self._call(self._index(refs))

        # Only the ready Gateway's patch is persisted.
        mock_patch_obj.assert_called_once()
        _plural, _ns, name, _shim = mock_patch_obj.call_args.args
        assert name == "gw-ready"
