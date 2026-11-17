import datetime as dt
import os
import subprocess
import time
from base64 import b64encode
from collections.abc import Callable

import orjson as json
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509.oid import NameOID

KUBECTL_COMMAND = os.environ.get("KUBECTL_COMMAND", "kubectl")

DEFAULT_TIMEOUT = 10

# Deletes block until the operator's delete handlers have round-tripped the
# Twingate API and dropped their finalizers, which can take far longer than a
# plain read. Used for bulk cleanup deletes.
DELETE_TIMEOUT = 60

# Polling cadence for the wait helpers below. What they wait on is typically a
# single Twingate API round-trip (~1-2s), so poll sub-second at first and back
# off. Both are overridable, so a test that starts failing can be re-run at the
# old coarse granularity to tell a real race from a polling artifact:
#   TG_TEST_POLL_MIN_INTERVAL=10 TG_TEST_POLL_MAX_INTERVAL=10 make test-int
POLL_MIN_INTERVAL = float(os.environ.get("TG_TEST_POLL_MIN_INTERVAL", "0.3"))
POLL_MAX_INTERVAL = float(os.environ.get("TG_TEST_POLL_MAX_INTERVAL", "2.0"))
POLL_BACKOFF = 1.6

# Deadlines are >= the worst case of the retry-count budgets they replace. That
# worst case is not just the sleeps: every iteration also ran a kubectl
# subprocess that could burn DEFAULT_TIMEOUT before raising, so for N retries it
# is (N + 1) * DEFAULT_TIMEOUT + N * sleep_time. These deadlines cover both, so a
# slow cluster keeps at least the tolerance it had:
#   wait_object    5 retries x 10s sleep -> 6*10 + 5*10 = 110s
#   delete_wait   10 retries x  5s sleep -> 11*10 + 10*5 = 160s
#   wait_to_exist  5 retries x  5s sleep -> 6*10 + 5*5  =  85s
# They bound failures only - a passing wait returns as soon as its predicate does.
WAIT_OBJECT_TIMEOUT = 120
DELETE_WAIT_TIMEOUT = 180
WAIT_TO_EXIST_TIMEOUT = 90
# Connector deployments pull an image and wait on a /connectorctl health probe,
# so genuine availability can take far longer than the other waits.
DEPLOYMENT_TIMEOUT = 120

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
    now = dt.datetime.now(dt.UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + dt.timedelta(days=365))
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


def kubectl(
    command: str, input: str | None = None, *, timeout: int = DEFAULT_TIMEOUT
) -> subprocess.CompletedProcess:
    return subprocess.run(
        f"{KUBECTL_COMMAND} {command}",
        shell=True,
        check=True,
        timeout=timeout,
        capture_output=True,
        input=input.encode() if input else None,
    )


def kubectl_create(obj: str) -> subprocess.CompletedProcess:
    return kubectl("create -f -", input=obj)


def kubectl_apply(obj: str) -> subprocess.CompletedProcess:
    return kubectl("apply -f -", input=obj)


def kubectl_delete(
    resource_type: str, resource_name: str
) -> subprocess.CompletedProcess:
    # kubectl delete defaults to --wait=true, so this blocks until the operator's
    # delete handler has round-tripped the Twingate API and dropped its finalizer.
    # That is not comparable to a plain read, hence DELETE_TIMEOUT rather than the
    # default: under the 10s default this is killed mid-delete and surfaces as a
    # TimeoutExpired escaping the caller's retry loop.
    return kubectl(f"delete {resource_type}/{resource_name}", timeout=DELETE_TIMEOUT)


def kubectl_get(resource_type: str, resource_name: str) -> dict:
    result = kubectl(f"get {resource_type}/{resource_name} -o json")
    return json.loads(result.stdout)


def kubectl_patch(
    resource: str, patch: dict | list, merge_type: str = "merge"
) -> subprocess.CompletedProcess:
    patch_str = json.dumps(patch).decode()
    return kubectl(f"patch {resource} -p '{patch_str}' --type={merge_type}")


# kubectl errors that waiting will not fix. Polling through them would only turn
# a clear failure into a timeout minutes later.
_NON_TRANSIENT_KUBECTL_ERRORS = (b"(Forbidden)", b"doesn't have a resource type")


def poll_until[T](
    attempt: Callable[[], T | None],
    *,
    timeout: float,
    description: str,
    last_seen: Callable[[], object] | None = None,
) -> T:
    """Call ``attempt`` until it returns a non-``None`` value, or time out.

    ``attempt`` returns ``None`` to mean "not yet". A kubectl failure it raises
    (``CalledProcessError`` / ``TimeoutExpired``) also counts as "not yet" and is
    kept for the timeout error, except for non-transient errors such as
    Forbidden, which are re-raised right away.

    The interval starts at ``POLL_MIN_INTERVAL`` and grows towards
    ``POLL_MAX_INTERVAL``, with a floor proportional to the probe's own cost: CI
    runs with ``KUBECTL_COMMAND="minikube kubectl -- "``, where every invocation
    costs 200-500ms, and polling faster than that is pure exec overhead.

    On timeout, raises ``TimeoutError`` naming the last kubectl error and, if
    ``last_seen`` is given, the last state it reports.
    """
    deadline = time.monotonic() + timeout
    interval = POLL_MIN_INTERVAL
    last_exc: subprocess.SubprocessError | None = None

    while True:
        started = time.monotonic()
        try:
            result = attempt()
            last_exc = None
        except subprocess.CalledProcessError as e:
            if any(err in (e.stderr or b"") for err in _NON_TRANSIENT_KUBECTL_ERRORS):
                raise
            result, last_exc = None, e
        except subprocess.TimeoutExpired as e:
            result, last_exc = None, e
        if result is not None:
            return result
        probe_cost = time.monotonic() - started

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            message = (
                f"Timed out after {round(timeout, 1):g}s waiting for {description}"
            )
            if last_seen is not None:
                message += f"; last seen: {last_seen()!r}"
            if isinstance(last_exc, subprocess.CalledProcessError):
                stderr = (last_exc.stderr or b"").decode(errors="replace").strip()
                message += f"; last kubectl error: {stderr}"
            elif last_exc is not None:
                message += f"; last kubectl error: {last_exc}"
            raise TimeoutError(message) from last_exc

        time.sleep(min(max(interval, probe_cost / 2), POLL_MAX_INTERVAL, remaining))
        interval = min(interval * POLL_BACKOFF, POLL_MAX_INTERVAL)


