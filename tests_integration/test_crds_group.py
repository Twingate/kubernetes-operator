import subprocess

import pytest

from tests_integration.utils import kubectl_create


def test_name_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGroup
            metadata:
              name: {unique_resource_name}
            spec:
              members: ["foo@bar.com"]
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.name: Required" in stderr


def test_members_array_is_unique(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGroup
            metadata:
              name: {unique_resource_name}
            spec:
              name: My K8S Group
              members: ["same", "same", "but-different"]
        """)

    stderr = ex.value.stderr.decode()
    assert 'Duplicate value: "same"' in stderr
