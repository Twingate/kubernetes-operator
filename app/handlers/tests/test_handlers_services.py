from unittest.mock import MagicMock, PropertyMock, patch

import kopf
import kubernetes
import pytest
import yaml
from kopf._core.intents.causes import Reason

from app.crds import ResourceType
from app.handlers.handlers_services import (
    ALLOWED_EXTRA_ANNOTATIONS,
    TLS_OBJECT_ANNOTATION,
    k8s_get_twingate_resource,
    service_to_twingate_resource,
    twingate_service_annotation_removed,
    twingate_service_create,
)

# Ignore the fact we use _cogs here

HELM_OWNERSHIP_METADATA = {
    "meta.helm.sh/release-name": "twingate-operator",
    "meta.helm.sh/release-namespace": "twingate",
}


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

    def test_marks_kubernetes_resource_as_helm_owned(
        self, example_cluster_ip_gateway_service_body
    ):
        example_cluster_ip_gateway_service_body.metadata["annotations"].update(
            HELM_OWNERSHIP_METADATA
        )

        result = service_to_twingate_resource(
            example_cluster_ip_gateway_service_body, "default"
        )

        assert result["metadata"]["annotations"] == HELM_OWNERSHIP_METADATA
        assert result["metadata"]["labels"]["app.kubernetes.io/managed-by"] == "Helm"

    @pytest.mark.parametrize("annotation", HELM_OWNERSHIP_METADATA)
    def test_does_not_mark_as_helm_owned_on_partial_ownership_metadata(
        self, example_cluster_ip_gateway_service_body, annotation
    ):
        # Helm won't adopt on a subset of the ownership annotations, so propagating one
        # only sets the managed-by label, which makes v2's operator drop the Service
        # owner reference without Helm ever taking over.
        example_cluster_ip_gateway_service_body.metadata["annotations"][annotation] = (
            HELM_OWNERSHIP_METADATA[annotation]
        )

        result = service_to_twingate_resource(
            example_cluster_ip_gateway_service_body, "default"
        )

        assert "annotations" not in result["metadata"]
        assert "app.kubernetes.io/managed-by" not in result["metadata"]["labels"]

    def test_does_not_mark_other_resource_types_as_helm_owned(
        self, example_service_body
    ):
        # Only the Kubernetes Resource is handed over to Helm. Marking any other one
        # would make v2's operator drop its Service owner reference, which is the only
        # thing that cleans it up when the Service goes away.
        example_service_body.metadata["annotations"].update(HELM_OWNERSHIP_METADATA)

        result = service_to_twingate_resource(example_service_body, "default")

        assert "annotations" not in result["metadata"]
        assert "app.kubernetes.io/managed-by" not in result["metadata"]["labels"]

    def test_kubernetes_resource_type_annotation(
        self, example_cluster_ip_gateway_service_body
    ):
        tls_object_name = "gateway-tls"
        namespace = "custom-namespace"

        result = service_to_twingate_resource(
            example_cluster_ip_gateway_service_body, namespace
        )

        assert result["spec"] == {
            "name": "kubernetes-gateway-resource",
            "address": "kubernetes.default.svc.cluster.local",
            "alias": "alias.int",
            "proxy": {
                "address": "kubernetes-gateway.custom-namespace.svc.cluster.local:443",
                "certificateAuthorityCertSecretRef": {
                    "name": tls_object_name,
                    "namespace": namespace,
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

    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            ({"loadBalancer": {"ingress": [{"ip": "1.2.3.4"}]}}, "1.2.3.4:443"),
            (
                {"loadBalancer": {"ingress": [{"hostname": "gateway.hostname.int"}]}},
                "gateway.hostname.int:443",
            ),
        ],
    )
    def test_kubernetes_resource_with_load_balancer_service_type(
        self, example_load_balancer_gateway_service_body, status, expected
    ):
        tls_object_name = "gateway-tls"
        namespace = "default"

        with patch(
            "kopf._cogs.structs.bodies.Body.status",
            new_callable=PropertyMock,
            return_value=status,
        ):
            result = service_to_twingate_resource(
                example_load_balancer_gateway_service_body, namespace
            )

        assert result["spec"] == {
            "name": "kubernetes-gateway-resource",
            "address": "kubernetes.default.svc.cluster.local",
            "alias": "alias.int",
            "proxy": {
                "address": expected,
                "certificateAuthorityCertSecretRef": {
                    "name": tls_object_name,
                    "namespace": namespace,
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

    def test_unsupported_resource_type_annotation(self, example_service_body):
        example_service_body.metadata["annotations"]["resource.twingate.com/type"] = (
            "Bogus"
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"Unsupported resource type 'Bogus'",
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

    def test_webapp_resource_request_header_rewrites(self, example_webapp_service_body):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/requestHeaderRewrites"
        ] = '{"Host": "example.com", "X-Foo": "bar"}'

        result = service_to_twingate_resource(example_webapp_service_body, "default")

        assert result["spec"]["requestHeaderRewrites"] == [
            {"name": "Host", "value": "example.com"},
            {"name": "X-Foo", "value": "bar"},
        ]

    def test_webapp_resource_without_request_header_rewrites(
        self, example_webapp_service_body
    ):
        result = service_to_twingate_resource(example_webapp_service_body, "default")

        assert "requestHeaderRewrites" not in result["spec"]

    def test_webapp_resource_invalid_request_header_rewrites(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/requestHeaderRewrites"
        ] = "not-json"

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/requestHeaderRewrites annotation must be a JSON",
        ):
            service_to_twingate_resource(example_webapp_service_body, "default")

    def test_webapp_resource_non_object_request_header_rewrites(
        self, example_webapp_service_body
    ):
        example_webapp_service_body.metadata["annotations"][
            "resource.twingate.com/requestHeaderRewrites"
        ] = '[{"key": "Host", "value": "example.com"}]'

        with pytest.raises(
            kopf.PermanentError,
            match=r"resource.twingate.com/requestHeaderRewrites annotation must be a JSON",
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

    def test_create_drops_chart_revision_labels_from_kubernetes_resource(
        self,
        example_cluster_ip_gateway_service_body,
        kopf_handler_runner,
        kopf_adopt_mock,
        k8s_customobjects_client_mock,
    ):
        example_cluster_ip_gateway_service_body.metadata["annotations"].update(
            HELM_OWNERSHIP_METADATA
        )
        example_cluster_ip_gateway_service_body.metadata["labels"].update(
            {
                "helm.sh/chart": "gateway-0.21.1",
                "app.kubernetes.io/version": "0.21.1",
                "app.kubernetes.io/name": "gateway",
            }
        )
        # Mirror kopf.adopt, which copies the owner's labels onto the child, so this
        # covers the ordering: filtering before the adopt call would be undone by it.
        kopf_adopt_mock.side_effect = lambda obj: [
            obj["metadata"]["labels"].setdefault(key, value)
            for key, value in example_cluster_ip_gateway_service_body.metadata[
                "labels"
            ].items()
        ]
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = None

        twingate_service_create(
            example_cluster_ip_gateway_service_body,
            example_cluster_ip_gateway_service_body.spec,
            "default",
            example_cluster_ip_gateway_service_body.metadata,
            MagicMock(),
            Reason.CREATE,
        )

        created = (
            k8s_customobjects_client_mock.create_namespaced_custom_object.call_args[0][
                4
            ]
        )
        assert created["metadata"]["labels"] == {
            "env": "dev",
            "app.kubernetes.io/name": "gateway",
            "app.kubernetes.io/managed-by": "Helm",
        }

    def test_create_keeps_chart_revision_labels_on_other_resource_types(
        self,
        example_service_body,
        kopf_handler_runner,
        kopf_adopt_mock,
        k8s_customobjects_client_mock,
    ):
        # Labels become Twingate tags when syncLabels is on, so only the Resource handed
        # over to Helm loses them.
        chart_labels = {
            "helm.sh/chart": "myapp-1.2.3",
            "app.kubernetes.io/version": "1.2.3",
        }
        example_service_body.metadata["labels"].update(chart_labels)
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = None

        twingate_service_create(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
            Reason.CREATE,
        )

        created = (
            k8s_customobjects_client_mock.create_namespaced_custom_object.call_args[0][
                4
            ]
        )
        assert created["metadata"]["labels"] == {"env": "dev"} | chart_labels

    def test_update_service_merges_helm_annotations_into_existing_resource(
        self,
        example_cluster_ip_gateway_service_body,
        kopf_handler_runner,
        k8s_customobjects_client_mock,
    ):
        example_cluster_ip_gateway_service_body.metadata["annotations"].update(
            HELM_OWNERSHIP_METADATA
        )
        kopf_annotation = {"kopf.zalando.org/last-handled-configuration": "{}"}
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = {
            "metadata": {
                "name": "kubernetes-gateway-resource",
                "labels": {},
                "annotations": dict(kopf_annotation),
            },
            "spec": {"id": "1", "name": "kubernetes-gateway-resource"},
        }

        twingate_service_create(
            example_cluster_ip_gateway_service_body,
            example_cluster_ip_gateway_service_body.spec,
            "default",
            example_cluster_ip_gateway_service_body.metadata,
            MagicMock(),
            Reason.UPDATE,
        )

        replaced = (
            k8s_customobjects_client_mock.replace_namespaced_custom_object.call_args[0][
                5
            ]
        )
        assert replaced["metadata"]["annotations"] == (
            kopf_annotation | HELM_OWNERSHIP_METADATA
        )


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

    def test_does_not_delete_kubernetes_twingate_resource(
        self, example_service_body, kopf_handler_runner, k8s_customobjects_client_mock
    ):
        k8s_customobjects_client_mock.get_namespaced_custom_object.return_value = {
            "metadata": {"name": "my-service-resource"},
            "spec": {
                "id": "1",
                "name": "my-service-resource",
                "type": ResourceType.KUBERNETES,
            },
        }

        twingate_service_annotation_removed(
            example_service_body,
            example_service_body.spec,
            "default",
            example_service_body.metadata,
            MagicMock(),
        )

        k8s_customobjects_client_mock.delete_namespaced_custom_object.assert_not_called()

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
