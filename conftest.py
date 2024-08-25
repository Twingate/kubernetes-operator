import os

import pytest


def pytest_collection_modifyitems(session, config, items):
    # mark all tests in `test_integration` as integration tests
    for item in items:
        if "tests_integration/" in str(item.fspath):
            item.add_marker("integration")


global_sequence = 0


@pytest.fixture
def sequential_number():
    global global_sequence
    yield global_sequence
    global_sequence += 1


@pytest.fixture(scope="session")
def is_ci():
    return os.environ.get("GITHUB_ACTIONS", False)


@pytest.fixture(scope="session")
def ci_run_id():
    """A unique number for each workflow run within a repository.

    This number does not change if you re-run the workflow run. For example, 1658821493.
    """
    return os.environ.get("GITHUB_RUN_ID", "local")


@pytest.fixture(scope="session")
def ci_run_number():
    """A unique number for each run of a particular workflow in a repository.

    This number begins at 1 for the workflow's first run, and increments with each new run.
    This number does not change if you re-run the workflow run.
    For example, 3.
    """
    return os.environ.get("GITHUB_RUN_NUMBER", "local")
