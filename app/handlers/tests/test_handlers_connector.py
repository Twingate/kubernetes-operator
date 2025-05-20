from unittest.mock import ANY, MagicMock, patch

import kopf
import pendulum
import pytest

from app.api.client_connectors import ConnectorTokens
from app.crds import (
    ConnectorImagePolicy,
    ConnectorSpec,
    K8sMetadata,
    TwingateConnectorCRD,
)
from app.handlers import get_connector_deployment
from app.handlers.handlers_connectors import (
    ANNOTATION_LAST_VERSION_CHECK,
    ANNOTATION_NEXT_VERSION_CHECK,
    twingate_connector_create,
    twingate_connector_delete,
    twingate_connector_pod_reconciler,
    twingate_connector_resume,
    twingate_connector_update,
)
from app.settings import get_version


@pytest.fixture(autouse=True)
def mock_connector_spec_get_image():
    with patch("app.crds.ConnectorSpec.get_image") as mock_get_image:
        mock_get_image.return_value = "twingate/connector:test"
        yield mock_get_image


@pytest.fixture
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_connectors.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


@pytest.fixture
def mock_create_or_replace_deployment():
    with patch("app.handlers.handlers_connectors.create_or_replace_deployment") as m:
        yield m


@pytest.fixture
def get_connector_and_crd(connector_factory):
    def get(*, spec_overrides=None, status=None, with_id=False, annotations=None):
        annotations = annotations or {}
        spec_overrides = spec_overrides or {}

        connector = connector_factory()
        connector_spec = ConnectorSpec(
            **spec_overrides, **connector.model_dump(exclude=[] if with_id else ["id"])
        )
        spec = connector_spec.model_dump(by_alias=True)
        crd = TwingateConnectorCRD(
            api_version="twingate.com/v1beta",
            kind="TwingateConnector",
            metadata=K8sMetadata(
                uid="123",
                name=connector_spec.name,
                namespace="default",
                annotations=annotations,
            ),
            spec=spec,
            status=status,
        )
        return connector, crd

    return get


class TestTwingateConnectorResume:
    def test_resume_deletes_old_pod_as_we_migrated_to_deployment(
        self, get_connector_and_crd, kopf_handler_runner, k8s_core_client_mock
    ):
        connector, crd = get_connector_and_crd(
            with_id=True, status={"twingate_connector_create": {"success": True}}
        )

        run = kopf_handler_runner(
            twingate_connector_resume,
            crd,
            MagicMock(),
            new={},
            diff={},
        )
        k8s_core_client_mock.delete_namespaced_pod.assert_called_once()
        assert run.result == {
            "success": True,
            "twingate_id": connector.id,
            "ts": ANY,
        }


