from unittest.mock import ANY, MagicMock, patch

import pendulum
import pytest

from app.api.client_connectors import ConnectorTokens
from app.crds import ConnectorImagePolicy, ConnectorSpec, TwingateConnectorCRD
from app.handlers.handlers_connectors import (
    ANNOTATION_LAST_VERSION_CHECK,
    ANNOTATION_NEXT_VERSION_CHECK,
    get_connector_pod,
    timer_check_image_version,
    twingate_connector_create,
    twingate_connector_delete,
    twingate_connector_update,
    twingate_connector_version_policy_update,
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
    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is None

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
    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is not None

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


def test_twingate_connector_version_policy_update(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy())
    )

    run = kopf_handler_runner(
        twingate_connector_version_policy_update, crd, MagicMock()
    )

    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is not None


def test_timer_check_image_version_without_imagepolicy(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd()
    run = kopf_handler_runner(timer_check_image_version, crd, MagicMock())
    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is None


def test_timer_check_image_version_with_imagepolicy_updates_pod_if_check_due(
    get_connector_and_crd, kopf_handler_runner, freezer
):
    full_url = "https://test.twingate.com"
    now = pendulum.now("UTC").start_of("minute")
    now_iso = now.to_iso8601_string()

    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy()),
        annotations={ANNOTATION_NEXT_VERSION_CHECK: now_iso},
    )
    memo = MagicMock()
    memo.twingate_settings.full_url = full_url

    run = kopf_handler_runner(timer_check_image_version, crd, memo)

    expected_pod = get_connector_pod(crd, full_url, "twingate/connector:test")

    assert run.patch_mock.meta["annotations"][ANNOTATION_LAST_VERSION_CHECK] == now_iso
    assert (
        run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK]
        == crd.spec.image_policy.get_next_date_iso8601()
    )
    run.k8s_client_mock.patch_namespaced_pod.assert_called_once_with(
        crd.spec.name, "default", body=expected_pod
    )


def test_timer_check_image_version_with_imagepolicy_do_nothing_if_check_not_due(
    get_connector_and_crd, kopf_handler_runner, freezer
):
    full_url = "https://test.twingate.com"
    now = pendulum.now("UTC").start_of("minute")
    now_iso = now.to_iso8601_string()
    now_minus_onem = now.subtract(minutes=1)

    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy()),
        annotations={ANNOTATION_NEXT_VERSION_CHECK: now_iso},
    )
    memo = MagicMock()
    memo.twingate_settings.full_url = full_url

    freezer.move_to(now_minus_onem)

    run = kopf_handler_runner(timer_check_image_version, crd, memo)

    run.k8s_client_mock.patch_namespaced_pod.assert_not_called()
    assert run.patch_mock.meta == {}


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
