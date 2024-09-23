from unittest.mock import MagicMock, patch

import pytest

from app.handlers.handlers_groups import twingate_group_delete


@pytest.fixture
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_groups.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


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
