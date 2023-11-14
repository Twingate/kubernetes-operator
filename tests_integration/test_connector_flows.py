import time
from subprocess import CalledProcessError
from unittest.mock import ANY

import pytest
from kopf.testing import KopfRunner

from tests_integration.utils import kubectl_create, kubectl_delete, kubectl_get


def test_connector_flows(kopf_settings, kopf_runner_args, ci_run_number):
    connector_name = f"test-connector-{ci_run_number}"
    OBJ = f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateConnector
        metadata:
            name: {connector_name}
        spec:
            name: {connector_name}
            imagePolicy:
                provider: "dockerhub"
                schedule: "* * * * *"
                repository: twingate/connector
                version: "^1.0.0"
    """

    with KopfRunner(kopf_runner_args, settings=kopf_settings) as runner:
        kubectl_create(OBJ)
        time.sleep(5)

        connector = kubectl_get("tc", connector_name)
        secret = kubectl_get("secret", connector_name)
        pod = kubectl_get("pod", connector_name)

        # connector was properly provisioned
        expected_status = {"success": True, "image": ANY, "ts": ANY, "twingate_id": ANY}
        assert connector["status"]["twingate_connector_create"] == expected_status
        assert connector["metadata"]["annotations"]["twingate.com/next-version-check"] is not None  # fmt: skip
        # Secret was properly created
        assert secret["data"] == {"TWINGATE_ACCESS_TOKEN": ANY, "TWINGATE_REFRESH_TOKEN": ANY}  # fmt: skip
        # pod was properly created
        assert pod["status"]["phase"] == "Running"
        assert pod["metadata"]["annotations"]["twingate.com/kopf-managed"] == "yes"
        assert pod["metadata"]["labels"]["twingate.com/connector"] == connector_name
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
