from unittest.mock import ANY, MagicMock, patch

import kopf
import pytest

from app.crds import ResourceSpec, ResourceType
from app.handlers.handlers_resource import (
    _release_service_ownership,
    _repair_missing_gateway_ref,
    twingate_resource_address_from_index,
    twingate_resource_create,
    twingate_resource_delete,
    twingate_resource_gateway_index,
    twingate_resource_ingress_load_balancer_changed,
    twingate_resource_service_load_balancer_changed,
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


class TestRepairMissingGatewayRef:
    @pytest.fixture
    def mock_get_custom_object(self):
        with patch(
            "app.handlers.handlers_resource.k8s_get_twingate_custom_object"
        ) as mock:
            yield mock

    @pytest.fixture
    def patch_mock(self):
        mock = MagicMock()
        mock.spec = {}
        return mock

    @pytest.mark.parametrize(
        "service_ref",
        [{"name": "gw"}, {"name": "gw", "namespace": "default"}],
    )
    def test_binds_to_the_gateway_referencing_the_same_service(
        self, mock_get_custom_object, patch_mock, service_ref
    ):
        mock_get_custom_object.return_value = {"spec": {"serviceRef": service_ref}}

        repaired = _repair_missing_gateway_ref(
            "gw-resource",
            "default",
            {"type": ResourceType.KUBERNETES},
            patch_mock,
            MagicMock(),
        )

        assert repaired is True
        assert patch_mock.spec == {"gatewayRef": {"name": "gw", "namespace": "default"}}
        mock_get_custom_object.assert_called_once_with(
            "twingategateways", "default", "gw"
        )

    def test_retries_while_the_gateway_does_not_exist_yet(
        self, mock_get_custom_object, patch_mock
    ):
        mock_get_custom_object.return_value = None

        with pytest.raises(kopf.TemporaryError):
            _repair_missing_gateway_ref(
                "gw-resource",
                "default",
                {"type": ResourceType.KUBERNETES},
                patch_mock,
                MagicMock(),
            )

        assert patch_mock.spec == {}

    @pytest.mark.parametrize(
        "service_ref",
        [{"name": "unrelated"}, {"name": "gw", "namespace": "other"}],
    )
    def test_refuses_a_gateway_referencing_a_different_service(
        self, mock_get_custom_object, patch_mock, service_ref
    ):
        mock_get_custom_object.return_value = {"spec": {"serviceRef": service_ref}}

        with pytest.raises(kopf.PermanentError):
            _repair_missing_gateway_ref(
                "gw-resource",
                "default",
                {"type": ResourceType.KUBERNETES},
                patch_mock,
                MagicMock(),
            )

        assert patch_mock.spec == {}

    @pytest.mark.parametrize(
        "spec",
        [
            {"type": ResourceType.NETWORK},
            {"type": ResourceType.WEB_APP, "gatewayRef": {"name": "gw"}},
            {"type": ResourceType.KUBERNETES, "gatewayRef": {"name": "gw"}},
        ],
    )
    def test_leaves_resources_that_need_no_repair_alone(
        self, spec, mock_get_custom_object, patch_mock
    ):
        repaired = _repair_missing_gateway_ref(
            "gw-resource", "default", spec, patch_mock, MagicMock()
        )

        assert repaired is False
        assert patch_mock.spec == {}
        mock_get_custom_object.assert_not_called()

    def test_leaves_hand_authored_names_alone(self, mock_get_custom_object, patch_mock):
        # Only Resources the operator generated from a Service carry the `-resource`
        # suffix; anything else is user-authored and they must set gatewayRef.
        repaired = _repair_missing_gateway_ref(
            "my-cluster",
            "default",
            {"type": ResourceType.KUBERNETES},
            patch_mock,
            MagicMock(),
        )

        assert repaired is False
        assert patch_mock.spec == {}
        mock_get_custom_object.assert_not_called()


SERVICE_OWNER_REF = {
    "apiVersion": "v1",
    "kind": "Service",
    "name": "gw",
    "uid": "3dee908b-1d75-4a34-a20a-36c08da0c39c",
    "controller": True,
}
KUBERNETES_SPEC = {"type": ResourceType.KUBERNETES, "gatewayRef": {"name": "gw"}}


class TestReleaseServiceOwnership:
    @pytest.fixture
    def patch_mock(self):
        mock = MagicMock()
        mock.meta = {}
        return mock

    def test_drops_the_service_owner_reference(self, patch_mock):
        _release_service_ownership(
            {"name": "gw-resource", "ownerReferences": [SERVICE_OWNER_REF]},
            KUBERNETES_SPEC,
            patch_mock,
            MagicMock(),
        )

        assert patch_mock.meta == {"ownerReferences": []}

    @pytest.mark.parametrize(
        "resource_type", [ResourceType.NETWORK, ResourceType.WEB_APP]
    )
    def test_keeps_ownership_of_resources_the_operator_still_generates(
        self, resource_type, patch_mock
    ):
        # An annotation-generated Resource has no other cleanup path: nothing watches
        # Service deletions, so garbage collection is what deprovisions it.
        _release_service_ownership(
            {"name": "gw-resource", "ownerReferences": [SERVICE_OWNER_REF]},
            {"type": resource_type},
            patch_mock,
            MagicMock(),
        )

        assert patch_mock.meta == {}

    def test_keeps_owner_references_from_other_kinds(self, patch_mock):
        other_ref = {"kind": "TwingateGateway", "name": "gw", "uid": "other-uid"}

        _release_service_ownership(
            {
                "name": "gw-resource",
                "ownerReferences": [SERVICE_OWNER_REF, other_ref],
            },
            KUBERNETES_SPEC,
            patch_mock,
            MagicMock(),
        )

        assert patch_mock.meta == {"ownerReferences": [other_ref]}

    @pytest.mark.parametrize("owner_references", [[], None])
    def test_is_a_no_op_once_already_released(self, owner_references, patch_mock):
        _release_service_ownership(
            {"name": "gw-resource", "ownerReferences": owner_references},
            KUBERNETES_SPEC,
            patch_mock,
            MagicMock(),
        )

        assert patch_mock.meta == {}


class TestResourceCreateHandler:
    def test_create_network_resource(
        self,
        network_resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        resource = network_resource_factory()
        resource_spec = resource.to_spec(id=None)
        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_create.return_value = resource

        result = twingate_resource_create(
            body="",
            namespace="default",
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
            resource_type=ResourceType.NETWORK,
            **resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"},
                owner_namespace="default",
                exclude={"id"},
            ),
        )
        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Created on Twingate as {resource.id}"
        )
        assert patch_mock.spec == {"id": resource.id}

    def test_create_kubernetes_resource(
        self,
        kubernetes_resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo,
    ):
        resource = kubernetes_resource_factory()
        resource_spec = resource.to_spec(id=None, gateway_ref={"name": "my-gateway"})
        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_create.return_value = resource

        with patch("app.crds.resolve_ref_to_twingate_id", return_value="gw-1"):
            result = twingate_resource_create(
                body="",
                namespace="default",
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
                "ts": ANY,
            }

            mock_api_client.resource_create.assert_called_once_with(
                resource_type=ResourceType.KUBERNETES,
                **resource_spec.to_graphql_arguments(
                    labels={"env": "dev"}, owner_namespace="default", exclude={"id"}
                ),
            )
        mock_api_client.resource_update.assert_not_called()
        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Created on Twingate as {resource.id}"
        )
        assert patch_mock.spec == {"id": resource.id}

    def test_when_id_is_specified_update_instead_of_create(
        self,
        network_resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo,
    ):
        resource = network_resource_factory(id="pre-existing-id")
        resource_spec = resource.to_spec()

        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_update.return_value = resource

        result = twingate_resource_create(
            body="",
            namespace="default",
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
            resource_type=ResourceType.NETWORK,
            **resource_spec.to_graphql_arguments(
                labels={"env": "dev"}, owner_namespace="default"
            ),
        )
        mock_api_client.resource_create.assert_not_called()

        kopf_info_mock.assert_called_once_with(
            "", reason="Success", message=f"Imported {resource.id}"
        )

    def test_update_resource_when_id_is_specified(
        self,
        kubernetes_resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo,
    ):
        resource = kubernetes_resource_factory(id="existing-id")
        resource_spec = resource.to_spec(gateway_ref={"name": "my-gateway"})
        spec = resource_spec.model_dump(by_alias=True)

        logger_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}

        mock_api_client.resource_update.return_value = resource

        with patch("app.crds.resolve_ref_to_twingate_id", return_value="gw-1"):
            result = twingate_resource_create(
                body="",
                namespace="default",
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
                resource_type=ResourceType.KUBERNETES,
                **resource_spec.to_graphql_arguments(
                    labels={"env": "dev"}, owner_namespace="default"
                ),
            )
        mock_api_client.resource_create.assert_not_called()


