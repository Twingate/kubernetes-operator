import os
import pathlib

import pytest

from app.version_policy_providers.dockerhub import DockerhubVersionPolicyProvider


@pytest.fixture()
def dockerhub_connector_provider(mocked_responses):
    provider = DockerhubVersionPolicyProvider()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = pathlib.Path(dir_path, "../test_data/dockerhub_connector_tags_response.json")
    with open(file) as f:
        data = f.read()

    mocked_responses.get(provider.tags_api_url, status=200, body=data)

    return provider


@pytest.fixture()
def dockerhub_operator_provider(mocked_responses):
    provider = DockerhubVersionPolicyProvider()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = pathlib.Path(dir_path, "../test_data/dockerhub_operator_tags_response.json")
    with open(file) as f:
        data = f.read()

    mocked_responses.get(provider.tags_api_url, status=200, body=data)

    return provider


def test_get_all_semver_tags(dockerhub_operator_provider):
    all_semver_tags = [
        str(x) for x in dockerhub_operator_provider.get_all_semver_tags()
    ]
    assert all_semver_tags == ["0.1.2", "0.1.1", "0.1.0"]


def test_get_all_semver_tags_with_prereleases(dockerhub_operator_provider):
    all_semver_tags = [
        str(x)
        for x in dockerhub_operator_provider.get_all_semver_tags(allow_prerelease=True)
    ]
    assert all_semver_tags == [
        "0.1.3-dev.6817865879",
        "0.1.2-dev.6815191123",
        "0.1.2-dev.6804070815",
        "0.1.2-dev.6735993470",
        "0.1.2-dev.6722290577",
        "0.1.2",
        "0.1.2-dev.6716132391",
        "0.1.2-dev.6716010709",
        "0.1.1-dev.6702190178",
        "0.1.1",
        "0.1.1-dev.6702103173",
        "0.1.0-dev.6698032918",
        "0.1.0",
        "0.1.0-dev.6697571821",
        "0.1.0-dev.6697098399",
        "0.1.0-dev.6697032623",
        "0.1.0-dev.6686861896",
        "0.1.0-dev.6683812832",
        "0.1.0-dev.6672988848",
    ]


def test_get_latest_with_valid_specifier_returns_latest(dockerhub_connector_provider):
    actual = dockerhub_connector_provider.get_latest("<1.60.0")
    assert str(actual) == "1.59.0"

    actual = dockerhub_connector_provider.get_latest("1.x.0")
    assert str(actual) == "1.60.0"


def test_get_latest_with_invalid_specifier_returns_none():
    assert DockerhubVersionPolicyProvider().get_latest("latest") is None


def test_get_latest_with_prerelease_returns_latest(dockerhub_operator_provider):
    actual = dockerhub_operator_provider.get_latest("<0.1.1", allow_prerelease=True)
    assert str(actual) == "0.1.1-dev.6702190178"

    actual = dockerhub_operator_provider.get_latest("<0.1.3", allow_prerelease=True)
    assert str(actual) == "0.1.3-dev.6817865879"
