from unittest.mock import MagicMock, patch

import pytest
import responses
from pydantic import ValidationError
from requests.exceptions import ConnectionError as RequestsConnectionError
from tenacity import wait_none

from app.settings import TwingateOperatorSettings, _resolve_shard_host, get_host


@pytest.fixture(autouse=True)
def _disable_retry_wait():
    original_wait = _resolve_shard_host.retry.wait
    _resolve_shard_host.retry.wait = wait_none()
    yield
    _resolve_shard_host.retry.wait = original_wait


@pytest.fixture
def mock_get_remote_network_by_name():
    with patch("app.api.TwingateAPIClient.get_remote_network_by_name") as m:
        yield m


def test_remote_network_id_fails_if_invalid_base64():
    with pytest.raises(ValidationError) as e:
        TwingateOperatorSettings(
            api_key="foo", network="foo", host="foo", remote_network_id="foo"
        )

    errors = e.value.errors()
    assert len(errors) == 1

    assert errors[0]["loc"] == ("remote_network_id",)
    assert errors[0]["msg"] == "Value error, Invalid global id"
    assert errors[0]["type"] == "value_error"


def test_remote_network_id_fails_if_invalid_globalid():
    with pytest.raises(ValidationError) as e:
        TwingateOperatorSettings(
            api_key="foo",
            network="foo",
            host="foo",
            remote_network_id="ZXJhbiBrYW1wZiBpcyBhd2Vzb21lCg==",
        )

    errors = e.value.errors()
    assert len(errors) == 1

    assert errors[0]["loc"] == ("remote_network_id",)
    assert errors[0]["msg"] == "Value error, Invalid global id"
    assert errors[0]["type"] == "value_error"


def test_remote_network_name_gets_network_id(mock_get_remote_network_by_name):
    mock_get_remote_network_by_name.return_value = MagicMock(id="bar", name="test")
    settings = TwingateOperatorSettings(
        api_key="foo", network="foo", host="foo", remote_network_name="foo"
    )

    assert settings.remote_network_id == "bar"


def test_remote_network_id_pass_if_base64_with_globalid_content():
    TwingateOperatorSettings(
        api_key="foo",
        network="foo",
        host="foo",
        remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
    )


def test_full_url():
    with patch("app.settings.get_host", return_value="testhost.com"):
        settings = TwingateOperatorSettings(
            api_key="foo",
            network="foo",
            host="testhost.com",
            remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
        )

    assert settings.full_url == "https://foo.testhost.com"


def test_get_host_extracts_host_from_308_redirect(mocked_responses):
    mocked_responses.add(
        responses.HEAD,
        "https://mynetwork.twingate.com/api/graphql/",
        status=308,
        headers={"location": "https://mynetwork.us1.twingate.com/api/graphql/"},
    )

    result = get_host("mynetwork", "twingate.com")

    assert result == "us1.twingate.com"


def test_get_host_retains_host_when_no_redirect(mocked_responses):
    mocked_responses.add(
        responses.HEAD,
        "https://mynetwork.twingate.com/api/graphql/",
        status=200,
    )

    result = get_host("mynetwork", "twingate.com")

    assert result == "twingate.com"


@pytest.mark.parametrize(
    "headers",
    [
        pytest.param({}, id="empty_headers"),
        pytest.param({"location": ""}, id="empty_location"),
        pytest.param({"location": "not-a-url"}, id="bad_location"),
        pytest.param({"location": "https://mynetwork"}, id="missing_host_suffix"),
        pytest.param(
            {"location": "https://mynetwork.evil.com/api/graphql/"}, id="different_host"
        ),
        pytest.param(
            {"location": "https://us1.twingate.com/api/graphql/"},
            id="missing_network_prefix",
        ),
        pytest.param(
            {"location": "https://othernetwork.us1.twingate.com/api/graphql/"},
            id="different_network",
        ),
    ],
)
def test_get_host_fallback_to_default(mocked_responses, headers):
    mocked_responses.add(
        responses.HEAD,
        "https://mynetwork.twingate.com/api/graphql/",
        status=308,
        headers=headers,
    )

    result = get_host("mynetwork", "twingate.com")

    assert result == "twingate.com"


def test_get_host_retries_then_succeeds(mocked_responses):
    mocked_responses.assert_all_requests_are_fired = True
    mocked_responses.add(
        responses.HEAD,
        "https://mynetwork.twingate.com/api/graphql/",
        body=RequestsConnectionError("connection failed"),
    )
    mocked_responses.add(
        responses.HEAD,
        "https://mynetwork.twingate.com/api/graphql/",
        status=308,
        headers={"location": "https://mynetwork.us1.twingate.com/api/graphql/"},
    )

    result = get_host("mynetwork", "twingate.com")

    assert result == "us1.twingate.com"
    assert len(mocked_responses.calls) == 2


def test_get_host_fallback_to_default_when_retries_exhausted(mocked_responses):
    mocked_responses.add(
        responses.HEAD,
        "https://mynetwork.twingate.com/api/graphql/",
        body=RequestsConnectionError("connection failed"),
    )

    result = get_host("mynetwork", "twingate.com")

    assert result == "twingate.com"
    assert len(mocked_responses.calls) == 5


def test_settings_init_get_sharded_host_before_remote_network_lookup(
    mock_get_remote_network_by_name,
):
    call_order = []

    def get_sharded_host(_network, _host):
        call_order.append("get_sharded_host")
        return "us1.twingate.com"

    def get_remote_network_by_name(_name):
        call_order.append("get_remote_network_by_name")
        return MagicMock(id="bar", name="test")

    mock_get_remote_network_by_name.side_effect = get_remote_network_by_name
    with patch("app.settings.get_host", side_effect=get_sharded_host):
        settings = TwingateOperatorSettings(
            api_key="foo",
            network="foo",
            host="twingate.com",
            remote_network_name="test",
        )

    assert settings.full_url == "https://foo.us1.twingate.com"
    assert settings.remote_network_id == "bar"
    assert call_order == ["get_sharded_host", "get_remote_network_by_name"]
