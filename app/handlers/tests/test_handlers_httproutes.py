import copy
from unittest.mock import MagicMock, patch

import kopf
import kubernetes
import pytest
from kopf._core.intents.causes import Reason

from app.handlers.handlers_httproutes import (
    hostname_matches,
    httproute_to_twingate_resource,
    httproutes_by_gateway,
    twingate_httproute_annotation_removed,
    twingate_httproute_create,
    twingate_httproute_gateway_event,
)

GATEWAY_API_GROUP = "gateway.networking.k8s.io"


def make_route(
    *,
    hostnames: list[str] | None = None,
    parent_refs: list[dict] | None = None,
    annotations: dict[str, str] | None = None,
) -> kopf.Body:
    spec: dict = {
        "parentRefs": (
            parent_refs
            if parent_refs is not None
            else [
                {
                    "group": GATEWAY_API_GROUP,
                    "kind": "Gateway",
                    "name": "internal-gw",
                    "sectionName": "https",
                }
            ]
        ),
        "rules": [{"backendRefs": [{"name": "app", "port": 8080}]}],
    }
    spec["hostnames"] = ["app.example.com"] if hostnames is None else hostnames
    return kopf.Body(
        {
            "apiVersion": f"{GATEWAY_API_GROUP}/v1",
            "kind": "HTTPRoute",
            "metadata": {
                "name": "my-route",
                "namespace": "default",
                "labels": {"env": "dev"},
                "annotations": {"resource.twingate.com": "true", **(annotations or {})},
            },
            "spec": spec,
        }
    )


def make_gateway(
    name: str = "internal-gw",
    namespace: str = "default",
    addresses: list[dict] | None = None,
) -> dict:
    return {
        "apiVersion": f"{GATEWAY_API_GROUP}/v1",
        "kind": "Gateway",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "gatewayClassName": "internal",
            "listeners": [
                {
                    "name": "http",
                    "protocol": "HTTP",
                    "port": 80,
                    "hostname": "*.example.com",
                },
                {
                    "name": "https",
                    "protocol": "HTTPS",
                    "port": 443,
                    "hostname": "*.example.com",
                },
                {
                    "name": "other",
                    "protocol": "HTTPS",
                    "port": 8443,
                    "hostname": "other.test",
                },
                {"name": "any-host", "protocol": "HTTP", "port": 8080},
                {"name": "postgres", "protocol": "TCP", "port": 5432},
            ],
        },
        "status": {
            "addresses": (
                [{"type": "IPAddress", "value": "10.96.12.34"}]
                if addresses is None
                else addresses
            )
        },
    }


@pytest.fixture
def gateways() -> dict:
    return {("default", "internal-gw"): make_gateway()}


@pytest.fixture
def twingate_resources() -> dict:
    return {}


@pytest.fixture
def k8s_customobjects_client_mock(gateways, twingate_resources):
    def get_namespaced_custom_object(group, version, namespace, plural, name):
        store = gateways if plural == "gateways" else twingate_resources
        if (namespace, name) not in store:
            raise kubernetes.client.exceptions.ApiException(status=404)
        # A fresh copy per read, as from the API server.
        return copy.deepcopy(store[(namespace, name)])

    client_mock = MagicMock()
    client_mock.get_namespaced_custom_object.side_effect = get_namespaced_custom_object
    with patch("kubernetes.client.CustomObjectsApi", return_value=client_mock):
        yield client_mock


def expected_resource(ports: list[int], **spec) -> dict:
    return {
        "apiVersion": "twingate.com/v1beta",
        "kind": "TwingateResource",
        "metadata": {"name": "my-route-httproute-resource", "labels": {"env": "dev"}},
        "spec": {
            "name": "my-route-httproute-resource",
            "address": "10.96.12.34",
            "alias": "app.example.com",
            "protocols": {
                "allowIcmp": False,
                "tcp": {
                    "policy": "RESTRICTED",
                    "ports": [{"start": port, "end": port} for port in ports],
                },
                "udp": {"policy": "RESTRICTED", "ports": []},
            },
            **spec,
        },
    }


@pytest.mark.parametrize(
    ("pattern", "hostname", "expected"),
    [
        ("app.example.com", "app.example.com", True),
        ("app.example.com", "other.example.com", False),
        ("*.example.com", "app.example.com", True),
        ("*.example.com", "a.b.example.com", True),
        ("*.example.com", "example.com", False),
        ("*.example.com", "app.example.org", False),
    ],
)
def test_hostname_matches(pattern, hostname, expected):
    assert hostname_matches(pattern, hostname) is expected


