from unittest.mock import MagicMock, patch

import kopf
import kubernetes
import pytest
import yaml  # type: ignore

from app.handlers.handlers_services import (
    ALLOWED_EXTRA_ANNOTATIONS,
    k8s_get_twingate_resource,
    service_to_twingate_resource,
    twingate_service_create,
)

# Ignore the fact we use _cogs here


@pytest.fixture()
def example_service_body():
    yaml_str = """
    apiVersion: v1
    kind: Service
    metadata:
      name: my-service
      annotations:
        twingate.com/expose: "true"
        twingate.com/expose-alias: "myapp.internal"
    spec:
      selector:
        app.kubernetes.io/name: MyApp
      ports:
        - name: http
          protocol: TCP
          port: 80
          targetPort: 9376
        - name: https
          protocol: TCP
          port: 443
          targetPort: 9377
        - protocol: UDP
          port: 22
          targetPort: 9376
          name: ssh
    """
    return kopf._cogs.structs.bodies.Body(  # noqa: SLF001
        yaml.safe_load(yaml_str)
    )


@pytest.fixture()
def k8s_customobjects_client_mock():
    client_mock = MagicMock()
    with patch("kubernetes.client.CustomObjectsApi") as k8sclient_mock:
        k8sclient_mock.return_value = client_mock
        yield client_mock


class TestServiceToTwingateResource:
    @pytest.mark.parametrize("annotation_name", ["", *ALLOWED_EXTRA_ANNOTATIONS])
    def test_with_extra_annotation(self, example_service_body, annotation_name):
        expected = {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateResource",
            "metadata": {
                "name": "my-service-resource",
            },
            "spec": {
                "name": "my-service-resource",
                "address": "my-service.default.svc.cluster.local",
                "alias": "myapp.internal",
                "protocols": {
                    "allowIcmp": False,
                    "tcp": {
                        "policy": "RESTRICTED",
                        "ports": [{"start": 80, "end": 80}, {"start": 443, "end": 443}],
                    },
                    "udp": {
                        "policy": "RESTRICTED",
                        "ports": [{"start": 22, "end": 22}],
                    },
                },
            },
        }

        if annotation_name:
            example_service_body.metadata["annotations"][
                f"twingate.com/expose-{annotation_name}"
            ] = f"{annotation_name} value"

            expected["spec"][annotation_name] = f"{annotation_name} value"

        result = service_to_twingate_resource(example_service_body, "default")
        assert result == expected


def test_k8s_get_twingate_resource_handles_404_returns_none(
    k8s_customobjects_client_mock,
):
    k8s_customobjects_client_mock.get_namespaced_custom_object.side_effect = (
        kubernetes.client.exceptions.ApiException(status=404)
    )
    assert k8s_get_twingate_resource("default", "test") is None


def test_k8s_get_twingate_resource_reraises_non_404_exceptions(
    k8s_customobjects_client_mock,
):
    k8s_customobjects_client_mock.get_namespaced_custom_object.side_effect = (
        kubernetes.client.exceptions.ApiException(status=500)
    )
    with pytest.raises(kubernetes.client.exceptions.ApiException):
        k8s_get_twingate_resource("default", "test")


class TestTwingateServiceCreate:
    def test_create_service_triggers_creation_of_twingate_resource(
        self, example_service_body, kopf_handler_runner, k8s_customobjects_client_mock
    ):
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = None

        twingate_service_create(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.patch_namespaced_custom_object.assert_not_called()
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            service_to_twingate_resource(example_service_body, "default"),
        )

    def test_update_service_propogates_changes_to_twingate_resource(
        self, example_service_body, kopf_handler_runner, k8s_customobjects_client_mock
    ):
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = {
            "metadata": {"name": "my-service-resource"},
            "spec": {"address": "my-service.default.svc.cluster.local"},
        }

        twingate_service_create(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.patch_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-service-resource",
            service_to_twingate_resource(example_service_body, "default"),
        )
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_not_called()