class TestTwingateConnectorCreate:
    def test_connector_provisioning(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd()

        mock_api_client.connector_create.return_value = connector
        mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
            access_token="at",
            refresh_token="rt",  # nosec
        )
        run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())

        assert run.result == {
            "success": True,
            "twingate_id": connector.id,
            "ts": ANY,
        }

        assert run.patch_mock.spec == {"id": connector.id, "name": connector.name}

        run.kopf_adopt_mock.assert_called_once_with(
            ANY, owner=ANY, strict=True, forced=True
        )

        run.k8s_core_client_mock.create_namespaced_secret.assert_called_once()
        call_kw = run.k8s_core_client_mock.create_namespaced_secret.call_args.kwargs
        assert call_kw["namespace"] == "default"
        assert call_kw["body"].string_data == {
            "TWINGATE_ACCESS_TOKEN": "at",
            "TWINGATE_REFRESH_TOKEN": "rt",
        }

    def test_connector_provisioning_with_id(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd(with_id=True)

        mock_api_client.get_connector.return_value = connector
        mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
            access_token="at",
            refresh_token="rt",  # nosec
        )
        run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())

        assert run.result == {
            "success": True,
            "twingate_id": connector.id,
            "ts": ANY,
        }

        # didnt need to patch - connector already has id
        assert run.patch_mock.spec == {}

        run.kopf_adopt_mock.assert_called_once_with(
            ANY, owner=ANY, strict=True, forced=True
        )

        run.k8s_core_client_mock.create_namespaced_secret.assert_called_once()
        call_kw = run.k8s_core_client_mock.create_namespaced_secret.call_args.kwargs
        assert call_kw["namespace"] == "default"
        assert call_kw["body"].string_data == {
            "TWINGATE_ACCESS_TOKEN": "at",
            "TWINGATE_REFRESH_TOKEN": "rt",
        }

    def test_with_imagepolicy_sets_check_annotation(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd(
            spec_overrides=dict(image_policy=ConnectorImagePolicy())
        )

        mock_api_client.connector_create.return_value = connector
        mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
            access_token="at",
            refresh_token="rt",  # nosec
        )

        run = kopf_handler_runner(twingate_connector_create, crd, MagicMock())
        assert run.result == {
            "success": True,
            "twingate_id": connector.id,
            "ts": ANY,
        }

        assert run.patch_mock.spec == {"id": connector.id, "name": connector.name}

        run.k8s_core_client_mock.create_namespaced_secret.assert_called_once()
        call_kw = run.k8s_core_client_mock.create_namespaced_secret.call_args.kwargs
        assert call_kw["namespace"] == "default"
        assert call_kw["body"].string_data == {
            "TWINGATE_ACCESS_TOKEN": "at",
            "TWINGATE_REFRESH_TOKEN": "rt",
        }


