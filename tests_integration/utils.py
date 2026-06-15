import datetime
import os
import subprocess
import time
from base64 import b64encode

import orjson as json
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509.oid import NameOID

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


def generate_base64_ca_cert(common_name: str = "Test CA") -> str:
    key = ed25519.Ed25519PrivateKey.generate()
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    now = datetime.datetime.now(datetime.UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, None)
    )
    return b64encode(cert.public_bytes(Encoding.PEM)).decode()


def create_tls_secret(secret_name, base64_ca_cert):
    # The operator only reads `ca.crt`; tls.crt/tls.key are dummy values required
    # by the `kubernetes.io/tls` Secret type.
    return f"""
    apiVersion: v1
    kind: Secret
    metadata:
      name: {secret_name}
      namespace: default
    type: kubernetes.io/tls
    data:
      ca.crt: {base64_ca_cert}
      tls.crt: ZHVtbXk=
      tls.key: ZHVtbXk=
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
