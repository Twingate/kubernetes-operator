from unittest.mock import ANY, MagicMock, patch

import kubernetes
import orjson as json
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
    twingate_connector_pod_deleted,
    twingate_connector_recreate_pod,
    twingate_connector_resume,
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
        access_token="at", refresh_token="rt"  # nosec
    )
    run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())

    assert run.result == {
        "success": True,
        "twingate_id": connector.id,
        "image": "twingate/connector:test",
        "ts": ANY,
    }

    assert run.patch_mock.spec == {"id": connector.id, "name": connector.name}
    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is None

    run.kopf_adopt_mock.assert_called_once_with(
        ANY, owner=ANY, strict=True, forced=True
    )
    run.kopf_label_mock.assert_called_once_with(
        ANY, {"twingate.com/connector": crd.spec.name}
    )

    run.k8s_client_mock.create_namespaced_secret.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_secret.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].string_data == {
        "TWINGATE_ACCESS_TOKEN": "at",
        "TWINGATE_REFRESH_TOKEN": "rt",
    }

    run.k8s_client_mock.create_namespaced_pod.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_pod.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].spec["containers"][0] == {
        "env": ANY,
        "envFrom": [{"secretRef": {"name": crd.spec.name, "optional": False}}],
        "image": "twingate/connector:test",
        "imagePullPolicy": "Always",
        "name": "connector",
        "securityContext": ANY,
    }


def test_twingate_connector_create_with_imagepolicy_sets_check_annotation(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy())
    )

    mock_api_client.connector_create.return_value = connector
    mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at", refresh_token="rt"  # nosec
    )

    run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())
    assert run.result == {
        "success": True,
        "twingate_id": connector.id,
        "image": "twingate/connector:test",
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

    run.k8s_client_mock.create_namespaced_pod.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_pod.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].spec["containers"][0] == {
        "env": ANY,
        "envFrom": [{"secretRef": {"name": crd.spec.name, "optional": False}}],
        "image": "twingate/connector:test",
        "imagePullPolicy": "Always",
        "name": "connector",
        "securityContext": ANY,
    }


def test_twingate_connector_resume_without_image_policy_doesnt_annotates(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd()
    run = kopf_handler_runner(twingate_connector_resume, crd, MagicMock())
    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is None


def test_twingate_connector_resume_with_image_policy_annotates(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy())
    )
    run = kopf_handler_runner(twingate_connector_resume, crd, MagicMock())
    assert run.patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is not None


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


def test_twingate_connector_recreate_pod(get_connector_and_crd, kopf_handler_runner):
    connector, crd = get_connector_and_crd()
    run = kopf_handler_runner(twingate_connector_recreate_pod, crd, MagicMock())

    run.kopf_adopt_mock.assert_called_once_with(
        ANY, owner=ANY, strict=True, forced=True
    )
    run.kopf_label_mock.assert_called_once_with(
        ANY, {"twingate.com/connector": crd.spec.name}
    )
    run.k8s_client_mock.create_namespaced_pod.assert_called_once()


def test_twingate_connector_delete_deletes_connector(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd(
        status={"twingate_connector_create": {"success": True}}, with_id=True
    )
    run = kopf_handler_runner(twingate_connector_delete, crd, MagicMock())

    run.logger_mock.exception.assert_not_called()
    mock_api_client.connector_delete.assert_called_once()
    run.k8s_client_mock.patch_namespaced_pod.assert_called_once_with(
        crd.spec.name,
        "default",
        body={"metadata": {"labels": {"twingate.com/connector": None}}},
    )


def test_twingate_connector_delete_ignores_k8s_api_errors(
    get_connector_and_crd, kopf_handler_runner, k8s_client_mock, mock_api_client
):
    connector, crd = get_connector_and_crd(
        status={"twingate_connector_create": {"success": True}}, with_id=True
    )

    k8s_client_mock.patch_namespaced_pod.side_effect = (
        kubernetes.client.exceptions.ApiException()
    )

    run = kopf_handler_runner(twingate_connector_delete, crd, MagicMock())

    run.logger_mock.exception.assert_called_once()
    mock_api_client.connector_delete.assert_called_once()
    run.k8s_client_mock.patch_namespaced_pod.assert_called_once_with(
        crd.spec.name,
        "default",
        body={"metadata": {"labels": {"twingate.com/connector": None}}},
    )


def test_twingate_connector_delete_without_status_does_nothing(
    get_connector_and_crd, kopf_handler_runner, mock_api_client
):
    connector, crd = get_connector_and_crd()
    kopf_handler_runner(twingate_connector_delete, crd, MagicMock())
    mock_api_client.connector_delete.assert_not_called()


def test_twingate_connector_pod_deleted_tags_owner(get_connector_and_crd):
    connector, crd = get_connector_and_crd()
    pod = get_connector_pod(crd, "http://test.twingate.com", "twingate/1")
    pod.metadata = {
        "ownerReferences": [
            {
                "apiVersion": "twingate.com/v1beta",
                "kind": "TwingateConnector",
                "name": crd.spec.name,
            }
        ]
    }
    body = json.dumps(pod.to_dict())

    with patch(
        "kubernetes.client.CustomObjectsApi.patch_namespaced_custom_object"
    ) as patch_namespaced_custom_object_mock:
        twingate_connector_pod_deleted(
            body, pod.spec, pod.metadata, MagicMock(), "default", MagicMock()
        )

    patch_namespaced_custom_object_mock.assert_called_once_with(
        "twingate.com",
        "v1beta",
        "default",
        "twingateconnectors",
        crd.spec.name,
        {"metadata": {"labels": {"twingate.com/connector-pod-deleted": "true"}}},
    )


def test_twingate_connector_pod_deleted_does_nothing_if_owner_not_found(
    get_connector_and_crd,
):
    connector, crd = get_connector_and_crd()
    pod = get_connector_pod(crd, "http://test.twingate.com", "twingate/1")
    pod.metadata = {"ownerReferences": []}
    body = json.dumps(pod.to_dict())

    with patch(
        "kubernetes.client.CustomObjectsApi.patch_namespaced_custom_object"
    ) as patch_namespaced_custom_object_mock:
        twingate_connector_pod_deleted(
            body, pod.spec, pod.metadata, MagicMock(), "default", MagicMock()
        )

    patch_namespaced_custom_object_mock.assert_not_called()


def test_twingate_connector_pod_deleted_catches_k8s_api_exceptions(
    get_connector_and_crd,
):
    connector, crd = get_connector_and_crd()
    pod = get_connector_pod(crd, "http://test.twingate.com", "twingate/1")
    pod.metadata = {
        "ownerReferences": [
            {
                "apiVersion": "twingate.com/v1beta",
                "kind": "TwingateConnector",
                "name": crd.spec.name,
            }
        ]
    }
    body = json.dumps(pod.to_dict())

    logger = MagicMock()

    with patch(
        "kubernetes.client.CustomObjectsApi.patch_namespaced_custom_object",
        side_effect=kubernetes.client.exceptions.ApiException(),
    ) as patch_namespaced_custom_object_mock:
        twingate_connector_pod_deleted(
            body, pod.spec, pod.metadata, logger, "default", MagicMock()
        )

    logger.exception.assert_called_once()
    patch_namespaced_custom_object_mock.assert_called_once_with(
        "twingate.com",
        "v1beta",
        "default",
        "twingateconnectors",
        crd.spec.name,
        {"metadata": {"labels": {"twingate.com/connector-pod-deleted": "true"}}},
    )
