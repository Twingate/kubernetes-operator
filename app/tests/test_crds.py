from app.crds import K8sMetadata


def test_k8smetadata_owner_reference_object():
    meta = K8sMetadata(uid="uuid", name="foo", namespace="default")
    assert meta.owner_reference_object == {
        "apiVersion": "twingate.com/v1",
        "kind": "TwingateResource",
        "name": "foo",
        "uid": "uuid",
    }
