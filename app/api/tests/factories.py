import datetime
from base64 import b64encode

import factory.fuzzy

from app.api.client_connectors import Connector
from app.api.client_resources import (
    Resource,
    ResourceAddress,
    ResourceRemoteNetwork,
    ResourceSecurityPolicy,
    Tag,
)


# encode string to base64
def to_global_id(type_: str, id_: str) -> str:
    value = f"{type_}:{id_}"
    return b64encode(value.encode()).decode()


class ResourceAddressFactory(factory.Factory):
    class Meta:
        model = ResourceAddress

    class Params:
        hostname = factory.Faker("slug")

    type = "DNS"
    value = factory.LazyAttribute(lambda o: o.hostname + ".default.cluster.local")


class ResourceRemoteNetworkFactory(factory.Factory):
    class Meta:
        model = ResourceRemoteNetwork

    id = factory.Sequence(lambda n: to_global_id("RemoteNetwork", str(n)))


class ResourceSecurityPolicyFactory(factory.Factory):
    class Meta:
        model = ResourceSecurityPolicy

    id = factory.Sequence(lambda n: to_global_id("SecurityPolicy", str(n)))


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    key = factory.fuzzy.FuzzyText(length=3)
    value = factory.fuzzy.FuzzyText(length=3)


class ResourceFactory(factory.Factory):
    class Meta:
        model = Resource

    id = factory.Sequence(lambda n: to_global_id("Resource", str(n)))
    name = factory.Faker("slug")
    created_at = factory.LazyFunction(datetime.datetime.now)
    updated_at = factory.LazyFunction(datetime.datetime.now)
    address = factory.SubFactory(
        ResourceAddressFactory, hostname=factory.SelfAttribute("..name")
    )
    alias = factory.SelfAttribute("name")
    is_visible = True
    is_browser_shortcut_enabled = False
    remote_network = factory.SubFactory(ResourceRemoteNetworkFactory)
    security_policy = factory.SubFactory(ResourceSecurityPolicyFactory)
    tags = factory.List([factory.SubFactory(TagFactory)])


class ConnectorFactory(factory.Factory):
    class Meta:
        model = Connector

    id = factory.Sequence(lambda n: to_global_id("Connector", str(n)))
    name = factory.Faker("slug")
    has_status_notifications_enabled = False
