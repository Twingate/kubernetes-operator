import os
import random
import string
import uuid
from contextlib import contextmanager

import kopf
import pytest
from kopf.testing import KopfRunner

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


@pytest.fixture
def unique_resource_name(request):
    return request.node.originalname.replace("_", "-") + "-" + str(uuid.uuid4())


@pytest.fixture
def random_name_generator(ci_run_number):
    def generate(prefix: str, k: int = 8, max_length: int = 30) -> str:
        random_str = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=k)  # noqa: S311
        )
        result = f"{prefix}-{ci_run_number}-{random_str}"
        assert len(result) <= max_length
        return result

    return generate


@pytest.fixture
def run_kopf(kopf_runner_args, kopf_settings):
    @contextmanager
    def inner(*, enable_connector_reconciler=True, enable_group_reconciler=True):
        env = {}
        if enable_connector_reconciler:
            env["CONNECTOR_RECONCILER_INTERVAL"] = "1"
            env["CONNECTOR_RECONCILER_INIT_DELAY"] = "1"

        if enable_group_reconciler:
            env["GROUP_RECONCILER_INTERVAL"] = "1"
            env["GROUP_RECONCILER_INIT_DELAY"] = "1"

        with KopfRunner(
            kopf_runner_args,
            settings=kopf_settings,
            env=env,
        ) as runner:
            yield runner

        assert runner.exception is None
        assert runner.exit_code == 0

    return inner
