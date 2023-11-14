import collections
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


HandlerRunnerResult = collections.namedtuple(
    "HandlerRunnerResult",
    [
        "result",
        "memo_mock",
        "logger_mock",
        "patch_mock",
        "k8s_client_mock",
        "kopf_info_mock",
    ],
)


@pytest.fixture()
def kopf_handler_runner(k8s_client_mock, kopf_info_mock):
    def run(handler_f, crd, memo_mock, namespace="default"):
        logger_mock = MagicMock()

        patch_mock = MagicMock()
        patch_mock.spec = {}
        patch_mock.meta = {}

        result = handler_f(
            body=crd.model_dump(by_alias=True),
            spec=crd.spec.model_dump(by_alias=True),
            memo=memo_mock,
            logger=logger_mock,
            namespace=namespace,
            patch=patch_mock,
        )
        return HandlerRunnerResult(
            result, memo_mock, logger_mock, patch_mock, k8s_client_mock, kopf_info_mock
        )

    return run


@pytest.fixture()
def get_connector_and_crd(connector_factory):
    def get(*, spec_overrides=None):
        spec_overrides = spec_overrides or {}

        connector = connector_factory()
        connector_spec = ConnectorSpec(
            **spec_overrides, **connector.model_dump(exclude=["id"])
        )
        spec = connector_spec.model_dump(by_alias=True)
        crd = TwingateConnectorCRD(
            api_version="twingate.com/v1beta",
            kind="TwingateConnector",
            metadata=dict(uid="123", name="test-connector", namespace="default"),
            spec=spec,
        )
        return connector, crd

    return get


def test_twingate_connector_create(get_connector_and_crd, kopf_handler_runner):
    connector, crd = get_connector_and_crd()

    memo_mock = MagicMock()
    memo_mock.twingate_client.connector_create.return_value = connector
    memo_mock.twingate_client.connector_generate_tokens.return_value = ConnectorTokens(
        access_token="at", refresh_token="rt"
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
        access_token="at", refresh_token="rt"
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