@pytest.mark.usefixtures("k8s_customobjects_client_mock")
class TestHttpRouteToTwingateResource:
    def test_maps_route_to_network_resource_through_parent_gateway(self):
        result = httproute_to_twingate_resource(make_route(), "default")

        assert result == expected_resource([443])

    @pytest.mark.parametrize(
        ("annotation", "value", "spec"),
        [
            ("name", "My Route", {"name": "My Route"}),
            ("securityPolicyId", "12345", {"securityPolicyId": "12345"}),
            ("isVisible", "false", {"isVisible": False}),
            ("isBrowserShortcutEnabled", "false", {"isBrowserShortcutEnabled": False}),
            ("syncLabels", "false", {"syncLabels": False}),
            ("type", "Network", {"type": "Network"}),
        ],
    )
    def test_extra_annotations(self, annotation, value, spec):
        route = make_route(annotations={f"resource.twingate.com/{annotation}": value})

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443], **spec)

    def test_alias_annotation_is_rejected(self):
        route = make_route(annotations={"resource.twingate.com/alias": "x.internal"})

        with pytest.raises(kopf.PermanentError, match="alias annotation"):
            httproute_to_twingate_resource(route, "default")

    @pytest.mark.parametrize("resource_type", ["WebApp", "Kubernetes", "Bogus"])
    def test_unsupported_resource_type(self, resource_type):
        route = make_route(annotations={"resource.twingate.com/type": resource_type})

        with pytest.raises(kopf.PermanentError, match="Unsupported resource type"):
            httproute_to_twingate_resource(route, "default")

    def test_parent_ref_without_section_name_uses_every_listener_for_hostname(self):
        route = make_route(parent_refs=[{"name": "internal-gw"}])

        result = httproute_to_twingate_resource(route, "default")

        # Not 8443 (hostname other.test) or 5432 (TCP).
        assert result == expected_resource([80, 443, 8080])

    def test_parent_ref_port_selects_listener(self):
        route = make_route(parent_refs=[{"name": "internal-gw", "port": 80}])

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([80])

    def test_parent_refs_to_the_same_gateway_are_combined(self):
        route = make_route(
            parent_refs=[
                {"name": "internal-gw", "sectionName": "http"},
                {"name": "internal-gw", "sectionName": "https"},
            ]
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([80, 443])

    def test_no_listener_for_hostname(self):
        route = make_route(
            parent_refs=[{"name": "internal-gw", "sectionName": "other"}]
        )

        with pytest.raises(kopf.PermanentError, match="no HTTP or HTTPS listener"):
            httproute_to_twingate_resource(route, "default")

    def test_hostname_annotation_selects_one_of_several_hostnames(self):
        route = make_route(
            hostnames=["api.example.com", "app.example.com"],
            annotations={"resource.twingate.com/hostname": "app.example.com"},
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443])

    def test_hostname_annotation_may_match_a_wildcard_hostname(self):
        route = make_route(
            hostnames=["*.example.com"],
            annotations={"resource.twingate.com/hostname": "app.example.com"},
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443])

    def test_hostname_annotation_on_route_without_hostnames(self):
        route = make_route(
            hostnames=[],
            annotations={"resource.twingate.com/hostname": "app.example.com"},
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443])

    def test_hostname_annotation_not_matching_route_hostnames(self):
        route = make_route(
            annotations={"resource.twingate.com/hostname": "api.example.com"}
        )

        with pytest.raises(kopf.PermanentError, match="must match one of"):
            httproute_to_twingate_resource(route, "default")

    def test_hostname_annotation_with_wildcard(self):
        route = make_route(
            hostnames=["*.example.com"],
            annotations={"resource.twingate.com/hostname": "*.example.com"},
        )

        with pytest.raises(kopf.PermanentError, match="must not contain a wildcard"):
            httproute_to_twingate_resource(route, "default")

    @pytest.mark.parametrize(
        "hostnames",
        [[], ["api.example.com", "app.example.com"], ["*.example.com"]],
    )
    def test_hostname_annotation_required(self, hostnames):
        route = make_route(hostnames=hostnames)

        with pytest.raises(
            kopf.PermanentError, match="hostname annotation is required"
        ):
            httproute_to_twingate_resource(route, "default")

    def test_parent_gateway_in_another_namespace(self, gateways):
        gateways["infra", "shared-gw"] = make_gateway("shared-gw", "infra")
        route = make_route(
            parent_refs=[
                {"name": "shared-gw", "namespace": "infra", "sectionName": "https"}
            ]
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443])

    def test_non_gateway_parent_refs_are_ignored(self):
        route = make_route(
            parent_refs=[
                {"group": "", "kind": "Service", "name": "mesh-svc"},
                {"name": "internal-gw", "sectionName": "https"},
            ]
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443])

    def test_without_parent_gateway(self):
        route = make_route(
            parent_refs=[{"group": "", "kind": "Service", "name": "mesh-svc"}]
        )

        with pytest.raises(
            kopf.PermanentError, match="parentGateway annotation is required"
        ):
            httproute_to_twingate_resource(route, "default")

    def test_parent_gateway_annotation_required_with_several_gateways(self):
        route = make_route(parent_refs=[{"name": "internal-gw"}, {"name": "public-gw"}])

        with pytest.raises(
            kopf.PermanentError, match="parentGateway annotation is required"
        ):
            httproute_to_twingate_resource(route, "default")

    @pytest.mark.parametrize("selected", ["internal-gw", "default/internal-gw"])
    def test_parent_gateway_annotation_selects_gateway(self, selected):
        route = make_route(
            parent_refs=[
                {"name": "public-gw", "sectionName": "https"},
                {"name": "internal-gw", "sectionName": "https"},
            ],
            annotations={"resource.twingate.com/parentGateway": selected},
        )

        result = httproute_to_twingate_resource(route, "default")

        assert result == expected_resource([443])

    def test_parent_gateway_annotation_not_in_parent_refs(self):
        route = make_route(
            annotations={"resource.twingate.com/parentGateway": "infra/internal-gw"}
        )

        with pytest.raises(kopf.PermanentError, match="must name a Gateway"):
            httproute_to_twingate_resource(route, "default")

    def test_missing_gateway_is_retried(self, gateways):
        gateways.clear()

        with pytest.raises(kopf.TemporaryError, match="not found"):
            httproute_to_twingate_resource(make_route(), "default")

    def test_gateway_lookup_reraises_non_404_exceptions(
        self, k8s_customobjects_client_mock
    ):
        k8s_customobjects_client_mock.get_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )

        with pytest.raises(kubernetes.client.exceptions.ApiException):
            httproute_to_twingate_resource(make_route(), "default")

    @pytest.mark.parametrize(
        "addresses",
        [
            [],
            [{"type": "IPAddress", "value": "fd00::1"}],
            [{"type": "NamedAddress", "value": "internal-pool"}],
        ],
    )
    def test_gateway_without_usable_address_is_retried(self, gateways, addresses):
        gateways["default", "internal-gw"] = make_gateway(addresses=addresses)

        with pytest.raises(kopf.TemporaryError, match="no IPv4 or hostname address"):
            httproute_to_twingate_resource(make_route(), "default")

    def test_gateway_address_skips_unusable_addresses(self, gateways):
        gateways["default", "internal-gw"] = make_gateway(
            addresses=[
                {"type": "NamedAddress", "value": "internal-pool"},
                {"type": "IPAddress", "value": "fd00::1"},
                {"type": "Hostname", "value": "gw.internal.example.com"},
            ]
        )

        result = httproute_to_twingate_resource(make_route(), "default")

        assert result["spec"]["address"] == "gw.internal.example.com"

    def test_gateway_address_type_defaults_to_ip_address(self, gateways):
        gateways["default", "internal-gw"] = make_gateway(
            addresses=[{"value": "10.96.12.35"}]
        )

        result = httproute_to_twingate_resource(make_route(), "default")

        assert result["spec"]["address"] == "10.96.12.35"


