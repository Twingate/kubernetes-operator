import os
import time
from unittest.mock import ANY

import orjson as json
import pytest
from kopf.testing import KopfRunner

from tests_integration.utils import (
    assert_log_message_starts_with,
    kubectl,
    kubectl_apply,
    kubectl_create,
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
        # "OBJ_ACCESS_BY_PRINCIPAL_ID",
        # "OBJ_ACCESS_BY_PRINCIPAL_NAME_GROUP",
        # "OBJ_ACCESS_BY_PRINCIPAL_NAME_SA",
        "OBJ_ACCESS_BY_GROUPREF",
    ],
)
def test_resource_access_flows(
    access_object_yaml_tmpl_name, kopf_settings, kopf_runner_args, unique_resource_name
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
    with KopfRunner(kopf_runner_args,
                    settings=kopf_settings,
                    env={
                        "GROUP_RECONCILER_INTERVAL": "1",
                        "GROUP_RECONCILER_INIT_DELAY": "1",
                    },
    ) as runner:
        kubectl_create(RESOURCE_OBJ)
        kubectl_create(GROUP_OBJ)
        time.sleep(5)  # give it some time to react

        kubectl_create(access_object_yaml)
        time.sleep(10)  # give it some time to react

        json.loads(kubectl(f"get tgra/{unique_resource_name} -o json").stdout)

        delete_command = kubectl(f"delete tgra/{unique_resource_name}")

        time.sleep(1)  # give it some time to react

        kubectl(f"delete tgr/{unique_resource_name}")
        kubectl("delete tgg/test-group")

        time.sleep(5)  # give it some time to react

    # fmt: on

    # Ensure that the operator did not die on start, or during the operation.
    assert runner.exception is None
    assert runner.exit_code == 0

    logs = load_stdout(runner.stdout)

    # Create
    assert {
        "message": "Handler 'twingate_resource_access_change' succeeded.",
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
