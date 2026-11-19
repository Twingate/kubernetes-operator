import json
from unittest.mock import ANY

from tests_integration.utils import (
    kubectl,
    kubectl_create,
    kubectl_delete_wait,
    kubectl_patch,
    kubectl_wait_object,
    kubectl_wait_object_handler_success,
)


def tcp_ports(obj: dict) -> list[dict]:
    return obj.get("spec", {}).get("protocols", {}).get("tcp", {}).get("ports", [])


def test_httproute_flows(run_kopf, random_name_generator):
    route_name = random_name_generator("test-route")
    gateway_name = f"{route_name}-gw"
    resource_name = f"{route_name}-httproute-resource"
    hostname = f"{route_name}.internal"
    GATEWAY_OBJ = f"""
        apiVersion: gateway.networking.k8s.io/v1
        kind: Gateway
        metadata:
          name: {gateway_name}
        spec:
          # No controller serves this class; the test sets the Gateway's status.
          gatewayClassName: twingate-integration-test
          listeners:
            - name: http
              protocol: HTTP
              port: 80
              hostname: "*.internal"
            - name: https
              protocol: HTTPS
              port: 443
              hostname: "*.internal"
              tls:
                mode: Terminate
                certificateRefs:
                  - name: {gateway_name}-cert
    """
    ROUTE_OBJ = f"""
        apiVersion: gateway.networking.k8s.io/v1
        kind: HTTPRoute
        metadata:
          name: {route_name}
          labels:
            env: dev
          annotations:
            resource.twingate.com: "true"
            resource.twingate.com/name: "My Route"
            resource.twingate.com/isBrowserShortcutEnabled: "false"
        spec:
          parentRefs:
            - name: {gateway_name}
              sectionName: https
          hostnames:
            - {hostname}
          rules:
            - backendRefs:
                - name: app
                  port: 8080
    """
    gateway_status = {
        "status": {"addresses": [{"type": "IPAddress", "value": "10.0.0.10"}]}
    }

    with run_kopf() as runner:
        kubectl_create(GATEWAY_OBJ)
        kubectl(
            f"patch gateway/{gateway_name} --subresource=status --type=merge "
            f"-p '{json.dumps(gateway_status)}'"
        )
        kubectl_create(ROUTE_OBJ)

        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )
        assert tgr["metadata"]["labels"] == {"env": "dev"}
        assert tgr["spec"] == {
            "address": "10.0.0.10",
            "alias": hostname,
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Route",
            "protocols": {
                "allowIcmp": False,
                "tcp": {"policy": "RESTRICTED", "ports": [{"end": 443, "start": 443}]},
                "udp": {"policy": "RESTRICTED", "ports": []},
            },
            "syncLabels": True,
            "type": "Network",
        }

        # Test changing the Gateway's address updates the resource
        new_gateway_status = {
            "status": {"addresses": [{"type": "IPAddress", "value": "10.0.0.11"}]}
        }
        kubectl(
            f"patch gateway/{gateway_name} --subresource=status --type=merge "
            f"-p '{json.dumps(new_gateway_status)}'"
        )
        tgr = kubectl_wait_object(
            "twingateresource",
            resource_name,
            lambda o: o.get("spec", {}).get("address") == "10.0.0.11",
            description="the Gateway's new address",
        )
        # The Gateway watcher only changes the Gateway-derived fields.
        assert tgr["spec"]["alias"] == hostname
        assert tgr["spec"]["name"] == "My Route"

        # Test moving the Gateway's HTTPS listener to another port updates the resource
        kubectl_patch(
            f"gateway/{gateway_name}",
            [{"op": "replace", "path": "/spec/listeners/1/port", "value": 8443}],
            "json",
        )
        tgr = kubectl_wait_object(
            "twingateresource",
            resource_name,
            lambda o: tcp_ports(o) == [{"end": 8443, "start": 8443}],
            description="the HTTPS listener's new port",
        )
        assert tgr["spec"]["address"] == "10.0.0.11"

        # Test attaching the route to another listener adds its port
        kubectl_patch(
            f"httproute/{route_name}",
            [
                {
                    "op": "add",
                    "path": "/spec/parentRefs/-",
                    "value": {"name": gateway_name, "sectionName": "http"},
                }
            ],
            "json",
        )
        tgr = kubectl_wait_object(
            "twingateresource",
            resource_name,
            lambda o: {"end": 80, "start": 80} in tcp_ports(o),
            description="the added 80 port",
        )
        assert tcp_ports(tgr) == [
            {"end": 80, "start": 80},
            {"end": 8443, "start": 8443},
        ]

        # Test setting the annotation to false deletes the resource
        kubectl_patch(
            f"httproute/{route_name}",
            {"metadata": {"annotations": {"resource.twingate.com": "false"}}},
        )
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

        kubectl_delete_wait("httproute", route_name)
        kubectl_delete_wait("gateway", gateway_name)

    assert runner.exception is None
    assert runner.exit_code == 0


def test_httproute_flows_deleting_route_deletes_resource(
    run_kopf, random_name_generator
):
    route_name = random_name_generator("test-route")
    gateway_name = f"{route_name}-gw"
    resource_name = f"{route_name}-httproute-resource"
    GATEWAY_OBJ = f"""
        apiVersion: gateway.networking.k8s.io/v1
        kind: Gateway
        metadata:
          name: {gateway_name}
        spec:
          gatewayClassName: twingate-integration-test
          listeners:
            - name: http
              protocol: HTTP
              port: 80
    """
    ROUTE_OBJ = f"""
        apiVersion: gateway.networking.k8s.io/v1
        kind: HTTPRoute
        metadata:
          name: {route_name}
          annotations:
            resource.twingate.com: "true"
        spec:
          parentRefs:
            - name: {gateway_name}
          hostnames:
            - {route_name}.internal
    """
    gateway_status = {
        "status": {"addresses": [{"type": "Hostname", "value": "gw.internal"}]}
    }

    with run_kopf() as runner:
        kubectl_create(GATEWAY_OBJ)
        kubectl(
            f"patch gateway/{gateway_name} --subresource=status --type=merge "
            f"-p '{json.dumps(gateway_status)}'"
        )
        kubectl_create(ROUTE_OBJ)

        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )
        assert tgr["spec"]["address"] == "gw.internal"
        assert tcp_ports(tgr) == [{"end": 80, "start": 80}]

        # The TwingateResource is owned by the HTTPRoute, so deleting the route
        # garbage-collects it.
        kubectl_delete_wait("httproute", route_name)
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)
        kubectl_delete_wait("gateway", gateway_name)

    assert runner.exception is None
    assert runner.exit_code == 0
