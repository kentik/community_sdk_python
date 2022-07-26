import os

import pytest

from kentik_api.cloudexport.cloud_export import AzureProperties, CloudExport, CloudExportType, CloudProviderType
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import clear_readonly_fields, client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_azure_crud() -> None:
    PLAN_ID = ID(os.environ["KTAPI_PLAN_ID"])
    PROPERTIES1 = AzureProperties(
        location="Singapore",
        resource_group="testresourcegroup",
        storage_account="teststorageaccount",
        subscription_id="bda574ce-5d2e-5d2c-83da-0f7b0762e10c",
        security_principal_enabled=True,
    )
    PROPERTIES2 = AzureProperties(
        location="Osaka",
        resource_group="testresourcegroupupdated",
        storage_account="teststorageaccountupdated",
        subscription_id="aaaaaaaa-bbbb-ccc-dddd-eeeeeeeeeeee",
        security_principal_enabled=False,
    )
    AZURE = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-azure-cloudexport",
        description="E2E test AZURE CloudExport description",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.AZURE,
        azure=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(AZURE)
        assert isinstance(created, CloudExport)
        assert created.id != ID()
        assert created.type == AZURE.type
        assert created.enabled == AZURE.enabled
        assert created.name == AZURE.name
        assert created.description == AZURE.description
        assert created.plan_id == AZURE.plan_id
        assert created.cloud_provider == AZURE.cloud_provider
        assert created.azure == AZURE.azure

        # read
        received = client().cloud_export.get(created.id)
        assert clear_readonly_fields(received) == clear_readonly_fields(created)

        # update
        to_update = received
        to_update.type = CloudExportType.KENTIK_MANAGED
        # to_update.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        to_update.name = f"{received.name}-updated"
        to_update.description = f"{received.description} updated"
        to_update.azure = PROPERTIES2
        updated = client().cloud_export.update(to_update)
        assert clear_readonly_fields(updated) == clear_readonly_fields(to_update)

        # patch
        to_patch = received
        to_patch.description = f"{received.description} patched"
        patched = client().cloud_export.patch(to_patch, "export.description")
        assert clear_readonly_fields(patched) == clear_readonly_fields(to_patch)
    finally:
        # delete (even if assertion failed)
        client().cloud_export.delete(created.id)
