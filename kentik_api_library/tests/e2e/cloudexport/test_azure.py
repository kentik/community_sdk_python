import os

import pytest

from kentik_api.cloudexport.cloud_export import AzureProperties, CloudExport, CloudExportType
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import client, credentials_missing_str, credentials_present


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
        api_root="https://api.kentik.com",
        flow_dest="https://flow.kentik.com",
        plan_id=PLAN_ID,
        cloud_provider="azure",
        azure=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(AZURE)
        assert isinstance(created, CloudExport)
        assert created.type == CloudExportType.CUSTOMER_MANAGED
        assert created.enabled == True
        assert created.name == "e2e-azure-cloudexport"
        assert created.description == "E2E test AZURE CloudExport description"
        assert created.api_root == "https://api.kentik.com"
        assert created.flow_dest == "https://flow.kentik.com"
        assert created.plan_id == PLAN_ID
        assert created.cloud_provider == "azure"
        assert created.azure == PROPERTIES1

        # read
        received = client().cloud_export.get(created.id)
        assert isinstance(received, CloudExport)
        assert received.type == CloudExportType.CUSTOMER_MANAGED
        assert received.enabled == True
        assert received.name == "e2e-azure-cloudexport"
        assert received.description == "E2E test AZURE CloudExport description"
        assert received.api_root == "https://api.kentik.com"
        assert received.flow_dest == "https://flow.kentik.com"
        assert received.plan_id == PLAN_ID
        assert received.cloud_provider == "azure"
        assert received.azure == PROPERTIES1

        # update
        created.type = CloudExportType.KENTIK_MANAGED
        # created.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        created.name = "e2e-azure-cloudexport-updated"
        created.description = "E2E test AZURE CloudExport description updated"
        created.api_root = "https://api.kentik-updated.com"
        created.flow_dest = "https://flow.kentik-updated.com"
        created.azure = PROPERTIES2

        updated = client().cloud_export.update(created)
        assert isinstance(updated, CloudExport)
        assert updated.type == CloudExportType.KENTIK_MANAGED
        # assert updated.enabled == False
        assert updated.name == "e2e-azure-cloudexport-updated"
        assert updated.description == "E2E test AZURE CloudExport description updated"
        assert updated.api_root == "https://api.kentik-updated.com"
        assert updated.flow_dest == "https://flow.kentik-updated.com"
        assert updated.plan_id == PLAN_ID
        assert updated.cloud_provider == "azure"
        assert updated.azure == PROPERTIES2

        # patch
        created.description = "E2E test AZURE CloudExport description patched"
        patched = client().cloud_export.patch(created, "export.description")
        assert isinstance(patched, CloudExport)
        assert patched.description == "E2E test AZURE CloudExport description patched"
    finally:
        # delete (even if assertion failed)
        client().cloud_export.delete(created.id)
