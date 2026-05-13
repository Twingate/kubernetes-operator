import subprocess

import pytest

from tests_integration.utils import kubectl_create, kubectl_delete


@pytest.fixture
def unique_access_name(sequential_number, ci_run_number):
    unique_name = f"acc-{ci_run_number}-{sequential_number}"
    yield unique_name
    kubectl_delete("tacc", unique_name)


def test_spec_is_required(sequential_number, ci_run_number):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: f"acc-{ci_run_number}-{sequential_number}"
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec: Required value" in stderr


def test_have_to_specify_resourceRef():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: failing
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.resourceRef: Required value" in stderr


def test_have_to_specify_principalId_or_principalExternalRef():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: failing
            spec:
              resourceRef:
                name: my-twingate-resource
                namespace: default
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.principalId: Required value" in stderr


def test_with_principalId(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalId: R3JvdXA6MTE1NzI2MA==
          resourceRef:
            name: my-twingate-resource
            namespace: default
    """
    )

    assert result.returncode == 0


def test_with_groupRef(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          groupRef:
            name: my-group
            namespace: myNS
          resourceRef:
            name: my-twingate-resource
            namespace: default
    """
    )

    assert result.returncode == 0


def test_with_groupRef_ns_is_optional(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          groupRef:
            name: my-group
          resourceRef:
            name: my-twingate-resource
            namespace: default
    """
    )

    assert result.returncode == 0


def test_with_principalExternalRef(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalExternalRef:
            type: group
            name: my-group
          resourceRef:
            name: my-twingate-resource
            namespace: default
    """
    )

    assert result.returncode == 0


def test_with_principalExternalRef_fails_for_missing_type_or_nameame():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalExternalRef:
                type: group
              resourceRef:
                name: my-twingate-resource
                namespace: default
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.principalExternalRef.name" in stderr

    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalExternalRef:
                name: my-group
              resourceRef:
                name: my-twingate-resource
                namespace: default
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.principalExternalRef.type" in stderr


def test_both_principalId_and_principalExternalRef_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              principalExternalRef:
                name: foo
                type: group
              resourceRef:
                name: my-twingate-resource
                namespace: default
        """
        )

    stderr = ex.value.stderr.decode()
    assert (
        "must validate one and only one schema (oneOf). Found 2 valid alternatives"
        in stderr
    )


def test_both_principalId_and_groupRef_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              groupRef:
                name: foo
                namespace: bar
              resourceRef:
                name: my-twingate-resource
                namespace: default
        """
        )

    stderr = ex.value.stderr.decode()
    assert (
        "must validate one and only one schema (oneOf). Found 2 valid alternatives"
        in stderr
    )


def test_accessPolicy_auto_lock_without_durationSeconds_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              accessPolicy:
                mode: AUTO_LOCK
        """
        )

    stderr = ex.value.stderr.decode()
    assert "durationSeconds is required when mode is AUTO_LOCK" in stderr


def test_accessPolicy_manual_with_durationSeconds_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              accessPolicy:
                mode: MANUAL
                durationSeconds: 3600
        """
        )

    stderr = ex.value.stderr.decode()
    assert "durationSeconds must not be set when mode is MANUAL" in stderr


def test_accessPolicy_durationSeconds_below_minimum_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              accessPolicy:
                mode: AUTO_LOCK
                durationSeconds: 100
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.accessPolicy.durationSeconds" in stderr
    assert "3600" in stderr


def test_accessPolicy_durationSeconds_above_maximum_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              accessPolicy:
                mode: AUTO_LOCK
                durationSeconds: 99999999
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.accessPolicy.durationSeconds" in stderr
    assert "31536000" in stderr


def test_accessPolicy_invalid_mode_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              accessPolicy:
                mode: NOT_A_MODE
                durationSeconds: 3600
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.accessPolicy.mode" in stderr


def test_accessPolicy_missing_mode_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              accessPolicy:
                durationSeconds: 3600
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.accessPolicy.mode" in stderr


def test_approvalMode_invalid_value_fails():
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(
            """
            apiVersion: twingate.com/v1beta
            kind: TwingateResourceAccess
            metadata:
              name: fail
            spec:
              principalId: R3JvdXA6MTE1NzI2MA==
              resourceRef:
                name: my-twingate-resource
                namespace: default
              approvalMode: NOT_VALID
        """
        )

    stderr = ex.value.stderr.decode()
    assert "spec.approvalMode" in stderr


def test_with_accessPolicy_auto_lock(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalId: R3JvdXA6MTE1NzI2MA==
          resourceRef:
            name: my-twingate-resource
            namespace: default
          accessPolicy:
            mode: AUTO_LOCK
            durationSeconds: 3600
    """
    )

    assert result.returncode == 0


def test_with_accessPolicy_access_request(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalId: R3JvdXA6MTE1NzI2MA==
          resourceRef:
            name: my-twingate-resource
            namespace: default
          accessPolicy:
            mode: ACCESS_REQUEST
            durationSeconds: 7200
    """
    )

    assert result.returncode == 0


def test_with_accessPolicy_manual(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalId: R3JvdXA6MTE1NzI2MA==
          resourceRef:
            name: my-twingate-resource
            namespace: default
          accessPolicy:
            mode: MANUAL
    """
    )

    assert result.returncode == 0


def test_with_approvalMode_automatic(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalId: R3JvdXA6MTE1NzI2MA==
          resourceRef:
            name: my-twingate-resource
            namespace: default
          approvalMode: AUTOMATIC
    """
    )

    assert result.returncode == 0


def test_with_expiresAt(unique_access_name):
    result = kubectl_create(
        f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateResourceAccess
        metadata:
          name: {unique_access_name}
        spec:
          principalId: R3JvdXA6MTE1NzI2MA==
          resourceRef:
            name: my-twingate-resource
            namespace: default
          expiresAt: "2027-01-01T00:00:00Z"
    """
    )

    assert result.returncode == 0
