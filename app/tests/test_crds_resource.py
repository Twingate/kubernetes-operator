import pytest

from app.crds import TwingateResourceCRD


@pytest.fixture()
def sample_resource_yaml():
    return {
        "apiVersion": "twingate.com/v1",
        "kind": "TwingateResource",
        "metadata": {
            "annotations": {
                "kopf.zalando.org/last-handled-configuration": '{"spec":{"address":"my.default.cluster.local","id":"UmVzb3VyY2U6OTM3Mzkw","name":"My K8S Resource"}}\n'
            },
            "creationTimestamp": "2023-09-29T16:44:14Z",
            "finalizers": ["kopf.zalando.org/KopfFinalizerMarker"],
            "generation": 3,
            "managedFields": [
                {
                    "apiVersion": "twingate.com/v1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:metadata": {
                            "f:annotations": {
                                ".": {},
                                "f:kopf.zalando.org/last-handled-configuration": {},
                            },
                            "f:finalizers": {
                                ".": {},
                                'v:"kopf.zalando.org/KopfFinalizerMarker"': {},
                            },
                        },
                        "f:spec": {"f:id": {}},
                        "f:status": {
                            ".": {},
                            "f:twingate_resource_create": {
                                ".": {},
                                "f:created_at": {},
                                "f:twingate_id": {},
                                "f:updated_at": {},
                            },
                            "f:twingate_resource_update": {
                                ".": {},
                                "f:created_at": {},
                                "f:twingate_id": {},
                                "f:updated_at": {},
                            },
                        },
                    },
                    "manager": "kopf",
                    "operation": "Update",
                    "time": "2023-09-29T16:44:14Z",
                },
                {
                    "apiVersion": "twingate.com/v1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {"f:spec": {".": {}, "f:address": {}, "f:name": {}}},
                    "manager": "kubectl-create",
                    "operation": "Update",
                    "time": "2023-09-29T16:44:14Z",
                },
            ],
            "name": "foo",
            "namespace": "default",
            "resourceVersion": "603560",
            "uid": "c560d138-a93a-4463-8b44-d7717851a265",
        },
        "spec": {
            "address": "my.default.cluster.local",
            "id": "UmVzb3VyY2U6OTM3Mzkw",
            "name": "My K8S Resource",
            "protocols": {
                "tcp": {"policy": "RESTRICTED", "ports": [{"start": 80, "end": 80}]}
            },
        },
        "status": {
            "twingate_resource_create": {
                "created_at": "2023-09-29T16:44:14.480198+00:00",
                "twingate_id": "UmVzb3VyY2U6OTM3Mzkw",
                "updated_at": "2023-09-29T16:44:14.480222+00:00",
            },
            "twingate_resource_update": {
                "created_at": "2023-09-29T16:44:14.480198+00:00",
                "twingate_id": "UmVzb3VyY2U6OTM3Mzkw",
                "updated_at": "2023-09-29T16:44:14.793943+00:00",
            },
        },
    }


def test_deserialization(sample_resource_yaml):
    crd = TwingateResourceCRD(**sample_resource_yaml)
    assert crd.spec.id == "UmVzb3VyY2U6OTM3Mzkw"
    assert crd.spec.address == "my.default.cluster.local"
    assert crd.spec.name == "My K8S Resource"
    assert crd.metadata.name == "foo"
    assert crd.metadata.uid == "c560d138-a93a-4463-8b44-d7717851a265"


def test_is_browser_shortcut_enabled_disallowed_on_wildcard_resource():
    with pytest.raises(ValueError, match="isBrowserShortcutEnabled"):
        TwingateResourceCRD(
            apiVersion="twingate.com/v1",
            kind="TwingateResource",
            spec={
                "address": "my*.default.cluster.local",
                "id": "UmVzb3VyY2U6OTM3Mzkw",
                "name": "My K8S Resource",
                "isBrowserShortcutEnabled": True,
            },
        )


def test_resourceprotocols_validation():
    with pytest.raises(ValueError, match="ports can't be set"):
        TwingateResourceCRD(
            apiVersion="twingate.com/v1",
            kind="TwingateResource",
            spec={
                "address": "my.default.cluster.local",
                "id": "UmVzb3VyY2U6OTM3Mzkw",
                "name": "My K8S Resource",
                "protocols": {
                    "tcp": {"policy": "ALLOW_ALL", "ports": [{"start": 80, "end": 80}]}
                },
            },
        )

    with pytest.raises(ValueError, match="ports must be set"):
        TwingateResourceCRD(
            apiVersion="twingate.com/v1",
            kind="TwingateResource",
            spec={
                "address": "my.default.cluster.local",
                "id": "UmVzb3VyY2U6OTM3Mzkw",
                "name": "My K8S Resource",
                "protocols": {"tcp": {"policy": "RESTRICTED"}},
            },
        )


def test_resourceprotocol_ports_validation():
    with pytest.raises(ValueError, match="Input should be less than or equal to 65535"):
        TwingateResourceCRD(
            apiVersion="twingate.com/v1",
            kind="TwingateResource",
            spec={
                "address": "my.default.cluster.local",
                "id": "UmVzb3VyY2U6OTM3Mzkw",
                "name": "My K8S Resource",
                "protocols": {
                    "tcp": {
                        "policy": "RESTRICTED",
                        "ports": [{"start": 1_000_000, "end": 80}],
                    }
                },
            },
        )

    with pytest.raises(ValueError, match="Input should be greater than or equal to 0"):
        TwingateResourceCRD(
            apiVersion="twingate.com/v1",
            kind="TwingateResource",
            spec={
                "address": "my.default.cluster.local",
                "id": "UmVzb3VyY2U6OTM3Mzkw",
                "name": "My K8S Resource",
                "protocols": {
                    "tcp": {"policy": "RESTRICTED", "ports": [{"start": -1, "end": 80}]}
                },
            },
        )

    with pytest.raises(
        ValueError, match="Start port value must be less or equal to end port value"
    ):
        TwingateResourceCRD(
            apiVersion="twingate.com/v1",
            kind="TwingateResource",
            spec={
                "address": "my.default.cluster.local",
                "id": "UmVzb3VyY2U6OTM3Mzkw",
                "name": "My K8S Resource",
                "protocols": {
                    "tcp": {
                        "policy": "RESTRICTED",
                        "ports": [{"start": 8080, "end": 7080}],
                    }
                },
            },
        )
