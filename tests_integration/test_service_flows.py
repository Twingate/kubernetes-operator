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
)


def test_service_flows(kopf_runner_args, kopf_settings, ci_run_number):
    service_name = f"my-service-{ci_run_number}"
    resource_name = f"{service_name}-resource"
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
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
            - protocol: UDP
              port: 22
              targetPort: 9376
              name: ssh
    """

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(SERVICE_OBJ)
        time.sleep(2)

        kubectl_get("service", service_name)
        tgr = kubectl_get("twingateresource", resource_name)

        assert tgr["spec"] == {
            "address": f"{service_name}.default.svc.cluster.local",
            "alias": "myapp.internal",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": f"{service_name}-resource",
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
            "name": f"{service_name}-resource",
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
        kubectl_delete(f"service/{service_name}")
        time.sleep(5)
        with pytest.raises(CalledProcessError):
            kubectl_get("twingateresource", resource_name)

    assert runner.exception is None
    assert runner.exit_code == 0
