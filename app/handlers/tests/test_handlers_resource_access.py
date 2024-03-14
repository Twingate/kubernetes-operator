from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.api.client import GraphQLMutationError
from app.crds import K8sMetadata
from app.handlers.handlers_resource_access import (
    twingate_resource_access_create,
    twingate_resource_access_delete,
    twingate_resource_access_sync,
    twingate_resource_access_update,
)


@pytest.fixture()
def mock_api_client():
    api_client_instance = MagicMock()
    with patch(
        "app.handlers.handlers_resource_access.TwingateAPIClient"
    ) as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


class TestResourceAccessCreateHandler:
    def test_create_success(self, resource_factory, kopf_info_mock, mock_api_client):
        resource = resource_factory()
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
        patch_mock.metadata["ownerReferences"] = []

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            result = twingate_resource_access_create(
                body="",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_mock,
            )
            assert result == {"success": True, "ts": ANY}

        kopf_info_mock.assert_called_once_with("", reason="Success", message=ANY)
        assert patch_mock.metadata["ownerReferences"] == [
            {
                "apiVersion": "twingate.com/v1",
                "kind": "TwingateResource",
                "name": "foo",
                "uid": "uid",
            }
        ]

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
                result = twingate_resource_access_create(
                    body="",
                    spec=resource_access_spec,
                    memo=memo_mock,
                    logger=logger_mock,
                    patch=patch_mock,
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

    def test_create_resource_no_id(self, resource_factory, mock_api_client):
        resource = resource_factory()
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

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ), pytest.raises(kopf.TemporaryError):
            twingate_resource_access_create(
                body="",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_mock,
            )

    def test_create_graphql_error_returns_it(self, resource_factory, mock_api_client):
        resource = resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        memo_mock.twingate_client.resource_access_add.side_effect = (
            GraphQLMutationError("resourceCreate", "some error")
        )
        patch_mock = MagicMock()
        patch_mock.metadata = {}
        patch_mock.metadata["ownerReferences"] = []

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ), patch("kopf.exception") as kopf_exception_mock:
            result = twingate_resource_access_create(
                body="",
                spec=resource_access_spec,
                memo=memo_mock,
                logger=logger_mock,
                patch=patch_mock,
            )
            assert result == {"success": False, "error": "some error", "ts": ANY}

        kopf_exception_mock.assert_called_once_with(
            "", reason="Failure", message="resourceCreate failed: some error"
        )
        assert patch_mock.metadata["ownerReferences"] == []


class TestResourceAccessUpdateHandler:
    def test_update_success(self, resource_factory, mock_api_client):
        resource = resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }
        status = {"twingate_resource_access_create": {"ok": True}}

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.resource_access_add.return_value = True

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ):
            result = twingate_resource_access_update(
                spec=resource_access_spec,
                diff={},
                status=status,
                memo=memo_mock,
                logger=logger_mock,
            )
            assert result == {"success": True, "ts": ANY}

    def test_update_fails_to_find_resource(self, mock_api_client):
        resource_access_spec = {
            "resourceRef": {"name": "doesnt-exist"},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }
        status = {"twingate_resource_access_create": {"ok": True}}

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.resource_access_add.return_value = True

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=None,
        ):
            result = twingate_resource_access_update(
                spec=resource_access_spec,
                diff={},
                status=status,
                memo=memo_mock,
                logger=logger_mock,
            )
            assert result == {
                "success": False,
                "error": "Resource default/doesnt-exist not found",
                "ts": ANY,
            }

    def test_update_resource_not_yet_created_should_raise_temp_error(self):
        new = {"principalId": "R3JvdXA6MTE1NzI2MA=="}
        diff = {}
        status = {}
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        with pytest.raises(kopf.TemporaryError) as excinfo:
            twingate_resource_access_update(
                spec=new,
                diff=diff,
                status=status,
                memo=memo_mock,
                logger=logger_mock,
            )

        assert excinfo.value.args[0] == "Resource not yet created, retrying..."


class TestResourceAccessDelete:
    def test_delete_success(self, resource_factory, mock_api_client):
        resource = resource_factory()
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

    def test_delete_resource_doesnt_exist_does_nothing(self, mock_api_client):
        resource_access_spec = {
            "resourceRef": {"name": "doesnt-exist"},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=None,
        ):
            twingate_resource_access_delete(
                resource_access_spec, {}, memo_mock, logger_mock
            )

        mock_api_client.resource_access_remove.assert_not_called()


class TestResourceAccessSync:
    def test_sync_success(self, resource_factory, mock_api_client):
        resource = resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.resource_access_add.return_value = True

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
                status={},
                memo=memo_mock,
                logger=logger_mock,
            )

            assert result == {"success": True, "ts": ANY}

    def test_sync_api_fails(self, resource_factory, mock_api_client):
        resource = resource_factory()
        resource_spec = resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.resource_access_add.side_effect = GraphQLMutationError(
            "resourceAccessAdd", "some error"
        )

        resource_crd_mock = MagicMock()
        resource_crd_mock.spec = resource_spec
        resource_crd_mock.metadata = K8sMetadata(uid="uid", name="foo", namespace="bar")

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=resource_crd_mock,
        ), patch("kopf.exception") as kopf_exception_mock:
            result = twingate_resource_access_sync(
                body="",
                spec=resource_access_spec,
                status={},
                memo=memo_mock,
                logger=logger_mock,
            )

            assert result == {"success": False, "error": "some error", "ts": ANY}

        kopf_exception_mock.assert_called_once_with("", reason="Failure", message=ANY)

    def test_sync_resource_not_found_should_warn(
        self, resource_factory, mock_api_client
    ):
        resource = resource_factory()
        resource.to_spec()

        resource_access_spec = {
            "resourceRef": {"name": "impossible"},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.get_resource.return_value = None

        expected_err = "Resource default/impossible not found"

        with patch(
            "app.handlers.handlers_resource_access.ResourceAccessSpec.get_resource",
            return_value=None,
        ), patch("kopf.warn") as kopf_warn_mock:
            result = twingate_resource_access_sync(
                body="",
                spec=resource_access_spec,
                status={},
                memo=memo_mock,
                logger=logger_mock,
            )
            assert result == {"success": False, "error": expected_err, "ts": ANY}

        kopf_warn_mock.assert_called_once_with(
            "", reason="ResourceNotFound", message=expected_err
        )

    def test_sync_resource_spec_missing_id_should_skip(
        self, resource_factory, mock_api_client
    ):
        resource = resource_factory()
        resource_spec = resource.to_spec(id=None)

        resource_access_spec = {
            "resourceRef": {"name": resource_spec.name},
            "principalId": "R3JvdXA6MTE1NzI2MA==",
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()

        mock_api_client.get_resource.return_value = resource

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
                status={},
                memo=memo_mock,
                logger=logger_mock,
            )

            assert result == {
                "success": True,
                "status": "Skipped as resource not yet created",
                "ts": ANY,
            }