class TestTwingateHttpRouteCreate:
    def test_creates_twingate_resource(
        self, k8s_customobjects_client_mock, kopf_adopt_mock, kopf_info_mock
    ):
        route = make_route()

        twingate_httproute_create(
            body=route, namespace="default", logger=MagicMock(), reason=Reason.CREATE
        )

        kopf_adopt_mock.assert_called_once_with(expected_resource([443]), owner=route)
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            expected_resource([443]),
        )
        k8s_customobjects_client_mock.replace_namespaced_custom_object.assert_not_called()

    def test_updates_existing_twingate_resource(
        self,
        k8s_customobjects_client_mock,
        twingate_resources,
        kopf_adopt_mock,
        kopf_info_mock,
    ):
        twingate_resources["default", "my-route-httproute-resource"] = {
            "metadata": {"name": "my-route-httproute-resource", "labels": {}},
            "spec": {
                "id": "1",
                "name": "my-route-httproute-resource",
                "address": "10.96.0.1",
                "alias": "app.example.com",
            },
        }

        twingate_httproute_create(
            body=make_route(),
            namespace="default",
            logger=MagicMock(),
            reason=Reason.UPDATE,
        )

        expected = expected_resource([443])
        k8s_customobjects_client_mock.replace_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-route-httproute-resource",
            {
                "metadata": expected["metadata"],
                "spec": {"id": "1", **expected["spec"]},
            },
        )
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_not_called()


