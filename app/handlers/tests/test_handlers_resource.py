from unittest.mock import ANY, MagicMock, patch

import pytest

from app.crds import ResourceSpec
from app.handlers.handlers_resource import (
    twingate_resource_create,
    twingate_resource_delete,
    twingate_resource_sync,
    twingate_resource_update,
)
from app.settings import TwingateOperatorSettings


@pytest.fixture
def mock_api_client():
    api_client_instance = MagicMock()
    with patch("app.handlers.handlers_resource.TwingateAPIClient") as mock_api_client:
        mock_api_client.return_value = api_client_instance
        yield api_client_instance


@pytest.fixture
def mock_k8s_metadata():
    return {
        "name": "my-resource",
        "namespace": "default",
        "uid": "ad0298c5-b84f-4617-b4a2-d3cbbe9f6a4c",
        "labels": {"env": "dev"},
    }


@pytest.fixture
def mock_memo():
    return MagicMock(
        twingate_settings=TwingateOperatorSettings(
            network="slug",
            host="test.com",
            api_key="test_key",
            remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
        )
    )


@pytest.fixture
def mock_memo_with_default_resource_tags():
    return MagicMock(
        twingate_settings=TwingateOperatorSettings(
            network="slug",
            host="test.com",
            api_key="test_key",
            remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
            default_resource_tags={
                "managed_by": "test",
                "env": "test",
            },
        )
    )


class TestResourceCreateHandler:
    def test_create(
        self,
        resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        resource = resource_factory()
        resource_spec = resource.to_spec(id=None)
        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_create.return_value = resource

        result = twingate_resource_create(
            body="",
            labels=mock_k8s_metadata["labels"],
            spec=spec,
            memo=mock_memo_with_default_resource_tags,
            logger=logger_mock,
            patch=patch_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": resource.id,
            "created_at": ANY,
            "updated_at": ANY,
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_not_called()
        mock_api_client.resource_create.assert_called_once_with(
            **resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"},
                exclude={"id"},
            )
        )
        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Created on Twingate as {resource.id}"
        )
        assert patch_mock.spec == {"id": resource.id}

    def test_when_id_is_specified_update_instead_of_create(
        self,
        resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo,
    ):
        resource = resource_factory(id="pre-existing-id")
        resource_spec = resource.to_spec()

        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_update.return_value = resource

        result = twingate_resource_create(
            body="",
            labels=mock_k8s_metadata["labels"],
            spec=spec,
            memo=mock_memo,
            logger=logger_mock,
            patch=patch_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": resource.id,
            "created_at": ANY,
            "updated_at": ANY,
            "message": ANY,
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_called_once_with(
            **resource_spec.to_graphql_arguments(labels={"env": "dev"}, exclude={"id"})
        )
        mock_api_client.resource_create.assert_not_called()

        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Imported {resource.id}"
        )


