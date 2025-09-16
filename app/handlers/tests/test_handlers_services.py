from unittest.mock import MagicMock, PropertyMock, patch

import kopf
import kubernetes
import pytest
import yaml
from kopf._core.intents.causes import Reason

from app.api.tests.factories import BASE64_OF_VALID_CA_CERT
from app.crds import ResourceType
from app.handlers.handlers_services import (
    ALLOWED_EXTRA_ANNOTATIONS,
    TLS_OBJECT_ANNOTATION,
    k8s_get_tls_secret,
    k8s_get_twingate_resource,
    service_to_twingate_resource,
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
def example_cluster_ip_gateway_service_body():
    yaml_str = """
    apiVersion: v1
    kind: Service
    metadata:
      name: kubernetes-gateway
      labels:
        env: dev
      annotations:
        resource.twingate.com: "true"
        resource.twingate.com/type: "Kubernetes"
        resource.twingate.com/tlsSecret: "gateway-tls"
        resource.twingate.com/alias: "alias.int"
    spec:
      selector:
        app.kubernetes.io/name: gateway
        app.kubernetes.io/instance: kubernetes
      type: ClusterIP
      ports:
        - name: https
          protocol: TCP
          port: 443
          targetPort: https
    """
    return kopf.Body(yaml.safe_load(yaml_str))


@pytest.fixture
def example_load_balancer_gateway_service_body():
    yaml_str = """
    apiVersion: v1
    kind: Service
    metadata:
      name: kubernetes-gateway
      labels:
        env: dev
      annotations:
        resource.twingate.com: "true"
        resource.twingate.com/type: "Kubernetes"
        resource.twingate.com/tlsSecret: "gateway-tls"
        resource.twingate.com/alias: "alias.int"
    spec:
      selector:
        app.kubernetes.io/name: gateway
        app.kubernetes.io/instance: kubernetes
      type: LoadBalancer
      ports:
        - name: https
          protocol: TCP
          port: 443
          targetPort: https
    status:
      loadBalancer:
        ingress:
        - ip: 10.0.0.1
          ipMode: VIP
    """
    return kopf.Body(yaml.safe_load(yaml_str))


@pytest.fixture
def k8s_tls_secret_mock():
    return kubernetes.client.V1Secret(
        type="kubernetes.io/tls",
        metadata=kubernetes.client.V1ObjectMeta(name="gateway-tls"),
        data={"ca.crt": BASE64_OF_VALID_CA_CERT},
    )


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

    def test_kubernetes_resource_type_annotation(
        self,
        example_cluster_ip_gateway_service_body,
        k8s_core_client_mock,
        k8s_tls_secret_mock,
    ):
        tls_object_name = "gateway-tls"
        namespace = "custom-namespace"
        k8s_core_client_mock.read_namespaced_secret.return_value = k8s_tls_secret_mock

        result = service_to_twingate_resource(
            example_cluster_ip_gateway_service_body, namespace
        )
        k8s_core_client_mock.read_namespaced_secret.assert_called_once_with(
            namespace=namespace, name=tls_object_name
        )

        assert result["spec"] == {
            "name": "kubernetes-gateway-resource",
            "address": "kubernetes.default.svc.cluster.local",
            "alias": "alias.int",
            "proxy": {
                "address": "kubernetes-gateway.custom-namespace.svc.cluster.local",
                "certificateAuthorityCert": BASE64_OF_VALID_CA_CERT,
            },
            "protocols": {
                "allowIcmp": False,
                "tcp": {
                    "policy": "RESTRICTED",
                    "ports": [{"start": 443, "end": 443}],
                },
                "udp": {
                    "policy": "RESTRICTED",
                    "ports": [],
                },
            },
            "type": ResourceType.KUBERNETES,
        }

    def test_kubernetes_resource_type_annotation_without_tls_secret_annotation(
        self, example_cluster_ip_gateway_service_body
    ):
        example_cluster_ip_gateway_service_body.metadata["annotations"][
            TLS_OBJECT_ANNOTATION
        ] = None

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/tlsSecret annotation is not provided",
        ):
            service_to_twingate_resource(
                example_cluster_ip_gateway_service_body, "default"
            )

    def test_kubernetes_resource_type_annotation_without_k8s_secret_object(
        self, example_cluster_ip_gateway_service_body, k8s_core_client_mock
    ):
        k8s_core_client_mock.read_namespaced_secret.return_value = None

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls is missing.",
        ):
            service_to_twingate_resource(
                example_cluster_ip_gateway_service_body, "default"
            )

    def test_kubernetes_resource_type_annotation_with_invalid_secret_type(
        self,
        example_cluster_ip_gateway_service_body,
        k8s_core_client_mock,
        k8s_tls_secret_mock,
    ):
        k8s_tls_secret_mock.type = "kubernetes.io/token"
        k8s_core_client_mock.read_namespaced_secret.return_value = k8s_tls_secret_mock

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls type is invalid.",
        ):
            service_to_twingate_resource(
                example_cluster_ip_gateway_service_body, "default"
            )

    def test_kubernetes_resource_type_annotation_without_ca_cert(
        self,
        example_cluster_ip_gateway_service_body,
        k8s_core_client_mock,
        k8s_tls_secret_mock,
    ):
        k8s_tls_secret_mock.data = {}
        k8s_core_client_mock.read_namespaced_secret.return_value = k8s_tls_secret_mock

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls is missing ca.crt.",
        ):
            service_to_twingate_resource(
                example_cluster_ip_gateway_service_body, "default"
            )

    def test_kubernetes_resource_type_annotation_with_invalid_ca_cert(
        self,
        example_cluster_ip_gateway_service_body,
        k8s_core_client_mock,
        k8s_tls_secret_mock,
    ):
        k8s_tls_secret_mock.data["ca.crt"] = (
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tIE1JSUZmakNDQTJhZ0F3SUJBZ0lVQk50IC0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0="
        )
        k8s_core_client_mock.read_namespaced_secret.return_value = k8s_tls_secret_mock

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls ca.crt is invalid.",
        ):
            service_to_twingate_resource(
                example_cluster_ip_gateway_service_body, "default"
            )

    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            ({"loadBalancer": {"ingress": [{"ip": "1.2.3.4"}]}}, "1.2.3.4"),
            (
                {"loadBalancer": {"ingress": [{"hostname": "gateway.hostname.int"}]}},
                "gateway.hostname.int",
            ),
        ],
    )
    def test_kubernetes_resource_with_load_balancer_service_type(
        self,
        example_load_balancer_gateway_service_body,
        k8s_core_client_mock,
        k8s_tls_secret_mock,
        status,
        expected,
    ):
        tls_object_name = "gateway-tls"
        namespace = "default"
        k8s_core_client_mock.read_namespaced_secret.return_value = k8s_tls_secret_mock

        with patch(
            "kopf._cogs.structs.bodies.Body.status",
            new_callable=PropertyMock,
            return_value=status,
        ):
            result = service_to_twingate_resource(
                example_load_balancer_gateway_service_body, namespace
            )

        k8s_core_client_mock.read_namespaced_secret.assert_called_once_with(
            namespace=namespace, name=tls_object_name
        )

        assert result["spec"] == {
            "name": "kubernetes-gateway-resource",
            "address": "kubernetes.default.svc.cluster.local",
            "alias": "alias.int",
            "proxy": {
                "address": expected,
                "certificateAuthorityCert": BASE64_OF_VALID_CA_CERT,
            },
            "protocols": {
                "allowIcmp": False,
                "tcp": {
                    "policy": "RESTRICTED",
                    "ports": [{"start": 443, "end": 443}],
                },
                "udp": {
                    "policy": "RESTRICTED",
                    "ports": [],
                },
            },
            "type": ResourceType.KUBERNETES,
        }

    @pytest.mark.parametrize(
        "status",
        [
            {},
            {"loadBalancer": {}},
            {"loadBalancer": {"ingress": []}},
            {"loadBalancer": {"ingress": [{"ip": None}]}},
            {"loadBalancer": {"ingress": [{"hostname": None}]}},
        ],
    )
    def test_kubernetes_resource_when_load_balancer_ip_is_not_ready(
        self,
        example_load_balancer_gateway_service_body,
        kopf_handler_runner,
        k8s_customobjects_client_mock,
        status,
    ):
        with (
            patch(
                "kopf._cogs.structs.bodies.Body.status",
                new_callable=PropertyMock,
                return_value=status,
            ),
            pytest.raises(
                kopf.TemporaryError,
                match=r"Kubernetes Service: kubernetes-gateway LoadBalancer is not ready.",
            ),
        ):
            service_to_twingate_resource(
                example_load_balancer_gateway_service_body, "default"
            )


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


class TestK8sGetTLSSecret:
    def test_handles_404_returns_none(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_secret.side_effect = (
            kubernetes.client.exceptions.ApiException(status=404)
        )
        assert k8s_get_tls_secret("default", "test") is None

    def test_reraises_non_404_exceptions(self, k8s_core_client_mock):
        k8s_core_client_mock.read_namespaced_secret.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )
        with pytest.raises(kubernetes.client.exceptions.ApiException):
            k8s_get_tls_secret("default", "test")


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
