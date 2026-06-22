import base64
from unittest.mock import patch

import kopf
import pytest

from app.api.tests.factories import BASE64_OF_VALID_CA_CERT, VALID_CA_CERT
from app.crds import (
    ProtocolPolicy,
    ProtocolRange,
    ResourceProtocol,
    ResourceProxy,
    ResourceSpec,
    ResourceType,
    TwingateResourceCRD,
    _KubernetesObjectRef,
)


@pytest.fixture
def sample_network_resource_object():
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
            "type": ResourceType.NETWORK,
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
def sample_kubernetes_resource_object():
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
            "type": ResourceType.KUBERNETES,
            "proxy": {
                "address": "proxy.default.cluster.local",
                "certificate_authority_cert": BASE64_OF_VALID_CA_CERT,
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


def test_deserialization(sample_network_resource_object):
    crd = TwingateResourceCRD(**sample_network_resource_object)
    assert crd.spec.id == "UmVzb3VyY2U6OTM3Mzkw"
    assert crd.spec.address == "my.default.cluster.local"
    assert crd.spec.name == "My K8S Resource"
    assert crd.metadata.name == "foo"
    assert crd.metadata.uid == "c560d138-a93a-4463-8b44-d7717851a265"


def test_is_browser_shortcut_enabled_disallowed_on_wildcard_resource():
    with pytest.raises(ValueError, match=r"isBrowserShortcutEnabled"):
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
    with pytest.raises(ValueError, match=r"ports can't be set"):
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


def test_resourceprotocol_ports_validation():
    with pytest.raises(
        ValueError, match=r"Input should be less than or equal to 65535"
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

    with pytest.raises(ValueError, match=r"Input should be greater than or equal to 1"):
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
        ValueError, match=r"Start port value must be less or equal to end port value"
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


class TestResourceProtocolNormalizePort:
    def test_sorted_and_merged(self):
        protocol = ResourceProtocol(
            policy=ProtocolPolicy.RESTRICTED,
            ports=[
                ProtocolRange(start=443, end=443),
                ProtocolRange(start=80, end=80),
                ProtocolRange(start=81, end=81),
            ],
        )
        assert protocol.ports == [
            ProtocolRange(start=80, end=81),
            ProtocolRange(start=443, end=443),
        ]

    def test_overlapping_ports_merged(self):
        protocol = ResourceProtocol(
            policy=ProtocolPolicy.RESTRICTED,
            ports=[ProtocolRange(start=80, end=90), ProtocolRange(start=85, end=100)],
        )
        assert protocol.ports == [ProtocolRange(start=80, end=100)]

    def test_disjoint_ports_stay_separate(self):
        protocol = ResourceProtocol(
            policy=ProtocolPolicy.RESTRICTED,
            ports=[ProtocolRange(start=80, end=80), ProtocolRange(start=443, end=443)],
        )
        assert protocol.ports == [
            ProtocolRange(start=80, end=80),
            ProtocolRange(start=443, end=443),
        ]

    def test_single_port_unchanged(self):
        protocol = ResourceProtocol(
            policy=ProtocolPolicy.RESTRICTED,
            ports=[ProtocolRange(start=8080, end=8080)],
        )
        assert protocol.ports == [ProtocolRange(start=8080, end=8080)]

    def test_empty_ports_unchanged(self):
        protocol = ResourceProtocol(policy=ProtocolPolicy.RESTRICTED, ports=[])
        assert protocol.ports == []


def test_resource_proxy_get_certificate_authority_cert_without_secret_ref():
    proxy = ResourceProxy(
        address="proxy.default.cluster.local",
        certificate_authority_cert=BASE64_OF_VALID_CA_CERT,
        certificate_authority_cert_secret_ref=None,
    )

    assert proxy.get_certificate_authority_cert() == VALID_CA_CERT


def test_resource_proxy_get_certificate_authority_cert_with_secret_ref(
    k8s_core_client_mock, k8s_secret_mock
):
    proxy = ResourceProxy(
        address="proxy.default.cluster.local",
        certificate_authority_cert_secret_ref=_KubernetesObjectRef(name="gateway-tls"),
        certificate_authority_cert=None,
    )
    k8s_core_client_mock.read_namespaced_secret.return_value = k8s_secret_mock

    with patch(
        "app.crds.ResourceProxy.read_certificate_authority_cert_from_secret",
        wraps=proxy.read_certificate_authority_cert_from_secret,
    ) as read_ca_cert_mock:
        assert proxy.get_certificate_authority_cert() == VALID_CA_CERT
        read_ca_cert_mock.assert_called_once_with(k8s_secret_mock)


def test_resource_proxy_get_certificate_authority_cert_with_non_existing_secret(
    k8s_core_client_mock, k8s_secret_mock
):
    proxy = ResourceProxy(
        address="proxy.default.cluster.local",
        certificate_authority_cert_secret_ref=_KubernetesObjectRef(name="gateway-tls"),
        certificate_authority_cert=None,
    )
    k8s_core_client_mock.read_namespaced_secret.return_value = None

    assert proxy.get_certificate_authority_cert() is None


def test_resource_proxy_x509_ca_cert_returns_none_when_no_cert():
    proxy = ResourceProxy(
        address="proxy.default.cluster.local",
        certificate_authority_cert=None,
        certificate_authority_cert_secret_ref=None,
    )

    assert proxy.x509_ca_cert is None


def test_network_resource_spec_to_graphql_arguments(sample_network_resource_object):
    resource_spec = ResourceSpec(
        **sample_network_resource_object["spec"],
        sync_labels=True,
    )
    graphql_arguments = resource_spec.to_graphql_arguments(
        labels={"key": "value"}, exclude={"id"}
    )

    assert graphql_arguments == {
        "name": "My K8S Resource",
        "address": "my.default.cluster.local",
        "alias": None,
        "remote_network_id": "UmVtb3RlTmV0d29yazoxMjMK",
        "security_policy_id": None,
        "is_visible": True,
        "is_browser_shortcut_enabled": True,
        "protocols": {
            "allowIcmp": True,
            "tcp": {"policy": "RESTRICTED", "ports": [{"start": 80, "end": 80}]},
            "udp": {"policy": "ALLOW_ALL", "ports": []},
        },
        "tags": [{"key": "key", "value": "value"}],
    }


def test_kubernetes_resource_spec_to_graphql_arguments(
    sample_kubernetes_resource_object,
):
    resource_spec = ResourceSpec(
        **sample_kubernetes_resource_object["spec"],
        sync_labels=True,
    )
    graphql_arguments = resource_spec.to_graphql_arguments(
        labels={"key": "value"}, exclude={"id"}
    )

    assert graphql_arguments == {
        "name": "My K8S Resource",
        "address": "my.default.cluster.local",
        "alias": None,
        "remote_network_id": "UmVtb3RlTmV0d29yazoxMjMK",
        "security_policy_id": None,
        "is_visible": True,
        "protocols": {
            "allowIcmp": True,
            "tcp": {"policy": "RESTRICTED", "ports": [{"start": 80, "end": 80}]},
            "udp": {"policy": "ALLOW_ALL", "ports": []},
        },
        "tags": [{"key": "key", "value": "value"}],
        "proxy_address": "proxy.default.cluster.local",
        "certificate_authority_cert": VALID_CA_CERT,
    }


def test_kubernetes_resource_spec_to_graphql_arguments_when_certificate_authority_cert_not_found(
    sample_kubernetes_resource_object,
):
    sample_kubernetes_resource_object["spec"]["proxy"]["certificate_authority_cert"] = (
        None
    )
    resource_spec = ResourceSpec(**sample_kubernetes_resource_object["spec"])

    with pytest.raises(
        kopf.PermanentError,
        match="Certificate authority cert is not found for Kubernetes Resource type",
    ):
        resource_spec.to_graphql_arguments(labels={"key": "value"})


def test_kubernetes_resource_spec_to_graphql_arguments_with_gateway_ref():
    resource_spec = ResourceSpec(
        name="My K8S Resource",
        address="kubernetes.default.svc.cluster.local",
        type=ResourceType.KUBERNETES,
        gateway_ref=_KubernetesObjectRef(name="my-gateway", namespace="twingate"),
    )

    with patch(
        "app.crds.resolve_ref_to_twingate_id", return_value="R2F0ZXdheTo5Nwo="
    ) as resolve_mock:
        graphql_arguments = resource_spec.to_graphql_arguments(
            labels={"key": "value"}, exclude={"id"}
        )

    resolve_mock.assert_called_once_with("twingategateways", "twingate", "my-gateway")
    assert graphql_arguments["gateway_id"] == "R2F0ZXdheTo5Nwo="
    assert "proxy_address" not in graphql_arguments
    assert "certificate_authority_cert" not in graphql_arguments
    assert "gateway_ref" not in graphql_arguments


def test_kubernetes_resource_requires_proxy_or_gateway_ref():
    with pytest.raises(ValueError, match=r"exactly one of `proxy` .* or `gatewayRef`"):
        ResourceSpec(
            name="My K8S Resource",
            address="kubernetes.default.svc.cluster.local",
            type=ResourceType.KUBERNETES,
        )


def test_kubernetes_resource_rejects_both_proxy_and_gateway_ref():
    with pytest.raises(ValueError, match=r"exactly one of `proxy` .* or `gatewayRef`"):
        ResourceSpec(
            name="My K8S Resource",
            address="kubernetes.default.svc.cluster.local",
            type=ResourceType.KUBERNETES,
            proxy=ResourceProxy(
                address="proxy.default.cluster.local",
                certificate_authority_cert=BASE64_OF_VALID_CA_CERT,
            ),
            gateway_ref=_KubernetesObjectRef(name="my-gateway"),
        )


def test_kubernetes_resource_accepts_gateway_ref_only():
    resource_spec = ResourceSpec(
        name="My K8S Resource",
        address="kubernetes.default.svc.cluster.local",
        type=ResourceType.KUBERNETES,
        gateway_ref=_KubernetesObjectRef(name="my-gateway"),
    )
    assert resource_spec.gateway_ref is not None
    assert resource_spec.proxy is None


def test_network_resource_rejects_gateway_ref():
    with pytest.raises(
        ValueError, match="Network resources cannot set `proxy` or `gatewayRef`"
    ):
        ResourceSpec(
            name="My Network Resource",
            address="my.default.cluster.local",
            type=ResourceType.NETWORK,
            gateway_ref=_KubernetesObjectRef(name="my-gateway"),
        )


def test_web_app_resource_requires_gateway_ref():
    with pytest.raises(ValueError, match="WebApp resources require `gatewayRef`"):
        ResourceSpec(
            name="My WebApp Resource",
            address="webapp.default.cluster.local",
            type=ResourceType.WEB_APP,
        )


def test_web_app_resource_rejects_proxy():
    with pytest.raises(ValueError, match="WebApp resources cannot set `proxy`"):
        ResourceSpec(
            name="My WebApp Resource",
            address="webapp.default.cluster.local",
            type=ResourceType.WEB_APP,
            proxy=ResourceProxy(
                address="proxy.default.cluster.local",
                certificate_authority_cert=BASE64_OF_VALID_CA_CERT,
            ),
            gateway_ref=_KubernetesObjectRef(name="my-gateway"),
        )


def test_web_app_resource_spec_to_graphql_arguments():
    resource_spec = ResourceSpec(
        name="My WebApp Resource",
        address="webapp.default.cluster.local",
        type=ResourceType.WEB_APP,
        gateway_ref=_KubernetesObjectRef(name="my-gateway", namespace="twingate"),
    )

    with patch(
        "app.crds.resolve_ref_to_twingate_id", return_value="R2F0ZXdheTo5Nwo="
    ) as resolve_mock:
        graphql_arguments = resource_spec.to_graphql_arguments(
            labels={"key": "value"}, exclude={"id"}
        )

    resolve_mock.assert_called_once_with("twingategateways", "twingate", "my-gateway")
    assert graphql_arguments["gateway_id"] == "R2F0ZXdheTo5Nwo="
    assert "proxy_address" not in graphql_arguments
    assert "gateway_ref" not in graphql_arguments
    assert "type" not in graphql_arguments


def test_resource_spec_to_graphql_arguments_when_sync_labels_disabled(
    sample_network_resource_object,
):
    resource_spec = ResourceSpec(
        **sample_network_resource_object["spec"], sync_labels=False
    )
    graphql_arguments = resource_spec.to_graphql_arguments(labels={"key": "value"})

    assert graphql_arguments["tags"] == []


@pytest.mark.parametrize(
    "certificate_authority_cert",
    [
        ("\n" + VALID_CA_CERT + "\n"),
        ("\r\n" + VALID_CA_CERT + "\r\n"),
        ("  " + VALID_CA_CERT + "  "),
    ],
)
def test_resource_proxy_certificate_authority_cert_should_trim_whitespace(
    sample_kubernetes_resource_object, certificate_authority_cert
):
    sample_kubernetes_resource_object["spec"]["proxy"]["certificate_authority_cert"] = (
        base64.b64encode(certificate_authority_cert.encode()).decode()
    )

    resource_spec = ResourceSpec(
        **sample_kubernetes_resource_object["spec"],
    )

    assert resource_spec.proxy.certificate_authority_cert == VALID_CA_CERT


class TestResourceProxyReadCACertFromSecret:
    def test_read_ca_cert_from_secret(self, k8s_secret_mock):
        assert (
            ResourceProxy.read_certificate_authority_cert_from_secret(k8s_secret_mock)
            == VALID_CA_CERT
        )

    def test_read_ca_cert_from_secret_with_missing_ca_cert(self, k8s_secret_mock):
        k8s_secret_mock.data = {}

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls is missing ca.crt.",
        ):
            ResourceProxy.read_certificate_authority_cert_from_secret(k8s_secret_mock)

    def test_read_ca_cert_from_secret_with_invalid_ca_cert(self, k8s_secret_mock):
        k8s_secret_mock.data["ca.crt"] = (
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tIE1JSUZmakNDQTJhZ0F3SUJBZ0lVQk50IC0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0="
        )

        with pytest.raises(
            kopf.PermanentError,
            match=r"Kubernetes Secret object: gateway-tls ca.crt is invalid.",
        ):
            ResourceProxy.read_certificate_authority_cert_from_secret(k8s_secret_mock)
