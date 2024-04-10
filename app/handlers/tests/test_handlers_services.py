from unittest.mock import MagicMock, patch

import kopf
import pytest
import yaml  # type: ignore

from app.handlers.handlers_services import (
    service_to_twingate_resource,
    twingate_service_create,
)

# Ignore the fact we use _cogs here

EXAMPLE_SERVICE_BODY = kopf._cogs.structs.bodies.Body(  # noqa: SLF001
    yaml.safe_load("""
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
""")
)


@pytest.fixture()
def k8s_customobjects_client_mock():
    client_mock = MagicMock()
    with patch("kubernetes.client.CustomObjectsApi") as k8sclient_mock:
        k8sclient_mock.return_value = client_mock
        yield client_mock


def test_service_to_twingate_resource_with_alias():
    result = service_to_twingate_resource(EXAMPLE_SERVICE_BODY, "default")

    assert result == {
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


def test_service_to_twingate_resource_without_alias():
    body = EXAMPLE_SERVICE_BODY
    del body.meta["annotations"]["twingate.com/expose-alias"]
    result = service_to_twingate_resource(body, "default")

    assert result == {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResource",
        "metadata": {
            "name": "my-service-resource",
        },
        "spec": {
            "name": "my-service-resource",
            "address": "my-service.default.svc.cluster.local",
            "protocols": {
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


class TestTwingateServiceCreate:
    def test_create_service(self, kopf_handler_runner, k8s_customobjects_client_mock):
        service_body = EXAMPLE_SERVICE_BODY

        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = None

        twingate_service_create(
            service_body,
            service_body.spec,
            "default",
            service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.patch_namespaced_custom_object.assert_not_called()
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            service_to_twingate_resource(service_body, "default"),
        )

    def test_update_service(self, kopf_handler_runner, k8s_customobjects_client_mock):
        service_body = EXAMPLE_SERVICE_BODY

        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = {
            "metadata": {"name": "my-service-resource"},
            "spec": {"address": "my-service.default.svc.cluster.local"},
        }

        twingate_service_create(
            service_body,
            service_body.spec,
            "default",
            service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.patch_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-service-resource",
            service_to_twingate_resource(service_body, "default"),
        )
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_not_called()
