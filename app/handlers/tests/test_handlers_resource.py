from unittest.mock import ANY, MagicMock, patch

import pytest

from app.crds import ResourceSpec
from app.handlers.handlers_resource import (
    twingate_resource_create,
    twingate_resource_delete,
    twingate_resource_sync,
    twingate_resource_update,
)


@pytest.fixture()
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_resource.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


class TestResourceCreateHandler:
    def test_create(self, resource_factory, kopf_info_mock, mock_api_client):
        resource = resource_factory()
        resource_spec = resource.to_spec(id=None)

        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_create.return_value = resource

        result = twingate_resource_create(
            body="", spec=spec, memo=memo_mock, logger=logger_mock, patch=patch_mock
        )
        assert result == {
            "success": True,
            "twingate_id": resource.id,
            "created_at": ANY,
            "updated_at": ANY,
            "ts": ANY,
        }

        mock_api_client.resource_create.assert_called_once_with(resource_spec)
        logger_mock.info.assert_called_once_with("Got a create request: %s", spec)
        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Created on Twingate as {resource.id}"
        )
        assert patch_mock.spec == {"id": resource.id}


class TestResourceUpdateHandler:
    def test_update(self):
        rid = "UmVzb3VyY2U6OTMxODE3"
        old = {
            "spec": {
                "id": rid,
                "address": "my.default.cluster.local",
                "name": "My K8S Resource",
            }
        }
        new = {
            "spec": {
                "id": rid,
                "address": "my.default.cluster.local",
                "name": "new-name",
            }
        }
        diff = (("change", ("spec", "name"), "My K8S Resource", "new-name"),)
        status = {
            "twingate_resource_create": {
                "twingate_id": rid,
                "created_at": "2023-09-27T04:02:55.249011+00:00",
                "updated_at": "2023-09-27T04:02:55.249035+00:00",
            }
        }
        new_resource_spec = ResourceSpec(**new["spec"])

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        memo_mock.twingate_client.resource_update.return_value = MagicMock(id=rid)
        patch_mock = MagicMock()
        patch_mock.spec = {}

        result = twingate_resource_update(
            old, new, diff, status, memo_mock, logger_mock
        )
        assert result == {
            "success": True,
            "twingate_id": rid,
            "created_at": ANY,
            "updated_at": ANY,
            "ts": ANY,
        }

        memo_mock.twingate_client.resource_update.assert_called_once_with(
            new_resource_spec
        )
        assert patch_mock.spec == {}


class TestResourceDeleteHandler:
    def test_delete(self):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {
            "id": "test-id",
            "address": "my.default.cluster.local",
            "name": "My K8S Resource",
        }

        twingate_resource_delete(
            spec,
            {"twingate_resource_create": {"twingate_id": "test-id"}},
            memo_mock,
            logger_mock,
        )

        memo_mock.twingate_client.resource_delete.assert_called_once_with("test-id")

    def test_delete_without_status_does_nothing(self):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {"address": "my.default.cluster.local", "name": "My K8S Resource"}

        twingate_resource_delete(spec, {}, memo_mock, logger_mock)

        memo_mock.twingate_client.resource_delete.assert_not_called()

    def test_delete_without_twingate_id_does_nothing(self):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {"address": "my.default.cluster.local", "name": "My K8S Resource"}

        twingate_resource_delete(spec, {"foo": "bar"}, memo_mock, logger_mock)

        memo_mock.twingate_client.resource_delete.assert_not_called()


class TestResourceSyncTimer:
    def test_sync_when_resource_exists_and_doesnt_need_update(self, resource_factory):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            resource_spec.model_dump(by_alias=True, exclude="id"),
            status,
            memo_mock,
            logger_mock,
            patch_mock,
        )

        memo_mock.twingate_client.resource_update.assert_not_called()
        assert patch_mock.spec == {}

    def test_sync_when_resource_exists_and_requires_update(self, resource_factory):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        mutated_resource = resource.model_copy(update={"name": "new-name"})

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        memo_mock.twingate_client.get_resource.return_value = mutated_resource
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            resource_spec.model_dump(by_alias=True),
            status,
            memo_mock,
            logger_mock,
            patch_mock,
        )

        memo_mock.twingate_client.resource_update.assert_called_once_with(resource_spec)
        assert patch_mock.spec == {}

    def test_sync_when_resource_doesnt_exists_recreate_it(self, resource_factory):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        resource_spec_without_id = resource_spec.model_copy(update={"id": None})
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        memo_mock.twingate_client.get_resource.return_value = None
        memo_mock.twingate_client.resource_create.return_value = resource
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            resource_spec.model_dump(by_alias=True),
            status,
            memo_mock,
            logger_mock,
            patch_mock,
        )

        memo_mock.twingate_client.resource_update.assert_not_called()
        memo_mock.twingate_client.resource_create.assert_called_once_with(
            resource_spec_without_id
        )

        assert patch_mock.spec == {"id": resource.id}