class TestTwingateHttpRouteAnnotationRemoved:
    def test_deletes_twingate_resource_when_it_exists(
        self, k8s_customobjects_client_mock, twingate_resources, kopf_info_mock
    ):
        twingate_resources["default", "my-route-httproute-resource"] = {
            "metadata": {"name": "my-route-httproute-resource"},
            "spec": {"id": "1", "name": "my-route-httproute-resource"},
        }

        twingate_httproute_annotation_removed(
            body=make_route(), namespace="default", logger=MagicMock()
        )

        k8s_customobjects_client_mock.delete_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-route-httproute-resource",
        )

    def test_does_not_delete_when_twingate_resource_does_not_exist(
        self, k8s_customobjects_client_mock, kopf_info_mock
    ):
        twingate_httproute_annotation_removed(
            body=make_route(), namespace="default", logger=MagicMock()
        )

        k8s_customobjects_client_mock.delete_namespaced_custom_object.assert_not_called()


class TestHttpRoutesByGateway:
    def test_indexes_route_by_each_parent_gateway(self):
        route = make_route(
            parent_refs=[
                {"name": "internal-gw", "sectionName": "http"},
                {"name": "internal-gw", "sectionName": "https"},
                {"name": "shared-gw", "namespace": "infra"},
                {"group": "", "kind": "Service", "name": "mesh-svc"},
            ]
        )

        assert httproutes_by_gateway(body=route, namespace="default") == {
            ("default", "internal-gw"): route,
            ("infra", "shared-gw"): route,
        }


def existing_twingate_resource(address: str = "10.96.12.34", port: int = 443):
    """The TwingateResource as the API returns it, CRD defaults included."""
    resource = expected_resource([port])
    return {
        **resource,
        "metadata": {**resource["metadata"], "resourceVersion": "7"},
        "spec": {
            **resource["spec"],
            "id": "UmVzb3VyY2U6MQ==",
            "address": address,
            "isVisible": True,
            "syncLabels": True,
            "type": "Network",
        },
    }


