from unittest.mock import ANY, MagicMock, patch

import kubernetes
import orjson as json
import pytest

from app.api.client_connectors import ConnectorTokens
from app.crds import ConnectorImagePolicy, ConnectorSpec, TwingateConnectorCRD
from app.handlers.handlers_connectors import (
    ANNOTATION_NEXT_VERSION_CHECK,
    get_connector_pod,
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
def get_connector_and_crd(connector_factory):
    def get(*, spec_overrides=None, status=None, with_id=False):
        spec_overrides = spec_overrides or {}

        connector = connector_factory()
        connector_spec = ConnectorSpec(
            **spec_overrides, **connector.model_dump(exclude=[] if with_id else ["id"])
        )
        spec = connector_spec.model_dump(by_alias=True)
        crd = TwingateConnectorCRD(
            api_version="twingate.com/v1beta",
            kind="TwingateConnector",
            metadata=dict(uid="123", name="test-connector", namespace="default"),
            spec=spec,
            status=status,
        )
        return connector, crd

    return get


def test_twingate_connector_create(get_connector_and_crd, kopf_handler_runner):
    connector, crd = get_connector_and_crd()

    memo_mock = MagicMock()
    memo_mock.twingate_client.connector_create.return_value = connector
    memo_mock.twingate_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at", refresh_token="rt"  # nosec
    )
    run = kopf_handler_runner(twingate_connector_create, crd, memo_mock)

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
        ANY, {"twingate.com/connector": "test-connector"}
    )

    run.k8s_client_mock.create_namespaced_secret.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_secret.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].data == {
        "TWINGATE_ACCESS_TOKEN": "YXQ=",
        "TWINGATE_REFRESH_TOKEN": "cnQ=",
    }

    run.k8s_client_mock.create_namespaced_pod.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_pod.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].spec["containers"][0] == {
        "env": ANY,
        "envFrom": [{"secretRef": {"name": "test-connector", "optional": False}}],
        "image": "twingate/connector:test",
        "imagePullPolicy": "Always",
        "name": "connector",
        "securityContext": ANY,
    }


def test_twingate_connector_create_with_imagepolicy_sets_check_annotation(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd(
        spec_overrides=dict(image_policy=ConnectorImagePolicy())
    )

    memo_mock = MagicMock()
    memo_mock.twingate_client.connector_create.return_value = connector
    memo_mock.twingate_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at", refresh_token="rt"  # nosec
    )

    run = kopf_handler_runner(twingate_connector_create, crd, memo_mock)
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
    assert call_kw["body"].data == {
        "TWINGATE_ACCESS_TOKEN": "YXQ=",
        "TWINGATE_REFRESH_TOKEN": "cnQ=",
    }

    run.k8s_client_mock.create_namespaced_pod.assert_called_once()
    call_kw = run.k8s_client_mock.create_namespaced_pod.call_args.kwargs
    assert call_kw["namespace"] == "default"
    assert call_kw["body"].spec["containers"][0] == {
        "env": ANY,
        "envFrom": [{"secretRef": {"name": "test-connector", "optional": False}}],
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


def test_twingate_connector_version_policy_update(get_connector_and_crd):
    connector, crd = get_connector_and_crd()

    patch = MagicMock()
    logger = MagicMock()

    twingate_connector_version_policy_update(
        crd.model_dump(by_alias=True), patch, logger
    )
    assert patch.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is not None


def test_twingate_connector_recreate_pod(get_connector_and_crd, kopf_handler_runner):
    connector, crd = get_connector_and_crd()
    run = kopf_handler_runner(twingate_connector_recreate_pod, crd, MagicMock())

    run.kopf_adopt_mock.assert_called_once_with(
        ANY, owner=ANY, strict=True, forced=True
    )
    run.kopf_label_mock.assert_called_once_with(
        ANY, {"twingate.com/connector": "test-connector"}
    )
    run.k8s_client_mock.create_namespaced_pod.assert_called_once()


def test_twingate_connector_delete_deletes_connector(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd(
        status={"twingate_connector_create": {"success": True}}, with_id=True
    )
    run = kopf_handler_runner(twingate_connector_delete, crd, MagicMock())

    run.logger_mock.exception.assert_not_called()
    run.memo_mock.twingate_client.connector_delete.assert_called_once()
    run.k8s_client_mock.patch_namespaced_pod.assert_called_once_with(
        "test-connector",
        "default",
        body={"metadata": {"labels": {"twingate.com/connector": None}}},
    )


def test_twingate_connector_delete_ignores_k8s_api_errors(
    get_connector_and_crd, kopf_handler_runner, k8s_client_mock
):
    connector, crd = get_connector_and_crd(
        status={"twingate_connector_create": {"success": True}}, with_id=True
    )

    k8s_client_mock.patch_namespaced_pod.side_effect = (
        kubernetes.client.exceptions.ApiException()
    )

    run = kopf_handler_runner(twingate_connector_delete, crd, MagicMock())

    run.logger_mock.exception.assert_called_once()
    run.memo_mock.twingate_client.connector_delete.assert_called_once()
    run.k8s_client_mock.patch_namespaced_pod.assert_called_once_with(
        "test-connector",
        "default",
        body={"metadata": {"labels": {"twingate.com/connector": None}}},
    )


def test_twingate_connector_delete_without_status_does_nothing(
    get_connector_and_crd, kopf_handler_runner
):
    connector, crd = get_connector_and_crd()
    run = kopf_handler_runner(twingate_connector_delete, crd, MagicMock())
    run.memo_mock.twingate_client.connector_delete.assert_not_called()


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
