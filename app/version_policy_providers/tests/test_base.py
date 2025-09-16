import pytest

from app.version_policy_providers import (
    DockerhubVersionPolicyProvider,
    GoogleVersionPolicyProvider,
    get_provider,
)


@pytest.mark.parametrize(
    ("value", "repo", "expected"),
    [
        ("dockerhub", "twingate/test", DockerhubVersionPolicyProvider),
        (
            "google",
            "us-docker.pkg.dev/proj/d/connector",
            GoogleVersionPolicyProvider,
        ),
    ],
)
def test_get_provider_valid_value(value, repo, expected):
    provider = get_provider(value, repo)
    assert isinstance(provider, expected)


def test_get_provider_with_invalid_value_raises():
    with pytest.raises(ValueError, match=r"Invalid provider_name"):
        get_provider("invalid")
