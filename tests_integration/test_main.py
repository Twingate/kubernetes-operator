import os
import subprocess
import time
from unittest.mock import ANY

import kopf
import orjson as json
import pytest
from kopf.testing import KopfRunner

# ruff: noqa: S602 (subprocess_popen_with_shell_equals_true)

main_py = os.path.relpath(os.path.join(os.path.dirname(__file__), "../main.py"))
kopf_runner_args = [
    "run",
    "--verbose",
    "--log-format=json",
    "-A",
    "--standalone",
    main_py,
]

kubectl_command = os.environ.get("KUBECTL_COMMAND", "kubectl")


def load_stdout(stdout):
    return [json.loads(line) for line in stdout.split("\n") if line]


def assert_log_message_starts_with(logs, message):
    assert any(
        log["message"].startswith(message) for log in logs
    ), f"Could not find log message starting with '{message}'"


def kubectl(command: str, input: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        f"{kubectl_command} {command}",
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


@pytest.fixture(scope="module")
def kopf_settings():
    settings = kopf.OperatorSettings()
    settings.watching.server_timeout = 10
    return settings


@pytest.mark.integration()
def test_resource_flows(kopf_settings):
    OBJ = """
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: my-twingate-resource
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    OBJ_UPDATED = """
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: my-twingate-resource
            spec:
              name: My K8S Resource Renamed
              address: my.default.cluster.local
        """

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(OBJ)
        time.sleep(5)  # give it some time to react

        created_object = json.loads(kubectl("get tgr/my-twingate-resource -o json").stdout)

        # Update the name
        kubectl_apply(OBJ_UPDATED)
        json.loads(kubectl("get tgr/my-twingate-resource -o json").stdout)

        delete_command = kubectl("delete tgr/my-twingate-resource")
        time.sleep(1)  # give it some time to react

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)
    for log in logs:
        print(log)

    # fmt: off

    assert "twingate_resource_create" in created_object["status"], f"status not updated: {created_object['status']}"

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": "my-twingate-resource", "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert twingate_id

    # Update
    assert {"message": f"Updating resource {twingate_id}", "timestamp": ANY, "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": "my-twingate-resource", "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert_log_message_starts_with(logs, f"Got resource id='{twingate_id}' name='My K8S Resource Renamed'")

    # Delete
    assert {"message": "Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": "my-twingate-resource", "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert delete_command.stdout == b'twingateresource.twingate.com "my-twingate-resource" deleted\n'

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "severity": "info"} in logs

    # fmt: on


@pytest.mark.integration()
def test_resource_created_before_operator_runs(kopf_settings):
    OBJ = """
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: my-twingate-resource
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    kubectl_create(OBJ)
    time.sleep(5)  # give it some time to react

    # Make sure no `status` as kopf isnt running yet
    created_object = json.loads(kubectl("get tgr/my-twingate-resource -o json").stdout)
    assert "status" not in created_object

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        time.sleep(5)  # give it some time to react
        created_object = json.loads(kubectl("get tgr/my-twingate-resource -o json").stdout)

        delete_command = kubectl("delete tgr/my-twingate-resource")
        time.sleep(1)  # give it some time to react

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    logs = load_stdout(runner.stdout)

    # fmt: off

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": "my-twingate-resource", "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert twingate_id

    # Delete
    assert {"message": "Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": "my-twingate-resource", "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert delete_command.stdout == b'twingateresource.twingate.com "my-twingate-resource" deleted\n'

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "severity": "info"} in logs

    # fmt: on