def kubectl_wait_to_exist(
    resource_type: str, resource_name: str, *, timeout: float = WAIT_TO_EXIST_TIMEOUT
) -> dict:
    # poll_until treats the NotFound from kubectl_get as "not yet".
    return poll_until(
        lambda: kubectl_get(resource_type, resource_name),
        timeout=timeout,
        description=f"{resource_type}/{resource_name} to exist",
    )


def kubectl_delete_wait(
    resource_type: str,
    resource_name: str,
    *,
    timeout: float = DELETE_WAIT_TIMEOUT,
    perform_deletion: bool = True,
) -> None:
    deadline = time.monotonic() + timeout
    if perform_deletion:
        # --wait=false so the poll below covers the whole wait and `timeout` is
        # the total budget, rather than a blocking delete running first under
        # its own DELETE_TIMEOUT.
        kubectl(f"delete {resource_type}/{resource_name} --wait=false")

    def _attempt() -> bool | None:
        try:
            kubectl_get(resource_type, resource_name)
        except subprocess.CalledProcessError as e:
            # Only NotFound means gone. Any other failure (connection refused,
            # 5xx, ...) is re-raised for poll_until to retry, so a broken
            # kubectl can't make a deletion check pass.
            if b"(NotFound)" in (e.stderr or b""):
                return True
            raise
        return None

    poll_until(
        _attempt,
        timeout=max(0.0, deadline - time.monotonic()),
        description=f"{resource_type}/{resource_name} to be deleted",
    )


def kubectl_wait_deployment_available(
    deployment_name: str, *, timeout: float = DEPLOYMENT_TIMEOUT
) -> dict:
    deadline = time.monotonic() + timeout

    def _attempt() -> dict | None:
        remaining = max(1, int(deadline - time.monotonic()))
        # The subprocess budget must exceed kubectl's own --timeout, otherwise
        # the watch is killed and restarted before it can ever be used. A
        # failure here (not created yet - kubectl wait fails fast on a missing
        # object - or not available in time) is retried by poll_until.
        result = kubectl(
            f"wait --for=condition=available --timeout={remaining}s "
            f"deployment/{deployment_name} -o json",
            timeout=remaining + 10,
        )
        return json.loads(result.stdout)

    return poll_until(
        _attempt,
        timeout=timeout,
        description=f"deployment/{deployment_name} to become available",
    )


def kubectl_wait_object_handler_success(
    resource_type: str,
    resource_name: str,
    handler_name: str,
    *,
    message: str | None = None,
    timeout: float = WAIT_OBJECT_TIMEOUT,
):
    def _handler_succeeded(obj: dict) -> bool:
        handler_status = obj.get("status", {}).get(handler_name, {})
        return bool(handler_status.get("success")) and (
            message is None or handler_status.get("message") == message
        )

    return kubectl_wait_object(
        resource_type,
        resource_name,
        _handler_succeeded,
        description=f"handler '{handler_name}' success",
        timeout=timeout,
    )


def kubectl_wait_object(
    resource_type: str,
    resource_name: str,
    predicate: Callable[[dict], bool],
    *,
    description: str = "expected condition",
    timeout: float = WAIT_OBJECT_TIMEOUT,
) -> dict:
    """Poll an object until ``predicate(obj)`` is truthy, then return it.

    Polling sub-second is safe here because none of the Twingate CRDs declare a
    ``status`` subresource, so kopf writes spec, status, the handler result and
    its progress annotation in a single PATCH. There is no window in which a
    handler reads as successful before the spec it produced is visible. **If a
    status subresource is ever added to these CRDs, revisit every predicate.**
    """
    last_obj: dict | None = None

    def _attempt() -> dict | None:
        nonlocal last_obj
        last_obj = kubectl_get(resource_type, resource_name)
        return last_obj if predicate(last_obj) else None

    # poll_until tolerates the object being absent (kubectl_get raising
    # NotFound): it may not exist yet, and an operator that recreates an object
    # deletes it first, so it is briefly missing. This does not cover observing
    # the OLD generation while its finalizer still holds it - a predicate
    # spanning a recreate must itself require changed state.
    return poll_until(
        _attempt,
        timeout=timeout,
        description=f"{resource_type}/{resource_name} to reach {description}",
        last_seen=lambda: last_obj,
    )
