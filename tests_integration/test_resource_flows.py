import os
from unittest.mock import ANY

import pytest
from kopf.testing import KopfRunner

from tests_integration.utils import (
    assert_log_message_contains,
    assert_log_message_starts_with,
    kubectl_apply,
    kubectl_create,
    kubectl_delete_wait,
    kubectl_wait_object_handler_success,
    kubectl_wait_to_exist,
    load_stdout,
)


def test_resource_flows(kopf_settings, kopf_runner_args, unique_resource_name):
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
          protocols:
            allowIcmp: false
            tcp:
                policy: RESTRICTED
                ports:
                    - start: 80
                      end: 80
    """

    OBJ_UPDATED = f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Resource Renamed
              address: my.default.cluster.local
              protocols:
                allowIcmp: false
                udp:
                    policy: RESTRICTED
                    ports:
                        - start: 80
                          end: 80

        """

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(OBJ)
        created_object = kubectl_wait_object_handler_success("tgr", unique_resource_name, "twingate_resource_create")

        # Update the name
        kubectl_apply(OBJ_UPDATED)
        updated_object = kubectl_wait_object_handler_success("tgr", unique_resource_name, "twingate_resource_update")
        assert updated_object["spec"]["name"] == "My K8S Resource Renamed"

        kubectl_delete_wait("tgr", unique_resource_name)

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)

    # fmt: off

    assert "twingate_resource_create" in created_object["status"], f"status not updated: {created_object['status']}"

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    expected_object = {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name, "uid": ANY, "namespace": "default"}

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert twingate_id

    # Update
    assert {"message": f"Updating resource {twingate_id}", "timestamp": ANY,  "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert_log_message_starts_with(logs, f"Got resource id='{twingate_id}' name='My K8S Resource Renamed'")

    # Delete
    assert {"message": "Twingate API Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "object": expected_object, "taskName": ANY, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "taskName": ANY, "severity": "info"} in logs

    # fmt: on


def test_kubernetes_resource_flows(
    kopf_settings, kopf_runner_args, unique_resource_name
):
    secret_name = "kubernetes-access-gateway-tls"  # noqa: S105
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: kubernetes.default.svc.cluster.local
          type: Kubernetes
          proxy:
            address: kubernetes-access-gateway.default.svc.cluster.local:443
            certificateAuthorityCert: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUZmekNDQTJlZ0F3SUJBZ0lWQUxvT0pBb1NQMW04MUJRM0RBalJIY1lYckxSOE1BMEdDU3FHU0liM0RRRUJDd1VBTUhjeEN6QUpCZ05WQkFZVEFsVlRNUXN3Q1FZRFZRUUlFd0pEVHpFUU1BNEdBMVVFQnhNSFFtOTFiR1JsY2pFU01CQUdBMVVFQ2hNSlNuVnRjRU5zYjNWa01Sa3dGd1lEVlFRTEV4QktkVzF3UTJ4dmRXUlRRVTFNU1dSUU1Sb3dHQVlEVlFRREV4RktkVzF3UTJ4dmRXUlRRVTFNVlhObGNqQWVGdzB5TVRFeE1qa3dNVEF5TVRSYUZ3MHlOakV4TWprd01UQXlNVFJhTUhjeEN6QUpCZ05WQkFZVEFsVlRNUXN3Q1FZRFZRUUlFd0pEVHpFUU1BNEdBMVVFQnhNSFFtOTFiR1JsY2pFU01CQUdBMVVFQ2hNSlNuVnRjRU5zYjNWa01Sa3dGd1lEVlFRTEV4QktkVzF3UTJ4dmRXUlRRVTFNU1dSUU1Sb3dHQVlEVlFRREV4RktkVzF3UTJ4dmRXUlRRVTFNVlhObGNqQ0NBaUl3RFFZSktvWklodmNOQVFFQkJRQURnZ0lQQURDQ0Fnb0NnZ0lCQUxjNktKT0czTm0wMnZIZnZvYVdrcjBzUjk0SE9Wd2lLNzlqZHhQNHNhQ2k1aEw3RmoyRW5FbXo3M0JIL0J4QkZRL3VIY1JqTU85dUxuNldSY1QyUDhXRE10eVV1QlNJVUw0bEx4b1RPbTAvMzdxcllZQUhmYllKdVBXQWJ2SXhuZTJOczBpWFlGa2dIU1o2RHVkWjM3U1NkWG5QQnVSNmNhZXltYm92ckNIUGJFVGIzU3BnY1ZNdXV1RzFYaENUTjBsWi94cnBCMUc4SHFMMzd4VkNtSkF6bUJtVWdZcHU5K3pIMXVCUHdVb1dhOFRIZWxYcnAyQ1VaM210d28wdUtuZnlYSmNKeUM1ckp2MFJMbzRvSlJldFUzbWlURjcvdHJjWE1oWEdzb3NNL1UvYTVzbjc5RWgzdngrQkpDRGRySnRlNXowV0NDUitGY0xZdEU5aXdlV3BJS2g5ODc0NnJVb1M0ck1IcFVhZTBOczZlU3BVK093SW1NdzZvVUNITzgreDFna2NWQkcydGZEMG12N1RJZFc1aWI2TTlMOVQ2M0wxNXFla2U5QVBQY3BHMHZHNUl4ZUdiQ2xSY2pFNHVzaVRnK2lLOCtBQ1Q3aDJodFNjU0dsUHNJM0RibG45RDRMWFJLTkhDY3lCY3BWT0hJMDZaMEQwaEs3eWNscGl1SUxTSGFUVENQbDM4eHdVTkZsSkRxWGpVdnpMeE0xc1d6ZWJ0NEl0M2c4ODZNa1M0bDB3WmdhWUh4bWNtQ2RsSnZ5UHFWOHR4Z1FaWUJZM2pUN0VqZ1BGb3g0a0xNVktBK2pBemY5c0hUaDd6UW5PZ1JFMzJyaGoyTlVBSzNoQmJIdjFhT2VVbGh4U0xEbGU3WDZsWEd4eEhDdkEzbDFOcG1vNUExT1poTUJGQWdNQkFBR2pBakFBTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElDQVFDVUlvcDJUU1FKenNSaGd3T0dZa2JwQWJsU2prTlE1VEJaZnJyWm9GWU9NQTBqaTYycWxXRDNDNU9VYVdRYkJydkcvOEx2Q09YbTRtUG1wMWUwSmVsaTZEWkJJbjJVbzduZTI5VitpdHZnQi9kdTYrcGtySXIwZWdBYmtKZmtTK2YzbFFqZXBqRmFraVFxSzNZTEp0WEpVckt2d2pXa2RnVG1XcjhTMVA5TFg0ZkU0UmxyOWkrcGc2TlZzcFNEZXptREhnN2piZ2NxMXRLOGczcmFEcEFNNExreUdKSENTRTB0V21ORHc2UUtSYi9ldjZmQmR6MVVWVFhhV1pvQTIycldjZk1IMzVZd2NDUDVvWHBpa0lTaStKbUc2SG9qQnM0bGpwYlpGWWNSUnU5UC9pMG12cGRKUXRQUlJudk5DNXY1RXdQdWt0RTFXaTZxa3A2OE43aitRTGw4anlhWExuNkdIRTZDamdnRTRZQjh2ZXFjZUxhRERZdXR4UmpUNzdMaEVTeFdONlhSQnpoTWNPckhGcE5KUUkxVmxhbEFCVzJZanBKSVB2bytpV2xBWlp4MjBrMitHRkpWTml3ZTBYemR5cWwxZUdNeENrS3BkNXdCZXpKZUJVdXJNUSt0cWQrMWRHMTBmRUJMM2dpa0JHbFpMU1d1czNwRnhTaXdZemhTU29BcUs5ekY3VCtBNjc0cDdFUUI5Zms4VjRadFI2T28yMFI0TldPWDRWcnFzekZjWWFOSnJwS3VCOEZhRHZVcWNFMmFRK3ZrWVhmaTBGYWRMRm1jN1dlTWVQSU12a2ZpbnI5cUVnWWMreXE1WGEwV0hiM1hlKzF5N2wwVEt5dUtIZEJnSEdKVUJBYkFFeWF1NFVjSUJqbjFnWDJZTlEvTjFUUnZxSWJrY1E9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0t
          protocols:
            allowIcmp: false
            tcp:
              policy: RESTRICTED
              ports:
              - end: 443
                start: 443
            udp:
              policy: RESTRICTED
              ports: []
    """

    OBJ_UPDATED = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: kubernetes.default.svc.cluster.local
          type: Kubernetes
          proxy:
            address: kubernetes-access-gateway.default.svc.cluster.local:443
            certificateAuthorityCertSecretRef:
                name: {secret_name}
          protocols:
            allowIcmp: false
            tcp:
              policy: RESTRICTED
              ports:
              - end: 443
                start: 443
            udp:
              policy: RESTRICTED
              ports: []
        """

    SECRET_OBJ = f"""
        apiVersion: v1
        kind: Secret
        metadata:
          name: {secret_name}
          namespace: default
        type: kubernetes.io/tls
        data:
          ca.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURKakNDQWc2Z0F3SUJBZ0lRQ3VzQW56OWxEcGcxY3d5TmhlU045VEFOQmdrcWhraUc5dzBCQVFzRkFEQXQKTVNzd0tRWURWUVFERXlKc2IyTmhiQzFyZFdKbGNtNWxkR1Z6TFdGalkyVnpjeTFuWVhSbGQyRjVMV05oTUI0WApEVEkxTVRBd09ERTFNekkwTjFvWERUSTJNREV3TmpFMU16STBOMW93TFRFck1Da0dBMVVFQXhNaWJHOWpZV3d0CmEzVmlaWEp1WlhSbGN5MWhZMk5sYzNNdFoyRjBaWGRoZVMxallUQ0NBU0l3RFFZSktvWklodmNOQVFFQkJRQUQKZ2dFUEFEQ0NBUW9DZ2dFQkFPdlNGUUdNejZtRnhYMFVDcXNkTWZMMUthUHUrR1Jpa0xkRDJMaUM4N1dpK3V3dQpyOXFpK1I3MU53VFd4cWFSeHZlcE5zVzBhZEYrdjhnd0c3Nm5KanU2S3dvNVV3M3EwSWg3WWp4cXFsN0taeGJlCkNMM0JYSzhtdW9Kbk5yUmt6MzJDTFNYajZUUXNZclNGcUZabW5OSS9ma2hRT3ZoWG85SldtaGxuYXY2WCtSRGUKYWdqc29Ed2VkV2J2eXZuZHpUd1ZodVJCR0VDelhFU0dSQXkyR1VrNXoxeTY1ZjNNUDdOVit1MFowdk53MEtSawpRcmNTVDA1V0t5RWZYZUpDOHM1czZZVm9zZE1xRnRzZ1drTzg0N01OR3ZYc01yY3RTN1hNUkdNeTRwVUl6VEI1CnRyK3JhNENkZTYwZFpNNHNJODMvVmh6bnU5enhidUFGTGRVNkdGTUNBd0VBQWFOQ01FQXdEZ1lEVlIwUEFRSC8KQkFRREFnS2tNQThHQTFVZEV3RUIvd1FGTUFNQkFmOHdIUVlEVlIwT0JCWUVGSWVsd3dsWGNnUy9rakZZY2hqQwpZWU1zNFFDb01BMEdDU3FHU0liM0RRRUJDd1VBQTRJQkFRQUk2V3JiUzA2TEdxRDl4VDdTbnhYZjl6YlQrRGhqCjZDaFhOb3NSOEJKNnhEL3YwU3NEV3ZuNkdIeFY0ZEd6YXJwVTdROUpLM0d2NlJhcmJ6M2orU2syN2I2MURmNmsKRGM1QUQ3N1hRSVovOTExUm4rcFk3c3lGaG91dVpjdFNJQXRLOTVhVnNGeTNuWkk3UFU2c01sWjNPRG5iWEpORgpMQkYwemYxYVIrdTk4Y2ZFWEIxWFJneWVJajNTdUNiQVZSNjFZY0h5NEZTNmdRMzhkR2FkalFnNlN4QWZyUlpaCkR5dEoyL3YzdmJCNFFiYVdZOHNOTDBxRVpjUGQ1eHZVTldQOVZibnZlVW1OZXBhbllabXJGV3dGMlE3V1dnZWgKVUp6dDV2ZzFENVRUcnE0eDZ1aUVML3lDZXFjaU8vSFJISTdwRk13WnlFWTYySnNONE5CejkybWYKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
          tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR1VENDQXFHZ0F3SUJBZ0lSQU16QkJzcHV0Smg2bHE5TklEOHhmUmt3RFFZSktvWklodmNOQVFFTEJRQXcKTFRFck1Da0dBMVVFQXhNaWJHOWpZV3d0YTNWaVpYSnVaWFJsY3kxaFkyTmxjM010WjJGMFpYZGhlUzFqWVRBZQpGdzB5TlRFd01Ea3dOVEUwTXpsYUZ3MHlOVEV3TURrd05qRTBNemxhTUVJeEVUQVBCZ05WQkFvVENGUjNhVzVuCllYUmxNUzB3S3dZRFZRUURFeVJyZFdKbGNtNWxkR1Z6TG1SbFptRjFiSFF1YzNaakxtTnNkWE4wWlhJdWJHOWoKWVd3d2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUURlTFUxVjhtODV4eStTTlY1WApMa3M0N1hvNnZXOTlvaVBPcTJtS0dScDZhUlFkcVl1U3lDdmlSS1NjRkFlSElwY2lqY1diR0NFWUZ4Ull0VjNsCnplZHM2SEkxUzUvcGYwbG82b2k5dDRCaWFId0svbjdYZW96QitlT1JRSmgzM2Z3NnBGby9Nenc4WndUcXBPMjEKcFo0U1RyaHlnbzZZaENHR0l2Y3FlSE9TcUtkTHZMRzltSktCdFJVcUZpRmZ1T2orcHRKYmhiWmVaRldKdzVCYgpKWEpWZit6M29CeUF2NExjRkhPdGJjbTVpUmM2TTZyT1JNN1BSczFuOWpwTmxZOHdPODdmRGRWK282eEJmemxZCjFKYzZsdmxIRDdib0NwVWFidFpSaGdnem5NYitnTzJQZ1l3MnhLR1BCbXYrRVBEUkEwKy91VU45djIrT0FJUS8KS0dpbEFnTUJBQUdqZ2I0d2dic3dEZ1lEVlIwUEFRSC9CQVFEQWdXZ01Bd0dBMVVkRXdFQi93UUNNQUF3SHdZRApWUjBqQkJnd0ZvQVVoNlhEQ1ZkeUJMK1NNVmh5R01KaGd5emhBS2d3ZWdZRFZSMFJCSE13Y1lJS2EzVmlaWEp1ClpYUmxjNElTYTNWaVpYSnVaWFJsY3k1a1pXWmhkV3gwZ2hacmRXSmxjbTVsZEdWekxtUmxabUYxYkhRdWMzWmoKZ2lScmRXSmxjbTVsZEdWekxtUmxabUYxYkhRdWMzWmpMbU5zZFhOMFpYSXViRzlqWVd5Q0VXeHZZMkZzTFdOcwpkWE4wWlhJdWFXNTBNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUUJrOFhuUkQ5QURHOGxqK09WOURiWGtWbFBaClYwVFY4TFRBR1FhbnhpVGQ5VFFDOTNmRVZFSkJXV2RPNGNBdENVc0p3UjFSN0Rqam1nNGs5UmRHc0g5ZXlwVTQKSmRRSlV6QzlYTXJDNTQ1ZXNaVkh2V1ZhaWZUWWwwTyt4cHlJM0ZhTWQyZloxT1Vydk5mMmVFckdsTk80ZzRwOQpMTGlMaDR6eThpVVZmbktkaFRSTUlVNHcvSUlHSTV1S0ZKTHZKZzkwRDdXMnVSNkl6Sm5QRCt4ZFRkT3JkdnlrCmlFbncwc2lTYnlxaWVZSk40MjBFOVJBRDZRMTRiQ1gwUi85amRWNit6N2wvRGZicVp5TkFlVEROMkxlQ2Vwc0oKYlZ1R2RiQmEybkpobDBPVzNVNEdVVS8xMnBXUitBUkRXaUVoMEJLOEZySkVPcjh0dmd4eWxkZ3BWWWc4Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
          tls.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBM2kxTlZmSnZPY2N2a2pWZVZ5NUxPTzE2T3IxdmZhSWp6cXRwaWhrYWVta1VIYW1MCmtzZ3I0a1NrbkJRSGh5S1hJbzNGbXhnaEdCY1VXTFZkNWMzbmJPaHlOVXVmNlg5SmFPcUl2YmVBWW1oOEN2NSsKMTNxTXdmbmprVUNZZDkzOE9xUmFQek04UEdjRTZxVHR0YVdlRWs2NGNvS09tSVFoaGlMM0tuaHprcWluUzd5eAp2WmlTZ2JVVktoWWhYN2pvL3FiU1c0VzJYbVJWaWNPUVd5VnlWWC9zOTZBY2dMK0MzQlJ6clczSnVZa1hPak9xCnprVE96MGJOWi9ZNlRaV1BNRHZPM3czVmZxT3NRWDg1V05TWE9wYjVSdysyNkFxVkdtN1dVWVlJTTV6Ry9vRHQKajRHTU5zU2hqd1pyL2hEdzBRTlB2N2xEZmI5dmpnQ0VQeWhvcFFJREFRQUJBb0lCQUNEYldrQ0hwZU5KamNOMQptUW9Ua3BSTXFuTGRhUXVQV3ZSSmJVWTdDQ3RxTnN0Y000UDFqbWZiOXV3T0dqN2w0cXY5ZzJlNFhjeU9QVGdSCk9sMnQ0YmU5ZUlaaE5MajNWZ2ZxQjJibktGbGxVbExkNkN3OXQydElaVnNwem1LTHRhMkdlTUkzOVlTSlI3VGIKeHp2QnptcXVzYUJkcG5EdnVYVjQza3l0bTRub21LcXp4aW12NXNIcE5yakJiWWExeVFLUjNPR1VUb3JsdSttdQp3cW03enRraDdXbFBoNENFcVFibytSZmJ6dUNKd2pWMXRiSDhpQTFmdDRkckd0dC9rRmhnKytZa3BmSi9sb1hXCkxodlVwdTdDL0Z3enVpWFA5V2VpMkVjbnd3b3lPNFVBcTk5VWFNN1BFUWlzZG5QQzNUZ0tlN2pEeE1NaTVZZXQKNEpubS9kRUNnWUVBNzlNR3VSVDR3VVlpdmhLYXRWdFdhWkNtQjZSckRia1hITGl4Y2lPV3MxZTVtN201aU1VVQphZWlMaGU3bGFZNm1qRTF1UGVLbEh6OVB3bkUxTWM2a1lZdmc1QzYvZUpsaE0wbGMraU9kWUlHN3hCVzFRWkY0CjU5WkFEVWQxeVFva0lnQlBJNDJyRjQ1RHhFa1lOWU81ZmFBdW5ZYmQ0Ni9ZSVY4M1BtUEdRbWNDZ1lFQTdTbVEKY1BYTmpjY0pMelZGeTRaYmlEQ0t5bW03NGorTXBWYkNJUE56ZU0vbWVZUWl4MHFDS3lLYWtxWC9SUnhrdmQ3dQp3akQ2ejd5T29mZHNqaTl0SFY5dSs5UGxxRC9lMEU3QWFhQ3kzSjFWNVR2cW5Ud1prWmg4K0wzOXpnOXlYWmRJClJUTXJ0d2VZYmV1cGo0bldocWozcklsZy9JU3h1SjAxNE1CenpSTUNnWUJRMjRWWXdZbGRJSmgySFMrc0ZhOTgKeUJneVcyejhvM3IzWkEzdnZiQUJwNEljenZHTysyTjJrY0Q0MXlMaUJBYURKMWdUNVdabXNxSGhuT21pY1ZsYQp5aDU0MElvZHp4akdnZVduTUhyUEh1NS9uaElPbVUxNlhQSWJpQXhlUzkwQzJiZlU5TjdLZ2x5MndTNDRYTUVkCmFmUk5pRHNubVJIMXJuU2h4R0lENFFLQmdRREF6NWJuejE3alVock1iNUlqeWtMbU1SalZRU3NINE1TV3N6YzIKbE5hZk5ON2FraXU0UElJaFVZdTdpQXRHQTdSL2pSd3RjcWFtZDFTNnB5NXhWbXR1Z3VUM0JhbmpwTEdnUnpZMQphZm1nVktXOXJYMnJnVzRFS2FZSWtHWWt2ZmdyME05bnV4ZGlRV0dTbEJLUmFPMnBJdnZoSVB0aHNQdlA3TGdkCjFqa1BVd0tCZ1FESVNRZGlUWW1HTkdaS2dSa2hoOFZndm1WZUJVdy82bEJzNnVzMEMzM2NkYWpJbGtYZ3lEOEMKZHJ0a2QvUXdBeDBCcmliZWxCUzl2VVhNOFZIUlJwZzFqVy9yTHpKTzhBc2g0Q1ZCSG55eXFnb2hwdC9iV0RXQQo4bkhRdHViY2JpOGE3OFhuM3krOXRKVnMyWllGYjNzOWRGNCt2SHYveDk4c0dSRityOTg3MWc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
    """

    CA_CERT = r"-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIQCusAnz9lDpg1cwyNheSN9TANBgkqhkiG9w0BAQsFADAt\nMSswKQYDVQQDEyJsb2NhbC1rdWJlcm5ldGVzLWFjY2Vzcy1nYXRld2F5LWNhMB4X\nDTI1MTAwODE1MzI0N1oXDTI2MDEwNjE1MzI0N1owLTErMCkGA1UEAxMibG9jYWwt\na3ViZXJuZXRlcy1hY2Nlc3MtZ2F0ZXdheS1jYTCCASIwDQYJKoZIhvcNAQEBBQAD\nggEPADCCAQoCggEBAOvSFQGMz6mFxX0UCqsdMfL1KaPu+GRikLdD2LiC87Wi+uwu\nr9qi+R71NwTWxqaRxvepNsW0adF+v8gwG76nJju6Kwo5Uw3q0Ih7Yjxqql7KZxbe\nCL3BXK8muoJnNrRkz32CLSXj6TQsYrSFqFZmnNI/fkhQOvhXo9JWmhlnav6X+RDe\nagjsoDwedWbvyvndzTwVhuRBGECzXESGRAy2GUk5z1y65f3MP7NV+u0Z0vNw0KRk\nQrcST05WKyEfXeJC8s5s6YVosdMqFtsgWkO847MNGvXsMrctS7XMRGMy4pUIzTB5\ntr+ra4Cde60dZM4sI83/Vhznu9zxbuAFLdU6GFMCAwEAAaNCMEAwDgYDVR0PAQH/\nBAQDAgKkMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFIelwwlXcgS/kjFYchjC\nYYMs4QCoMA0GCSqGSIb3DQEBCwUAA4IBAQAI6WrbS06LGqD9xT7SnxXf9zbT+Dhj\n6ChXNosR8BJ6xD/v0SsDWvn6GHxV4dGzarpU7Q9JK3Gv6Rarbz3j+Sk27b61Df6k\nDc5AD77XQIZ/911Rn+pY7syFhouuZctSIAtK95aVsFy3nZI7PU6sMlZ3ODnbXJNF\nLBF0zf1aR+u98cfEXB1XRgyeIj3SuCbAVR61YcHy4FS6gQ38dGadjQg6SxAfrRZZ\nDytJ2/v3vbB4QbaWY8sNL0qEZcPd5xvUNWP9VbnveUmNepanYZmrFWwF2Q7WWgeh\nUJzt5vg1D5TTrq4x6uiEL/yCeqciO/HRHI7pFMwZyEY62JsN4NBz92mf\n-----END CERTIFICATE-----"

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(SECRET_OBJ)
        kubectl_wait_to_exist("Secret", secret_name)

        kubectl_apply(OBJ)
        created_object = kubectl_wait_object_handler_success("tgr", unique_resource_name, "twingate_resource_create")

        # Update the CA cert
        kubectl_apply(OBJ_UPDATED)
        updated_object = kubectl_wait_object_handler_success("tgr", unique_resource_name, "twingate_resource_update")
        assert "certificateAuthorityCertSecretRef" in updated_object["spec"]["proxy"]
        assert updated_object["spec"]["proxy"]["certificateAuthorityCertSecretRef"]["name"] == secret_name

        kubectl_delete_wait("tgr", unique_resource_name)
        kubectl_delete_wait("Secret", secret_name)

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)

    # fmt: off

    assert "twingate_resource_create" in created_object["status"], f"status not updated: {created_object['status']}"

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    expected_object = {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name, "uid": ANY, "namespace": "default"}

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert twingate_id

    # Update
    assert {"message": f"Updating resource {twingate_id}", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert_log_message_contains(logs, CA_CERT)

    # Delete
    assert {"message": "Twingate API Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "taskName": ANY, "severity": "info"} in logs

    # fmt: on


def test_resource_created_before_operator_runs(run_kopf, unique_resource_name):
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    kubectl_create(OBJ)

    # Make sure no `status` as kopf isnt running yet
    created_object = kubectl_wait_to_exist("tgr", unique_resource_name)
    assert "status" not in created_object

    # fmt: off
    with run_kopf() as runner:
        created_object = kubectl_wait_object_handler_success("tgr", unique_resource_name, "twingate_resource_create")
        assert created_object["spec"]["id"] is not None
        kubectl_delete_wait("tgr", unique_resource_name)


    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    logs = load_stdout(runner.stdout)

    # fmt: off

    expected_object =  {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name, "uid": ANY, "namespace": "default"}

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert twingate_id

    # Delete
    assert {"message": "Twingate API Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "taskName": ANY, "object": expected_object, "severity": "info"} in logs

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "taskName": ANY, "severity": "info"} in logs

    # fmt: on


ACCESS_OBJECTS = {
    "OBJ_ACCESS_BY_PRINCIPAL_ID": """
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {resource_name}
        spec:
          resourceRef:
            name: {resource_name}
          principalId: {principal_id}
    """,
    "OBJ_ACCESS_BY_PRINCIPAL_NAME_GROUP": """
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {resource_name}
        spec:
          resourceRef:
            name: {resource_name}
          principalExternalRef:
            type: group
            name: "{principal_name}"
    """,
    "OBJ_ACCESS_BY_PRINCIPAL_NAME_SA": """
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {resource_name}
        spec:
          resourceRef:
            name: {resource_name}
          principalExternalRef:
            type: serviceAccount
            name: "{principal_name}"
    """,
    "OBJ_ACCESS_BY_GROUPREF": """
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {resource_name}
        spec:
          resourceRef:
            name: {resource_name}
          groupRef:
            name: "test-group"
    """,
}


@pytest.mark.parametrize(
    "access_object_yaml_tmpl_name",
    [
        "OBJ_ACCESS_BY_PRINCIPAL_ID",
        "OBJ_ACCESS_BY_PRINCIPAL_NAME_GROUP",
        "OBJ_ACCESS_BY_PRINCIPAL_NAME_SA",
        "OBJ_ACCESS_BY_GROUPREF",
    ],
)
def test_resource_access_flows(
    access_object_yaml_tmpl_name, run_kopf, unique_resource_name
):
    assert "TWINGATE_TEST_PRINCIPAL_ID" in os.environ
    principal_id = os.environ["TWINGATE_TEST_PRINCIPAL_ID"]
    princiapl_name = "test_resource_access_flows"

    RESOURCE_OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    GROUP_OBJ = """
        apiVersion: twingate.com/v1beta
        kind: TwingateGroup
        metadata:
          name: test-group
        spec:
            name: Test Group
    """

    access_object_yaml_tmpl = ACCESS_OBJECTS[access_object_yaml_tmpl_name]
    access_object_yaml = access_object_yaml_tmpl.format(
        resource_name=unique_resource_name,
        principal_id=principal_id,
        principal_name=princiapl_name,
    )

    # fmt: off
    with run_kopf(enable_connector_reconciler=False) as runner:
        kubectl_create(RESOURCE_OBJ)
        kubectl_create(GROUP_OBJ)

        # Make sure resource is created
        resource = kubectl_wait_object_handler_success("tgr", unique_resource_name, "twingate_resource_create") # fmt: skip
        group = kubectl_wait_object_handler_success("tgg", "test-group", "twingate_group_create_update") # fmt: skip
        assert resource["spec"]["id"] is not None
        assert group["spec"]["id"] is not None

        kubectl_create(access_object_yaml)
        access = kubectl_wait_object_handler_success("tacc", unique_resource_name, "twingate_resource_access_change")  # fmt: skip
        assert access["status"]["twingate_resource_access_change"]["resource_id"] == resource["spec"]["id"]

        kubectl_delete_wait("tacc", unique_resource_name)
        kubectl_delete_wait("tgr", unique_resource_name)
        kubectl_delete_wait("tgg", "test-group")

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)

    expected_object = {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResourceAccess",
        "name": unique_resource_name,
        "uid": ANY,
        "namespace": "default",
    }

    # Create
    assert {
        "message": "Handler 'twingate_resource_access_change' succeeded.",
        "timestamp": ANY,
        "taskName": ANY,
        "object": expected_object,
        "severity": "info",
    } in logs

    # Delete
    assert {
        "message": "Twingate API Result: {'resourceAccessRemove': {'ok': True, 'error': None}}",
        "object": expected_object,
        "timestamp": ANY,
        "taskName": ANY,
        "severity": "info",
    } in logs
    assert {
        "message": "Handler 'twingate_resource_access_delete' succeeded.",
        "timestamp": ANY,
        "taskName": ANY,
        "object": expected_object,
        "severity": "info",
    } in logs

    # Shutdown
    assert {
        "message": "Activity 'shutdown' succeeded.",
        "timestamp": ANY,
        "taskName": ANY,
        "severity": "info",
    } in logs