class TestTwingateGatewayEvent:
    @pytest.fixture
    def route(self):
        return make_route()

    @pytest.fixture
    def run_event(self, route, gateways):
        logger = MagicMock()

        def run(event_type="MODIFIED", gateway=None, routes=None):
            twingate_httproute_gateway_event(
                event={"type": event_type},
                namespace="default",
                name="internal-gw",
                body=kopf.Body(gateway or gateways["default", "internal-gw"]),
                logger=logger,
                httproutes_by_gateway={
                    ("default", "internal-gw"): [route] if routes is None else routes
                },
            )
            return logger

        return run

    def test_updates_address_and_ports_and_keeps_route_owned_fields(
        self, run_event, route, twingate_resources, k8s_customobjects_client_mock
    ):
        twingate_resources["default", "my-route-httproute-resource"] = (
            existing_twingate_resource(address="10.96.0.1", port=8443)
        )
        expected = existing_twingate_resource()

        with patch("kopf.info") as kopf_info_mock:
            run_event()

        k8s_customobjects_client_mock.replace_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            "my-route-httproute-resource",
            expected,
        )
        kopf_info_mock.assert_called_once_with(
            route,
            reason="twingate_httproute_gateway_event",
            message="Updated TwingateResource my-route-httproute-resource from "
            "Gateway default/internal-gw",
        )

    def test_does_nothing_when_twingate_resource_is_in_step(
        self, run_event, twingate_resources, k8s_customobjects_client_mock
    ):
        twingate_resources["default", "my-route-httproute-resource"] = (
            existing_twingate_resource()
        )

        run_event()

        k8s_customobjects_client_mock.replace_namespaced_custom_object.assert_not_called()
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_not_called()

    def test_creates_missing_twingate_resource(
        self, run_event, route, k8s_customobjects_client_mock, kopf_adopt_mock
    ):
        with patch("kopf.info"):
            run_event()

        kopf_adopt_mock.assert_called_once_with(expected_resource([443]), owner=route)
        k8s_customobjects_client_mock.create_namespaced_custom_object.assert_called_once_with(
            "twingate.com",
            "v1beta",
            "default",
            "twingateresources",
            expected_resource([443]),
        )

    def test_ignores_deleted_gateway(self, run_event, k8s_customobjects_client_mock):
        run_event(event_type="DELETED")

        assert k8s_customobjects_client_mock.method_calls == []

    def test_ignores_gateway_without_routes(
        self, run_event, k8s_customobjects_client_mock
    ):
        run_event(routes=[])

        assert k8s_customobjects_client_mock.method_calls == []

    def test_skips_route_served_by_another_parent_gateway(
        self, run_event, k8s_customobjects_client_mock
    ):
        route = make_route(
            parent_refs=[
                {"name": "internal-gw", "sectionName": "https"},
                {"name": "public-gw", "sectionName": "https"},
            ],
            annotations={"resource.twingate.com/parentGateway": "public-gw"},
        )

        run_event(routes=[route])

        assert k8s_customobjects_client_mock.method_calls == []

    def test_waits_for_gateway_address(
        self, run_event, k8s_customobjects_client_mock, kopf_warn_mock
    ):
        logger = run_event(gateway=make_gateway(addresses=[]))

        assert k8s_customobjects_client_mock.method_calls == []
        kopf_warn_mock.assert_not_called()
        logger.info.assert_called_once()

    def test_warns_route_it_cannot_sync(
        self, run_event, route, k8s_customobjects_client_mock, kopf_warn_mock
    ):
        gateway = make_gateway()
        gateway["spec"]["listeners"] = [
            listener
            for listener in gateway["spec"]["listeners"]
            if listener["name"] != "https"
        ]

        run_event(gateway=gateway)

        assert k8s_customobjects_client_mock.method_calls == []
        kopf_warn_mock.assert_called_once()
        assert kopf_warn_mock.call_args.args == (route,)
        assert "no HTTP or HTTPS listener" in kopf_warn_mock.call_args.kwargs["message"]

    def test_retries_after_concurrent_write(
        self, run_event, twingate_resources, k8s_customobjects_client_mock
    ):
        twingate_resources["default", "my-route-httproute-resource"] = (
            existing_twingate_resource(address="10.96.0.1")
        )
        replace = k8s_customobjects_client_mock.replace_namespaced_custom_object
        replace.side_effect = [
            kubernetes.client.exceptions.ApiException(status=409),
            {},
        ]

        with patch("kopf.info"):
            run_event()

        assert replace.call_count == 2

    def test_gives_up_after_repeated_conflicts(
        self, run_event, twingate_resources, k8s_customobjects_client_mock
    ):
        twingate_resources["default", "my-route-httproute-resource"] = (
            existing_twingate_resource(address="10.96.0.1")
        )
        replace = k8s_customobjects_client_mock.replace_namespaced_custom_object
        replace.side_effect = kubernetes.client.exceptions.ApiException(status=409)

        logger = run_event()

        assert replace.call_count == 3
        logger.warning.assert_called_once()

    def test_reraises_other_api_errors(
        self, run_event, twingate_resources, k8s_customobjects_client_mock
    ):
        twingate_resources["default", "my-route-httproute-resource"] = (
            existing_twingate_resource(address="10.96.0.1")
        )
        k8s_customobjects_client_mock.replace_namespaced_custom_object.side_effect = (
            kubernetes.client.exceptions.ApiException(status=500)
        )

        with pytest.raises(kubernetes.client.exceptions.ApiException):
            run_event()


def test_route_handler_reads_twingate_resource_before_gateway(
    k8s_customobjects_client_mock, kopf_adopt_mock, kopf_info_mock
):
    twingate_httproute_create(
        body=make_route(), namespace="default", logger=MagicMock(), reason=Reason.CREATE
    )

    plurals = [
        call.args[3]
        for call in k8s_customobjects_client_mock.get_namespaced_custom_object.call_args_list
    ]
    assert plurals == ["twingateresources", "gateways"]
