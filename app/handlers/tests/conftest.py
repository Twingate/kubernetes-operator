from pytest_factoryboy import register

from app.api.tests.factories import ConnectorFactory, ResourceFactory

register(ResourceFactory)
register(ConnectorFactory)
