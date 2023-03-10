import pytest

from .utils import client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_get_all_agents() -> None:
    agents = client().synthetics.get_all_agents()
    assert isinstance(agents, list)
