import os
import uuid

import kopf
import pytest

from .utils import kubectl


@pytest.fixture(scope="module", autouse=True)
def _load_crds():
    kubectl("apply -f ./deploy/twingate-operator/crds/")


@pytest.fixture(scope="module")
def kopf_settings():
    assert "TWINGATE_API_KEY" in os.environ
    assert "TWINGATE_NETWORK" in os.environ
    assert "TWINGATE_REMOTE_NETWORK_ID" in os.environ

    settings = kopf.OperatorSettings()
    settings.watching.server_timeout = 10
    return settings


@pytest.fixture()
def unique_resource_name(request):
    return request.node.name.replace("_", "-") + "-" + str(uuid.uuid4())
