import time
from unittest.mock import ANY

from tests_integration.utils import (
    kubectl,
    kubectl_create,
    kubectl_delete,
    kubectl_delete_wait,
    kubectl_get,
    kubectl_patch,
    kubectl_wait_pod_running,
    kubectl_wait_pod_status,
    kubectl_wait_to_exist,
)


def test_connector_flows(run_kopf, random_name_generator):
    connector_name = random_name_generator("t")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
        spec:
            name: {connector_name}
            logLevel: 7
            hasStatusNotificationsEnabled: false
            imagePolicy:
                provider: "dockerhub"
                schedule: "* * * * *"
                repository: twingate/connector
                version: "^1.0.0"
    """

    with run_kopf():
        kubectl_create(OBJ)

        secret = kubectl_wait_to_exist("secret", connector_name)
        pod = kubectl_wait_pod_running(connector_name)

        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status
        # Secret was properly created
        assert secret["data"] == {"TWINGATE_ACCESS_TOKEN": ANY, "TWINGATE_REFRESH_TOKEN": ANY}  # fmt: skip
        # pod was properly created
        assert pod["status"]["phase"] == "Running"
        assert pod["metadata"]["ownerReferences"][0]["name"] == connector_name
        assert pod["metadata"]["ownerReferences"][0]["kind"] == "TwingateConnector"

        container = pod["spec"]["containers"][0]
        container_env = {t["name"]: t["value"] for t in container["env"]}
        assert container_env["TWINGATE_LOG_LEVEL"] == "7"

        # Check that if pod is deleted we recreate it
        kubectl_delete_wait("pod", connector_name)
        pod = kubectl_wait_pod_status(connector_name, "Running")

        assert pod["status"]["phase"] == "Running"
        assert pod["metadata"]["ownerReferences"][0]["name"] == connector_name
        assert pod["metadata"]["ownerReferences"][0]["kind"] == "TwingateConnector"

        # Check patching TwingateConnector updates the pod
        kubectl_patch(
            f"tc/{connector_name}",
            {
                "spec": {
                    "containerExtra": {"env": [{"name": "FOO", "value": "bar"}]},
                    "podExtra": {"restartPolicy": "OnFailure"},
                    "podAnnotations": {"some/annotation": "some-value"},
                }
            },
        )
        time.sleep(5)
        pod = kubectl_wait_pod_running(connector_name)

        assert pod["status"]["phase"] == "Running"
        assert pod["spec"]["restartPolicy"] == "OnFailure"
        assert pod["spec"]["containers"][0]["env"][-1]["name"] == "FOO"
        assert pod["spec"]["containers"][0]["env"][-1]["value"] == "bar"
        assert pod["metadata"]["annotations"]["some/annotation"] == "some-value"

        kubectl_delete_wait("tc", connector_name)
        time.sleep(10)
        # secret & pod are deleted
        kubectl_delete_wait("secret", connector_name)
        kubectl_delete_wait("pod", connector_name)


def test_connector_flows_image_change(run_kopf, random_name_generator):
    connector_name = random_name_generator("t-image")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
        spec:
            name: {connector_name}
            hasStatusNotificationsEnabled: false
            image:
                tag: "1.62.0"
    """

    with run_kopf():
        kubectl_create(OBJ)
        secret = kubectl_wait_to_exist("secret", connector_name)
        pod = kubectl_wait_pod_running(connector_name)
        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status

        # Secret was properly created
        assert secret["data"] == {"TWINGATE_ACCESS_TOKEN": ANY, "TWINGATE_REFRESH_TOKEN": ANY}  # fmt: skip
        # pod was properly created
        assert pod["status"]["phase"] == "Running"
        assert pod["metadata"]["ownerReferences"][0]["name"] == connector_name
        assert pod["metadata"]["ownerReferences"][0]["kind"] == "TwingateConnector"

        # Change image tag
        # kubectl patch tc/test-connector-image-local -p '{"spec": {"image": {"tag": "1.63.0"}}}' --type=merge
        kubectl_patch(f"tc/{connector_name}", {"spec": {"image": {"tag": "1.63.0"}}})
        time.sleep(5)
        pod = kubectl_wait_pod_running(connector_name)
        assert pod["status"]["phase"] == "Running"
        assert pod["spec"]["containers"][0]["image"] == "twingate/connector:1.63.0"

        kubectl_delete_wait("tc", connector_name)
        time.sleep(10)

        # secret & pod are deleted
        kubectl_delete_wait("secret", connector_name)
        kubectl_delete_wait("pod", connector_name)


def test_connector_flows_pod_gone_while_operator_down(run_kopf, random_name_generator):
    connector_name = random_name_generator("t-gone")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
        spec:
            name: {connector_name}
            hasStatusNotificationsEnabled: false
            image:
                tag: "1.63.0"
    """

    with run_kopf():
        kubectl_create(OBJ)
        kubectl_wait_to_exist("secret", connector_name)
        kubectl_wait_pod_running(connector_name)
        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status

    kubectl_delete("pod", connector_name)

    # run operator again
    with run_kopf():
        # pod was recreated
        pod = kubectl_wait_pod_running(connector_name)
        assert pod["status"]["phase"] == "Running"

        # Test done, delete connector
        kubectl_delete("tc", connector_name)
        time.sleep(5)


def test_connector_flows_pod_migration_from_older_pod_with_finalizers(
    run_kopf, ci_run_number, random_name_generator
):
    connector_name = random_name_generator("t-migration")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
        spec:
            name: {connector_name}
            hasStatusNotificationsEnabled: false
            image:
                tag: "1.63.0"
    """

    with run_kopf():
        kubectl_create(OBJ)
        kubectl_wait_to_exist("secret", connector_name)
        kubectl_wait_pod_running(connector_name)
        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status

        # Patch pod to add finalizers and make operator think its old
        kubectl_patch(
            f"pod/{connector_name}",
            {
                "metadata": {
                    "finalizers": ["twingate.com/finalizer"],
                }
            },
        )
        kubectl(
            f"annotate pod/{connector_name} --overwrite twingate.com/connector-podspec-version=not_what_op_expects"
        )

        # wait for timer to run
        time.sleep(10)

        # check pod was recreated
        pod = kubectl_wait_pod_running(connector_name)
        assert pod["metadata"]["annotations"]["twingate.com/connector-podspec-version"] == "v1"  # fmt: skip
        assert pod["status"]["phase"] == "Running"

        # Test done, delete connector
        kubectl_delete("tc", connector_name)
        time.sleep(5)
