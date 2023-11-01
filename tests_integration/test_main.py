import os
import subprocess
import time
import uuid
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
    assert "TWINGATE_API_KEY" in os.environ
    assert "TWINGATE_NETWORK" in os.environ
    assert "TWINGATE_REMOTE_NETWORK_ID" in os.environ

    settings = kopf.OperatorSettings()
    settings.watching.server_timeout = 10
    return settings


@pytest.fixture()
def unique_resource_name(request):
    return request.node.name.replace("_", "-") + "-" + str(uuid.uuid4())


@pytest.fixture(scope="module", autouse=True)
def _load_crds():
    kubectl("apply -f ./deploy/twingate-operator/crds/")


@pytest.mark.integration()
def test_resource_flows(kopf_settings, unique_resource_name):
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
def test_resource_created_before_operator_runs(kopf_settings, unique_resource_name):
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
def test_resource_access_flows(kopf_settings, unique_resource_name):
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


@pytest.mark.integration()
class TestResourceCRD:
    def test_browser_shortcut_false_allows_wildcard_address(self, unique_resource_name):
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "*.default.cluster.local"
                isBrowserShortcutEnabled: false
        """
        )

        assert result.returncode == 0
        kubectl(f"delete tgr/{unique_resource_name}")

    def test_browser_shortcut_cant_have_wildcard_address(self, unique_resource_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "*.default.cluster.local"
                    isBrowserShortcutEnabled: true
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "if isBrowserShortcutEnabled is set to true, then address can't be wildcard"
            in stderr
        )

        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo?.default.cluster.local"
                    isBrowserShortcutEnabled: true
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "if isBrowserShortcutEnabled is set to true, then address can't be wildcard"
            in stderr
        )

    def test_protocols_tcp_allowall_cant_specify_ports(self, unique_resource_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        tcp:
                            policy: ALLOW_ALL
                            ports:
                                - start: 80
                                  end: 80
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "*.default.cluster.local"
                protocols:
                    tcp:
                        policy: ALLOW_ALL
        """
        )

        assert result.returncode == 0, result.value.stderr.decode()
        kubectl(f"delete tgr/{unique_resource_name}")

    def test_protocols_udp_allowall_cant_specify_ports(self, unique_resource_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        udp:
                            policy: ALLOW_ALL
                            ports:
                                - start: 80
                                  end: 80
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "*.default.cluster.local"
                protocols:
                    udp:
                        policy: ALLOW_ALL
        """
        )

        assert result.returncode == 0, result.value.stderr.decode()

    def test_protocols_tcp_restricted_must_specify_ports(self, unique_resource_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        tcp:
                            policy: RESTRICTED
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    tcp:
                        policy: RESTRICTED
                        ports:
                            - start: 80
                              end: 80
        """
        )

        assert result.returncode == 0, result.value.stderr.decode()

    def test_protocols_udp_restricted_must_specify_ports(self, unique_resource_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        udp:
                            policy: RESTRICTED
            """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "Can't specify port ranges for ALLOW_ALL policy, and must specify port ranges for RESTRICTED policy"
            in stderr
        )

        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResource
            metadata:
                name: {unique_resource_name}
            spec:
                name: My K8S Resource
                address: "foo.default.cluster.local"
                protocols:
                    udp:
                        policy: RESTRICTED
                        ports:
                            - start: 80
                              end: 80
        """
        )

        assert result.returncode == 0, result.value.stderr.decode()

    def test_protocols_tcp_restricted_port_values_must_be_valid(
        self, unique_resource_name
    ):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        tcp:
                            policy: RESTRICTED
                            ports:
                                - start: -1
                                  end: 10
            """
            )

        stderr = ex.value.stderr.decode()
        assert "Invalid value: -1" in stderr

    def test_protocols_tcp_restricted_port_values_start_must_be_lte_end(
        self, unique_resource_name
    ):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        tcp:
                            policy: RESTRICTED
                            ports:
                                - start: 8080
                                  end: 7080
            """
            )

        stderr = ex.value.stderr.decode()
        assert "Start port value must be less or equal to end port value" in stderr

    def test_protocols_udp_restricted_port_values_must_be_valid(
        self, unique_resource_name
    ):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        tcp:
                            policy: RESTRICTED
                            ports:
                                - start: 1
                                  end: 1000000000
            """
            )

        stderr = ex.value.stderr.decode()
        assert "Invalid value: 1000000000" in stderr, stderr

    def test_protocols_udp_restricted_port_values_start_must_be_lte_end(
        self, unique_resource_name
    ):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateResource
                metadata:
                    name: {unique_resource_name}
                spec:
                    name: My K8S Resource
                    address: "foo.default.cluster.local"
                    protocols:
                        udp:
                            policy: RESTRICTED
                            ports:
                                - start: 8080
                                  end: 7080
            """
            )

        stderr = ex.value.stderr.decode()
        assert "Start port value must be less or equal to end port value" in stderr
