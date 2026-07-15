from unittest.mock import MagicMock, patch

import kopf
import kubernetes
import pytest
import yaml
from kopf._core.intents.causes import Reason

from app.crds import ResourceType
from app.handlers.handlers_services import (
    ALLOWED_EXTRA_ANNOTATIONS,
    k8s_get_twingate_resource,
    service_to_twingate_resource,
    twingate_service_annotation_removed,
    twingate_service_create,
)

# Ignore the fact we use _cogs here


@pytest.fixture
def example_service_body():
    yaml_str = """
    apiVersion: v1
    kind: Service
    metadata:
      name: my-service
      labels:
        env: dev
      annotations:
        twingate.com/resource: "true"
        twingate.com/resource-alias: "myapp.internal"
    spec:
      type: ClusterIP
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
    return kopf.Body(yaml.safe_load(yaml_str))


@pytest.fixture
def example_webapp_service_body():
    yaml_str = """
    apiVersion: v1
    kind: Service
    metadata:
      name: web-app
      labels:
        env: dev
      annotations:
        resource.twingate.com: "true"
        resource.twingate.com/type: "WebApp"
        resource.twingate.com/gatewayName: "example-gateway"
        resource.twingate.com/downstreamPort: "80"
        resource.twingate.com/upstreamPort: "8080"
        resource.twingate.com/alias: "alias.int"
    spec:
      selector:
        app.kubernetes.io/name: web-app
      type: ClusterIP
      ports:
        - name: http
          protocol: TCP
          port: 8080
          targetPort: http
    """
    return kopf.Body(yaml.safe_load(yaml_str))


@pytest.fixture
def k8s_customobjects_client_mock():
    client_mock = MagicMock()
    with patch("kubernetes.client.CustomObjectsApi") as k8sclient_mock:
        k8sclient_mock.return_value = client_mock
        yield client_mock


class TestServiceToTwingateResource:
    @pytest.mark.parametrize(
        "annotation_name_converter", [None, *ALLOWED_EXTRA_ANNOTATIONS]
    )
    def test_with_extra_annotation(
        self, example_service_body, annotation_name_converter
    ):
        expected = {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateResource",
            "metadata": {"name": "my-service-resource", "labels": {"env": "dev"}},
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

        expected_annotation_values = {
            "name": "my resource",
            "alias": "myapp.internal",
            "isBrowserShortcutEnabled": True,
            "securityPolicyId": "12345",
            "isVisible": True,
            "syncLabels": True,
            "type": ResourceType.NETWORK,
        }

        if annotation_name_converter is not None:
            name, _ = annotation_name_converter
            example_service_body.metadata["annotations"][
                f"twingate.com/resource-{name}"
            ] = str(expected_annotation_values[name])

            expected["spec"][name] = expected_annotation_values[name]

        result = service_to_twingate_resource(example_service_body, "default")
        assert result == expected

    def test_webapp_resource_type_annotation(self, example_webapp_service_body):
        namespace = "custom-namespace"

        result = service_to_twingate_resource(example_webapp_service_body, namespace)

        assert result["spec"] == {
            "name": "web-app-resource",
            "address": "web-app.custom-namespace.svc.cluster.local",
            "alias": "alias.int",
            "type": ResourceType.WEB_APP,
            "gatewayRef": {
                "name": "example-gateway",
                "namespace": namespace,
            },
            "downstream": {"port": 80},
            "upstream": {"port": 8080},
        }

    def test_webapp_resource_type_annotation_with_explicit_gateway_namespace(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/gatewayNamespace"
        ] = "gateway-namespace"

        result = service_to_twingate_resource(
            example_webapp_service_body, "custom-namespace"
        )

        assert result["spec"]["gatewayRef"] == {
            "name": "example-gateway",
            "namespace": "gateway-namespace",
        }

    @pytest.mark.parametrize("resource_type", ["Bogus", "Kubernetes"])
    def test_unsupported_resource_type_annotation(
        self, example_service_body, resource_type
    ):
        example_service_body.metadata["annotations"]["resource.twingate.com/type"] = (
            resource_type
        )

        with pytest.raises(
            kopf.PermanentError,
            match=rf"Unsupported resource type '{resource_type}'",
        ):
            service_to_twingate_resource(example_service_body, "default")

    def test_webapp_resource_type_annotation_without_gateway_name(
        self, example_webapp_service_body
    ):
        del example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/gatewayName"
        ]

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/gatewayName annotation is required",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")

    def test_webapp_resource_downstream_port_defaults_to_single_service_port(
        self, example_webapp_service_body
    ):
        del example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/downstreamPort"
        ]

        result = service_to_twingate_resource(example_webapp_service_body, "default")

        # The fixture Service exposes a single TCP port (8080).
        assert result["spec"]["downstream"] == {"port": 8080}

    def test_webapp_resource_downstream_port_required_when_multiple_service_ports(
        self, example_webapp_service_body
    ):
        del example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/downstreamPort"
        ]
        example_webapp_service_body.spec["ports"].append(
            {"name": "https", "protocol": "TCP", "port": 9090, "targetPort": "https"}
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/downstreamPort annotation is required",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")

    def test_webapp_resource_explicit_downstream_port_need_not_match_service_port(
        self, example_webapp_service_body
    ):
        # downstream is client-facing and arbitrary; it need not be a Service port.
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/downstreamPort"
        ] = "12345"

        result = service_to_twingate_resource(example_webapp_service_body, "default")

        assert result["spec"]["downstream"] == {"port": 12345}

    def test_webapp_resource_upstream_port_defaults_to_single_service_port(
        self, example_webapp_service_body
    ):
        del example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/upstreamPort"
        ]

        result = service_to_twingate_resource(example_webapp_service_body, "default")

        # The fixture Service exposes a single TCP port (8080).
        assert result["spec"]["upstream"] == {"port": 8080}

    def test_webapp_resource_upstream_port_required_when_multiple_service_ports(
        self, example_webapp_service_body
    ):
        del example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/upstreamPort"
        ]
        example_webapp_service_body.spec["ports"].append(
            {"name": "https", "protocol": "TCP", "port": 9090, "targetPort": "https"}
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/upstreamPort annotation is required",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")

    def test_webapp_resource_explicit_upstream_port_selects_among_service_ports(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.spec["ports"].append(
            {"name": "https", "protocol": "TCP", "port": 9090, "targetPort": "https"}
        )
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/upstreamPort"
        ] = "9090"

        result = service_to_twingate_resource(example_webapp_service_body, "default")

        assert result["spec"]["upstream"] == {"port": 9090}

    def test_webapp_resource_explicit_upstream_port_not_exposed_by_service(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/upstreamPort"
        ] = "9999"

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/upstreamPort annotation \(9999\) must match "
            r"a TCP port exposed by the Service",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")

    def test_webapp_resource_non_integer_downstream_port(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/downstreamPort"
        ] = "not-a-number"

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/downstreamPort annotation must be an integer",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")

    def test_webapp_resource_non_integer_upstream_port(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/upstreamPort"
        ] = "not-a-number"

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/upstreamPort annotation must be an integer",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")


class TestK8sGetTwingateResource:
    def test_handles_404_returns_none(self, k8s_customobjects_client_mock):
        k8s_customobjects_client_mock.get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        assert k8s_get_twingate_resource("default", "test") is None

    def test_reraises_non_404_exceptions(self, k8s_customobjects_client_mock):
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
            Reason.CREATE,
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
        existing_resource = {
            "metadata": {"name": "my-service-resource", "labels": {}},
            "spec": {
                "id": "1",
                "name": "my-service-resource",
                "address": "my-service.default.svc.cluster.local",
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
        updated_resource = {
            "metadata": {**existing_resource["metadata"], "labels": {"env": "dev"}},
            "spec": {
                **existing_resource["spec"],
                "alias": "myapp.internal",
            },
        }
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = (
            existing_resource
        )

        twingate_service_create(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
            Reason.UPDATE,
        )

        k8s_customobjects_client_mock.replace_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-service-resource",
            updated_resource,
        )
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_not_called()


class TestTwingateServiceAnnotationRemoved:
    def test_deletes_twingate_resource_when_it_exists(
        self, example_service_body, kopf_handler_runner, k8s_customobjects_client_mock
    ):
        existing_resource = {
            "metadata": {"name": "my-service-resource"},
            "spec": {"id": "1", "name": "my-service-resource"},
        }
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = (
            existing_resource
        )

        twingate_service_annotation_removed(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.delete_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-service-resource",
        )

    def test_does_not_delete_when_twingate_resource_does_not_exist(
        self, example_service_body, kopf_handler_runner, k8s_customobjects_client_mock
    ):
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = None

        twingate_service_annotation_removed(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.delete_namespaced_custom_object.assert_not_called()
