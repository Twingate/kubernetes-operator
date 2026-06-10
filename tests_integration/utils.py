import os
import subprocess
import time

import orjson as json

KUBECTL_COMMAND = os.environ.get("KUBECTL_COMMAND", "kubectl")

# ruff: noqa: S602 (subprocess_popen_with_shell_equals_true)


def load_stdout(stdout):
    return [json.loads(line) for line in stdout.split("\n") if line]


def assert_log_message_starts_with(logs, message):
    assert any(log["message"].startswith(message) for log in logs), (
        f"Could not find log message starting with '{message}'"
    )


def assert_log_message_contains(logs, message):
    assert any(message in log["message"] for log in logs), (
        f"Could not find log message containing '{message}'"
    )


def create_tls_secret(secret_name, base64_ca_cert):
    return f"""
    apiVersion: v1
    kind: Secret
    metadata:
      name: {secret_name}
      namespace: default
    type: kubernetes.io/tls
    data:
      ca.crt: {base64_ca_cert}
      tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR1VENDQXFHZ0F3SUJBZ0lSQU16QkJzcHV0Smg2bHE5TklEOHhmUmt3RFFZSktvWklodmNOQVFFTEJRQXcKTFRFck1Da0dBMVVFQXhNaWJHOWpZV3d0YTNWaVpYSnVaWFJsY3kxaFkyTmxjM010WjJGMFpYZGhlUzFqWVRBZQpGdzB5TlRFd01Ea3dOVEUwTXpsYUZ3MHlOVEV3TURrd05qRTBNemxhTUVJeEVUQVBCZ05WQkFvVENGUjNhVzVuCllYUmxNUzB3S3dZRFZRUURFeVJyZFdKbGNtNWxkR1Z6TG1SbFptRjFiSFF1YzNaakxtTnNkWE4wWlhJdWJHOWoKWVd3d2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUURlTFUxVjhtODV4eStTTlY1WApMa3M0N1hvNnZXOTlvaVBPcTJtS0dScDZhUlFkcVl1U3lDdmlSS1NjRkFlSElwY2lqY1diR0NFWUZ4Ull0VjNsCnplZHM2SEkxUzUvcGYwbG82b2k5dDRCaWFId0svbjdYZW96QitlT1JRSmgzM2Z3NnBGby9Nenc4WndUcXBPMjEKcFo0U1RyaHlnbzZZaENHR0l2Y3FlSE9TcUtkTHZMRzltSktCdFJVcUZpRmZ1T2orcHRKYmhiWmVaRldKdzVCYgpKWEpWZit6M29CeUF2NExjRkhPdGJjbTVpUmM2TTZyT1JNN1BSczFuOWpwTmxZOHdPODdmRGRWK282eEJmemxZCjFKYzZsdmxIRDdib0NwVWFidFpSaGdnem5NYitnTzJQZ1l3MnhLR1BCbXYrRVBEUkEwKy91VU45djIrT0FJUS8KS0dpbEFnTUJBQUdqZ2I0d2dic3dEZ1lEVlIwUEFRSC9CQVFEQWdXZ01Bd0dBMVVkRXdFQi93UUNNQUF3SHdZRApWUjBqQkJnd0ZvQVVoNlhEQ1ZkeUJMK1NNVmh5R01KaGd5emhBS2d3ZWdZRFZSMFJCSE13Y1lJS2EzVmlaWEp1ClpYUmxjNElTYTNWaVpYSnVaWFJsY3k1a1pXWmhkV3gwZ2hacmRXSmxjbTVsZEdWekxtUmxabUYxYkhRdWMzWmoKZ2lScmRXSmxjbTVsZEdWekxtUmxabUYxYkhRdWMzWmpMbU5zZFhOMFpYSXViRzlqWVd5Q0VXeHZZMkZzTFdOcwpkWE4wWlhJdWFXNTBNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUUJrOFhuUkQ5QURHOGxqK09WOURiWGtWbFBaClYwVFY4TFRBR1FhbnhpVGQ5VFFDOTNmRVZFSkJXV2RPNGNBdENVc0p3UjFSN0Rqam1nNGs5UmRHc0g5ZXlwVTQKSmRRSlV6QzlYTXJDNTQ1ZXNaVkh2V1ZhaWZUWWwwTyt4cHlJM0ZhTWQyZloxT1Vydk5mMmVFckdsTk80ZzRwOQpMTGlMaDR6eThpVVZmbktkaFRSTUlVNHcvSUlHSTV1S0ZKTHZKZzkwRDdXMnVSNkl6Sm5QRCt4ZFRkT3JkdnlrCmlFbncwc2lTYnlxaWVZSk40MjBFOVJBRDZRMTRiQ1gwUi85amRWNit6N2wvRGZicVp5TkFlVEROMkxlQ2Vwc0oKYlZ1R2RiQmEybkpobDBPVzNVNEdVVS8xMnBXUitBUkRXaUVoMEJLOEZySkVPcjh0dmd4eWxkZ3BWWWc4Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
      tls.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBM2kxTlZmSnZPY2N2a2pWZVZ5NUxPTzE2T3IxdmZhSWp6cXRwaWhrYWVta1VIYW1MCmtzZ3I0a1NrbkJRSGh5S1hJbzNGbXhnaEdCY1VXTFZkNWMzbmJPaHlOVXVmNlg5SmFPcUl2YmVBWW1oOEN2NSsKMTNxTXdmbmprVUNZZDkzOE9xUmFQek04UEdjRTZxVHR0YVdlRWs2NGNvS09tSVFoaGlMM0tuaHprcWluUzd5eAp2WmlTZ2JVVktoWWhYN2pvL3FiU1c0VzJYbVJWaWNPUVd5VnlWWC9zOTZBY2dMK0MzQlJ6clczSnVZa1hPak9xCnprVE96MGJOWi9ZNlRaV1BNRHZPM3czVmZxT3NRWDg1V05TWE9wYjVSdysyNkFxVkdtN1dVWVlJTTV6Ry9vRHQKajRHTU5zU2hqd1pyL2hEdzBRTlB2N2xEZmI5dmpnQ0VQeWhvcFFJREFRQUJBb0lCQUNEYldrQ0hwZU5KamNOMQptUW9Ua3BSTXFuTGRhUXVQV3ZSSmJVWTdDQ3RxTnN0Y000UDFqbWZiOXV3T0dqN2w0cXY5ZzJlNFhjeU9QVGdSCk9sMnQ0YmU5ZUlaaE5MajNWZ2ZxQjJibktGbGxVbExkNkN3OXQydElaVnNwem1LTHRhMkdlTUkzOVlTSlI3VGIKeHp2QnptcXVzYUJkcG5EdnVYVjQza3l0bTRub21LcXp4aW12NXNIcE5yakJiWWExeVFLUjNPR1VUb3JsdSttdQp3cW03enRraDdXbFBoNENFcVFibytSZmJ6dUNKd2pWMXRiSDhpQTFmdDRkckd0dC9rRmhnKytZa3BmSi9sb1hXCkxodlVwdTdDL0Z3enVpWFA5V2VpMkVjbnd3b3lPNFVBcTk5VWFNN1BFUWlzZG5QQzNUZ0tlN2pEeE1NaTVZZXQKNEpubS9kRUNnWUVBNzlNR3VSVDR3VVlpdmhLYXRWdFdhWkNtQjZSckRia1hITGl4Y2lPV3MxZTVtN201aU1VVQphZWlMaGU3bGFZNm1qRTF1UGVLbEh6OVB3bkUxTWM2a1lZdmc1QzYvZUpsaE0wbGMraU9kWUlHN3hCVzFRWkY0CjU5WkFEVWQxeVFva0lnQlBJNDJyRjQ1RHhFa1lOWU81ZmFBdW5ZYmQ0Ni9ZSVY4M1BtUEdRbWNDZ1lFQTdTbVEKY1BYTmpjY0pMelZGeTRaYmlEQ0t5bW03NGorTXBWYkNJUE56ZU0vbWVZUWl4MHFDS3lLYWtxWC9SUnhrdmQ3dQp3akQ2ejd5T29mZHNqaTl0SFY5dSs5UGxxRC9lMEU3QWFhQ3kzSjFWNVR2cW5Ud1prWmg4K0wzOXpnOXlYWmRJClJUTXJ0d2VZYmV1cGo0bldocWozcklsZy9JU3h1SjAxNE1CenpSTUNnWUJRMjRWWXdZbGRJSmgySFMrc0ZhOTgKeUJneVcyejhvM3IzWkEzdnZiQUJwNEljenZHTysyTjJrY0Q0MXlMaUJBYURKMWdUNVdabXNxSGhuT21pY1ZsYQp5aDU0MElvZHp4akdnZVduTUhyUEh1NS9uaElPbVUxNlhQSWJpQXhlUzkwQzJiZlU5TjdLZ2x5MndTNDRYTUVkCmFmUk5pRHNubVJIMXJuU2h4R0lENFFLQmdRREF6NWJuejE3alVock1iNUlqeWtMbU1SalZRU3NINE1TV3N6YzIKbE5hZk5ON2FraXU0UElJaFVZdTdpQXRHQTdSL2pSd3RjcWFtZDFTNnB5NXhWbXR1Z3VUM0JhbmpwTEdnUnpZMQphZm1nVktXOXJYMnJnVzRFS2FZSWtHWWt2ZmdyME05bnV4ZGlRV0dTbEJLUmFPMnBJdnZoSVB0aHNQdlA3TGdkCjFqa1BVd0tCZ1FESVNRZGlUWW1HTkdaS2dSa2hoOFZndm1WZUJVdy82bEJzNnVzMEMzM2NkYWpJbGtYZ3lEOEMKZHJ0a2QvUXdBeDBCcmliZWxCUzl2VVhNOFZIUlJwZzFqVy9yTHpKTzhBc2g0Q1ZCSG55eXFnb2hwdC9iV0RXQQo4bkhRdHViY2JpOGE3OFhuM3krOXRKVnMyWllGYjNzOWRGNCt2SHYveDk4c0dSRityOTg3MWc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
"""


