from unittest.mock import patch

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
