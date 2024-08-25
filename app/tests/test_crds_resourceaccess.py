from unittest.mock import patch

import kubernetes.client
import pytest

from app.crds import TwingateResourceAccessCRD, TwingateResourceCRD


@pytest.fixture
def mock_get_namespaced_custom_object():
    with patch(
        "kubernetes.client.CustomObjectsApi.get_namespaced_custom_object"
    ) as mock:
        yield mock


@pytest.fixture
def sample_resource_object():
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


@pytest.fixture
def sample_resourceaccess_object():
    return {
        "apiVersion": "twingate.com/v1",
        "kind": "TwingateResourceAccess",
        "metadata": {
            "creationTimestamp": "2023-09-29T19:30:39Z",
            "finalizers": ["kopf.zalando.org/KopfFinalizerMarker"],
            "generation": 1,
            "managedFields": [
                {
                    "apiVersion": "twingate.com/v1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:metadata": {
                            "f:finalizers": {
                                ".": {},
                                'v:"kopf.zalando.org/KopfFinalizerMarker"': {},
                            }
                        }
                    },
                    "manager": "kopf",
                    "operation": "Update",
                    "time": "2023-09-29T19:30:39Z",
                },
                {
                    "apiVersion": "twingate.com/v1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:spec": {
                            ".": {},
                            "f:principalId": {},
                            "f:resourceRef": {".": {}, "f:name": {}, "f:namespace": {}},
                        }
                    },
                    "manager": "kubectl-create",
                    "operation": "Update",
                    "time": "2023-09-29T19:30:39Z",
                },
            ],
            "name": "foo-access-to-bar",
            "namespace": "default",
            "resourceVersion": "612168",
            "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        },
        "spec": {
            "principalId": "R3JvdXA6MTE1NzI2MA==",
            "resourceRef": {"name": "foo", "namespace": "default"},
        },
    }


def test_deserialization(sample_resourceaccess_object):
    crd = TwingateResourceAccessCRD(**sample_resourceaccess_object)
    assert crd.spec.principal_id == "R3JvdXA6MTE1NzI2MA=="
    assert crd.spec.resource_ref.name == "foo"
    assert crd.spec.resource_ref.namespace == "default"
    assert crd.metadata.name == "foo-access-to-bar"
    assert crd.metadata.uid == "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c"
    assert crd.spec.resource_ref_fullname == "default/foo"


def test_deserialization_with_principal_external_ref():
    data = {
        "apiVersion": "twingate.com/v1",
        "kind": "TwingateResourceAccess",
        "metadata": {
            "creationTimestamp": "2023-09-29T19:30:39Z",
            "finalizers": ["kopf.zalando.org/KopfFinalizerMarker"],
            "generation": 1,
            "managedFields": [
                {
                    "apiVersion": "twingate.com/v1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:metadata": {
                            "f:finalizers": {
                                ".": {},
                                'v:"kopf.zalando.org/KopfFinalizerMarker"': {},
                            }
                        }
                    },
                    "manager": "kopf",
                    "operation": "Update",
                    "time": "2023-09-29T19:30:39Z",
                },
                {
                    "apiVersion": "twingate.com/v1",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:spec": {
                            ".": {},
                            "f:principalId": {},
                            "f:resourceRef": {".": {}, "f:name": {}, "f:namespace": {}},
                        }
                    },
                    "manager": "kubectl-create",
                    "operation": "Update",
                    "time": "2023-09-29T19:30:39Z",
                },
            ],
            "name": "foo-access-to-bar",
            "namespace": "default",
            "resourceVersion": "612168",
            "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        },
        "spec": {
            "principalExternalRef": {"type": "group", "name": "My Group"},
            "resourceRef": {"name": "foo", "namespace": "default"},
        },
    }
    crd = TwingateResourceAccessCRD(**data)
    assert crd.spec.principal_external_ref.type == "group"
    assert crd.spec.principal_external_ref.name == "My Group"
    assert crd.spec.resource_ref.name == "foo"
    assert crd.spec.resource_ref.namespace == "default"
    assert crd.metadata.name == "foo-access-to-bar"
    assert crd.metadata.uid == "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c"
    assert crd.spec.resource_ref_fullname == "default/foo"


def test_spec_get_resource_ref_object(
    mock_get_namespaced_custom_object, sample_resourceaccess_object
):
    mock_get_namespaced_custom_object.return_value = sample_resourceaccess_object
    crd = TwingateResourceAccessCRD(**sample_resourceaccess_object)
    response = crd.spec.get_resource_ref_object()
    assert response == sample_resourceaccess_object


def test_spec_get_resource_ref_object_handles_404(
    mock_get_namespaced_custom_object, sample_resourceaccess_object
):
    mock_get_namespaced_custom_object.side_effect = (
        kubernetes.client.exceptions.ApiException(status=404)
    )
    crd = TwingateResourceAccessCRD(**sample_resourceaccess_object)
    assert crd.spec.get_resource_ref_object() is None


def test_spec_get_resource_ref_object_handles_other_errors(
    mock_get_namespaced_custom_object, sample_resourceaccess_object
):
    mock_get_namespaced_custom_object.side_effect = (
        kubernetes.client.exceptions.ApiException(status=500)
    )
    crd = TwingateResourceAccessCRD(**sample_resourceaccess_object)
    assert crd.spec.get_resource_ref_object() is None


def test_spec_get_resource(
    mock_get_namespaced_custom_object,
    sample_resourceaccess_object,
    sample_resource_object,
):
    mock_get_namespaced_custom_object.return_value = sample_resource_object
    crd = TwingateResourceAccessCRD(**sample_resourceaccess_object)
    response = crd.spec.get_resource()
    assert isinstance(response, TwingateResourceCRD), f"response is {response}"
    assert response.spec.id == "UmVzb3VyY2U6OTM3Mzkw"
    assert response.spec.address == "my.default.cluster.local"
    assert response.spec.name == "My K8S Resource"
    assert response.metadata.name == "foo"
    assert response.metadata.uid == "c560d138-a93a-4463-8b44-d7717851a265"


def test_spec_get_resource_failure_returns_none(
    mock_get_namespaced_custom_object, sample_resourceaccess_object
):
    mock_get_namespaced_custom_object.side_effect = (
        kubernetes.client.exceptions.ApiException()
    )
    crd = TwingateResourceAccessCRD(**sample_resourceaccess_object)
    response = crd.spec.get_resource()
    assert response is None
