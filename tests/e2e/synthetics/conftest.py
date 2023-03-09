import pytest


def pytest_addoption(parser):
    parser.addoption("--test_labels", action="store", default="")
    parser.addoption("--notification_channels", action="store", default="")


@pytest.fixture(scope="session")
def test_labels(pytestconfig):
    labels = pytestconfig.getoption("test_labels")
    if labels:
        return sorted(labels.split(","))
    else:
        return []


@pytest.fixture(scope="session")
def notification_channels(pytestconfig):
    channels = pytestconfig.getoption("notification_channels")
    if channels:
        return sorted(channels.split(","))
    else:
        return []
