import subprocess
from unittest.mock import ANY

import pytest

from tests_integration.utils import (
    kubectl_apply,
    kubectl_create,
    kubectl_delete,
    kubectl_get,
)


@pytest.mark.integration()
class TestConnectorCRD:
    def test_no_image_or_imagepolicy(self, unique_resource_name):
        name = f"connector-{unique_resource_name}"
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {name}
            spec:
                name: {name}
            """
        )

        assert result.returncode == 0
        kubectl_delete(f"tc/{name}")

    def test_image(self, unique_resource_name):
        name = f"connector-{unique_resource_name}"
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {name}
            spec:
                name: {name}
                image:
                    tag: "latest"
            """
        )

        assert result.returncode == 0
        data = kubectl_get("tc", name)
        assert data == {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateConnector",
            "metadata": {
                "creationTimestamp": ANY,
                "generation": 1,
                "name": name,
                "namespace": "default",
                "resourceVersion": ANY,
                "uid": ANY,
            },
            "spec": {
                "image": {"repository": "twingate/connector", "tag": "latest"},
                "name": name,
            },
        }

        kubectl_delete(f"tc/{name}")

    def test_imagepolicy(self, unique_resource_name):
        name = f"connector-{unique_resource_name}"
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {name}
            spec:
                name: {name}
                imagePolicy:
                    provider: "dockerhub"
                    version: "^1.0.0"
            """
        )
        assert result.returncode == 0

        data = kubectl_get("tc", name)
        assert data == {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateConnector",
            "metadata": {
                "creationTimestamp": ANY,
                "generation": 1,
                "name": name,
                "namespace": "default",
                "resourceVersion": ANY,
                "uid": ANY,
            },
            "spec": {
                "imagePolicy": {
                    "provider": "dockerhub",
                    "version": "^1.0.0",
                    "allowPrerelease": False,
                },
                "name": name,
            },
        }

        kubectl_delete(f"tc/{name}")

    def test_imagepolicy_validates_provider(self, unique_resource_name):
        name = f"connector-{unique_resource_name}"
        with pytest.raises(subprocess.CalledProcessError):
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {name}
                spec:
                    name: {name}
                    imagePolicy:
                        provider: "invalid"
                        version: "^1.0.0"
                """
            )

    def test_name_is_immutable(self, unique_resource_name):
        name = f"connector-{unique_resource_name}"
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {name}
            spec:
                name: {name}
            """
        )

        assert result.returncode == 0

        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_apply(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {name}
                spec:
                    name: {name}1
            """
            )

        stderr = ex.value.stderr.decode()
        assert "name is immutable once set" in stderr

        kubectl_delete(f"tc/{name}")
