from unittest.mock import patch

import pytest

from app.crds import K8sMetadata


@pytest.fixture()
def mock_get_namespaced_custom_object():
    with patch(
        "kubernetes.client.CustomObjectsApi.get_namespaced_custom_object"
    ) as mock:
        yield mock


def test_k8smetadata_owner_reference_object():
    meta = K8sMetadata(uid="uuid", name="foo", namespace="default")
    assert meta.owner_reference_object == {
        "apiVersion": "twingate.com/v1",
        "kind": "TwingateResource",
        "name": "foo",
        "uid": "uuid",
    }
