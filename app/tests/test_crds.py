from unittest.mock import patch

import kubernetes.client
import pendulum
import pytest
from freezegun import freeze_time

from app.crds import (
    K8sMetadata,
    TwingateConnectorCRD,
    TwingateResourceAccessCRD,
    TwingateResourceCRD,
)


@pytest.fixture()
def mock_get_namespaced_custom_object():
    with patch(
        "kubernetes.client.CustomObjectsApi.get_namespaced_custom_object"
    ) as mock:
        yield mock


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

    def test_deserialization(self):
        crd = TwingateResourceCRD(**self.SAMPLE_YAML)
        assert crd.spec.id == "UmVzb3VyY2U6OTM3Mzkw"
        assert crd.spec.address == "my.default.cluster.local"
        assert crd.spec.name == "My K8S Resource"
        assert crd.metadata.name == "foo"
        assert crd.metadata.uid == "c560d138-a93a-4463-8b44-d7717851a265"

    def test_is_browser_shortcut_enabled_disallowed_on_wildcard_resource(self):
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

    def test_resourceprotocols_validation(self):
        with pytest.raises(ValueError, match="ports can't be set"):
            TwingateResourceCRD(
                apiVersion="twingate.com/v1",
                kind="TwingateResource",
                spec={
                    "address": "my.default.cluster.local",
                    "id": "UmVzb3VyY2U6OTM3Mzkw",
                    "name": "My K8S Resource",
                    "protocols": {
                        "tcp": {
                            "policy": "ALLOW_ALL",
                            "ports": [{"start": 80, "end": 80}],
                        }
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

    def test_resourceprotocol_ports_validation(self):
        with pytest.raises(
            ValueError, match="Input should be less than or equal to 65535"
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
                            "ports": [{"start": 1_000_000, "end": 80}],
                        }
                    },
                },
            )

        with pytest.raises(
            ValueError, match="Input should be greater than or equal to 0"
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
                            "ports": [{"start": -1, "end": 80}],
                        }
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


class TestTwingateConnectorCRD:
    def test_deserialization(self, sample_connector_object):
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

    def test_deserialization_fails_on_invalid_version_specifier(
        self, sample_connector_object
    ):
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

    def test_deserialization_fails_on_invalid_cron(self, sample_connector_object):
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
        self, sample_connector_object
    ):
        sample_connector_object["spec"] = {
            "version_policy": {"schedule": None, "version": "^1.0.0"}
        }
        crd = TwingateConnectorCRD(**sample_connector_object)
        assert crd.spec.version_policy.get_next_date_iso8601() is None

    def test_version_policy_get_next_date_iso8601_returns_right_date(
        self, sample_connector_object
    ):
        sample_connector_object["spec"] = {
            "version_policy": {"schedule": "* * * * *", "version": "^1.0.0"}
        }
        crd = TwingateConnectorCRD(**sample_connector_object)

        with freeze_time():
            now = pendulum.now("UTC").start_of("minute")
            expected = now.add(minutes=1)
            result = crd.spec.version_policy.get_next_date_iso8601()
            assert result == expected.to_iso8601_string()

        sample_connector_object["spec"] = {
            "version_policy": {"schedule": "0 0 * * 1", "version": "^1.0.0"}
        }
        crd = TwingateConnectorCRD(**sample_connector_object)
        with freeze_time():
            now = pendulum.now("utc").start_of("day")
            expected = now.next(pendulum.MONDAY).start_of("day")
            result = crd.spec.version_policy.get_next_date_iso8601()
            assert result == expected.to_iso8601_string()

    def test_spec_get_image_tag_by_policy(self, sample_connector_object):
        sample_connector_object["spec"] = {"version_policy": {"version": "^1.0.0"}}
        crd = TwingateConnectorCRD(**sample_connector_object)
        with patch(
            "app.dockerhub.get_all_operator_tags",
            return_value=["1.0.0", "1.0.1", "2.0.0"],
        ):
            assert str(crd.spec.get_image_tag_by_policy()) == "1.0.1"

    def test_spec_get_image_tag_by_policy_raises_if_no_match(
        self, sample_connector_object
    ):
        sample_connector_object["spec"] = {"version_policy": {"version": "^10.0.0"}}
        crd = TwingateConnectorCRD(**sample_connector_object)
        with patch(
            "app.dockerhub.get_all_operator_tags", return_value=["1.0.0", "latest"]
        ), pytest.raises(ValueError, match="Could not find valid tag for"):
            crd.spec.get_image_tag_by_policy()
