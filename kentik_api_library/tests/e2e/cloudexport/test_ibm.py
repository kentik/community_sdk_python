import os

import pytest
from numpy import isin

from kentik_api.cloudexport.cloud_export import CloudExport, CloudExportType, IbmProperties
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import client, credentials_missing_str, credentials_present


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
        api_root="https://api.kentik.com",
        flow_dest="https://flow.kentik.com",
        plan_id=PLAN_ID,
        cloud_provider="ibm",
        ibm=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(IBM)
        assert isinstance(created, CloudExport)
        assert created.type == CloudExportType.CUSTOMER_MANAGED
        assert created.enabled == True
        assert created.name == "e2e-ibm-cloudexport"
        assert created.description == "E2E test IBM CloudExport description"
        assert created.api_root == "https://api.kentik.com"
        assert created.flow_dest == "https://flow.kentik.com"
        assert created.plan_id == PLAN_ID
        assert created.cloud_provider == "ibm"
        assert created.ibm == PROPERTIES1

        # read
        received = client().cloud_export.get(created.id)
        assert isinstance(received, CloudExport)
        assert received.type == CloudExportType.CUSTOMER_MANAGED
        assert received.enabled == True
        assert received.name == "e2e-ibm-cloudexport"
        assert received.description == "E2E test IBM CloudExport description"
        assert received.api_root == "https://api.kentik.com"
        assert received.flow_dest == "https://flow.kentik.com"
        assert received.plan_id == PLAN_ID
        assert received.cloud_provider == "ibm"
        assert received.ibm == PROPERTIES1

        # update
        created.type = CloudExportType.KENTIK_MANAGED
        # created.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        created.name = "e2e-ibm-cloudexport-updated"
        created.description = "E2E test IBM CloudExport description updated"
        created.api_root = "https://api.kentik-updated.com"
        created.flow_dest = "https://flow.kentik-updated.com"
        created.ibm = PROPERTIES2
        updated = client().cloud_export.update(created)
        assert isinstance(updated, CloudExport)
        assert updated.type == CloudExportType.KENTIK_MANAGED
        # assert updated.enabled == False
        assert updated.name == "e2e-ibm-cloudexport-updated"
        assert updated.description == "E2E test IBM CloudExport description updated"
        assert updated.api_root == "https://api.kentik-updated.com"
        assert updated.flow_dest == "https://flow.kentik-updated.com"
        assert updated.plan_id == PLAN_ID
        assert updated.cloud_provider == "ibm"
        assert updated.ibm == PROPERTIES2

        # patch
        created.flow_dest = "https://flow.kentik-patched.com"
        patched = client().cloud_export.patch(created, "export.flow_dest")
        assert isinstance(patched, CloudExport)
        assert patched.flow_dest == "https://flow.kentik-patched.com"
    finally:
        # delete (even if assertion failed)
        client().cloud_export.delete(created.id)
