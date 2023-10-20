from unittest.mock import patch

import kubernetes.client
import pytest

from app.crds import K8sMetadata, TwingateResourceAccessCRD, TwingateResourceCRD


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


class TestTwingateResourceCRD:
    SAMPLE_YAML = {
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

    def test_deserialization(self):
        crd = TwingateResourceCRD(**self.SAMPLE_YAML)
        assert crd.spec.id == "UmVzb3VyY2U6OTM3Mzkw"
        assert crd.spec.address == "my.default.cluster.local"
        assert crd.spec.name == "My K8S Resource"
        assert crd.metadata.name == "foo"
        assert crd.metadata.uid == "c560d138-a93a-4463-8b44-d7717851a265"


class TestTwingateResourceAccessCRD:
    SAMPLE_YAML = {
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

    def test_deserialization(self):
        crd = TwingateResourceAccessCRD(**self.SAMPLE_YAML)
        assert crd.spec.principal_id == "R3JvdXA6MTE1NzI2MA=="
        assert crd.spec.resource_ref.name == "foo"
        assert crd.spec.resource_ref.namespace == "default"
        assert crd.metadata.name == "foo-access-to-bar"
        assert crd.metadata.uid == "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c"
        assert crd.spec.resource_ref_fullname == "default/foo"

    def test_spec_get_resource_ref_object(self, mock_get_namespaced_custom_object):
        mock_get_namespaced_custom_object.return_value = (
            TestTwingateResourceCRD.SAMPLE_YAML
        )
        crd = TwingateResourceAccessCRD(**self.SAMPLE_YAML)
        response = crd.spec.get_resource_ref_object()
        assert response == TestTwingateResourceCRD.SAMPLE_YAML

    def test_spec_get_resource_ref_object_handles_404(
        self, mock_get_namespaced_custom_object
    ):
        mock_get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        crd = TwingateResourceAccessCRD(**self.SAMPLE_YAML)
        assert crd.spec.get_resource_ref_object() is None

    def test_spec_get_resource_ref_object_handles_other_errors(
        self, mock_get_namespaced_custom_object
    ):
        mock_get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )
        crd = TwingateResourceAccessCRD(**self.SAMPLE_YAML)
        assert crd.spec.get_resource_ref_object() is None

    def test_spec_get_resource(self, mock_get_namespaced_custom_object):
        mock_get_namespaced_custom_object.return_value = (
            TestTwingateResourceCRD.SAMPLE_YAML
        )
        crd = TwingateResourceAccessCRD(**self.SAMPLE_YAML)
        response = crd.spec.get_resource()
        assert isinstance(response, TwingateResourceCRD), f"response is {response}"
        assert response.spec.id == "UmVzb3VyY2U6OTM3Mzkw"
        assert response.spec.address == "my.default.cluster.local"
        assert response.spec.name == "My K8S Resource"
        assert response.metadata.name == "foo"
        assert response.metadata.uid == "c560d138-a93a-4463-8b44-d7717851a265"

    def test_spec_get_resource_failure_returns_none(
        self, mock_get_namespaced_custom_object
    ):
        mock_get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException()
        )
        crd = TwingateResourceAccessCRD(**self.SAMPLE_YAML)
        response = crd.spec.get_resource()
        assert response is None