class TestTwingateConnectorUpdate:
    def test_updates_connector_and_deployment(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        mock_api_client,
        mock_create_or_replace_deployment,
    ):
        connector, crd = get_connector_and_crd(with_id=True)

        mock_api_client.connector_update.return_value = connector

        run = kopf_handler_runner(
            twingate_connector_update,
            crd,
            MagicMock(),
            new={},
            diff=(
                ("add", ("logLevel",), 3, 7),
                ("add", ("name",), "before", "after"),
            ),
        )

        mock_create_or_replace_deployment.assert_called_once()
        assert run.result == {"success": True, "twingate_id": connector.id, "ts": ANY}

    def test_does_nothing_if_only_id_changed(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd(with_id=False)

        mock_api_client.connector_update.return_value = connector

        run = kopf_handler_runner(
            twingate_connector_update,
            crd,
            MagicMock(),
            new={},
            diff=(("add", ("id",), None, "123"),),
        )
        assert run.result == {
            "success": True,
            "message": "No update required",
            "ts": ANY,
            "twingate_id": crd.spec.id,
        }

    def test_does_nothing_if_only_id_and_name_changed(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd(with_id=False)

        mock_api_client.connector_update.return_value = connector

        run = kopf_handler_runner(
            twingate_connector_update,
            crd,
            MagicMock(),
            new={},
            diff=(
                ("add", ("id",), None, "123"),
                ("add", ("name",), None, "lalala"),
            ),
        )
        assert run.result == {
            "success": True,
            "message": "No update required",
            "ts": ANY,
            "twingate_id": crd.spec.id,
        }

    def test_does_nothing_without_id(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd(with_id=False)

        mock_api_client.connector_update.return_value = connector

        run = kopf_handler_runner(
            twingate_connector_update, crd, MagicMock(), new={}, diff={}
        )
        assert run.result == {
            "error": "Update called before Connector has an ID",
            "success": False,
            "ts": ANY,
        }
        
    def test_recreates_connector_if_does_not_exist(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        mock_api_client,
        mock_create_or_replace_deployment,
    ):
        connector, crd = get_connector_and_crd(with_id=True)
        new_connector = connector
        new_connector.id = "new-id"

        # Simulate connector not found
        mock_api_client.connector_update.return_value = None
        # Simulate connector recreated
        mock_api_client.connector_create.return_value = new_connector
        mock_api_client.connector_generate_tokens.return_value = ConnectorTokens(
            access_token="at",
            refresh_token="rt",  # nosec
        )

        run = kopf_handler_runner(
            twingate_connector_update,
            crd,
            MagicMock(),
            new={},
            diff=(
                ("add", ("logLevel",), 3, 7),
                ("add", ("name",), "before", "after"),
            ),
        )

        # Check that it reset the ID and recreated the connector
        assert run.patch_mock.spec == {"id": None, "id": new_connector.id}
        mock_api_client.connector_create.assert_called_once()
        mock_api_client.connector_generate_tokens.assert_called_once_with(new_connector.id)
        mock_create_or_replace_deployment.assert_called_once()
        
        # Verify the secret operations
        run.k8s_core_client_mock.delete_namespaced_secret.assert_called_once()
        run.k8s_core_client_mock.create_namespaced_secret.assert_called_once()
        
        # Check the result
        assert run.result == {
            "success": True, 
            "twingate_id": new_connector.id, 
            "message": "Connector was recreated",
            "ts": ANY
        }


class TestTwingateConnectorDelete:
    def test_twingate_connector_delete_deletes_connector(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd(
            status={"twingate_connector_create": {"success": True}}, with_id=True
        )
        kopf_handler_runner(twingate_connector_delete, crd, MagicMock())
        mock_api_client.connector_delete.assert_called_once()

    def test_twingate_connector_delete_without_status_does_nothing(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd()
        kopf_handler_runner(twingate_connector_delete, crd, MagicMock())
        mock_api_client.connector_delete.assert_not_called()

    def test_twingate_connector_pod_reconciler_raises_if_ran_before_create(
        self, get_connector_and_crd, kopf_handler_runner, mock_api_client
    ):
        connector, crd = get_connector_and_crd()
        with pytest.raises(kopf.TemporaryError):
            kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())


class TestTwingateConnectorPodReconciler_Image:
    def test_deployment_create(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        k8s_core_client_mock,
        k8s_apps_client_mock,
    ):
        connector, crd = get_connector_and_crd(
            status={"twingate_connector_create": {"success": True}}, with_id=True
        )

        k8s_apps_client_mock.read_namespaced_deployment.return_value = None

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        run.k8s_apps_client_mock.create_namespaced_deployment.assert_called_once()

    def test_deployment_update(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        k8s_core_client_mock,
        k8s_apps_client_mock,
    ):
        connector, crd = get_connector_and_crd(
            status={"twingate_connector_create": {"success": True}}, with_id=True
        )

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        run.k8s_apps_client_mock.replace_namespaced_deployment.assert_called_once()


class TestTwingateConnectorPodReconciler_ImagePolicy:
    @pytest.fixture
    def mock_get_image(self):
        with patch("app.crds.ConnectorSpec.get_image") as mock_get_image:
            mock_get_image.return_value = "twingate/connector:test"
            yield mock_get_image

    def test_no_annotation(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        k8s_apps_client_mock,
        mock_get_image,
    ):
        connector, crd = get_connector_and_crd(
            spec_overrides=dict(image_policy=ConnectorImagePolicy()),
            status={"twingate_connector_create": {"success": True}},
            with_id=True,
        )

        mock_dep = MagicMock()
        k8s_apps_client_mock.read_namespaced_pod.return_value = mock_dep

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        run.k8s_apps_client_mock.replace_namespaced_deployment.assert_called_once()
        assert run.patch_mock.meta["annotations"] == {
            ANNOTATION_LAST_VERSION_CHECK: ANY,
            ANNOTATION_NEXT_VERSION_CHECK: ANY,
        }
        mock_get_image.assert_called_once()

    def test_past_due_annotation(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        k8s_apps_client_mock,
        mock_get_image,
    ):
        connector, crd = get_connector_and_crd(
            spec_overrides=dict(image_policy=ConnectorImagePolicy()),
            status={"twingate_connector_create": {"success": True}},
            annotations={ANNOTATION_NEXT_VERSION_CHECK: "2000-01-01T00:00:00Z"},
            with_id=True,
        )

        mock_dep = MagicMock()
        k8s_apps_client_mock.read_namespaced_pod.return_value = mock_dep

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        run.k8s_apps_client_mock.replace_namespaced_deployment.assert_called_once()
        assert run.patch_mock.meta["annotations"] == {
            ANNOTATION_LAST_VERSION_CHECK: ANY,
            ANNOTATION_NEXT_VERSION_CHECK: ANY,
        }
        mock_get_image.assert_called_once()

    def test_not_past_due_annotation(
        self,
        get_connector_and_crd,
        kopf_handler_runner,
        k8s_apps_client_mock,
        mock_get_image,
    ):
        now = pendulum.now("UTC").start_of("minute")
        connector, crd = get_connector_and_crd(
            spec_overrides=dict(image_policy=ConnectorImagePolicy()),
            status={"twingate_connector_create": {"success": True}},
            annotations={ANNOTATION_NEXT_VERSION_CHECK: str(now.add(minutes=1))},
            with_id=True,
        )

        mock_container = MagicMock()
        mock_container.image = "twingate/connector:latest"

        mock_dep = MagicMock()
        mock_dep.spec.template.containers = [mock_container]
        k8s_apps_client_mock.read_namespaced_pod.return_value = mock_dep

        run = kopf_handler_runner(twingate_connector_pod_reconciler, crd, MagicMock())
        assert run.result == {"success": True, "ts": ANY}
        assert run.patch_mock.meta == {}
        run.k8s_apps_client_mock.patch_namespaced_deployment.assert_not_called()
        mock_get_image.assert_not_called()


class TestGetConnectorDeployment:
    @pytest.fixture
    def mock_tenant_url(self):
        return "https://test.twingate.com"

    @pytest.fixture
    def mock_image(self):
        return "twingate/connector:latest"

    def test_default(self, get_connector_and_crd, mock_tenant_url, mock_image):
        _, crd = get_connector_and_crd()

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)

        assert dep.spec["template"]["spec"] == {
            "containers": [
                {
                    "env": [
                        {"name": "TWINGATE_LABEL_DEPLOYED_BY", "value": "operator"},
                        {
                            "name": "TWINGATE_LABEL_OPERATOR_VERSION",
                            "value": get_version(),
                        },
                        {"name": "TWINGATE_URL", "value": mock_tenant_url},
                        {"name": "TWINGATE_LOG_LEVEL", "value": "3"},
                        {"name": "TWINGATE_LOG_ANALYTICS", "value": "v2"},
                    ],
                    "envFrom": [
                        {"secretRef": {"name": crd.metadata.name, "optional": False}}
                    ],
                    "image": mock_image,
                    "imagePullPolicy": "Always",
                    "name": "connector",
                    "securityContext": {
                        "allowPrivilegeEscalation": False,
                        "capabilities": {
                            "drop": ["ALL"],
                        },
                        "runAsNonRoot": True,
                        "runAsUser": 65532,
                        "seccompProfile": {"type": "RuntimeDefault"},
                        "readOnlyRootFilesystem": True,
                    },
                    "readinessProbe": {
                        "exec": {
                            "command": [
                                "/connectorctl",
                                "health",
                            ]
                        },
                        "initialDelaySeconds": 5,
                        "periodSeconds": 5,
                    },
                    "livenessProbe": {
                        "exec": {
                            "command": [
                                "/connectorctl",
                                "health",
                            ]
                        },
                        "initialDelaySeconds": 5,
                        "periodSeconds": 5,
                    },
                    "volumeMounts": [
                        {
                            "name": "twingate-socket",
                            "mountPath": "/var/run/twingate",
                        },
                    ],
                },
            ],
            "volumes": [{"name": "twingate-socket", "emptyDir": {}}],
        }

    def test_connector_env_vars_with_image_policy_set(
        self, get_connector_and_crd, mock_tenant_url, mock_image
    ):
        image_policy = ConnectorImagePolicy()
        _, crd = get_connector_and_crd(
            spec_overrides={"image_policy": image_policy},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        container = dep.spec["template"]["spec"]["containers"][0]
        expected_env_vars = [
            {
                "name": "TWINGATE_LABEL_VERSION_POLICY_SCHEDULE",
                "value": image_policy.schedule,
            },
            {
                "name": "TWINGATE_LABEL_VERSION_POLICY_SPEC",
                "value": image_policy.version,
            },
        ]

        assert all(env in container["env"] for env in expected_env_vars)

    @pytest.mark.parametrize(
        ("log_analytics_enabled", "expected_in"),
        [(True, True), (False, False)],
    )
    def test_connector_env_vars_log_analytics(
        self,
        get_connector_and_crd,
        mock_tenant_url,
        mock_image,
        log_analytics_enabled,
        expected_in,
    ):
        _, crd = get_connector_and_crd(
            spec_overrides={"log_analytics": log_analytics_enabled}
        )
        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        container = dep.spec["template"]["spec"]["containers"][0]

        env_var = {"name": "TWINGATE_LOG_ANALYTICS", "value": "v2"}
        container_env = container["env"]

        if expected_in:
            assert env_var in container_env
        else:
            assert env_var not in container_env

    def test_extra_env(self, get_connector_and_crd, mock_tenant_url, mock_image):
        extra_env = {"name": "TWINGATE_EXTRA_ENV", "value": "extra-value"}
        _, crd = get_connector_and_crd(
            spec_overrides={"container_extra": {"env": [extra_env]}},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        container = dep.spec["template"]["spec"]["containers"][0]

        assert extra_env in container["env"]

    def test_extra_volume_mounts(
        self, get_connector_and_crd, mock_tenant_url, mock_image
    ):
        extra_volume_mount = {
            "name": "extra-volume-mount",
            "mountPath": "/var/run/extra-volume",
        }
        _, crd = get_connector_and_crd(
            spec_overrides={"container_extra": {"volumeMounts": [extra_volume_mount]}},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        container = dep.spec["template"]["spec"]["containers"][0]

        assert container["volumeMounts"] == [
            {"name": "twingate-socket", "mountPath": "/var/run/twingate"},
            extra_volume_mount,
        ]

    def test_sidecar_containers(
        self, get_connector_and_crd, mock_tenant_url, mock_image
    ):
        sidecar_container = {"name": "sidecar-extra", "image": "sidecar-extra-image"}
        _, crd = get_connector_and_crd(
            spec_overrides={"sidecar_containers": [sidecar_container]},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        containers = dep.spec["template"]["spec"]["containers"]

        assert containers[1] == sidecar_container

    def test_extra_volumes(self, get_connector_and_crd, mock_tenant_url, mock_image):
        extra_volume = {"name": "extra-volume", "emptyDir": {}}
        _, crd = get_connector_and_crd(
            spec_overrides={"pod_extra": {"volumes": [extra_volume]}},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        pod_spec = dep.spec["template"]["spec"]

        assert pod_spec["volumes"] == [
            {"name": "twingate-socket", "emptyDir": {}},
            extra_volume,
        ]

    def test_annotations(self, get_connector_and_crd, mock_tenant_url, mock_image):
        annotations = {"twingate.com/extra-annotation": "test-value"}
        _, crd = get_connector_and_crd(
            spec_overrides={"pod_annotations": annotations},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        pod_metadata = dep.spec["template"]["metadata"]

        assert pod_metadata["annotations"] == annotations

    def test_pod_labels(self, get_connector_and_crd, mock_tenant_url, mock_image):
        labels = {"env": "test"}
        _, crd = get_connector_and_crd(
            spec_overrides={"pod_labels": labels},
        )

        dep = get_connector_deployment(crd, mock_tenant_url, mock_image)
        pod_metadata = dep.spec["template"]["metadata"]

        assert pod_metadata["labels"] == labels | {
            "app.kubernetes.io/name": "TwingateConnector",
            "app.kubernetes.io/instance": crd.metadata.name,
        }