class TestResourceUpdateHandler:
    def test_update_network_resource(
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
            "type": ResourceType.NETWORK,
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
            "my-resource",
            "default",
            mock_k8s_metadata,
            mock_k8s_metadata["labels"],
            spec,
            diff,
            status,
            mock_memo_with_default_resource_tags,
            logger_mock,
            patch_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": rid,
            "created_at": ANY,
            "updated_at": ANY,
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_called_once_with(
            resource_type=ResourceType.NETWORK,
            **new_resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"}, owner_namespace="default"
            ),
        )
        assert patch_mock.spec == {}

    def test_update_kubernetes_resource(
        self, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        rid = "UmVzb3VyY2U6OTMxODE3"
        spec = new = {
            "id": rid,
            "address": "my.default.cluster.local",
            "name": "new-name",
            "type": ResourceType.KUBERNETES,
            "gatewayRef": {"name": "my-gateway"},
        }
        diff = (("change", ("spec", "name"), "My K8S Resource", "new-name"),)
        new_resource_spec = ResourceSpec(**new)
        mock_api_client.resource_update.return_value = MagicMock(id=rid)

        logger_mock = MagicMock()
        status_mock = MagicMock()
        patch_mock = MagicMock()
        patch_mock.spec = {}
        with patch("app.crds.resolve_ref_to_twingate_id", return_value="gw-1"):
            result = twingate_resource_update(
                name="my-resource",
                namespace="default",
                meta=mock_k8s_metadata,
                labels=mock_k8s_metadata["labels"],
                spec=spec,
                diff=diff,
                status=status_mock,
                memo=mock_memo,
                logger=logger_mock,
                patch=patch_mock,
            )

            assert result == {
                "success": True,
                "twingate_id": rid,
                "created_at": ANY,
                "updated_at": ANY,
                "ts": ANY,
            }
            mock_api_client.resource_update.assert_called_once_with(
                resource_type=ResourceType.KUBERNETES,
                **new_resource_spec.to_graphql_arguments(
                    labels={"env": "dev"}, owner_namespace="default"
                ),
            )

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
            "my-resource",
            "default",
            mock_k8s_metadata,
            mock_k8s_metadata["labels"],
            spec,
            diff,
            status,
            memo_mock,
            logger_mock,
            patch_mock,
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
            "my-resource",
            "default",
            mock_k8s_metadata,
            mock_k8s_metadata["labels"],
            spec,
            diff,
            status,
            memo_mock,
            logger_mock,
            patch_mock,
        )
        assert result == {
            "success": True,
            "twingate_id": rid,
            "message": "No update required",
            "ts": ANY,
        }

        mock_api_client.resource_update.assert_not_called()
        assert patch_mock.spec == {}

    def test_annotation_update_does_nothing(self, mock_api_client, mock_k8s_metadata):
        rid = "UmVzb3VyY2U6OTMxODE3"
        spec = {
            "id": rid,
            "address": "my.default.cluster.local",
            "name": "new-name",
        }
        diff = (("add", ("metadata", "annotations", "foo"), None, "bar"),)
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
            "my-resource",
            "default",
            mock_k8s_metadata,
            mock_k8s_metadata["labels"],
            spec,
            diff,
            status,
            memo_mock,
            logger_mock,
            patch_mock,
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
    def test_sync_repairs_a_resource_left_without_a_gateway_ref(
        self, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        # The timer is what reaches a pre-existing Resource, since no `on.resume`
        # handler is registered for twingateresource.
        patch_mock = MagicMock()
        patch_mock.spec = {}

        with (
            patch(
                "app.handlers.handlers_resource.k8s_get_twingate_custom_object",
                return_value={"spec": {"serviceRef": {"name": "gw"}}},
            ),
            pytest.raises(kopf.TemporaryError),
        ):
            twingate_resource_sync(
                "gw-resource",
                "default",
                mock_k8s_metadata,
                mock_k8s_metadata["labels"],
                {
                    "id": "UmVzb3VyY2U6OTMxODE3",
                    "address": "kubernetes.default.svc.cluster.local",
                    "name": "my-cluster",
                    "type": ResourceType.KUBERNETES,
                },
                {},
                mock_memo,
                MagicMock(),
                patch_mock,
            )

        assert patch_mock.spec == {"gatewayRef": {"name": "gw", "namespace": "default"}}
        mock_api_client.resource_update.assert_not_called()

    def test_sync_with_invalid_spec_fails_permanently(
        self, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        with pytest.raises(
            kopf.PermanentError, match="Only Network resources can set `protocols`"
        ):
            twingate_resource_sync(
                "my-resource",
                "default",
                mock_k8s_metadata,
                mock_k8s_metadata["labels"],
                {
                    "id": "UmVzb3VyY2U6OTMxODE3",
                    "address": "kubernetes.default.svc.cluster.local",
                    "name": "my-cluster",
                    "type": ResourceType.KUBERNETES,
                    "gatewayRef": {"name": "gw"},
                    "protocols": {"allowIcmp": True},
                },
                {},
                mock_memo,
                MagicMock(),
                MagicMock(),
            )

        mock_api_client.get_resource.assert_not_called()

    def test_sync_when_resource_exists_and_doesnt_need_update(
        self, network_resource_factory, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        resource = network_resource_factory()
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
            "my-resource",
            "default",
            mock_k8s_metadata,
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
        self, network_resource_factory, mock_api_client, mock_k8s_metadata, mock_memo
    ):
        resource = network_resource_factory()
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
            "my-resource",
            "default",
            mock_k8s_metadata,
            mock_k8s_metadata["labels"],
            resource_spec.model_dump(by_alias=True),
            status,
            mock_memo,
            logger_mock,
            patch_mock,
        )

        mock_api_client.resource_update.assert_called_once_with(
            resource_type=ResourceType.NETWORK,
            **resource_spec.to_graphql_arguments(
                labels=resource.to_metadata_labels(), owner_namespace="default"
            ),
        )
        assert patch_mock.spec == {}

    def test_sync_when_resource_exists_and_label_requires_update(
        self,
        network_resource_factory,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        resource = network_resource_factory()
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
            "my-resource",
            "default",
            mock_k8s_metadata,
            mock_k8s_metadata["labels"],
            resource_spec.model_dump(by_alias=True),
            status,
            mock_memo_with_default_resource_tags,
            logger_mock,
            patch_mock,
        )

        mock_api_client.resource_update.assert_called_once_with(
            resource_type=ResourceType.NETWORK,
            **resource_spec.to_graphql_arguments(
                labels={"managed_by": "test", "env": "dev"}
                | resource.to_metadata_labels(),
                owner_namespace="default",
            ),
        )
        assert patch_mock.spec == {}

    def test_sync_when_resource_doesnt_exists_recreate_it(
        self,
        kubernetes_resource_factory,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo_with_default_resource_tags,
    ):
        resource = kubernetes_resource_factory()
        resource_spec = resource.to_spec(gateway_ref={"name": "my-gateway"})
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

        with patch("app.crds.resolve_ref_to_twingate_id", return_value="gw-1"):
            twingate_resource_sync(
                "my-resource",
                "default",
                mock_k8s_metadata,
                mock_k8s_metadata["labels"],
                resource_spec.model_dump(by_alias=True),
                status,
                mock_memo_with_default_resource_tags,
                logger_mock,
                patch_mock,
            )

            mock_api_client.resource_update.assert_not_called()
            mock_api_client.resource_create.assert_called_once_with(
                resource_type=ResourceType.KUBERNETES,
                **resource_spec.to_graphql_arguments(
                    labels={"managed_by": "test", "env": "dev"},
                    owner_namespace="default",
                    exclude={"id"},
                ),
            )

        assert patch_mock.spec == {"id": resource.id}


class TestTwingateResourceGatewayIndex:
    def test_maps_gateway_to_resource(self):
        # gatewayRef omits namespace, so it resolves to the resource's own namespace.
        result = twingate_resource_gateway_index(
            namespace="ns1",
            name="my-resource-crd",
            spec={"gatewayRef": {"name": "my-gw"}},
        )

        assert result == {
            ("ns1", "my-gw"): {
                "namespace": "ns1",
                "name": "my-resource-crd",
            },
        }

    def test_uses_gateway_namespace_when_set(self):
        result = twingate_resource_gateway_index(
            namespace="ns1",
            name="my-resource-crd",
            spec={"gatewayRef": {"name": "my-gw", "namespace": "ns2"}},
        )

        assert result == {
            ("ns2", "my-gw"): {"namespace": "ns1", "name": "my-resource-crd"}
        }

    def test_none_without_gateway_ref(self):
        result = twingate_resource_gateway_index(
            namespace="default", name="my-resource-crd", spec={}
        )

        assert result is None


LB_HOST = "internal-my-app-1234.us-east-1.elb.amazonaws.com"
NEW_LB_HOST = "internal-my-app-5678.us-east-1.elb.amazonaws.com"
ADDRESS_FROM_SPEC = {
    "id": "UmVzb3VyY2U6OTMxODE3",
    "name": "my-app",
    "alias": "my-app.internal.example.com",
    "addressFrom": {"ingressRef": {"name": "my-app"}},
}


@pytest.fixture
def mock_resolve_lb_host():
    with patch(
        "app.crds.resolve_load_balancer_host", return_value=LB_HOST
    ) as resolve_mock:
        yield resolve_mock


def _patch_mock():
    patch_mock = MagicMock()
    patch_mock.spec = {}
    patch_mock.status = {}
    return patch_mock


class TestResourceAddressFrom:
    def test_create_resolves_address_from_ingress(
        self,
        network_resource_factory,
        kopf_info_mock,
        mock_api_client,
        mock_memo,
        mock_resolve_lb_host,
    ):
        resource = network_resource_factory()
        mock_api_client.resource_create.return_value = resource
        spec = {k: v for k, v in ADDRESS_FROM_SPEC.items() if k != "id"}
        patch_mock = _patch_mock()

        twingate_resource_create(
            body="",
            namespace="my-app",
            labels={},
            spec=spec,
            memo=mock_memo,
            logger=MagicMock(),
            patch=patch_mock,
        )

        mock_resolve_lb_host.assert_called_once_with("Ingress", "my-app", "my-app")
        call_kwargs = mock_api_client.resource_create.call_args.kwargs
        assert call_kwargs["address"] == LB_HOST
        assert call_kwargs["alias"] == "my-app.internal.example.com"
        assert "address_from" not in call_kwargs
        assert patch_mock.spec == {"id": resource.id}
        assert patch_mock.status == {"address": LB_HOST}

    def test_create_waits_for_the_load_balancer(
        self, mock_api_client, mock_memo, mock_resolve_lb_host
    ):
        mock_resolve_lb_host.side_effect = kopf.TemporaryError("not ready", delay=30)
        spec = {k: v for k, v in ADDRESS_FROM_SPEC.items() if k != "id"}

        with pytest.raises(kopf.TemporaryError):
            twingate_resource_create(
                body="",
                namespace="my-app",
                labels={},
                spec=spec,
                memo=mock_memo,
                logger=MagicMock(),
                patch=_patch_mock(),
            )

        mock_api_client.resource_create.assert_not_called()
        mock_api_client.resource_update.assert_not_called()

    def test_update_switching_to_address_from(
        self, mock_api_client, mock_k8s_metadata, mock_memo, mock_resolve_lb_host
    ):
        mock_api_client.resource_update.return_value = MagicMock(
            id=ADDRESS_FROM_SPEC["id"]
        )
        diff = (
            ("remove", ("spec", "address"), "my-app.internal", None),
            ("add", ("spec", "addressFrom"), None, ADDRESS_FROM_SPEC["addressFrom"]),
        )
        patch_mock = _patch_mock()

        twingate_resource_update(
            name="my-app",
            namespace="my-app",
            meta=mock_k8s_metadata,
            labels={},
            spec=ADDRESS_FROM_SPEC,
            diff=diff,
            status={},
            memo=mock_memo,
            logger=MagicMock(),
            patch=patch_mock,
        )

        mock_api_client.resource_update.assert_called_once()
        call_kwargs = mock_api_client.resource_update.call_args.kwargs
        assert call_kwargs["id"] == ADDRESS_FROM_SPEC["id"]
        assert call_kwargs["address"] == LB_HOST
        assert patch_mock.status == {"address": LB_HOST}

    def test_update_without_relevant_changes_does_not_resolve(
        self, mock_api_client, mock_k8s_metadata, mock_memo, mock_resolve_lb_host
    ):
        diff = (("change", ("metadata", "annotations", "foo"), "a", "b"),)

        twingate_resource_update(
            name="my-app",
            namespace="my-app",
            meta=mock_k8s_metadata,
            labels={},
            spec=ADDRESS_FROM_SPEC,
            diff=diff,
            status={},
            memo=mock_memo,
            logger=MagicMock(),
            patch=_patch_mock(),
        )

        mock_resolve_lb_host.assert_not_called()
        mock_api_client.resource_update.assert_not_called()

    def test_sync_pushes_a_recreated_load_balancer(
        self,
        network_resource_factory,
        mock_api_client,
        mock_k8s_metadata,
        mock_memo,
        mock_resolve_lb_host,
    ):
        # Twingate still has the old load balancer's hostname.
        resource = network_resource_factory(
            id=ADDRESS_FROM_SPEC["id"],
            name="my-app",
            alias="my-app.internal.example.com",
            address={"type": "DNS", "value": LB_HOST},
        )
        mock_api_client.get_resource.return_value = resource
        mock_resolve_lb_host.return_value = NEW_LB_HOST
        patch_mock = _patch_mock()

        twingate_resource_sync(
            "my-app",
            "my-app",
            mock_k8s_metadata,
            resource.to_metadata_labels(),
            ADDRESS_FROM_SPEC
            | {"remoteNetworkId": resource.remote_network.id, "isVisible": True},
            {},
            mock_memo,
            MagicMock(),
            patch_mock,
        )

        mock_api_client.resource_update.assert_called_once()
        assert mock_api_client.resource_update.call_args.kwargs["address"] == (
            NEW_LB_HOST
        )
        assert patch_mock.status == {"address": NEW_LB_HOST}


class TestTwingateResourceAddressFromIndex:
    @pytest.mark.parametrize(
        ("address_from", "key"),
        [
            ({"ingressRef": {"name": "web"}}, ("Ingress", "default", "web")),
            (
                {"serviceRef": {"name": "lb", "namespace": "infra"}},
                ("Service", "infra", "lb"),
            ),
        ],
    )
    def test_maps_source_to_resource(self, address_from, key):
        result = twingate_resource_address_from_index(
            namespace="default", name="my-app", spec={"addressFrom": address_from}
        )

        assert result == {key: {"namespace": "default", "name": "my-app"}}

    def test_none_without_address_from(self):
        assert (
            twingate_resource_address_from_index(
                namespace="default", name="my-app", spec={"address": "a.internal"}
            )
            is None
        )


class TestLoadBalancerChangedHandlers:
    @pytest.fixture
    def mock_get_custom_object(self):
        with patch(
            "app.handlers.handlers_resource.k8s_get_twingate_custom_object"
        ) as mock:
            mock.return_value = {
                "metadata": {"name": "my-app", "labels": {"team": "web"}},
                "spec": ADDRESS_FROM_SPEC,
                "status": {"address": LB_HOST},
            }
            yield mock

    @pytest.fixture
    def mock_patch_custom_object(self):
        with patch(
            "app.handlers.handlers_resource.k8s_patch_twingate_custom_object"
        ) as mock:
            yield mock

    @pytest.fixture
    def index(self):
        return {
            ("Ingress", "my-app", "my-app"): [{"namespace": "my-app", "name": "my-app"}]
        }

    def _run(self, index, event_type="MODIFIED", handler=None, name="my-app"):
        handler = handler or twingate_resource_ingress_load_balancer_changed
        handler(
            event={"type": event_type},
            namespace="my-app",
            name=name,
            memo=MagicMock(
                twingate_settings=TwingateOperatorSettings(
                    network="slug",
                    host="test.com",
                    api_key="test_key",
                    remote_network_id="UmVtb3RlTmV0d29yazoxMjMK",
                )
            ),
            logger=MagicMock(),
            twingate_resource_address_from_index=index,
        )

    def test_updates_resource_when_load_balancer_changes(
        self,
        index,
        mock_api_client,
        mock_get_custom_object,
        mock_patch_custom_object,
        mock_resolve_lb_host,
    ):
        mock_resolve_lb_host.return_value = NEW_LB_HOST

        self._run(index)

        mock_get_custom_object.assert_called_once_with(
            "twingateresources", "my-app", "my-app"
        )
        mock_api_client.resource_update.assert_called_once()
        kwargs = mock_api_client.resource_update.call_args.kwargs
        assert kwargs["id"] == ADDRESS_FROM_SPEC["id"]
        assert kwargs["address"] == NEW_LB_HOST
        assert kwargs["tags"] == [{"key": "team", "value": "web"}]
        mock_patch_custom_object.assert_called_once()
        args = mock_patch_custom_object.call_args.args
        assert args[:3] == ("twingateresources", "my-app", "my-app")
        assert args[3].status == {"address": NEW_LB_HOST}
        assert args[3].spec == {}

    def test_service_handler_uses_service_key(
        self,
        mock_api_client,
        mock_get_custom_object,
        mock_patch_custom_object,
        mock_resolve_lb_host,
    ):
        mock_get_custom_object.return_value["spec"] = ADDRESS_FROM_SPEC | {
            "addressFrom": {"serviceRef": {"name": "my-lb"}}
        }
        mock_resolve_lb_host.return_value = NEW_LB_HOST
        index = {
            ("Service", "my-app", "my-lb"): [{"namespace": "my-app", "name": "my-app"}]
        }

        self._run(
            index,
            handler=twingate_resource_service_load_balancer_changed,
            name="my-lb",
        )

        mock_resolve_lb_host.assert_called_once_with("Service", "my-app", "my-lb")
        mock_api_client.resource_update.assert_called_once()

    def test_no_update_when_address_is_unchanged(
        self,
        index,
        mock_api_client,
        mock_get_custom_object,
        mock_patch_custom_object,
        mock_resolve_lb_host,
    ):
        self._run(index)

        mock_api_client.resource_update.assert_not_called()
        mock_patch_custom_object.assert_not_called()

    def test_ignores_unreferenced_objects(
        self, mock_api_client, mock_get_custom_object, mock_resolve_lb_host
    ):
        self._run({}, name="unrelated")

        mock_get_custom_object.assert_not_called()
        mock_api_client.resource_update.assert_not_called()

    def test_ignores_deleted_events(
        self, index, mock_api_client, mock_get_custom_object
    ):
        self._run(index, event_type="DELETED")

        mock_get_custom_object.assert_not_called()

    def test_skips_resources_not_created_yet(
        self,
        index,
        mock_api_client,
        mock_get_custom_object,
        mock_patch_custom_object,
        mock_resolve_lb_host,
    ):
        spec = {k: v for k, v in ADDRESS_FROM_SPEC.items() if k != "id"}
        mock_get_custom_object.return_value["spec"] = spec

        self._run(index)

        mock_resolve_lb_host.assert_not_called()
        mock_api_client.resource_update.assert_not_called()

    def test_skips_until_the_load_balancer_is_ready(
        self,
        index,
        mock_api_client,
        mock_get_custom_object,
        mock_patch_custom_object,
        mock_resolve_lb_host,
    ):
        mock_resolve_lb_host.side_effect = kopf.TemporaryError("not ready")

        self._run(index)

        mock_api_client.resource_update.assert_not_called()
        mock_patch_custom_object.assert_not_called()

    def test_failed_update_does_not_record_the_new_address(
        self,
        mock_api_client,
        mock_get_custom_object,
        mock_patch_custom_object,
        mock_resolve_lb_host,
    ):
        # Two Resources share the Ingress: the first update fails, the second
        # still goes through, and only the second records the new address.
        index = {
            ("Ingress", "my-app", "my-app"): [
                {"namespace": "my-app", "name": "first"},
                {"namespace": "my-app", "name": "second"},
            ]
        }
        mock_resolve_lb_host.return_value = NEW_LB_HOST
        mock_api_client.resource_update.side_effect = [Exception("boom"), None]

        self._run(index)

        assert mock_api_client.resource_update.call_count == 2
        mock_patch_custom_object.assert_called_once()
        assert mock_patch_custom_object.call_args.args[2] == "second"
