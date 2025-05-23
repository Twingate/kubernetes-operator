import functools
import time
from unittest.mock import ANY

from tests_integration.utils import (
    kubectl_create,
    kubectl_delete,
    kubectl_delete_wait,
    kubectl_get,
    kubectl_patch,
    kubectl_wait_deployment_available,
    kubectl_wait_to_exist,
)


def test_connector_flows(run_kopf, random_name_generator):
    connector_name = random_name_generator("t")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
            labels:
              app.kubernetes.io/name: test
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
    wait_for_deployment = functools.partial(
        kubectl_wait_deployment_available,
        connector_name,
    )

    with run_kopf():
        kubectl_create(OBJ)

        secret = kubectl_wait_to_exist("secret", connector_name)
        deployment = wait_for_deployment()

        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status
        # Secret was properly created
        assert secret["data"] == {"TWINGATE_ACCESS_TOKEN": ANY, "TWINGATE_REFRESH_TOKEN": ANY}  # fmt: skip

        container = deployment["spec"]["template"]["spec"]["containers"][0]
        container_env = {t["name"]: t["value"] for t in container["env"]}
        assert container_env["TWINGATE_LOG_LEVEL"] == "7"

        # Check patching TwingateConnector updates the deployment
        kubectl_patch(
            f"tc/{connector_name}",
            {
                "spec": {
                    "containerExtra": {"env": [{"name": "FOO", "value": "bar"}]},
                    "podAnnotations": {"some/annotation": "some-value"},
                }
            },
        )
        time.sleep(5)
        deployment = wait_for_deployment()
        pod = deployment["spec"]["template"]

        container = pod["spec"]["containers"][0]
        container_env = container["env"]

        assert container_env[-1]["name"] == "FOO"
        assert container_env[-1]["value"] == "bar"
        assert pod["metadata"]["annotations"]["some/annotation"] == "some-value"

        kubectl_delete_wait("tc", connector_name)

        # ensure owned secret & deployment are deleted
        kubectl_delete_wait("secret", connector_name, perform_deletion=False)
        kubectl_delete_wait("deployment", connector_name, perform_deletion=False)


def test_connector_flows_image_change(run_kopf, random_name_generator):
    connector_name = random_name_generator("t-image")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
            labels:
              app.kubernetes.io/name: test
        spec:
            name: {connector_name}
            hasStatusNotificationsEnabled: false
            image:
                tag: "1.74.0"
    """
    wait_for_deployment = functools.partial(
        kubectl_wait_deployment_available,
        connector_name,
    )

    with run_kopf():
        kubectl_create(OBJ)

        secret = kubectl_wait_to_exist("secret", connector_name)
        wait_for_deployment()

        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status

        # Secret was properly created
        assert secret["data"] == {"TWINGATE_ACCESS_TOKEN": ANY, "TWINGATE_REFRESH_TOKEN": ANY}  # fmt: skip

        # Change image tag
        # kubectl patch tc/test-connector-image-local -p '{"spec": {"image": {"tag": "1.63.0"}}}' --type=merge
        kubectl_patch(f"tc/{connector_name}", {"spec": {"image": {"tag": "1.75.0"}}})
        time.sleep(5)
        wait_for_deployment()

        kubectl_delete_wait("tc", connector_name)

        # ensure owned secret & deployment are deleted
        kubectl_delete_wait("secret", connector_name, perform_deletion=False)
        kubectl_delete_wait("deployment", connector_name, perform_deletion=False)


def test_connector_flows_deployment_gone_while_operator_down(
    run_kopf, random_name_generator
):
    connector_name = random_name_generator("t-gone")
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
            labels:
              app.kubernetes.io/name: test
        spec:
            name: {connector_name}
            hasStatusNotificationsEnabled: false
            image:
                tag: "1.63.0"
    """

    wait_for_deployment = functools.partial(
        kubectl_wait_deployment_available,
        connector_name,
    )

    with run_kopf(cleanup=False):
        kubectl_create(OBJ)
        kubectl_wait_to_exist("secret", connector_name)
        wait_for_deployment()
        connector = kubectl_get("tc", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status

    kubectl_delete("deployment", connector_name)

    # run operator again
    with run_kopf():
        # deployment recreated was recreated
        wait_for_deployment()

        kubectl_delete_wait("tc", connector_name)

        # ensure owned secret & deployment are deleted
        kubectl_delete_wait("secret", connector_name, perform_deletion=False)
        kubectl_delete_wait("deployment", connector_name, perform_deletion=False)