def kubectl(command: str, input: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        f"{KUBECTL_COMMAND} {command}",
        shell=True,
        check=True,
        timeout=10,
        capture_output=True,
        input=input.encode() if input else None,
    )


def kubectl_create(obj: str) -> subprocess.CompletedProcess:
    return kubectl("create -f -", input=obj)


def kubectl_apply(obj: str) -> subprocess.CompletedProcess:
    return kubectl("apply -f -", input=obj)


def kubectl_delete(
    resource_type: str, resource_name: str, *, force: bool = False
) -> subprocess.CompletedProcess:
    if force:
        patch_str = '{"metadata":{"finalizers":null}}'
        kubectl(
            f"kubectl patch {resource_type}/{resource_name} -p '{patch_str}' --type=merge"
        )

    return kubectl(f"delete {resource_type}/{resource_name}")


def kubectl_get(resource_type: str, resource_name: str) -> dict:
    result = kubectl(f"get {resource_type}/{resource_name} -o json")
    return json.loads(result.stdout)


def kubectl_patch(
    resource: str, patch: dict | list, merge_type: str = "merge"
) -> subprocess.CompletedProcess:
    patch_str = json.dumps(patch).decode()
    return kubectl(f"patch {resource} -p '{patch_str}' --type={merge_type}")


