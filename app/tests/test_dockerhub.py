import os
import pathlib
from unittest.mock import patch

import pytest
from semantic_version import Version

from app.dockerhub import (
    _DOCKER_HUB_TAGS_API_URL,
    get_all_operator_semver_tags,
    get_all_operator_semver_tags_by_specifier,
    get_all_operator_tags,
    get_latest,
)

VERSIONS_LIST = [
    "latest",
    "dev",
    "1.1.2-dev.6722290577",
    "1.1.2",
    "1.1",
    "0.1.2-dev.6722290577",
    "0.1.2",
    "0.1",
    "0",
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


@pytest.fixture(scope="session")
def dockerhub_image_tags_sample_response():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = pathlib.Path(dir_path, "./test_data/dockerhub_tags_response.json")
    with open(file) as f:
        data = f.read()
    return data


def test_get_all_operator_tags(
    mocked_responses, snapshot, dockerhub_image_tags_sample_response
):
    mocked_responses.get(
        _DOCKER_HUB_TAGS_API_URL, status=200, body=dockerhub_image_tags_sample_response
    )
    actual = list(get_all_operator_tags())
    assert actual == snapshot


def test_get_operator_semver_tags(snapshot):
    with patch("app.dockerhub.get_all_operator_tags", return_value=VERSIONS_LIST):
        actual = list(get_all_operator_semver_tags())
        assert actual == snapshot


def test_get_operator_semver_tags_prerelease(snapshot):
    with patch("app.dockerhub.get_all_operator_tags", return_value=VERSIONS_LIST):
        actual = list(get_all_operator_semver_tags(allow_prerelease=True))
        assert actual == snapshot


def test_get_all_operator_semver_tags_by_specifier(snapshot):
    with patch("app.dockerhub.get_all_operator_tags", return_value=VERSIONS_LIST):
        actual = list(get_all_operator_semver_tags_by_specifier("0.1.x"))
        assert actual == snapshot


def test_get_latest():
    with patch("app.dockerhub.get_all_operator_tags", return_value=VERSIONS_LIST):
        actual = get_latest("0.1.x")
        assert actual == Version("0.1.2")

        actual = get_latest("^1.0.0")
        assert actual == Version("1.1.2")
