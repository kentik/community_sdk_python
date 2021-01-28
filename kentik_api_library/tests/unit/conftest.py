from unittest import mock
import pytest

from tests.unit.stub_api_connector import StubAPIConnector
from kentik_api import KentikAPI


@pytest.fixture
def connector():
    return StubAPIConnector()


@pytest.fixture
def client(connector):
    with mock.patch("kentik_api.kentik_api.new_connector", return_value=connector):
        return KentikAPI("email@example.com", "api-test-token")
