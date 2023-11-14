from unittest.mock import ANY, MagicMock, patch

import pytest

from app.api.client_connectors import ConnectorTokens
from app.crds import ConnectorImagePolicy, ConnectorSpec, TwingateConnectorCRD
from app.handlers.handlers_connectors import (
    ANNOTATION_NEXT_VERSION_CHECK,
    twingate_connector_create,
)


@pytest.fixture(autouse=True)
def mock_connector_spec_get_image():
    with patch("app.crds.ConnectorSpec.get_image") as mock_get_image:
        mock_get_image.return_value = "twingate/connector:test"
        yield mock_get_image


@pytest.fixture()
def k8s_client_mock():
    client_mock = MagicMock()
    with patch("kubernetes.client.CoreV1Api") as k8sclient_mock:
        k8sclient_mock.return_value = client_mock
        yield client_mock


@pytest.fixture()
def kopf_info_mock():
    with patch("kopf.info") as kopf_info_mock:
        yield kopf_info_mock


def test_twingate_connector_create(connector_factory, kopf_info_mock, k8s_client_mock):
    connector = connector_factory()
    connector_spec = ConnectorSpec(**connector.model_dump(exclude=["id"]))
    spec = connector_spec.model_dump(by_alias=True)
    crd = TwingateConnectorCRD(
        api_version="twingate.com/v1beta",
        kind="TwingateConnector",
        metadata=dict(uid="123", name="test-connector", namespace="default"),
        spec=spec,
    )

    logger_mock = MagicMock()
    memo_mock = MagicMock()
    memo_mock.twingate_client.connector_create.return_value = connector
    memo_mock.twingate_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at", refresh_token="rt"
    )
    patch_mock = MagicMock()
    patch_mock.spec = {}
    patch_mock.meta = {}

    result = twingate_connector_create(
        body=crd.model_dump(by_alias=True),
        spec=spec,
        memo=memo_mock,
        logger=logger_mock,
        namespace="default",
        patch=patch_mock,
    )

    assert result == {
        "success": True,
        "twingate_id": connector.id,
        "image": "twingate/connector:test",
        "ts": ANY,
    }

    assert patch_mock.spec == {"id": connector.id, "name": connector.name}
    assert patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is None

    k8s_client_mock.create_namespaced_secret.assert_called_once()
    assert (
        k8s_client_mock.create_namespaced_secret.call_args.kwargs["namespace"]
        == "default"
    )
    assert k8s_client_mock.create_namespaced_secret.call_args.kwargs["body"].data == {
        "TWINGATE_ACCESS_TOKEN": "YXQ=",
        "TWINGATE_REFRESH_TOKEN": "cnQ=",
    }

    k8s_client_mock.create_namespaced_pod.assert_called_once()
    assert (
        k8s_client_mock.create_namespaced_pod.call_args.kwargs["namespace"] == "default"
    )
    assert k8s_client_mock.create_namespaced_pod.call_args.kwargs["body"].spec[
        "containers"
    ][0] == {
        "env": ANY,
        "envFrom": [{"secretRef": {"name": "test-connector", "optional": False}}],
        "image": "twingate/connector:test",
        "imagePullPolicy": "Always",
        "name": "connector",
        "securityContext": ANY,
    }


def test_twingate_connector_create_w_imagepolicy_sets_check_annotation(
    connector_factory, kopf_info_mock, k8s_client_mock
):
    connector = connector_factory()
    connector_spec = ConnectorSpec(
        image_policy=ConnectorImagePolicy(), **connector.model_dump(exclude=["id"])
    )
    spec = connector_spec.model_dump(by_alias=True)
    crd = TwingateConnectorCRD(
        api_version="twingate.com/v1beta",
        kind="TwingateConnector",
        metadata=dict(uid="123", name="test-connector", namespace="default"),
        spec=spec,
    )

    logger_mock = MagicMock()
    memo_mock = MagicMock()
    memo_mock.twingate_client.connector_create.return_value = connector
    memo_mock.twingate_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at", refresh_token="rt"
    )
    patch_mock = MagicMock()
    patch_mock.spec = {}

    result = twingate_connector_create(
        body=crd.model_dump(by_alias=True),
        spec=spec,
        memo=memo_mock,
        logger=logger_mock,
        namespace="default",
        patch=patch_mock,
    )

    assert result == {
        "success": True,
        "twingate_id": connector.id,
        "image": "twingate/connector:test",
        "ts": ANY,
    }

    assert patch_mock.spec == {"id": connector.id, "name": connector.name}
    assert patch_mock.meta["annotations"][ANNOTATION_NEXT_VERSION_CHECK] is not None

    k8s_client_mock.create_namespaced_secret.assert_called_once()
    assert (
        k8s_client_mock.create_namespaced_secret.call_args.kwargs["namespace"]
        == "default"
    )
    assert k8s_client_mock.create_namespaced_secret.call_args.kwargs["body"].data == {
        "TWINGATE_ACCESS_TOKEN": "YXQ=",
        "TWINGATE_REFRESH_TOKEN": "cnQ=",
    }

    k8s_client_mock.create_namespaced_pod.assert_called_once()
    assert (
        k8s_client_mock.create_namespaced_pod.call_args.kwargs["namespace"] == "default"
    )
    assert k8s_client_mock.create_namespaced_pod.call_args.kwargs["body"].spec[
        "containers"
    ][0] == {
        "env": ANY,
        "envFrom": [{"secretRef": {"name": "test-connector", "optional": False}}],
        "image": "twingate/connector:test",
        "imagePullPolicy": "Always",
        "name": "connector",
        "securityContext": ANY,
    }
