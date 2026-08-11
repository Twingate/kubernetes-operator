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
    kubectl_wait_object,
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

    logs = load_stdout(runner.output)

    # fmt: off

    assert "twingate_resource_create" in created_object["status"], f"status not updated: {created_object['status']}"

    twingate_id = created_object["status"]["twingate_resource_create"]["twingate_id"]

    expected_object = {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name, "uid": ANY, "namespace": "default"}

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs
    assert twingate_id

    # Update
    assert {"message": f"Updating resource {twingate_id}", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs
    assert_log_message_starts_with(logs, f"Got resource id='{twingate_id}' name='My K8S Resource Renamed'")

    # Delete
    assert {"message": "Twingate API Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs

    # Shutdown
    assert {"message": "Activity 'shutdown' succeeded.", "timestamp": ANY, "severity": "info"} in logs

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

    logs = load_stdout(runner.output)

    # fmt: off

    expected_object =  {"apiVersion": "twingate.com/v1beta", "kind": "TwingateResource", "name": unique_resource_name, "uid": ANY, "namespace": "default"}

    # Create
    assert {"message": "Handler 'twingate_resource_create' succeeded.", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs
    assert twingate_id

    # Delete
    assert {"message": "Twingate API Result: {'resourceDelete': {'ok': True, 'error': None}}", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs
    assert {"message": "Handler 'twingate_resource_delete' succeeded.", "timestamp": ANY, "object": expected_object, "severity": "info"} in logs

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

    logs = load_stdout(runner.output)

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
        "object": expected_object,
        "severity": "info",
    } in logs

    # Delete
    assert {
        "message": "Twingate API Result: {'resourceAccessRemove': {'ok': True, 'error': None}}",
        "object": expected_object,
        "timestamp": ANY,
        "severity": "info",
    } in logs
    assert {
        "message": "Handler 'twingate_resource_access_delete' succeeded.",
        "timestamp": ANY,
        "object": expected_object,
        "severity": "info",
    } in logs

    # Shutdown
    assert {
        "message": "Activity 'shutdown' succeeded.",
        "timestamp": ANY,
        "severity": "info",
    } in logs


def test_resource_access_reconciled_when_resource_id_changes(
    run_kopf, unique_resource_name
):
    assert "TWINGATE_TEST_PRINCIPAL_ID" in os.environ
    principal_id = os.environ["TWINGATE_TEST_PRINCIPAL_ID"]

    resource_obj = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    access_obj = ACCESS_OBJECTS["OBJ_ACCESS_BY_PRINCIPAL_ID"].format(
        resource_name=unique_resource_name, principal_id=principal_id
    )

    with run_kopf(enable_connector_reconciler=False) as runner:
        kubectl_create(resource_obj)
        resource = kubectl_wait_object_handler_success(
            "tgr", unique_resource_name, "twingate_resource_create"
        )
        original_resource_id = resource["spec"]["id"]
        assert original_resource_id is not None

        kubectl_create(access_obj)
        access = kubectl_wait_object_handler_success(
            "tacc", unique_resource_name, "twingate_resource_access_change"
        )
        assert access_status(access)["resource_id"] == original_resource_id

        # Recreate the Resource so it is assigned a new backend id.
        kubectl_delete_wait("tgr", unique_resource_name)
        kubectl_create(resource_obj)
        recreated = kubectl_wait_object_handler_success(
            "tgr", unique_resource_name, "twingate_resource_create"
        )
        new_resource_id = recreated["spec"]["id"]
        assert new_resource_id is not None
        assert new_resource_id != original_resource_id

        # Access is re-applied to the new resource id and persisted onto the binding's
        # status, without waiting for the sync timer.
        kubectl_wait_object(
            "tacc",
            unique_resource_name,
            lambda obj: access_status(obj).get("resource_id") == new_resource_id,
            description=f"resource_id {new_resource_id}",
        )

        kubectl_delete_wait("tacc", unique_resource_name)
        kubectl_delete_wait("tgr", unique_resource_name)

    logs = load_stdout(runner.output)
    assert_log_message_contains(logs, "ID changed, reconciling resource access")
    assert_log_message_contains(
        logs, f"Deleting old access {original_resource_id}<>{principal_id}"
    )


def test_resource_access_reconciled_when_group_id_changes(
    run_kopf, unique_resource_name
):
    resource_obj = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResource
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Resource
          address: my.default.cluster.local
    """

    group_obj = """
        apiVersion: twingate.com/v1beta
        kind: TwingateGroup
        metadata:
          name: test-group
        spec:
            name: Test Group
    """

    access_obj = ACCESS_OBJECTS["OBJ_ACCESS_BY_GROUPREF"].format(
        resource_name=unique_resource_name
    )

    with run_kopf(enable_connector_reconciler=False) as runner:
        kubectl_create(resource_obj)
        resource = kubectl_wait_object_handler_success(
            "tgr", unique_resource_name, "twingate_resource_create"
        )
        resource_id = resource["spec"]["id"]

        kubectl_create(group_obj)
        group = kubectl_wait_object_handler_success(
            "tgg", "test-group", "twingate_group_create_update"
        )
        original_group_id = group["spec"]["id"]
        assert original_group_id is not None

        kubectl_create(access_obj)
        access = kubectl_wait_object_handler_success(
            "tacc", unique_resource_name, "twingate_resource_access_change"
        )
        assert access_status(access)["principal_id"] == original_group_id

        # Recreate the Group so it is assigned a new backend id.
        kubectl_delete_wait("tgg", "test-group")
        kubectl_create(group_obj)
        recreated = kubectl_wait_object_handler_success(
            "tgg", "test-group", "twingate_group_create_update"
        )
        new_group_id = recreated["spec"]["id"]
        assert new_group_id is not None
        assert new_group_id != original_group_id

        # Access is re-applied to the new group id and persisted onto the binding's
        # status, without waiting for the sync timer.
        kubectl_wait_object(
            "tacc",
            unique_resource_name,
            lambda obj: access_status(obj).get("principal_id") == new_group_id,
            description=f"principal_id {new_group_id}",
        )

        kubectl_delete_wait("tacc", unique_resource_name)
        kubectl_delete_wait("tgr", unique_resource_name)
        kubectl_delete_wait("tgg", "test-group")

    logs = load_stdout(runner.output)
    assert_log_message_contains(logs, "ID changed, reconciling resource access")
    assert_log_message_contains(
        logs, f"Deleting old access {resource_id}<>{original_group_id}"
    )


def access_status(access_object: dict) -> dict:
    return access_object.get("status", {}).get("twingate_resource_access_change", {})
