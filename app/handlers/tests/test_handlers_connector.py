from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client_connectors import ConnectorTokens
from app.crds import ConnectorImagePolicy, ConnectorSpec, TwingateConnectorCRD
from app.handlers.handlers_connectors import (
    twingate_connector_create,
    twingate_connector_delete,
    twingate_connector_pod_reconciler,
    twingate_connector_update,
)


@pytest.fixture(autouse=True)
def mock_connector_spec_get_image():
    with patch("app.crds.ConnectorSpec.get_image") as mock_get_image:
        mock_get_image.return_value = "twingate/connector:test"
        yield mock_get_image


@pytest.fixture()
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_connectors.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


@pytest.fixture()
def get_connector_and_crd(connector_factory):
    def get(*, spec_overrides=None, status=None, with_id=False, annotations=None):
        annotations = annotations or {}
        spec_overrides = spec_overrides or {}

        connector = connector_factory()
        connector_spec = ConnectorSpec(
            **spec_overrides, **connector.model_dump(exclude=[] if with_id else ["id"])
        )
        spec = connector_spec.model_dump(by_alias=True)
        crd = TwingateConnectorCRD(
            api_version="twingate.com/v1beta",
            kind="TwingateConnector",
            metadata=dict(
                uid="123",
                name=connector_spec.name,
                namespace="default",
                annotations=annotations,
            ),
            spec=spec,
            status=status,
        )
        return connector, crd

    return get


def test_twingate_connector_create(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd()

    mock_api_client.connector_create.return_value = connector
    mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at",
        refresh_token="rt",  # nosec
    )
    run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())

    assert run.result == {
        "success": True,
        "twingate_id": connector.id,
        "ts": ANY,
    }

    assert run.patch_mock.spec == {"id": connector.id, "name": connector.name}

    run.kopf_adopt_mock.assert_called_once_with(
        ANY, owner=ANY, strict=True, forced=True
    )

    run.k8s_client_mock.create_namespaced_secret.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_secret.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].string_data == {
        "TWINGATE_ACCESS_TOKEN": "at",
        "TWINGATE_REFRESH_TOKEN": "rt",
    }


def test_twingate_connector_create_with_imagepolicy_sets_check_annotation(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy())
    )

    mock_api_client.connector_create.return_value = connector
    mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at",
        refresh_token="rt",  # nosec
    )

    run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())
    assert run.result == {
        "success": True,
        "twingate_id": connector.id,
        "ts": ANY,
    }

    assert run.patch_mock.spec == {"id": connector.id, "name": connector.name}

    run.k8s_client_mock.create_namespaced_secret.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_secret.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].string_data == {
        "TWINGATE_ACCESS_TOKEN": "at",
        "TWINGATE_REFRESH_TOKEN": "rt",
    }


def test_twingate_connector_update(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd(with_id=True)

    mock_api_client.connector_update.return_value = connector

    run = kopf_handler_runner(
        twingate_connector_update, crd, MagicMock(), new={}, diff={}
    )
    assert run.result == {"success": True, "twingate_id": connector.id, "ts": ANY}


def test_twingate_connector_update_without_id_does_nothing(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd(with_id=False)

    mock_api_client.connector_update.return_value = connector

    run = kopf_handler_runner(
        twingate_connector_update, crd, MagicMock(), new={}, diff={}
    )
    assert run.result == {
        "error": "Update called before Connector has an ID",
        "success": False,
        "ts": ANY,
    }


def test_twingate_connector_delete_deletes_connector(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd(
        status={"twingate_connector_create": {"success": True}}, with_id=True
    )
    kopf_handler_runner(twingate_connector_delete, crd, MagicMock())
    mock_api_client.connector_delete.assert_called_once()


def test_twingate_connector_delete_without_status_does_nothing(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd()
    kopf_handler_runner(twingate_connector_delete, crd, MagicMock())
    mock_api_client.connector_delete.assert_not_called()


def test_twingate_connector_pod_reconciler_raises_if_ran_before_create(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd()
    with pytest.raises(kopf.TemporaryError):
        kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())


class TestTwingateConnectorPodReconciler_Image:
    def test_pod_create(
        self, get_connector_and_crd, kopf_handler_runner, k8s_client_mock
    ):
        connector, crd = get_connector_and_crd(
            status={"twingate_connector_create": {"success": True}}, with_id=True
        )

        k8s_client_mock.read_namespaced_pod.return_value = None

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        run.k8s_client_mock.create_namespaced_pod.assert_called_once()

    def test_pod_update(
        self, get_connector_and_crd, kopf_handler_runner, k8s_client_mock
    ):
        connector, crd = get_connector_and_crd(
            status={"twingate_connector_create": {"success": True}}, with_id=True
        )

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        run.k8s_client_mock.patch_namespaced_pod.assert_called_once()
