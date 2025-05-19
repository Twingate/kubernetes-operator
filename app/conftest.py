from unittest.mock import MagicMock, patch

import pytest
import responses


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture(scope="module", autouse=True)
def _mock_settings():
    from app.settings import TwingateOperatorSettings

    settings = TwingateOperatorSettings(
        api_key="apikey",
        network="network",
        remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
    )

    with patch("app.crds.get_settings", return_value=settings):
        yield


@pytest.fixture
def k8s_core_client_mock():
    client_mock = MagicMock()
    with patch("kubernetes.client.CoreV1Api") as k8sclient_mock:
        k8sclient_mock.return_value = client_mock
        yield client_mock


@pytest.fixture
def k8s_apps_client_mock():
    client_mock = MagicMock()
    with patch("kubernetes.client.AppsV1Api") as k8sclient_mock:
        k8sclient_mock.return_value = client_mock
        yield client_mock
