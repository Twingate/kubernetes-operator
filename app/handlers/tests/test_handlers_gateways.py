from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client_gateways import Gateway
from app.api.exceptions import GraphQLMutationError
from app.handlers.handlers_gateways import (
    twingate_gateway_create_update,
    twingate_gateway_delete,
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
    def run(spec, *, diff=None):
        patch_mock = MagicMock()
        patch_mock.spec = {}
        patch_mock.status = {}
        result = twingate_gateway_create_update(
            "",
            spec,
            MagicMock(),
            MagicMock(),
            patch_mock,
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
        assert patch_mock.status == {"address": "gateway.default.svc.cluster.local:443"}

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
        assert patch_mock.spec == {}

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
            diff=(("add", ("spec", "id"), None, "gateway-id"),),
        )

        assert result == {"success": True, "ts": ANY}
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


class TestGatewayDeleteHandler:
    def test_delete(self, mock_api_client):
        twingate_gateway_delete(
            _spec(with_id=True),
            {"twingate_gateway_create_update": {"success": True}},
            MagicMock(),
            MagicMock(),
        )
        mock_api_client.gateway_delete.assert_called_once_with("gateway-id")

    def test_delete_without_status_does_nothing(self, mock_api_client):
        twingate_gateway_delete(_spec(with_id=True), {}, MagicMock(), MagicMock())
        mock_api_client.gateway_delete.assert_not_called()

    def test_delete_without_id_does_nothing(self, mock_api_client):
        twingate_gateway_delete(_spec(), {"foo": "bar"}, MagicMock(), MagicMock())
        mock_api_client.gateway_delete.assert_not_called()

    def test_delete_in_use_raises_temporary_error(self, mock_api_client):
        mock_api_client.gateway_delete.side_effect = GraphQLMutationError(
            "DeleteGateway", "Gateway is being used by a resource"
        )

        with pytest.raises(kopf.TemporaryError):
            twingate_gateway_delete(
                _spec(with_id=True),
                {"twingate_gateway_create_update": {"success": True}},
                MagicMock(),
                MagicMock(),
            )

    def test_delete_returns_false_raises_temporary_error(self, mock_api_client):
        # A False return (e.g. transport error) must retry, not leak the Gateway.
        mock_api_client.gateway_delete.return_value = False

        with pytest.raises(kopf.TemporaryError):
            twingate_gateway_delete(
                _spec(with_id=True),
                {"twingate_gateway_create_update": {"success": True}},
                MagicMock(),
                MagicMock(),
            )
