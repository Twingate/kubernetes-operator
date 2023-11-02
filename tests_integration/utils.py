import os
import subprocess

import orjson as json

KUBECTL_COMMAND = os.environ.get("KUBECTL_COMMAND", "kubectl")

# ruff: noqa: S602 (subprocess_popen_with_shell_equals_true)


def load_stdout(stdout):
    return [json.loads(line) for line in stdout.split("\n") if line]


def assert_log_message_starts_with(logs, message):
    assert any(
        log["message"].startswith(message) for log in logs
    ), f"Could not find log message starting with '{message}'"


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
