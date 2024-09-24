from unittest.mock import ANY, MagicMock, patch

import pytest

from app.api.exceptions import GraphQLMutationError
from app.crds import GroupSpec
from app.handlers.handlers_groups import (
    twingate_group_create_update,
    twingate_group_delete,
)


@pytest.fixture
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_groups.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


class TestGroupCreateUpdateHandler:
    def test_create(self, kopf_info_mock, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        group_id = "test-group-id"
        spec = {
            "name": "Test Group",
        }

        mock_api_client.group_create.return_value = group_id

        result = twingate_group_create_update(
            "",
            spec,
            logger_mock,
            memo_mock,
            patch_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": group_id,
            "ts": ANY,
        }

        mock_api_client.group_update.assert_not_called()
        mock_api_client.group_create.assert_called_once_with(GroupSpec(**spec))
        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Created on Twingate as {group_id}"
        )
        assert patch_mock.spec == {"id": group_id}

    def test_update(self, kopf_info_mock, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        group_id = "test-group-id"
        spec = {
            "id": group_id,
            "name": "Test Group",
        }

        mock_api_client.group_update.return_value = group_id

        result = twingate_group_create_update(
            "",
            spec,
            logger_mock,
            memo_mock,
            patch_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": group_id,
            "ts": ANY,
        }

        mock_api_client.group_create.assert_not_called()
        mock_api_client.group_update.assert_called_once_with(GroupSpec(**spec))
        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Updated {group_id}"
        )
        assert patch_mock.spec == {}

    def test_update_when_remote_doesnt_exist_resets_id(
        self, kopf_exception_mock, mock_api_client
    ):
        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        group_id = "test-group-id"
        spec = {
            "id": group_id,
            "name": "Test Group",
        }

        mock_api_client.group_update.side_effect = GraphQLMutationError(
            "UpdateGroup", "Group does not exist"
        )

        result = twingate_group_create_update(
            "",
            spec,
            logger_mock,
            memo_mock,
            patch_mock,
        )
        assert result == {
            "success": False,
            "error": "UpdateGroup mutation failed - Group does not exist.",
            "ts": ANY,
        }

        mock_api_client.group_create.assert_not_called()
        mock_api_client.group_update.assert_called_once_with(GroupSpec(**spec))
        kopf_exception_mock.assert_called_once_with("", reason="Failed to update group", exc=mock_api_client.group_update.side_effect)  # fmt: skip
        assert patch_mock.spec == {"id": None}

    def test_update_if_diff_id_changes_from_none_then_skips(self, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        group_id = "test-group-id"
        spec = {
            "id": group_id,
            "name": "Test Group",
        }

        result = twingate_group_create_update(
            "",
            spec,
            logger_mock,
            memo_mock,
            patch_mock,
            diff=(("add", ("spec", "id"), None, group_id),),
        )
        assert result == {
            "success": True,
            "ts": ANY,
        }

        mock_api_client.group_create.assert_not_called()
        mock_api_client.group_update.assert_not_called()
        assert patch_mock.spec == {}


class TestGroupDeleteHandler:
    def test_delete(self, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        group_id = "test-group-id"
        spec = {
            "id": group_id,
            "name": "Test Group",
        }
        twingate_group_delete(
            spec,
            {
                "twingate_group_create_update": {
                    "success": True,
                    "twingate_id": group_id,
                }
            },
            memo_mock,
            logger_mock,
        )

        mock_api_client.group_delete.assert_called_once_with(group_id)

    def test_delete_without_status_does_nothing(self, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {"name": "My Group"}

        twingate_group_delete(spec, {}, memo_mock, logger_mock)

        mock_api_client.resource_delete.assert_not_called()

    def test_delete_without_twingate_id_does_nothing(self, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {"name": "My Group"}

        twingate_group_delete(spec, {"foo": "bar"}, memo_mock, logger_mock)

        mock_api_client.resource_delete.assert_not_called()
