from collections import namedtuple
from unittest.mock import MagicMock, patch

import pytest

from app.version_policy_providers import GoogleVersionPolicyProvider


@pytest.fixture(autouse=True, scope="module")
def _mock_google_auth():
    with patch("google.auth.default", return_value=(MagicMock(), "proj")):
        yield


def test_init_valid_repository():
    provider = GoogleVersionPolicyProvider(
        repository="us-docker.pkg.dev/proj/d/connector"
    )
    assert provider.location == "us"
    assert provider.project_id == "proj"
    assert provider.repo == "d"
    assert provider.image == "connector"
    assert (
        provider.parent_name
        == "projects/proj/locations/us/repositories/d/packages/connector"
    )


def test_init_invalid_repository():
    with pytest.raises(ValueError, match="Invalid image name: invalid"):
        GoogleVersionPolicyProvider(repository="invalid")


def test_init_none_repository():
    with pytest.raises(ValueError, match="Must specify 'repository'"):
        GoogleVersionPolicyProvider(repository=None)


def test_get_all_tags():
    Tag = namedtuple("Tag", ["name"])
    tag_mocks = [
        Tag(
            name=f"projects/proj/locations/us/repositories/d/packages/connector/tags/0.{i}.0"
        )
        for i in range(1, 6)
    ]
    list_tags_result = MagicMock(
        pages=[MagicMock(tags=tag_mocks[0:3]), MagicMock(tags=tag_mocks[3:])]
    )

    expected_tags = [f"0.{i}.0" for i in range(1, 6)]

    with patch(
        "app.version_policy_providers.google.artifactregistry_v1.ArtifactRegistryClient.list_tags",
        return_value=list_tags_result,
    ):
        provider = GoogleVersionPolicyProvider(
            repository="us-docker.pkg.dev/proj/d/connector"
        )
        assert list(provider.get_all_tags()) == expected_tags
