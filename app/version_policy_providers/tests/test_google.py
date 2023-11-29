import pytest

from app.version_policy_providers import GoogleVersionPolicyProvider


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
