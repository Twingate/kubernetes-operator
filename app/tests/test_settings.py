import pytest
from pydantic import ValidationError

from app.settings import TwingateOperatorSettings


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


def test_remote_network_id_pass_if_base64_with_globalid_content():
    TwingateOperatorSettings(
        api_key="foo",
        network="foo",
        host="foo",
        remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
    )


def test_full_url():
    settings = TwingateOperatorSettings(
        api_key="foo",
        network="foo",
        host="foo",
        remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
    )
    assert settings.full_url
