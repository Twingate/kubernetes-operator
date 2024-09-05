import pytest

from app.crds import TwingateGroupCRD


@pytest.fixture
def sample_group_object():
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateConnector",
        "metadata": {
            "name": "my-group",
            "namespace": "default",
            "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        },
        "spec": {
            "name": "My Group",
        },
    }


def test_group_deserialization(sample_group_object):
    group = TwingateGroupCRD(**sample_group_object)

    assert group.metadata.name == "my-group"
    assert group.spec.name == "My Group"
