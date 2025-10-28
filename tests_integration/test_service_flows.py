import time
from unittest.mock import ANY

from app.api.tests.factories import BASE64_OF_VALID_CA_CERT
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
            resource.twingate.com/syncLabels: "true"
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
            "syncLabels": True,
            "type": "Network",
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
            "syncLabels": True,
            "type": "Network",
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

        # Test removing the service annotations and labels updates the resource
        kubectl_patch(
            f"svc/{service_name}",
            [
                {
                    "op": "remove",
                    "path": "/metadata/annotations/resource.twingate.com~1alias",
                },
                {
                    "op": "remove",
                    "path": "/metadata/labels/team",
                },
            ],
            "json",
        )
        time.sleep(2)
        tgr = kubectl_get("twingateresource", resource_name)
        assert "alias" not in tgr["spec"]
        assert tgr["metadata"]["labels"] == {"env": "dev"}

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
            "syncLabels": True,
            "type": "Network",
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
            "syncLabels": True,
            "type": "Network",
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
            "syncLabels": True,
            "type": "Network",
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
            "syncLabels": True,
            "type": "Network",
        }

        # Test deleting the service deletes the resource
        kubectl_delete_wait("svc", service_name)
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

    assert runner.exception is None
    assert runner.exit_code == 0


def test_service_flows_with_kubernetes_resource(run_kopf, random_name_generator):
    service_name = random_name_generator("test-svc")
    secret_name = f"{service_name}-tls"
    resource_name = f"{service_name}-resource"
    SECRET_OBJ = f"""
        apiVersion: v1
        kind: Secret
        metadata:
          name: {secret_name}
        type: "kubernetes.io/tls"
        data:
          tls.crt: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURqVENDQW5XZ0F3SUJBZ0lSQU43OGVLSGtIanFTMHF0N2V4em5iU2N3RFFZSktvWklodmNOQVFFTEJRQXcKRlRFVE1CRUdBMVVFQXhNS1oyRjBaWGRoZVMxallUQWVGdzB5TlRFd01qY3hPVEV4TWpkYUZ3MHlOakV3TWpjeApPVEV4TWpkYU1CSXhFREFPQmdOVkJBTVRCMmRoZEdWM1lYa3dnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCCkR3QXdnZ0VLQW9JQkFRQzEyOGlnZTNlWmErY3Y5RUJSTXNENjg5ZDkwUFdHRXFPTFZOcVNDVXpxemJwL2d0ZkgKZUNIa01NVzNKMXBYcTlJOEFhOWFuaVFDRkFXMGxhRjBSTVdlVGFhVEovK0Q2cURBQmtwamFYWVVjYlE4dGNIcgo4d3ZrQzlRQ1NHbG1aOWptVkNwazVmUE05RGNQeHZaRHdYeDZvWTZZeXV0b1B1VDcxbExoZUZkeFhQNEwwdExCCis0dWMyaURQTUdRdVRJLzhmaDJhWngwd3RzRi9PR2dURVFNNzdJQW95UmFyaEo4L2M5TEhGbGtZaWZ1UjJKdksKVGUycEZiZllZZGd1a1lKSzQyeUJQMmRQc3FraHQyQXdEVkpXNVFwOGZBaHoycEUzWmpUSkZmT2JJU0JvcjFBcwpML3dRMzk4N21USE1DdnkzazB3WWlhcmF1M3Qzc21sS2pOUjlBZ01CQUFHamdkb3dnZGN3RGdZRFZSMFBBUUgvCkJBUURBZ1dnTUIwR0ExVWRKUVFXTUJRR0NDc0dBUVVGQndNQkJnZ3JCZ0VGQlFjREFqQU1CZ05WSFJNQkFmOEUKQWpBQU1COEdBMVVkSXdRWU1CYUFGQ3R1dll1NHVNOHppS3pKUzJCTCtISExGT1RmTUhjR0ExVWRFUVJ3TUc2QwpDbXQxWW1WeWJtVjBaWE9DRW10MVltVnlibVYwWlhNdVpHVm1ZWFZzZElJV2EzVmlaWEp1WlhSbGN5NWtaV1poCmRXeDBMbk4yWTRJa2EzVmlaWEp1WlhSbGN5NWtaV1poZFd4MExuTjJZeTVqYkhWemRHVnlMbXh2WTJGc2dnNXQKYVc1cGEzVmlaUzVzYjJOaGJEQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FRRUF5OXNIMTZHUHJudkFWK2w2dHl2dwpFOUZJK2lHVWJSUjI2aHpzVFNJLzNjU1NwSWZOb2E5ZDRaOG1IN0g0SVMzL2ZsM1MvNzU0MDlZRVNCRjhPU283CjQ3aWY4Vkg0MnBpQzQ0emd5UXAwOFZEb0FsbEdQelFvaFZYRzhiQ0tvWnpwbWppQzB3bk82aVkzV0QwYWtMOTAKaXRlelBsV1F5d3Y4YXBwNWJiL0owc29wR0ZxUkplR1NENE41YUFNdmJlZDJDdmNaUTVBN0Y0c2NEUFh2dmM2dwpGdlFab2RKZ1VXUysyd09PYkg2UlpGbVpCaE1NWHZPdVRxcDI5bVB5UDNpK2NnMXVrbU93aFpQMVcrS043Ly9ZCmYvQ2w5ZHdVSHU3VXAzaGVJcDV2UzNEL0NBRDRUbzdFZ2RaRHpmc3d0NnlnWjBsS08wR25YM0xDYkUvbkw3WG4KRlE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="
          tls.key: "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBdGR2SW9IdDNtV3ZuTC9SQVVUTEErdlBYZmREMWhoS2ppMVRha2dsTTZzMjZmNExYCngzZ2g1RERGdHlkYVY2dlNQQUd2V3A0a0FoUUZ0SldoZEVURm5rMm1reWYvZytxZ3dBWktZMmwyRkhHMFBMWEIKNi9NTDVBdlVBa2hwWm1mWTVsUXFaT1h6elBRM0Q4YjJROEY4ZXFHT21NcnJhRDdrKzlaUzRYaFhjVnorQzlMUwp3ZnVMbk5vZ3p6QmtMa3lQL0g0ZG1tY2RNTGJCZnpob0V4RURPK3lBS01rV3E0U2ZQM1BTeHhaWkdJbjdrZGliCnlrM3RxUlczMkdIWUxwR0NTdU5zZ1Q5blQ3S3BJYmRnTUExU1Z1VUtmSHdJYzlxUk4yWTB5Ulh6bXlFZ2FLOVEKTEMvOEVOL2ZPNWt4ekFyOHQ1Tk1HSW1xMnJ0N2Q3SnBTb3pVZlFJREFRQUJBb0lCQUNoQkNvTXZZVFZXRTVuagpSRnRVMHkrWlN2RkFFQ0RKdm1hb2RTc1BJUFgyYk5vdHNhcW05a1dHNERUZTRwbjJYL1pGWHpXOVBIWXpUV0lBCkh2bFlBYkE5T3VwbTE2R3hEVDBFQjNKQzFVN0lMbCtqMGRWeStvWlRjZTNCYm9jcTVIRnpYdUR2bjR3VjRKdysKNjZMcTBLMXFWbUNPeGhYUW1pbitjbUVUSExQc1JJdjk1TTNJTzFXQWhaU3lVMDBzRlcyK1p2RUNZOGV6d0Qzcgo5czJybnFlY1NaS1NLcmJMdXZYSHk0L01TbGd4Qk94Z0JjVDFhcFBPRTZpZ2J5ajV3eFM5RkJvekdUMEZ3UUhGClc0OVN3cVdTcndRajFCM1lSbllaUE5tZTV1MHByalhUcDdySWdQWCtoT29YQTVKREdEV2hVZEJMYXhxTndLTjIKa09jenRnY0NnWUVBMDlqYWNtVStvcjVMYXZtdHhOTUpVUy9tQ0FaQWFGVFFQcXRsejZnenNwV0k4Y1VaQjY1YQpPTWxDcHplK3RhakhWZnhEdUFtVExOWndFVmJNQlNGVU9BMnhhYU1GVm5WMkJWSHRURXk4UXVjRVVPbHNtV2o5Cno1ZFRoTCtDaEZ5emxZWkkxbzRCalJlOThkU1F0M1VUZUR1bERVYU4zYTJPWGU1RUpXYmt2SXNDZ1lFQTI4TGkKZXRJN2xxV0tyU3BWWGJuemVsZ1hBQWh3MktubGVJazVXZlllMHlONVJKZFBnVjdNMGpUMFY4UEIzMWNyMlZQegp6ODJPU0E4SWhSUWs1UUFsZ21KQWRWTEVDc01WZENEYXZWdzRvTkZ2VkxKdVdGUE01UmIxaHNXVG1mTDNZUElPClNDbWJ0L3Jjd0c5eGZDM1J3THlaT016dXNQeEhPSnFiVWkzSUxCY0NnWUJHbmVURGVVaFZ5NFVzVmFvOUQvUHQKSWtCVnNHL0wxMm5MV2lzSCs1T3dGZlNlVXdzeTZrV2M1RW5abjlWc2pLUlYzMDliaTZXSnJybVFyaFE0S1pILwpWV0VzUzNFK0RzMlduR2F6cG1pakRJcjl4Ykd6dWJIUmZ5b1IrQnl6cm9zV2JycmMrbDArQVFvS0VNZGt3QndMCldpWjh0R1laM1A2MkJQU21XeFFvWFFLQmdRQzN0ZWtpaDVEczFLSmpORnA4cWJCU2ZFVnQ3NkIyWDBESFROKzIKeHJycUFtT2o1V0cvWW9LU3oxWGI4SGVudnZXWERrbHBWQXMzVGVudlpmR1p4aytVK1pHdEFtMkVHYVZibVFPQwovUThSMFVMaWFPODV3NFFybHMvVnhHRXBkeVU1MCtBQWoxZnZxelRUWWRaYTJ1clgxbEc0WEFqRngzKzZYL1NyCjlEMjhMUUtCZ0FhVUdldUhIWVVpZGdhV1pJZE0ybk5FTWZvUmFsWURKQ2Jwamw3VzlTWVc2S0V2azkyaGlTYXAKVmdJd1NucFE4WmxiUXJPNXY3ZDVUZnl0N3FJQU1HM0VPUHhzeUtUTURoNjdyMCtqekUwajBFd3o2MEo0ZHRKUwpHZ1d2T2JSSUc4anZyS0ZmWVJTeHR2VXlVWEIxYkhGN3lXamoxcGFtaEg0VENRdWpOQktVCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg=="
          ca.crt: {BASE64_OF_VALID_CA_CERT}
    """
    SERVICE_OBJ = f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {service_name}
          annotations:
            resource.twingate.com: "true"
            resource.twingate.com/type: "Kubernetes"
            resource.twingate.com/tlsSecret: "{secret_name}"
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - name: https
              protocol: TCP
              port: 443
              targetPort: https
    """

    with run_kopf(
        enable_connector_reconciler=False, enable_group_reconciler=False
    ) as runner:
        kubectl_create(SECRET_OBJ)
        kubectl_create(SERVICE_OBJ)
        kubectl_get("service", service_name)
        tgr = kubectl_wait_object_handler_success(
            "twingateresource", resource_name, "twingate_resource_create"
        )

        assert tgr["spec"] == {
            "address": "kubernetes.default.svc.cluster.local",
            "id": ANY,
            "isBrowserShortcutEnabled": False,
            "isVisible": True,
            "name": resource_name,
            "protocols": {
                "allowIcmp": False,
                "tcp": {"policy": "RESTRICTED", "ports": [{"end": 443, "start": 443}]},
                "udp": {"policy": "RESTRICTED", "ports": []},
            },
            "syncLabels": True,
            "type": "Kubernetes",
            "proxy": {
                "address": f"{service_name}.default.svc.cluster.local:443",
                "certificateAuthorityCert": BASE64_OF_VALID_CA_CERT,
            },
        }

        # Test that there is no resource changes when reconciling
        resource = kubectl_wait_object_handler_success("tgr", resource_name, "twingate_resource_sync")  # fmt: skip
        assert (
            resource["status"]["twingate_resource_sync"]["message"]
            == "No update required"
        )

        # Test deleting the service deletes the resource
        kubectl_delete_wait("svc", service_name)
        kubectl_delete_wait("twingateresource", resource_name, perform_deletion=False)

    assert runner.exception is None
    assert runner.exit_code == 0
