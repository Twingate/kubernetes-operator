import subprocess
from unittest.mock import ANY

import pytest

from tests_integration.utils import kubectl_create, kubectl_delete, kubectl_get


@pytest.fixture
def unique_connector_name(sequential_number, ci_run_number):
    return f"conn-{ci_run_number}-{sequential_number}"


@pytest.mark.integration
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

    def test_both_image_or_imagepolicy(self, unique_connector_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}
                    image:
                        tag: "latest"
                    imagePolicy:
                        provider: "dockerhub"
                        schedule: "0 0 * * *"
                """
            )

        stderr = ex.value.stderr.decode()
        assert "Can define either `image` or `imagePolicy`, not both." in stderr

    def test_loglevel(self, unique_connector_name):
        result = kubectl_create(
            f"""
            apiVersion: twingate.com/v1beta
            kind: TwingateConnector
            metadata:
                name: {unique_connector_name}
            spec:
                name: {unique_connector_name}
                logLevel: 4
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
                "logLevel": 4,
                "logAnalytics": True,
                "name": unique_connector_name,
                "hasStatusNotificationsEnabled": True,
            },
        }

        kubectl_delete(f"tc/{unique_connector_name}")

    def test_loglevel_too_high(self, unique_connector_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}
                    logLevel: 8
                """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "spec.logLevel: Invalid value: 8: spec.logLevel in body should be less than or equal to 7"
            in stderr
        )

    def test_loglevel_too_low(self, unique_connector_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}
                    logLevel: -2
                """
            )

        stderr = ex.value.stderr.decode()
        assert (
            "spec.logLevel: Invalid value: -2: spec.logLevel in body should be greater than or equal to -1"
            in stderr
        )

    def test_has_status_notifications_enabled(self, unique_connector_name):
        result = kubectl_create(
            f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}
                    hasStatusNotificationsEnabled: false
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
                "hasStatusNotificationsEnabled": False,
                "logLevel": 3,
                "logAnalytics": True,
                "name": unique_connector_name,
            },
        }

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
                "logLevel": 3,
                "logAnalytics": True,
                "hasStatusNotificationsEnabled": True,
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
                "logLevel": 3,
                "logAnalytics": True,
                "hasStatusNotificationsEnabled": True,
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

    def test_google_provider_requires_repository(self, unique_connector_name):
        with pytest.raises(subprocess.CalledProcessError) as ex:
            kubectl_create(
                f"""
                apiVersion: twingate.com/v1beta
                kind: TwingateConnector
                metadata:
                    name: {unique_connector_name}
                spec:
                    name: {unique_connector_name}
                    logLevel: 3
                    imagePolicy:
                        provider: "google"
                        version: "^1.0.0"
                """
            )

        stderr = ex.value.stderr.decode()
        assert "Google provider requires specifying repository." in stderr
