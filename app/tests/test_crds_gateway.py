import pytest
from pydantic import ValidationError

from app.crds import GatewaySpec, TwingateGatewayCRD


@pytest.fixture
def sample_gateway_object():
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateGateway",
        "metadata": {
            "name": "my-gateway",
            "namespace": "default",
            "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        },
        "spec": {
            "serviceRef": {"name": "my-gateway-svc", "port": 443},
            "x509CertificateAuthorityRef": {"name": "my-ca"},
        },
    }


def test_gateway_deserialization(sample_gateway_object):
    gateway = TwingateGatewayCRD(**sample_gateway_object)

    assert gateway.metadata.name == "my-gateway"
    assert gateway.spec.service_ref.name == "my-gateway-svc"
    assert gateway.spec.service_ref.namespace is None
    assert gateway.spec.service_ref.port == 443
    assert gateway.spec.x509_certificate_authority_ref.name == "my-ca"
    assert gateway.spec.x509_certificate_authority_ref.namespace is None

    # Both refs omit a namespace, so they resolve to the gateway's own namespace.
    assert gateway.spec.service_ref.resolve_namespace("gw-ns") == "gw-ns"
    assert (
        gateway.spec.x509_certificate_authority_ref.resolve_namespace("gw-ns")
        == "gw-ns"
    )


def test_gateway_remote_network_id_defaults_to_settings(sample_gateway_object):
    gateway = TwingateGatewayCRD(**sample_gateway_object)
    # `_mock_settings` (app/conftest.py) sets the operator-wide default.
    assert gateway.spec.remote_network_id == "UmVtb3RlTmV0d29yazoxMjMK"


def test_gateway_remote_network_id_override(sample_gateway_object):
    sample_gateway_object["spec"]["remoteNetworkId"] = "UmVtb3RlTmV0d29yazo5OTkK"
    gateway = TwingateGatewayCRD(**sample_gateway_object)
    assert gateway.spec.remote_network_id == "UmVtb3RlTmV0d29yazo5OTkK"


def test_gateway_service_ref_required():
    with pytest.raises(ValidationError, match="serviceRef"):
        GatewaySpec(x509_certificate_authority_ref={"name": "my-ca"})


def test_gateway_service_ref_port_required():
    with pytest.raises(ValidationError, match="port"):
        GatewaySpec(
            service_ref={"name": "my-gateway-svc"},
            x509_certificate_authority_ref={"name": "my-ca"},
        )


@pytest.mark.parametrize("port", [0, 65536])
def test_gateway_service_ref_port_out_of_range(port):
    with pytest.raises(ValidationError, match="port"):
        GatewaySpec(
            service_ref={"name": "my-gateway-svc", "port": port},
            x509_certificate_authority_ref={"name": "my-ca"},
        )


def test_gateway_ca_ref_required():
    with pytest.raises(ValidationError, match="x509CertificateAuthorityRef"):
        GatewaySpec(service_ref={"name": "my-gateway-svc", "port": 443})
