from unittest.mock import patch

import pendulum
import pytest

from app.crds import TwingateConnectorCRD


@pytest.fixture()
def sample_connector_object_image():
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
            "image": {"repository": "twingate/connector", "tag": "1.60.0"},
            "containerExtra": {
                "resources": {
                    "requests": {"cpu": "100m", "memory": "128Mi"},
                    "limits": {"cpu": "100m", "memory": "128Mi"},
                }
            },
        },
    }


@pytest.fixture()
def sample_connector_object_imagepolicy():
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
            "imagePolicy": {
                "provider": "dockerhub",
                "schedule": "0 2 * * *",
                "version": "0.1.x",
            },
            "containerExtra": {
                "resources": {
                    "requests": {"cpu": "100m", "memory": "128Mi"},
                    "limits": {"cpu": "100m", "memory": "128Mi"},
                }
            },
        },
    }


def test_deserialization_image(sample_connector_object_image):
    crd = TwingateConnectorCRD(**sample_connector_object_image)
    assert crd.spec.name == "My K8S Connector"
    assert crd.spec.image_policy is None
    assert crd.spec.image.repository == "twingate/connector"
    assert crd.spec.image.tag == "1.60.0"
    assert crd.spec.container_extra == {
        "resources": {
            "limits": {"cpu": "100m", "memory": "128Mi"},
            "requests": {"cpu": "100m", "memory": "128Mi"},
        }
    }


def test_deserialization_imagepolicy(sample_connector_object_imagepolicy):
    crd = TwingateConnectorCRD(**sample_connector_object_imagepolicy)
    assert crd.spec.name == "My K8S Connector"
    assert crd.spec.image is None
    assert crd.spec.image_policy.provider == "dockerhub"
    assert crd.spec.image_policy.schedule == "0 2 * * *"
    assert crd.spec.image_policy.version == "0.1.x"
    assert crd.spec.container_extra == {
        "resources": {
            "limits": {"cpu": "100m", "memory": "128Mi"},
            "requests": {"cpu": "100m", "memory": "128Mi"},
        }
    }


def test_deserialization_imagepolicy_fails_on_invalid_version_specifier(
    sample_connector_object_imagepolicy,
):
    sample_connector_object_imagepolicy["spec"]["imagePolicy"]["version"] = "invalid"
    with pytest.raises(ValueError, match="Invalid version specifier"):
        TwingateConnectorCRD(**sample_connector_object_imagepolicy)


def test_deserialization_fails_on_invalid_schedule(sample_connector_object_imagepolicy):
    sample_connector_object_imagepolicy["spec"]["imagePolicy"]["schedule"] = (
        "100 2 * * *"
    )
    with pytest.raises(ValueError, match="Invalid schedule value"):
        TwingateConnectorCRD(**sample_connector_object_imagepolicy)


def test_version_policy_get_next_date_iso8601_returns_right_date(
    sample_connector_object_imagepolicy, freezer
):
    sample_connector_object_imagepolicy["spec"]["imagePolicy"]["schedule"] = "* * * * *"
    crd = TwingateConnectorCRD(**sample_connector_object_imagepolicy)

    now = pendulum.now("UTC").start_of("minute")
    expected = now.add(minutes=1)
    result = crd.spec.image_policy.get_next_date_iso8601()
    assert result == expected.to_iso8601_string()

    sample_connector_object_imagepolicy["spec"]["imagePolicy"]["schedule"] = "0 0 * * 1"
    crd = TwingateConnectorCRD(**sample_connector_object_imagepolicy)

    now = pendulum.now("utc").start_of("day")
    expected = now.next(pendulum.MONDAY).start_of("day")
    result = crd.spec.image_policy.get_next_date_iso8601()
    assert result == expected.to_iso8601_string()


def test_spec_get_image_with_imagepolicy(sample_connector_object_imagepolicy):
    sample_connector_object_imagepolicy["spec"]["imagePolicy"]["version"] = "^1.0.0"
    crd = TwingateConnectorCRD(**sample_connector_object_imagepolicy)

    with patch(
        "app.version_policy_providers.DockerhubVersionPolicyProvider.get_all_tags",
        return_value=["1.0.0", "1.0.1", "2.0.0"],
    ):
        assert crd.spec.get_image() == "twingate/connector:1.0.1"


def test_spec_get_image_w_imagepolicy_raises_if_no_match(
    sample_connector_object_imagepolicy,
):
    sample_connector_object_imagepolicy["spec"]["imagePolicy"]["version"] = "^10.0.0"
    crd = TwingateConnectorCRD(**sample_connector_object_imagepolicy)

    with patch(
        "app.version_policy_providers.DockerhubVersionPolicyProvider.get_all_tags",
        return_value=["1.0.0", "latest"],
    ), pytest.raises(ValueError, match="Could not find valid tag for"):
        crd.spec.get_image()


def test_spec_get_image_with_image(sample_connector_object_image):
    crd = TwingateConnectorCRD(**sample_connector_object_image)
    assert crd.spec.get_image() == "twingate/connector:1.60.0"
