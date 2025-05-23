from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client import GraphQLMutationError
from app.crds import K8sMetadata
from app.handlers.handlers_resource_access import (
    get_principal_id,
    twingate_resource_access_delete,
    twingate_resource_access_sync,
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
        assert get_principal_id(access_crd, None, MagicMock()) == "R3JvdXA6MTE1NzI2MA=="

    def test_id_invalid_spec(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.principal_external_ref = None
        access_crd.get_group_ref_object.return_value = None
        with pytest.raises(
            ValueError, match="Missing principal_id or principal_external_ref"
        ):
            get_principal_id(access_crd, None, MagicMock())

    def test_id_from_group_ref_object(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.principal_external_ref = None
        access_crd.get_group_ref_object.return_value = {"spec": {"id": "group-id"}}
        assert get_principal_id(access_crd, None, MagicMock()) == "group-id"

    def test_id_from_group_ref_object_not_ready_raises_temoraryerror(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.principal_external_ref = None
        access_crd.get_group_ref_object.return_value = {"spec": {"id": None}}
        with pytest.raises(kopf.TemporaryError):
            assert get_principal_id(access_crd, None, MagicMock()) == "group-id"

    def test_from_external_ref_group(self, mock_api_client):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "group"
        access_crd.principal_external_ref.name = "group-name"

        mock_api_client.get_group_id.return_value = "R3JvdXA6MTE1NzI2MA=="

        assert (
            get_principal_id(access_crd, None, mock_api_client)
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
            get_principal_id(access_crd, None, mock_api_client)
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
            ValueError, match="Principal serviceAccount sa-name not found"
        ):
            get_principal_id(access_crd, None, mock_api_client)

    def test_from_external_ref_invalid_type_returns_none(self, mock_api_client):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "invalid"
        access_crd.principal_external_ref.name = "sa-name"

        with pytest.raises(ValueError, match="Unknown principal type: invalid"):
            get_principal_id(access_crd, None, mock_api_client)

    def test_from_external_ref_uses_created_status_principal_id(self):
        access_crd = MagicMock()
        access_crd.principal_id = None
        access_crd.get_group_ref_object.return_value = None
        access_crd.principal_external_ref = MagicMock()
        access_crd.principal_external_ref.type = "invalid"
        access_crd.principal_external_ref.name = "sa-name"

        expected = "success"
        principal_id = get_principal_id(
            access_crd, {"principal_id": expected}, mock_api_client
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
        patch_mock = MagicMock()
        patch_mock.metadata = {}

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            result = twingate_resource_access_sync(
                body="",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_mock,
                status={},
            )
            assert result == {
                "success": True,
                "ts": ANY,
                "principal_id": ANY,
                "resource_id": ANY,
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

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=None,
        ):
            with patch("kopf.warn") as kopf_warn_mock:
                result = twingate_resource_access_sync(
                    body="",
                    spec=resource_access_spec,
                    memo=memo_mock,
                    logger=logger_mock,
                    patch=patch_mock,
                    status={},
                )
                assert result == {
                    "success": False,
                    "error": "Resource default/invalid not found",
                }

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
        patch_mock = MagicMock()
        patch_mock.metadata = {}
        patch_mock.metadata["ownerReferences"] = []

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
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_mock,
                status={},
            )
            assert result == {"success": False, "error": "some error", "ts": ANY}

        kopf_exception_mock.assert_called_once_with(
            "", reason="Failure", message="resourceCreate failed: some error"
        )
        assert patch_mock.metadata["ownerReferences"] == []


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
                resource_access_spec, status, memo_mock, logger_mock
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
        status = {
            "twingate_resource_access_change": {
                "success": True,
                "principal_id": resource_access_spec["principalId"],
            }
        }

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=None,
        ):
            twingate_resource_access_delete(
                resource_access_spec, status, memo_mock, logger_mock
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
                resource_access_spec, {}, memo_mock, logger_mock
            )

        mock_api_client.resource_access_remove.assert_not_called()
