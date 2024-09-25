import time
from subprocess import CalledProcessError
from unittest.mock import ANY

import pytest
from kopf.testing import KopfRunner

from tests_integration.utils import (
    kubectl_create,
    kubectl_delete,
    kubectl_get,
    kubectl_patch,
    kubectl_wait_to_exist,
)


def test_service_flows(kopf_runner_args, kopf_settings, random_name_generator):
    service_name = random_name_generator("test-svc")
    resource_name = f"{service_name}-resource"
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
          annotations:
            twingate.com/resource: "true"
            twingate.com/resource-name: "My Service"
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

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(SERVICE_OBJ)
        kubectl_get("service", service_name)
        tgr = kubectl_wait_to_exist("twingateresource", resource_name)

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

        # Test deleting the service deletes the resource
        kubectl_delete("svc", service_name)
        time.sleep(10)
        with pytest.raises(CalledProcessError):
            kubectl_get("twingateresource", resource_name)

    assert runner.exception is None
    assert runner.exit_code == 0
