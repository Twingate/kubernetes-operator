from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest
from gql.transport.exceptions import TransportServerError

from app.api.client import GraphQLMutationError
from app.crds import (
    AccessApprovalMode,
    AccessMode,
    AccessPolicyInput,
    K8sMetadata,
)
from app.handlers.handlers_resource_access import (
    get_principal_id,
    twingate_group_id_changed,
    twingate_resource_access_by_group,
    twingate_resource_access_by_resource,
    twingate_resource_access_delete,
    twingate_resource_access_sync,
    twingate_resource_id_changed,
)


@pytest.fixture
def mock_api_client():
    api_client_instance = MagicMock()
    with patch(
        "app.handlers.handlers_resource_access.TwingateAPIClient"
    ) as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


class TestGetPrincipalId:
    def test_id_from_spec(self):
        access_crd = MagicMock()
        access_crd.principal_id = "R3JvdXA6MTE1NzI2MA=="
        assert (
            get_principal_id(access_crd, None, MagicMock(), "default")
            == "R3JvdXA6MTE1NzI2MA=="
        )

    def test_id_invalid_spec(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.principal_external_ref = None
        access_crd.get_group_ref_object.return_value = None
        with pytest.raises(
            ValueError, match=r"Missing principal_id or principal_external_ref"
        ):
            get_principal_id(access_crd, None, MagicMock(), "default")

    def test_id_from_group_ref_object(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.principal_external_ref = None
        access_crd.get_group_ref_object.return_value = {"spec": {"id": "group-id"}}
        assert get_principal_id(access_crd, None, MagicMock(), "default") == "group-id"

    def test_id_from_group_ref_object_not_ready_raises_temoraryerror(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.principal_external_ref = None
        access_crd.get_group_ref_object.return_value = {"spec": {"id": None}}
        with pytest.raises(kopf.TemporaryError):
            assert (
                get_principal_id(access_crd, None, MagicMock(), "default") == "group-id"
            )

    def test_from_external_ref_group(self, mock_api_client):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "group"
        access_crd.principal_external_ref.name = "group-name"

        mock_api_client.get_group_id.return_value = "R3JvdXA6MTE1NzI2MA=="

        assert (
            get_principal_id(access_crd, None, mock_api_client, "default")
            == "R3JvdXA6MTE1NzI2MA=="
        )

    def test_from_external_ref_sa(self, mock_api_client):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "serviceAccount"
        access_crd.principal_external_ref.name = "sa-name"

        mock_api_client.get_service_account_id.return_value = "R3JvdXA6MTE1NzI2MA=="

        assert (
            get_principal_id(access_crd, None, mock_api_client, "default")
            == "R3JvdXA6MTE1NzI2MA=="
        )

    def test_from_external_ref_returns_none(self, mock_api_client):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "serviceAccount"
        access_crd.principal_external_ref.name = "sa-name"

        mock_api_client.get_service_account_id.return_value = None

        with pytest.raises(
            ValueError, match=r"Principal serviceAccount sa-name not found"
        ):
            get_principal_id(access_crd, None, mock_api_client, "default")

    def test_from_external_ref_invalid_type_returns_none(self, mock_api_client):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "invalid"
        access_crd.principal_external_ref.name = "sa-name"

        with pytest.raises(ValueError, match=r"Unknown principal type: invalid"):
            get_principal_id(access_crd, None, mock_api_client, "default")

    def test_from_external_ref_uses_recorded_principal_id(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "invalid"
        access_crd.principal_external_ref.name = "sa-name"

        expected = "R3JvdXA6MTE1NzI2MA=="
        principal_id = get_principal_id(
            access_crd, expected, mock_api_client, "default"
        )
        assert principal_id == expected


class TestResourceAccessChangeHandler:
    def test_create_success(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        mock_api_client.resource_access_add.return_value = True

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_shim = SimpleNamespace(spec={}, status={}, metadata={})

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            result = twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_shim,
                status={},
            )
            assert result == {
                "success": True,
                "ts": ANY,
                "principal_id": ANY,
                "resource_id": ANY,
            }

        assert patch_shim.status == {
            "resourceId": resource_spec.id,
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }
        kopf_info_mock.assert_called_once_with("", reason="Success", message=ANY)

    def test_create_invalid_ref(self, mock_api_client):
        resource_access_spec = {
            "resourceRef": {"name": "invalid"},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        mock_api_client.resource_access_add.return_value = True

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()

        with (
            patch(
                "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
                return_value=None,
            ),
            patch("kopf.warn") as kopf_warn_mock,
        ):
            with pytest.raises(
                kopf.TemporaryError, match=r"Resource default/invalid not found"
            ):
                twingate_resource_access_sync(
                    body="",
                    namespace="default",
                    spec=resource_access_spec,
                    memo=memo_mock,
                    logger=logger_mock,
                    patch=patch_mock,
                    status={},
                )

            kopf_warn_mock.assert_called_once_with(
                "",
                reason="ResourceNotFound",
                message="Resource default/invalid not found",
            )

    def test_create_resource_no_id(self, network_resource_factory, mock_api_client):
        resource = network_resource_factory()
        resource_spec = resource.to_spec(id=None)

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        mock_api_client.resource_access_add.return_value = True

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with (
            patch(
                "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
                return_value=resource_crd_mock,
            ),
            pytest.raises(kopf.TemporaryError),
        ):
            twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_mock,
                status={},
            )

    def test_create_graphql_error_returns_it(
        self, network_resource_factory, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        mock_api_client.resource_access_add.side_effect = GraphQLMutationError(
            "resourceCreate", "some error"
        )

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_shim = SimpleNamespace(
            spec={}, status={}, metadata={"ownerReferences": []}
        )

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with (
            patch(
                "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
                return_value=resource_crd_mock,
            ),
            patch("kopf.exception") as kopf_exception_mock,
        ):
            result = twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_shim,
                status={},
            )
            assert result == {"success": False, "error": "some error", "ts": ANY}

        kopf_exception_mock.assert_called_once_with(
            "", reason="Failure", message="resourceCreate failed: some error"
        )
        # A failed grant records nothing, leaving any previously recorded pair in place.
        assert patch_shim.status == {}
        assert patch_shim.metadata["ownerReferences"] == []

    def test_skip_reconciler(self):
        with (
            patch(
                "app.handlers.handlers_resource_access.ENABLE_RESOURCE_ACCESS_RECONCILER",
                "false",
            ),
            patch(
                "app.handlers.handlers_resource_access.reconcile_resource_access",
            ) as reconcile_mock,
        ):
            result = twingate_resource_access_sync(
                body={},
                namespace="default",
                spec={},
                memo={},
                logger={},
                patch={},
                status={},
            )
            assert result is None

        reconcile_mock.assert_not_called()

    def test_create_passes_expires_at_to_client(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
            "expiresAt": "2026-12-31T23:59:59Z",
        }

        mock_api_client.resource_access_add.return_value = True

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=resource_access_spec,
                memo=MagicMock(),
                logger=MagicMock(),
                patch=MagicMock(),
                status={},
            )

        call_kwargs = mock_api_client.resource_access_add.call_args.kwargs
        assert call_kwargs["expires_at"] == datetime(
            2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc
        )
        assert call_kwargs["access_policy"] is None
        assert call_kwargs["approval_mode"] is None

    def test_create_passes_access_policy_to_client(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
            "accessPolicy": {"mode": "AUTO_LOCK", "durationSeconds": 3600},
        }

        mock_api_client.resource_access_add.return_value = True

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=resource_access_spec,
                memo=MagicMock(),
                logger=MagicMock(),
                patch=MagicMock(),
                status={},
            )

        call_kwargs = mock_api_client.resource_access_add.call_args.kwargs
        assert call_kwargs["access_policy"] == AccessPolicyInput(
            mode=AccessMode.AUTO_LOCK, duration_seconds=3600
        )

    def test_create_passes_approval_mode_to_client(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
            "approvalMode": "AUTOMATIC",
        }

        mock_api_client.resource_access_add.return_value = True

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=resource_access_spec,
                memo=MagicMock(),
                logger=MagicMock(),
                patch=MagicMock(),
                status={},
            )

        call_kwargs = mock_api_client.resource_access_add.call_args.kwargs
        assert call_kwargs["approval_mode"] == AccessApprovalMode.AUTOMATIC


class TestDeleteOldAccess:
    PRINCIPAL_ID = "R3JvdXA6MTE1NzI2MA=="

    @staticmethod
    def run_sync(access_spec, resource_spec, status, patch_shim=None):
        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            return twingate_resource_access_sync(
                body="",
                namespace="default",
                spec=access_spec,
                memo=MagicMock(),
                logger=MagicMock(),
                patch=patch_shim
                if patch_shim is not None
                else SimpleNamespace(spec={}, status={}),
                status=status,
            )

    @classmethod
    def build_access_spec(cls, resource_spec):
        return {
            "resourceRef": {"name": resource_spec.name},
            "principalId": cls.PRINCIPAL_ID,
        }

    @classmethod
    def recorded_status(cls, resource_id):
        return {"resourceId": resource_id, "principalId": cls.PRINCIPAL_ID}

    @classmethod
    def legacy_recorded_status(cls, resource_id, *, success=True):
        return {
            "twingate_resource_access_change": {
                "success": success,
                "resource_id": resource_id,
                "principal_id": cls.PRINCIPAL_ID,
            }
        }

    def test_deletes_access_to_the_old_resource_id(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")

        result = self.run_sync(
            self.build_access_spec(resource_spec),
            resource_spec,
            self.recorded_status("old-resource-id"),
        )

        assert result["resource_id"] == "new-resource-id"
        mock_api_client.resource_access_remove.assert_called_once_with(
            "old-resource-id", self.PRINCIPAL_ID
        )
        assert [call[0] for call in mock_api_client.mock_calls] == [
            "resource_access_remove",
            "resource_access_add",
        ]

    def test_does_not_repeat_the_removal_on_the_next_tick(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        # Without a record of what it just granted, the timer would recompute the same
        # stale pair and re-issue the removal on every tick.
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")
        access_spec = self.build_access_spec(resource_spec)
        patch_shim = SimpleNamespace(spec={}, status={})
        status = self.recorded_status("old-resource-id")

        self.run_sync(access_spec, resource_spec, status, patch_shim)
        status |= patch_shim.status  # Kopf merge-patches patch.status into .status.
        self.run_sync(access_spec, resource_spec, status, patch_shim)

        mock_api_client.resource_access_remove.assert_called_once_with(
            "old-resource-id", self.PRINCIPAL_ID
        )

    def test_deletes_access_for_the_old_group_id(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource_spec = network_resource_factory().to_spec()
        status = self.recorded_status(resource_spec.id) | {
            "principalId": "old-group-id"
        }

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_group_ref_object",
            return_value={"spec": {"id": "new-group-id"}},
        ):
            result = self.run_sync(
                {
                    "resourceRef": {"name": resource_spec.name},
                    "groupRef": {"name": "group"},
                },
                resource_spec,
                status,
            )

        assert result["principal_id"] == "new-group-id"
        mock_api_client.resource_access_remove.assert_called_once_with(
            resource_spec.id, "old-group-id"
        )

    def test_keeps_access_when_the_ids_are_unchanged(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource_spec = network_resource_factory().to_spec()

        self.run_sync(
            self.build_access_spec(resource_spec),
            resource_spec,
            self.recorded_status(resource_spec.id),
        )

        mock_api_client.resource_access_remove.assert_not_called()

    def test_keeps_access_without_a_previous_status(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        # Nothing records an earlier grant, so there is no access to take away.
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")

        self.run_sync(self.build_access_spec(resource_spec), resource_spec, {})

        mock_api_client.resource_access_remove.assert_not_called()

    def test_retries_the_removal_after_a_failed_reconcile(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        # The IDs are recorded only on success, so a failed reconcile does not hide the
        # grant that an earlier one made and that still has to be taken away.
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")
        status = self.recorded_status("old-resource-id") | {
            "twingate_resource_access_change": {"success": False, "error": "boom"}
        }

        self.run_sync(self.build_access_spec(resource_spec), resource_spec, status)

        mock_api_client.resource_access_remove.assert_called_once_with(
            "old-resource-id", self.PRINCIPAL_ID
        )
        assert [call[0] for call in mock_api_client.mock_calls] == [
            "resource_access_remove",
            "resource_access_add",
        ]

    def test_deletes_access_recorded_by_an_earlier_operator_version(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        # Bindings last reconciled before the IDs moved to the root of the status carry them
        # under the create handler's result.
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")
        patch_shim = SimpleNamespace(spec={}, status={})

        self.run_sync(
            self.build_access_spec(resource_spec),
            resource_spec,
            self.legacy_recorded_status("old-resource-id"),
            patch_shim,
        )

        mock_api_client.resource_access_remove.assert_called_once_with(
            "old-resource-id", self.PRINCIPAL_ID
        )
        assert patch_shim.status == {
            "resourceId": "new-resource-id",
            "principalId": self.PRINCIPAL_ID,
        }

    def test_fails_when_the_deletion_is_rejected(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")
        mock_api_client.resource_access_remove.side_effect = GraphQLMutationError(
            "resourceAccessRemove", "some error"
        )

        with patch("kopf.exception") as kopf_exception_mock:
            result = self.run_sync(
                self.build_access_spec(resource_spec),
                resource_spec,
                self.recorded_status("old-resource-id"),
            )

        assert result == {"success": False, "error": "some error", "ts": ANY}
        mock_api_client.resource_access_add.assert_not_called()
        kopf_exception_mock.assert_called_once_with(
            "", reason="Failure", message="resourceAccessRemove failed: some error"
        )

    def test_transport_error_on_the_deletion_is_retried(
        self, network_resource_factory, kopf_info_mock, mock_api_client
    ):
        # Unlike the GraphQL rejection above, a transient error must propagate instead of
        # being recorded as a failure, so the handler is retried and the old access is
        # removed on a later attempt.
        resource_spec = network_resource_factory().to_spec(id="new-resource-id")
        mock_api_client.resource_access_remove.side_effect = TransportServerError(
            "boom"
        )

        with pytest.raises(TransportServerError):
            self.run_sync(
                self.build_access_spec(resource_spec),
                resource_spec,
                self.recorded_status("old-resource-id"),
            )

        mock_api_client.resource_access_add.assert_not_called()


class TestResourceAccessDelete:
    def test_delete_success(self, network_resource_factory, mock_api_client):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.resource_access_remove.return_value = True

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        status = {"principalId": resource_access_spec["principalId"]}

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            twingate_resource_access_delete(
                "default", resource_access_spec, status, memo_mock, logger_mock
            )

        mock_api_client.resource_access_remove.assert_called_once_with(
            resource.id, resource_access_spec["principalId"]
        )

    def test_delete_with_a_principal_recorded_by_an_earlier_operator_version(
        self, network_resource_factory, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        status = {
            "twingate_resource_access_change": {
                "success": True,
                "principal_id": resource_access_spec["principalId"],
            }
        }

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            twingate_resource_access_delete(
                "default", resource_access_spec, status, memo_mock, logger_mock
            )

        mock_api_client.resource_access_remove.assert_called_once_with(
            resource.id, resource_access_spec["principalId"]
        )

    def test_delete_resource_doesnt_exist_does_nothing(self, mock_api_client):
        resource_access_spec = {
            "resourceRef": {"name": "doesnt-exist"},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        status = {"principalId": resource_access_spec["principalId"]}

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=None,
        ):
            twingate_resource_access_delete(
                "default", resource_access_spec, status, memo_mock, logger_mock
            )

        mock_api_client.resource_access_remove.assert_not_called()

    def test_delete_success_without_calling_api_if_create_handler_never_ran(
        self, network_resource_factory, mock_api_client
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.resource_access_remove.return_value = True

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            twingate_resource_access_delete(
                "default", resource_access_spec, {}, memo_mock, logger_mock
            )

        mock_api_client.resource_access_remove.assert_not_called()


class TestResourceAccessByResource:
    def test_defaults_to_binding_namespace_when_ref_namespace_omitted(self):
        result = twingate_resource_access_by_resource(
            namespace="access-ns",
            name="access-name",
            spec={"resourceRef": {"name": "res"}},
        )
        assert result == {
            ("access-ns", "res"): {"namespace": "access-ns", "name": "access-name"}
        }

    def test_uses_resource_namespace_when_set(self):
        result = twingate_resource_access_by_resource(
            namespace="access-ns",
            name="access-name",
            spec={"resourceRef": {"name": "res", "namespace": "res-ns"}},
        )
        assert result == {
            ("res-ns", "res"): {"namespace": "access-ns", "name": "access-name"}
        }

    def test_none_without_resource_name(self):
        result = twingate_resource_access_by_resource(
            namespace="access-ns", name="access-name", spec={"resourceRef": {}}
        )
        assert result is None


class TestResourceAccessByGroup:
    def test_defaults_to_binding_namespace_when_ref_namespace_omitted(self):
        result = twingate_resource_access_by_group(
            namespace="access-ns",
            name="access-name",
            spec={"groupRef": {"name": "grp"}},
        )
        assert result == {
            ("access-ns", "grp"): {"namespace": "access-ns", "name": "access-name"}
        }

    def test_uses_group_namespace_when_set(self):
        result = twingate_resource_access_by_group(
            namespace="access-ns",
            name="access-name",
            spec={"groupRef": {"name": "grp", "namespace": "grp-ns"}},
        )
        assert result == {
            ("grp-ns", "grp"): {"namespace": "access-ns", "name": "access-name"}
        }

    def test_none_without_group_ref(self):
        result = twingate_resource_access_by_group(
            namespace="access-ns",
            name="access-name",
            spec={"principalId": "R3JvdXA6MTE1NzI2MA=="},
        )
        assert result is None


def make_access_obj(_plural=None, _namespace=None, name="access1", *, status=None):
    obj = {"metadata": {"namespace": "access-ns", "name": name}, "spec": {"x": name}}
    if status:
        obj["status"] = status
    return obj


def record_id(field, new_id="new-id"):
    """Stand in for a reconcile that recorded an ID on the patch shim it was passed."""

    def side_effect(*args):
        args[-1].status[field] = new_id

    return side_effect


@patch("app.handlers.handlers_resource_access.k8s_patch_twingate_custom_object")
@patch("app.handlers.handlers_resource_access.k8s_get_twingate_custom_object")
@patch("app.handlers.handlers_resource_access.reconcile_resource_access")
class TestResourceIdChanged:
    @staticmethod
    def build_index(refs=None):
        return {
            ("ns", "res"): refs
            if refs is not None
            else [{"namespace": "access-ns", "name": "access1"}]
        }

    def call_handler(self, index, new="new-id"):
        twingate_resource_id_changed(
            namespace="ns",
            name="res",
            new=new,
            memo=MagicMock(),
            logger=MagicMock(),
            twingate_resource_access_by_resource=index,
        )

    def test_reconciles_referencing_access(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        # Two bindings reference the same Resource - both must be reconciled, and what each
        # reconcile recorded persisted onto its own binding.
        mock_get_obj.side_effect = make_access_obj
        mock_reconcile.side_effect = record_id("resourceId")

        self.call_handler(
            self.build_index(
                [
                    {"namespace": "access-ns", "name": "access1"},
                    {"namespace": "access-ns", "name": "access2"},
                ]
            )
        )

        assert mock_reconcile.call_count == 2
        assert mock_patch_obj.call_count == 2
        for call, name in zip(
            mock_patch_obj.call_args_list, ("access1", "access2"), strict=True
        ):
            plural, namespace, obj_name, shim = call.args
            assert (plural, namespace, obj_name) == (
                "twingateresourceaccesses",
                "access-ns",
                name,
            )
            assert shim.status == {"resourceId": "new-id"}

    def test_reconciles_with_the_bindings_own_namespace_and_status(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        # Refs resolve in the binding's namespace, not that of the Resource whose ID
        # changed, and the status carries the principal ID recorded for
        # principalExternalRef bindings.
        status = {"resourceId": "stale-id", "principalId": "principal-id"}
        mock_get_obj.return_value = make_access_obj(status=status)

        self.call_handler(self.build_index())

        _body, namespace, _spec, passed_status = mock_reconcile.call_args.args[:4]
        assert (namespace, passed_status) == ("access-ns", status)

    def test_skips_binding_already_on_the_new_id(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        # Already reconciled onto the new id - nothing to re-issue.
        mock_get_obj.return_value = make_access_obj(status={"resourceId": "new-id"})

        self.call_handler(self.build_index())

        mock_reconcile.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_skips_binding_recorded_by_an_earlier_operator_version(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        mock_get_obj.return_value = make_access_obj(
            status={
                "twingate_resource_access_change": {
                    "success": True,
                    "resource_id": "new-id",
                }
            }
        )

        self.call_handler(self.build_index())

        mock_reconcile.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_noop_when_id_unset(self, mock_reconcile, mock_get_obj, mock_patch_obj):
        self.call_handler(self.build_index(), new=None)
        mock_get_obj.assert_not_called()
        mock_reconcile.assert_not_called()

    def test_noop_without_referencing_access(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        self.call_handler({})
        mock_get_obj.assert_not_called()
        mock_reconcile.assert_not_called()

    def test_records_nothing_when_the_reconcile_fails(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        # A failed reconcile writes no IDs, so the patch stays empty and persisting it is a
        # no-op rather than an overwrite with stale values.
        mock_get_obj.side_effect = make_access_obj
        mock_reconcile.return_value = {"success": False, "error": "boom"}

        self.call_handler(self.build_index())

        assert mock_patch_obj.call_args.args[3].status == {}

    def test_skips_when_access_object_missing(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        mock_get_obj.return_value = None

        self.call_handler(self.build_index())

        mock_reconcile.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_continues_on_non_transient_failure(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        # Swallowed; the resource access timer is the backstop.
        mock_get_obj.side_effect = make_access_obj
        mock_reconcile.side_effect = RuntimeError("boom")

        self.call_handler(self.build_index())

        mock_patch_obj.assert_not_called()

    def test_one_not_ready_does_not_starve_others(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        mock_get_obj.side_effect = make_access_obj

        def reconcile_side_effect(body, *args):
            if body["spec"]["x"] == "access1":
                raise kopf.TemporaryError("not ready")
            args[-1].status["resourceId"] = "new-id"

        mock_reconcile.side_effect = reconcile_side_effect

        with pytest.raises(kopf.TemporaryError):
            self.call_handler(
                self.build_index(
                    [
                        {"namespace": "access-ns", "name": "access1"},
                        {"namespace": "access-ns", "name": "access2"},
                    ]
                )
            )

        # The second binding was still attempted, and persisted, after the first raised.
        assert mock_reconcile.call_count == 2
        assert mock_patch_obj.call_count == 1


@patch("app.handlers.handlers_resource_access.k8s_patch_twingate_custom_object")
@patch("app.handlers.handlers_resource_access.k8s_get_twingate_custom_object")
@patch("app.handlers.handlers_resource_access.reconcile_resource_access")
class TestGroupIdChanged:
    def call_handler(self, index, new="new-id"):
        twingate_group_id_changed(
            namespace="ns",
            name="grp",
            new=new,
            memo=MagicMock(),
            logger=MagicMock(),
            twingate_resource_access_by_group=index,
        )

    def test_reconciles_referencing_access(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        mock_get_obj.side_effect = make_access_obj
        mock_reconcile.side_effect = record_id("principalId")

        self.call_handler(
            {("ns", "grp"): [{"namespace": "access-ns", "name": "access1"}]}
        )

        mock_reconcile.assert_called_once()
        plural, namespace, obj_name, shim = mock_patch_obj.call_args.args
        assert (plural, namespace, obj_name) == (
            "twingateresourceaccesses",
            "access-ns",
            "access1",
        )
        assert shim.status == {"principalId": "new-id"}

    def test_skips_binding_already_on_the_new_id(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        # The group handler compares the principal ID, not the resource ID.
        mock_get_obj.return_value = make_access_obj(status={"principalId": "new-id"})

        self.call_handler(
            {("ns", "grp"): [{"namespace": "access-ns", "name": "access1"}]}
        )

        mock_reconcile.assert_not_called()
        mock_patch_obj.assert_not_called()

    def test_noop_when_id_unset(self, mock_reconcile, mock_get_obj, mock_patch_obj):
        self.call_handler(
            {("ns", "grp"): [{"namespace": "access-ns", "name": "access1"}]}, new=None
        )
        mock_get_obj.assert_not_called()
        mock_reconcile.assert_not_called()

    def test_noop_without_referencing_access(
        self, mock_reconcile, mock_get_obj, mock_patch_obj
    ):
        self.call_handler({})
        mock_get_obj.assert_not_called()
        mock_reconcile.assert_not_called()