def kubectl_wait_to_exist(
    resource_type: str, resource_name: str, max_retries: int = 5
) -> dict:
    retry = 0
    while True:
        try:
            return kubectl_get(resource_type, resource_name)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # ruff: noqa: PERF203
            retry += 1
            if retry > max_retries:
                raise
            time.sleep(5)


def kubectl_delete_wait(
    resource_type: str,
    resource_name: str,
    *,
    force: bool = False,
    max_retries: int = 10,
    sleep_time: int = 5,
    perform_deletion: bool = True,
) -> None:
    if perform_deletion:
        kubectl_delete(resource_type, resource_name, force=force)

    retry = 0
    while True:
        try:
            kubectl_get(resource_type, resource_name)
        except subprocess.CalledProcessError:
            return
        except subprocess.TimeoutExpired:
            pass

        retry += 1
        if retry > max_retries:
            raise
        time.sleep(sleep_time)


def kubectl_wait_pod_status(
    pod_name: str, expected_status: str, max_retries: int = 10
) -> dict:
    retry = 0
    latest_status = None
    while True:
        try:
            pod = kubectl_get("pod", pod_name)
            latest_status = pod["status"]["phase"]
            if latest_status == expected_status:
                return pod
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass

        retry += 1
        if retry > max_retries:
            raise RuntimeError(
                f"Pod {pod_name} did not reach status {expected_status}. Last status is {latest_status}"
            )
        time.sleep(5)


def kubectl_wait_pod_running(pod_name: str, max_retries: int = 10) -> dict:
    return kubectl_wait_pod_status(pod_name, "Running", max_retries=max_retries)


def kubectl_wait_deployment_available(
    deployment_name: str, *, max_retries: int = 5
) -> dict:
    retry = 0
    while True:
        try:
            result = kubectl(
                f"wait --for=condition=available --timeout=60s deployment/{deployment_name} -o json"
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass

        retry += 1
        if retry > max_retries:
            raise RuntimeError(f"Deployment {deployment_name} isn't available")
        time.sleep(5)


def kubectl_wait_object_handler_success(
    resource_type: str,
    resource_name: str,
    handler_name: str,
    *,
    message: str | None = None,
    max_retries: int = 5,
):
    retry = 0
    obj = kubectl_wait_to_exist(resource_type, resource_name, max_retries=max_retries)
    while True:
        handler_status = obj.get("status", {}).get(handler_name, {})
        if handler_status.get("success") and (
            message is None or handler_status.get("message") == message
        ):
            return obj

        retry += 1
        if retry > max_retries:
            raise RuntimeError(
                f"Handler {handler_name} did not succeed for {resource_type}/{resource_name}"
            )
        time.sleep(10)
        obj = kubectl_get(resource_type, resource_name)
