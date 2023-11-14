import random
import subprocess
from unittest.mock import ANY

import pytest

from tests_integration.utils import (
    kubectl_apply,
    kubectl_create,
    kubectl_delete,
    kubectl_get,
)


@pytest.fixture()
def random_number():
    # ruff: noqa: S311
    return random.randint(0, 100000)  # nosec


@pytest.fixture()
def unique_connector_name(random_number, ci_run_number):
    return f"conn-{ci_run_number}-{random_number}"


@pytest.mark.integration()
class TestConnectorCRD:
    def test_no_image_or_imagepolicy(self, unique_connector_name):
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {unique_connector_name}
            spec:
                name: {unique_connector_name}
            """
        )

        assert result.returncode == 0
        kubectl_delete(f"tc/{unique_connector_name}")

    def test_image(self, unique_connector_name):
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {unique_connector_name}
            spec:
                name: {unique_connector_name}
                image:
                    tag: "latest"
            """
        )

        assert result.returncode == 0
        data = kubectl_get("tc", unique_connector_name)
        assert data == {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateConnector",
            "metadata": {
                "creationTimestamp": ANY,
                "generation": 1,
                "name": unique_connector_name,
                "namespace": "default",
                "resourceVersion": ANY,
                "uid": ANY,
            },
            "spec": {
                "image": {"repository": "twingate/connector", "tag": "latest"},
                "name": unique_connector_name,
            },
        }

        kubectl_delete(f"tc/{unique_connector_name}")

    def test_imagepolicy(self, unique_connector_name):
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {unique_connector_name}
            spec:
                name: {unique_connector_name}
                imagePolicy:
                    provider: "dockerhub"
                    version: "^1.0.0"
            """
        )
        assert result.returncode == 0

        data = kubectl_get("tc", unique_connector_name)
        assert data == {
            "apiVersion": "twingate.com/v1beta",
            "kind": "TwingateConnector",
            "metadata": {
                "creationTimestamp": ANY,
                "generation": 1,
                "name": unique_connector_name,
                "namespace": "default",
                "resourceVersion": ANY,
                "uid": ANY,
            },
            "spec": {
                "imagePolicy": {
                    "provider": "dockerhub",
                    "repository": "twingate/connector",
                    "version": "^1.0.0",
                    "allowPrerelease": False,
                },
                "name": unique_connector_name,
            },
        }

        kubectl_delete(f"tc/{unique_connector_name}")

    def test_imagepolicy_validates_provider(self, unique_connector_name):
        with pytest.raises(subprocess.CalledProcessError):
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}
                    imagePolicy:
                        provider: "invalid"
                        version: "^1.0.0"
                """
            )

    def test_name_is_immutable(self, unique_connector_name):
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {unique_connector_name}
            spec:
                name: {unique_connector_name}
            """
        )

        assert result.returncode == 0

        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_apply(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}1
            """
            )

        stderr = ex.value.stderr.decode()
        assert "name is immutable once set" in stderr

        kubectl_delete(f"tc/{unique_connector_name}")
