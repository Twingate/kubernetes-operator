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
