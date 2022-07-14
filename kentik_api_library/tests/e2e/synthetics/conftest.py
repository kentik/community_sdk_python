import pytest


def pytest_addoption(parser):
    parser.addoption("--test_labels", action="store", default="")


@pytest.fixture(scope="session")
def test_labels(pytestconfig):
    labels = pytestconfig.getoption("test_labels")
    if labels:
        return labels.split(",")
    else:
        return []
