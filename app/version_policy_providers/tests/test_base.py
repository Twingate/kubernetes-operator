import pytest

from app.version_policy_providers import get_provider


def test_get_provider_with_invalid_value_raises():
    with pytest.raises(ValueError, match="Invalid provider_name"):
        get_provider("invalid")
