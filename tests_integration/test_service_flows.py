import time
from unittest.mock import ANY

from tests_integration.utils import (
    kubectl_create,
    kubectl_delete_wait,
    kubectl_get,
    kubectl_patch,
    kubectl_wait_object_handler_success,
    kubectl_wait_to_exist,
)


def test_service_flows(run_kopf, random_name_generator):
    service_name = random_name_generator("test-svc")
    resource_name = f"{service_name}-resource"
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
          labels:
            env: dev
            team: engineering
          annotations:
            resource.twingate.com: "true"
            resource.twingate.com/name: "My Service"
            resource.twingate.com/alias: "myapp.internal"
            resource.twingate.com/isVisible: "true"
            resource.twingate.com/isBrowserShortcutEnabled: "false"
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - name: http
              protocol: TCP
              port: 80
              targetPort: 9376
            - protocol: UDP
              port: 22
              targetPort: 9376
              name: ssh
    """

    with run_kopf(
        enable_connector_reconciler=False, enable_group_reconciler=False
    ) as runner:
        kubectl_create(SERVICE_OBJ)
        kubectl_get("service", service_name)
        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )
        assert tgr["metadata"]["labels"] == {
            "env": "dev",
            "team": "engineering",
        }
        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Service",
            "protocols": {
                "allowIcmp": False,
                "tcp": {"policy": "RESTRICTED", "ports": [{"end": 80, "start": 80}]},
                "udp": {"policy": "RESTRICTED", "ports": [{"end": 22, "start": 22}]},
            },
        }

        # Test patching the service updates the resource
        kubectl_patch(
            f"svc/{service_name}",
            [
                {
                    "op": "add",
                    "path": "/spec/ports/-",
                    "value": {
                        "protocol": "TCP",
                        "port": 443,
                        "targetPort": 9377,
                        "name": "https",
                    },
                }
            ],
            "json",
        )
        time.sleep(2)
        tgr = kubectl_get("twingateresource", resource_name)
        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Service",
            "protocols": {
                "allowIcmp": False,
                "tcp": {
                    "policy": "RESTRICTED",
                    "ports": [{"end": 80, "start": 80}, {"end": 443, "start": 443}],
                },
                "udp": {"policy": "RESTRICTED", "ports": [{"end": 22, "start": 22}]},
            },
        }

        # Test patching the service annotations updates the resource
        kubectl_patch(
            f"svc/{service_name}",
            [
                {
                    "op": "replace",
                    "path": "/metadata/annotations/resource.twingate.com~1alias",
                    "value": "myappchanged.internal",
                }
            ],
            "json",
        )
        time.sleep(2)
        tgr = kubectl_get("twingateresource", resource_name)
        assert tgr["spec"]["alias"] == "myappchanged.internal"

        # Test deleting the service deletes the resource
        kubectl_delete_wait("svc", service_name)
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

    assert runner.exception is None
    assert runner.exit_code == 0


def test_service_flows_annotation_removed(run_kopf, random_name_generator):
    service_name = random_name_generator("test-svc")
    resource_name = f"{service_name}-resource"
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
          annotations:
            resource.twingate.com: "true"
            resource.twingate.com/name: "My Service"
            resource.twingate.com/alias: "myapp.internal"
            resource.twingate.com/isVisible: "true"
            resource.twingate.com/isBrowserShortcutEnabled: "false"
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - name: http
              protocol: TCP
              port: 80
              targetPort: 9376
            - protocol: UDP
              port: 22
              targetPort: 9376
              name: ssh
    """

    with run_kopf(
        enable_connector_reconciler=False, enable_group_reconciler=False
    ) as runner:
        kubectl_create(SERVICE_OBJ)
        kubectl_get("service", service_name)
        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )

        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Service",
            "protocols": {
                "allowIcmp": False,
                "tcp": {"policy": "RESTRICTED", "ports": [{"end": 80, "start": 80}]},
                "udp": {"policy": "RESTRICTED", "ports": [{"end": 22, "start": 22}]},
            },
        }

        # Test removing the resource annotation
        kubectl_patch(
            f"svc/{service_name}",
            [
                {
                    "op": "remove",
                    "path": "/metadata/annotations/resource.twingate.com",
                }
            ],
            "json",
        )
        time.sleep(2)
        # Test resource was deleted
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

        # cleanup
        kubectl_delete_wait("svc", service_name)

    assert runner.exception is None
    assert runner.exit_code == 0


