import pytest

from kentik_api.cloudexport.cloud_export import ListCloudExportResponse
from tests.e2e.cloudexport.utils import client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_ibm_crud() -> None:
    exports = client().cloud_export.get_all()
    assert isinstance(exports, ListCloudExportResponse)
