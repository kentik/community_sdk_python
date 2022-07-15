import os

import pytest

from kentik_api.cloudexport.cloud_export import CloudExport, CloudExportType, CloudProviderType, IbmProperties
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import clear_readonly_fields, client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_ibm_crud() -> None:
    PLAN_ID = ID(os.environ["KTAPI_PLAN_ID"])
    PROPERTIES1 = IbmProperties(bucket="cloudexport-bucket")
    PROPERTIES2 = IbmProperties(bucket="cloudexport-bucket-updated")
    IBM = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-ibm-cloudexport",
        description="E2E test IBM CloudExport description",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.IBM,
        ibm=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(IBM)
        assert isinstance(created, CloudExport)
        assert created.id != ID()
        assert created.type == CloudExportType.CUSTOMER_MANAGED
        assert created.enabled == True
        assert created.name == "e2e-ibm-cloudexport"
        assert created.description == "E2E test IBM CloudExport description"
        assert created.plan_id == PLAN_ID
        assert created.cloud_provider == CloudProviderType.IBM
        assert created.ibm == PROPERTIES1

        # read
        received = client().cloud_export.get(created.id)
        assert clear_readonly_fields(received) == clear_readonly_fields(created)

        # update
        to_update = received
        to_update.type = CloudExportType.KENTIK_MANAGED
        # to_update.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        to_update.name = f"{received.name}-updated"
        to_update.description = f"{received.description} updated"
        to_update.ibm = PROPERTIES2
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