def test_service_flows_annotation_changed_to_false(run_kopf, random_name_generator):
    service_name = random_name_generator("test-svc")
    resource_name = f"{service_name}-resource"
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
          annotations:
            resource.twingate.com: "true"
            resource.twingate.com/name: "My Service"
            resource.twingate.com/alias: "myapp.internal"
            resource.twingate.com/isVisible: "true"
            resource.twingate.com/isBrowserShortcutEnabled: "false"
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - name: http
              protocol: TCP
              port: 80
              targetPort: 9376
            - protocol: UDP
              port: 22
              targetPort: 9376
              name: ssh
    """

    with run_kopf(
        enable_connector_reconciler=False, enable_group_reconciler=False
    ) as runner:
        kubectl_create(SERVICE_OBJ)
        kubectl_get("service", service_name)
        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )

        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Service",
            "protocols": {
                "allowIcmp": False,
                "tcp": {"policy": "RESTRICTED", "ports": [{"end": 80, "start": 80}]},
                "udp": {"policy": "RESTRICTED", "ports": [{"end": 22, "start": 22}]},
            },
        }

        # Test changing resource annotation to false
        kubectl_patch(
            f"svc/{service_name}",
            [
                {
                    "op": "replace",
                    "path": "/metadata/annotations/resource.twingate.com",
                    "value": "false",
                }
            ],
            "json",
        )
        time.sleep(2)
        # Test resource was deleted
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

        # cleanup
        kubectl_delete_wait("svc", service_name)

    assert runner.exception is None
    assert runner.exit_code == 0


# TODO: Remove once we release v1.0 (see https://github.com/Twingate/kubernetes-operator/issues/530)
def test_service_flows_with_old_annotations(run_kopf, random_name_generator):
    service_name = random_name_generator("test-svc-old")
    resource_name = f"{service_name}-resource"
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
          annotations:
            twingate.com/resource: "true"
            twingate.com/resource-name: "My Service (old annotations)"
            twingate.com/resource-alias: "myapp.internal"
            twingate.com/resource-isVisible: "true"
            twingate.com/resource-isBrowserShortcutEnabled: "false"
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - name: http
              protocol: TCP
              port: 80
              targetPort: 9376
            - protocol: UDP
              port: 22
              targetPort: 9376
              name: ssh
    """

    with run_kopf(
        enable_connector_reconciler=False, enable_group_reconciler=False
    ) as runner:
        kubectl_create(SERVICE_OBJ)
        kubectl_get("service", service_name)
        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )

        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Service (old annotations)",
            "protocols": {
                "allowIcmp": False,
                "tcp": {"policy": "RESTRICTED", "ports": [{"end": 80, "start": 80}]},
                "udp": {"policy": "RESTRICTED", "ports": [{"end": 22, "start": 22}]},
            },
        }

        # Test patching the service updates the resource
        kubectl_patch(
            f"svc/{service_name}",
            [
                {
                    "op": "add",
                    "path": "/spec/ports/-",
                    "value": {
                        "protocol": "TCP",
                        "port": 443,
                        "targetPort": 9377,
                        "name": "https",
                    },
                }
            ],
            "json",
        )
        kubectl_wait_to_exist("twingateresource", resource_name)
        tgr = kubectl_get("twingateresource", resource_name)
        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": "My Service (old annotations)",
            "protocols": {
                "allowIcmp": False,
                "tcp": {
                    "policy": "RESTRICTED",
                    "ports": [{"end": 80, "start": 80}, {"end": 443, "start": 443}],
                },
                "udp": {"policy": "RESTRICTED", "ports": [{"end": 22, "start": 22}]},
            },
        }

        # Test deleting the service deletes the resource
        kubectl_delete_wait("svc", service_name)
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

    assert runner.exception is None
    assert runner.exit_code == 0
