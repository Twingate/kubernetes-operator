import subprocess

import pytest

from tests_integration.utils import kubectl_create, kubectl_delete


def test_success(unique_resource_name):
    result = kubectl_create(f"""
        apiVersion: twingate.com/v1beta
        kind: TwingateGroup
        metadata:
          name: {unique_resource_name}
        spec:
          name: My K8S Group
    """)

    assert result.returncode == 0
    kubectl_delete("tgg", unique_resource_name)


def test_name_required(unique_resource_name):
    with pytest.raises(subprocess.CalledProcessError) as ex:
        kubectl_create(f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateGroup
            metadata:
              name: {unique_resource_name}
            spec: {{}}
        """)

    stderr = ex.value.stderr.decode()
    assert "spec.name: Required" in stderr
