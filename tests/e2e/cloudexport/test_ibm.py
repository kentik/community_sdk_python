import pytest

from kentik_api.cloudexport.cloud_export import CloudExport, CloudExportType, CloudProviderType, IbmProperties
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import credentials_missing_str, credentials_present, execute_cloud_export_crud_steps


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_ibm_crud() -> None:
    ce = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-ibm-test",
        description="E2E IBM CloudExport test",
        plan_id=ID(),  # set to a valid value in execute_cloud_export_crud_steps
        cloud_provider=CloudProviderType.IBM,
        ibm=IbmProperties(bucket="test-bucket"),
    )
    update_properties = IbmProperties(bucket=ce.ibm.bucket + "-updated")  # type: ignore

    execute_cloud_export_crud_steps(ce, update_properties)