class TestResourceUpdateHandler:
    def test_update(
        self,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        rid = "UmVzb3VyY2U6OTMxODE3"
        spec = new = {
            "id": rid,
            "address": "my.default.cluster.local",
            "name": "new-name",
        }
        diff = (("change", ("spec", "name"), "My K8S Resource", "new-name"),)
        status = {
            "twingate_resource_create": {
                "twingate_id": rid,
                "created_at": "2023-09-27T04:02:55.249011+00:00",
                "updated_at": "2023-09-27T04:02:55.249035+00:00",
            }
        }
        new_resource_spec = ResourceSpec(**new)

        mock_api_client.resource_update.return_value = MagicMock(id=rid)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        result = twingate_resource_update(
            mock_k8s_metadata["labels"],
            spec,
            diff,
            status,
            mock_memo_with_default_resource_tags,
            logger_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": rid,
            "created_at": ANY,
            "updated_at": ANY,
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_called_once_with(
            **new_resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"}
            )
        )
        assert patch_mock.spec == {}

    def test_update_called_without_id_fails(self, mock_api_client, mock_k8s_metadata):
        spec = {
            "address": "my.default.cluster.local",
            "name": "new-name",
        }
        diff = []
        status = {}

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        result = twingate_resource_update(
            mock_k8s_metadata["labels"], spec, diff, status, memo_mock, logger_mock
        )
        assert result == {
            "success": False,
            "error": "Resource ID is missing in the spec",
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_not_called()
        assert patch_mock.spec == {}

    def test_update_caused_by_create_does_nothing(
        self, mock_api_client, mock_k8s_metadata
    ):
        rid = "UmVzb3VyY2U6OTMxODE3"
        spec = {
            "id": rid,
            "address": "my.default.cluster.local",
            "name": "new-name",
        }
        diff = (("add", ("spec", "id"), None, rid),)
        status = {
            "twingate_resource_create": {
                "twingate_id": rid,
                "created_at": "2023-09-27T04:02:55.249011+00:00",
                "updated_at": "2023-09-27T04:02:55.249035+00:00",
            }
        }

        mock_api_client.resource_update.return_value = MagicMock(id=rid)

        logger_mock = MagicMock()
        memo_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        result = twingate_resource_update(
            mock_k8s_metadata["labels"], spec, diff, status, memo_mock, logger_mock
        )
        assert result == {
            "success": True,
            "twingate_id": rid,
            "message": "No update required",
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_not_called()
        assert patch_mock.spec == {}


class TestResourceDeleteHandler:
    def test_delete(self, mock_api_client):
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

        mock_api_client.resource_delete.assert_called_once_with("test-id")

    def test_delete_without_status_does_nothing(self, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {"address": "my.default.cluster.local", "name": "My K8S Resource"}

        twingate_resource_delete(spec, {}, memo_mock, logger_mock)

        mock_api_client.resource_delete.assert_not_called()

    def test_delete_without_twingate_id_does_nothing(self, mock_api_client):
        logger_mock = MagicMock()
        memo_mock = MagicMock()

        spec = {"address": "my.default.cluster.local", "name": "My K8S Resource"}

        twingate_resource_delete(spec, {"foo": "bar"}, memo_mock, logger_mock)

        mock_api_client.resource_delete.assert_not_called()


class TestResourceSyncTimer:
    def test_sync_when_resource_exists_and_doesnt_need_update(
        self, resource_factory, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        mock_k8s_metadata["labels"] = resource.to_metadata_labels()
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        mock_api_client.get_resource.return_value = resource

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            mock_k8s_metadata["labels"],
            resource_spec.model_dump(by_alias=True),
            status,
            mock_memo,
            logger_mock,
            patch_mock,
        )

        mock_api_client.resource_update.assert_not_called()
        assert patch_mock.spec == {}

    def test_sync_when_resource_exists_and_spec_requires_update(
        self, resource_factory, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        mock_k8s_metadata["labels"] = resource.to_metadata_labels()
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        mutated_resource = resource.model_copy(update={"name": "new-name"})

        mock_api_client.get_resource.return_value = mutated_resource

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            mock_k8s_metadata["labels"],
            resource_spec.model_dump(by_alias=True),
            status,
            mock_memo,
            logger_mock,
            patch_mock,
        )

        mock_api_client.resource_update.assert_called_once_with(
            **resource_spec.to_graphql_arguments(labels=resource.to_metadata_labels())
        )
        assert patch_mock.spec == {}

    def test_sync_when_resource_exists_and_label_requires_update(
        self,
        resource_factory,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        mock_k8s_metadata["labels"] = {"env": "dev"} | resource.to_metadata_labels()
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        mock_api_client.get_resource.return_value = resource
        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            mock_k8s_metadata["labels"],
            resource_spec.model_dump(by_alias=True),
            status,
            mock_memo_with_default_resource_tags,
            logger_mock,
            patch_mock,
        )

        mock_api_client.resource_update.assert_called_once_with(
            **resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"}
                | resource.to_metadata_labels()
            )
        )
        assert patch_mock.spec == {}

    def test_sync_when_resource_doesnt_exists_recreate_it(
        self,
        resource_factory,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        resource = resource_factory()
        resource_spec = resource.to_spec()
        status = {
            "twingate_resource_create": {
                "twingate_id": resource.id,
                "created_at": resource.created_at.isoformat(),
                "updated_at": resource.updated_at.isoformat(),
            }
        }

        mock_api_client.get_resource.return_value = None
        mock_api_client.resource_create.return_value = resource

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        twingate_resource_sync(
            mock_k8s_metadata["labels"],
            resource_spec.model_dump(by_alias=True),
            status,
            mock_memo_with_default_resource_tags,
            logger_mock,
            patch_mock,
        )

        mock_api_client.resource_update.assert_not_called()
        mock_api_client.resource_create.assert_called_once_with(
            **resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"},
                exclude={"id"},
            )
        )

        assert patch_mock.spec == {"id": resource.id}
