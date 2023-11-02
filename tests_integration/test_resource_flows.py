import os
import time
from unittest.mock import ANY

import orjson as json
import pytest
from kopf.testing import KopfRunner

from .utils import (
    assert_log_message_starts_with,
    kubectl,
    kubectl_apply,
    kubectl_create,
    load_stdout,
)


@pytest.mark.integration()
def test_resource_flows(kopf_settings, kopf_runner_args, unique_resource_name):
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    OBJ_UPDATED = f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Resource Renamed
              address: my.default.cluster.local
        """

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(OBJ)
        time.sleep(5)  # give it some time to react

        created_object = json.loads(kubectl(f"get tgr/{unique_resource_name} -o json").stdout)

        # Update the name
        kubectl_apply(OBJ_UPDATED)
        json.loads(kubectl(f"get tgr/{unique_resource_name} -o json").stdout)

        delete_command = kubectl(f"delete tgr/{unique_resource_name}")
        time.sleep(1)  # give it some time to react

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)

    # fmt: off

    assert "twingate_resource_create" in created_object["status"], f"status not updated: {created_object['status']}"

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY,
            "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name,
                       "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert twingate_id

    # Update
    assert {"message": f"Updating resource {twingate_id}", "timestamp": ANY,
            "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name,
                       "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert_log_message_starts_with(logs, f"Got resource id='{twingate_id}' name='My K8S Resource Renamed'")

    # Delete
    assert {"message": "Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY,
            "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY,
            "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name,
                       "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert delete_command.stdout.decode() == f'twingateresource.twingate.com "{unique_resource_name}" deleted\n'

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "severity": "info"} in logs

    # fmt: on


@pytest.mark.integration()
def test_resource_created_before_operator_runs(
    kopf_settings, kopf_runner_args, unique_resource_name
):
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
    time.sleep(5)  # give it some time to react

    # Make sure no `status` as kopf isnt running yet
    created_object = json.loads(
        kubectl(f"get tgr/{unique_resource_name} -o json").stdout
    )
    assert "status" not in created_object

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        time.sleep(5)  # give it some time to react
        created_object = json.loads(kubectl(f"get tgr/{unique_resource_name} -o json").stdout)

        delete_command = kubectl(f"delete tgr/{unique_resource_name}")
        time.sleep(1)  # give it some time to react

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    logs = load_stdout(runner.stdout)

    # fmt: off

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY,
            "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name,
                       "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert twingate_id

    # Delete
    assert {"message": "Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY,
            "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY,
            "object": {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name,
                       "uid": ANY, "namespace": "default"}, "severity": "info"} in logs
    assert delete_command.stdout.decode() == f'twingateresource.twingate.com "{unique_resource_name}" deleted\n'

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "severity": "info"} in logs

    # fmt: on


@pytest.mark.integration()
def test_resource_access_flows(kopf_settings, kopf_runner_args, unique_resource_name):
    assert "TWINGATE_TEST_PRINCIPAL_ID" in os.environ
    principal_id = os.environ["TWINGATE_TEST_PRINCIPAL_ID"]

    RESOURCE_OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_resource_name}
        spec:
          resourceRef:
            name: {unique_resource_name}
          principalId: {principal_id}
    """

    # fmt: off
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(RESOURCE_OBJ)
        time.sleep(5)  # give it some time to react

        kubectl_create(OBJ)
        time.sleep(5)  # give it some time to react

        json.loads(kubectl(f"get tgra/{unique_resource_name} -o json").stdout)

        delete_command = kubectl(f"delete tgra/{unique_resource_name}")

        time.sleep(1)  # give it some time to react

        kubectl(f"delete tgr/{unique_resource_name}")

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)

    # Create
    assert {
        "message": "Handler 'twingate_resource_access_create' succeeded.",
        "timestamp": ANY,
        "object": {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateResourceAccess",
            "name": unique_resource_name,
            "uid": ANY,
            "namespace": "default",
        },
        "severity": "info",
    } in logs
    # Delete
    assert {
        "message": "Result: {'resourceAccessRemove': {'ok': True, 'error': None}}",
        "timestamp": ANY,
        "severity": "info",
    } in logs
    assert {
        "message": "Handler 'twingate_resource_access_delete' succeeded.",
        "timestamp": ANY,
        "object": {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateResourceAccess",
            "name": unique_resource_name,
            "uid": ANY,
            "namespace": "default",
        },
        "severity": "info",
    } in logs
    assert (
        delete_command.stdout.decode()
        == f'twingateresourceaccess.twingate.com "{unique_resource_name}" deleted\n'
    )

    # Shutdown
    assert {
        "message": "Activity 'shutdown' succeeded.",
        "timestamp": ANY,
        "severity": "info",
    } in logs
