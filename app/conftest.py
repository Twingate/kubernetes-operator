from unittest.mock import MagicMock, patch

import kubernetes
import pytest
import responses

from app.api.tests.factories import BASE64_OF_VALID_CA_CERT


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture(autouse=True)
def _mock_shard_resolution():
    # Resolving the shard host makes a real (retried) HTTP request on every
    # TwingateOperatorSettings construction. Make it a no-op in unit tests so
    # they stay network-free. app/tests/test_settings.py overrides this with a
    # no-op fixture to exercise the real resolver.
    with patch(
        "app.settings._resolve_shard_host", side_effect=lambda network, host: host
    ):
        yield


@pytest.fixture(scope="module", autouse=True)
def _mock_settings():
    from app.settings import TwingateOperatorSettings

    # Module-scoped fixtures set up before the function-scoped
    # _mock_shard_resolution above, so patch the resolver here too to keep
    # construction network-free.
    with patch(
        "app.settings._resolve_shard_host", side_effect=lambda network, host: host
    ):
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


@pytest.fixture
def k8s_secret_mock():
    return kubernetes.client.V1Secret(
        type="kubernetes.io/tls",
        metadata=kubernetes.client.V1ObjectMeta(name="gateway-tls"),
        data={"ca.crt": BASE64_OF_VALID_CA_CERT},
    )
