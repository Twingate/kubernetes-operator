# noqa: F403,F403
from base64 import b64encode

import pytest
import responses
from pytest_factoryboy import register

from app.api import TwingateAPIClient
from app.settings import TwingateOperatorSettings

from .factories import ConnectorFactory, ResourceFactory

register(ConnectorFactory)
register(ResourceFactory)


@pytest.fixture()
def twingate_settings():
    return TwingateOperatorSettings(
        network="slug",
        host="test.com",
        api_key="test_key",
        remote_network_id=b64encode(b"RemoteNetwork:123").decode("utf-8"),
    )


@pytest.fixture()
def api_client(twingate_settings):
    return TwingateAPIClient(twingate_settings)


@pytest.fixture()
def test_url():
    return "https://slug.test.com/api/graphql/"
