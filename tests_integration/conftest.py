import os
import uuid

import kopf
import pytest

from .utils import kubectl


@pytest.fixture(scope="session")
def kopf_runner_args():
    main_py = os.path.relpath(os.path.join(os.path.dirname(__file__), "../main.py"))
    return ["run", "--verbose", "--log-format=json", "-A", "--standalone", main_py]


@pytest.fixture(scope="session", autouse=True)
def _load_crds():
    kubectl("apply -f ./deploy/twingate-operator/crds/")


@pytest.fixture(scope="session")
def kopf_settings():
    assert "TWINGATE_API_KEY" in os.environ
    assert "TWINGATE_NETWORK" in os.environ
    assert "TWINGATE_REMOTE_NETWORK_ID" in os.environ

    settings = kopf.OperatorSettings()
    settings.watching.server_timeout = 10
    return settings


@pytest.fixture()
def unique_resource_name(request):
    return request.node.originalname.replace("_", "-") + "-" + str(uuid.uuid4())
