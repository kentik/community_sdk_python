import pytest

from kentik_api.cloudexport.cloud_export import AzureProperties, CloudExport, CloudExportType, CloudProviderType
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import credentials_missing_str, credentials_present, execute_cloud_export_crud_steps


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_azure_crud() -> None:
    ce = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-azure-test",
        description="E2E Azure CloudExport test",
        plan_id=ID(),  # set to a valid value in execute_cloud_export_crud_steps
        cloud_provider=CloudProviderType.AZURE,
        azure=AzureProperties(
            location="Singapore",
            resource_group="test-rg",
            storage_account="test-storage-account",
            subscription_id="bda574ce-5d2e-5d2c-83da-0f7b0762e10c",
            security_principal_enabled=True,
        ),
    )
    update_properties = AzureProperties(
        location="Osaka",
        resource_group=ce.azure.resource_group + "-updated",  # type: ignore
        storage_account=ce.azure.storage_account + "-updated",  # type: ignore
        subscription_id="aaaaaaaa-bbbb-ccc-dddd-eeeeeeeeeeee",
        security_principal_enabled=False,
    )

    execute_cloud_export_crud_steps(ce, update_properties)
