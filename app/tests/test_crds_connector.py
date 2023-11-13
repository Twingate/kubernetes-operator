from unittest.mock import patch

import pendulum
import pytest

from app.crds import TwingateConnectorCRD


@pytest.fixture()
def sample_connector_object():
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateConnector",
        "metadata": {
            "name": "my-connector",
            "namespace": "default",
            "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        },
        "spec": {
            "name": "My K8S Connector",
            "versionPolicy": {"schedule": "0 2 * * *", "version": "0.1.x"},
            "containerExtra": {
                "resources": {
                    "requests": {"cpu": "100m", "memory": "128Mi"},
                    "limits": {"cpu": "100m", "memory": "128Mi"},
                }
            },
        },
    }


def test_deserialization(sample_connector_object):
    crd = TwingateConnectorCRD(**sample_connector_object)
    assert crd.spec.name == "My K8S Connector"
    assert crd.spec.version_policy.schedule == "0 2 * * *"
    assert crd.spec.version_policy.version == "0.1.x"
    assert crd.spec.container_extra == {
        "resources": {
            "limits": {"cpu": "100m", "memory": "128Mi"},
            "requests": {"cpu": "100m", "memory": "128Mi"},
        }
    }


def test_deserialization_fails_on_invalid_version_specifier(sample_connector_object):
    sample_connector_object["spec"] = {
        "name": "My K8S Connector",
        "versionPolicy": {"schedule": "0 2 * * *", "version": "invalid"},
        "containerExtra": {
            "resources": {
                "requests": {"cpu": "100m", "memory": "128Mi"},
                "limits": {"cpu": "100m", "memory": "128Mi"},
            }
        },
    }
    with pytest.raises(ValueError, match="Invalid version specifier"):
        TwingateConnectorCRD(**sample_connector_object)


def test_deserialization_fails_on_invalid_cron(sample_connector_object):
    sample_connector_object["spec"] = {
        "name": "My K8S Connector",
        "versionPolicy": {"schedule": "100 2 * * *", "version": "^1.0.0"},
        "containerExtra": {
            "resources": {
                "requests": {"cpu": "100m", "memory": "128Mi"},
                "limits": {"cpu": "100m", "memory": "128Mi"},
            }
        },
    }

    with pytest.raises(ValueError, match="Invalid schedule value"):
        TwingateConnectorCRD(**sample_connector_object)


def test_version_policy_get_next_date_iso8601_returns_none_if_no_schedule(
    sample_connector_object,
):
    sample_connector_object["spec"] = {
        "version_policy": {"schedule": None, "version": "^1.0.0"}
    }
    crd = TwingateConnectorCRD(**sample_connector_object)
    assert crd.spec.version_policy.get_next_date_iso8601() is None


def test_version_policy_get_next_date_iso8601_returns_right_date(
    sample_connector_object, freezer
):
    sample_connector_object["spec"] = {
        "version_policy": {"schedule": "* * * * *", "version": "^1.0.0"}
    }
    crd = TwingateConnectorCRD(**sample_connector_object)

    with freezer.freeze_time():
        now = pendulum.now("UTC").start_of("minute")
        expected = now.add(minutes=1)
        result = crd.spec.version_policy.get_next_date_iso8601()
        assert result == expected.to_iso8601_string()

    sample_connector_object["spec"] = {
        "version_policy": {"schedule": "0 0 * * 1", "version": "^1.0.0"}
    }
    crd = TwingateConnectorCRD(**sample_connector_object)
    with freezer.freeze_time():
        now = pendulum.now("utc").start_of("day")
        expected = now.next(pendulum.MONDAY).start_of("day")
        result = crd.spec.version_policy.get_next_date_iso8601()
        assert result == expected.to_iso8601_string()


def test_spec_get_image_tag_by_policy(sample_connector_object):
    sample_connector_object["spec"] = {"version_policy": {"version": "^1.0.0"}}
    crd = TwingateConnectorCRD(**sample_connector_object)

    with patch(
        "app.version_policy_providers.DockerhubVersionPolicyProvider.get_all_tags",
        return_value=["1.0.0", "1.0.1", "2.0.0"],
    ):
        assert str(crd.spec.get_image_tag_by_policy()) == "1.0.1"


def test_spec_get_image_tag_by_policy_raises_if_no_match(sample_connector_object):
    sample_connector_object["spec"] = {"version_policy": {"version": "^10.0.0"}}
    crd = TwingateConnectorCRD(**sample_connector_object)

    with patch(
        "app.version_policy_providers.DockerhubVersionPolicyProvider.get_all_tags",
        return_value=["1.0.0", "latest"],
    ), pytest.raises(ValueError, match="Could not find valid tag for"):
        crd.spec.get_image_tag_by_policy()
