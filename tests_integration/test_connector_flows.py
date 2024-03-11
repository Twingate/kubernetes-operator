import os
import time
from subprocess import CalledProcessError
from unittest.mock import ANY, patch

import pytest
from kopf.testing import KopfRunner

from tests_integration.utils import (
    kubectl,
    kubectl_create,
    kubectl_delete,
    kubectl_get,
    kubectl_patch,
)


@pytest.fixture(autouse=True)
def _connector_reconciler():
    with patch.dict(
        os.environ,
        {
            "CONNECTOR_RECONCILER_INTERVAL": "1",
            "CONNECTOR_RECONCILER_INIT_DELAY": "1",
        },
    ):
        yield


def test_connector_flows(kopf_settings, kopf_runner_args, ci_run_number):
    connector_name = f"test-connector-{ci_run_number}"
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

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        time.sleep(5)
        kubectl_create(OBJ)
        time.sleep(10)

        secret = kubectl_get("secret", connector_name)
        pod = kubectl_get("pod", connector_name)

        while pod["status"]["phase"] == "Pending":
            time.sleep(1)
            pod = kubectl_get("pod", connector_name)

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
        kubectl_delete(f"pod/{connector_name}")
        time.sleep(10)
        pod = kubectl_get("pod", connector_name)

        assert pod["status"]["phase"] == "Running"
        assert pod["metadata"]["ownerReferences"][0]["name"] == connector_name
        assert pod["metadata"]["ownerReferences"][0]["kind"] == "TwingateConnector"

        kubectl_delete(f"tc/{connector_name}")
        time.sleep(5)

        # secret & pod are deleted
        with pytest.raises(CalledProcessError):
            kubectl_get("secret", connector_name)

        with pytest.raises(CalledProcessError):
            kubectl_get("pod", connector_name)

    assert runner.exception is None
    assert runner.exit_code == 0


def test_connector_flows_image_change(kopf_settings, kopf_runner_args, ci_run_number):
    connector_name = f"test-connector-image-{ci_run_number}"
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

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        time.sleep(5)
        kubectl_create(OBJ)
        time.sleep(5)

        connector = kubectl_get("tc", connector_name)
        secret = kubectl_get("secret", connector_name)
        pod = kubectl_get("pod", connector_name)

        while pod["status"]["phase"] == "Pending":
            time.sleep(1)
            pod = kubectl_get("pod", connector_name)

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
        pod = kubectl_get("pod", connector_name)
        assert pod["status"]["phase"] == "Running"
        assert pod["spec"]["containers"][0]["image"] == "twingate/connector:1.63.0"

        kubectl_delete(f"tc/{connector_name}")
        time.sleep(5)

        # secret & pod are deleted
        with pytest.raises(CalledProcessError):
            kubectl_get("secret", connector_name)

        with pytest.raises(CalledProcessError):
            kubectl_get("pod", connector_name)

    assert runner.exception is None
    assert runner.exit_code == 0


def test_connector_flows_pod_gone_while_operator_down(
    kopf_settings, kopf_runner_args, ci_run_number
):
    connector_name = f"test-connector-gone-{ci_run_number}"
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

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as _runner:
        time.sleep(5)
        kubectl_create(OBJ)
        time.sleep(10)

        connector = kubectl_get("tc", connector_name)
        kubectl_get("secret", connector_name)
        pod = kubectl_get("pod", connector_name)

        while pod["status"]["phase"] == "Pending":
            time.sleep(1)
            pod = kubectl_get("pod", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status

    kubectl_delete(f"pod/{connector_name}")

    # run operator again
    with KopfRunner(kopf_runner_args, settings=kopf_settings) as _runner:
        time.sleep(10)

        # pod was recreated
        pod = kubectl_get("pod", connector_name)
        assert pod["status"]["phase"] == "Running"

        # Test done, delete connector
        kubectl_delete(f"tc/{connector_name}")
        time.sleep(5)


def test_connector_flows_pod_migration_from_older_pod_with_finalizers(
    kopf_settings, kopf_runner_args, ci_run_number
):
    connector_name = f"test-connector-migration-{ci_run_number}"
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

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as _runner:
        time.sleep(5)
        kubectl_create(OBJ)
        time.sleep(10)

        connector = kubectl_get("tc", connector_name)
        kubectl_get("secret", connector_name)
        pod = kubectl_get("pod", connector_name)

        while pod["status"]["phase"] == "Pending":
            time.sleep(1)
            pod = kubectl_get("pod", connector_name)

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
        pod = kubectl_get("pod", connector_name)
        assert pod["metadata"]["annotations"]["twingate.com/connector-podspec-version"] == "v1"  # fmt: skip
        # assert pod["status"]["phase"] in ["Running", "Pending"]
        assert pod["status"]["phase"] == "Running"

        # Test done, delete connector
        kubectl_delete(f"tc/{connector_name}")
        time.sleep(5)
