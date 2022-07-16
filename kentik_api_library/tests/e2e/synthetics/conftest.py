import pytest


def pytest_addoption(parser):
    parser.addoption("--test_labels", action="store", default="")
    parser.addoption("--notification_channels", action="store", default="")
    parser.addoption("--pass_edate_on_update", action="store_true", default=False)


@pytest.fixture(scope="session")
def test_labels(pytestconfig):
    labels = pytestconfig.getoption("test_labels")
    if labels:
        return labels.split(",")
    else:
        return []


@pytest.fixture(scope="session")
def notification_channels(pytestconfig):
    channels = pytestconfig.getoption("notification_channels")
    if channels:
        return channels.split(",")
    else:
        return []


@pytest.fixture(scope="session")
def pass_edate_on_update(pytestconfig):
    return pytestconfig.getoption("pass_edate_on_update")
