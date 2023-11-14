import collections
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pytest_factoryboy import register

from app.api.tests.factories import ConnectorFactory, ResourceFactory

register(ResourceFactory)
register(ConnectorFactory)


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
def kopf_handler_runner(k8s_client_mock: MagicMock, kopf_info_mock: MagicMock):
    def run(
        handler_f: Callable, crd: Any, memo_mock: MagicMock, namespace="default"
    ) -> HandlerRunnerResult:
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
