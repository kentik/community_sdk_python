import os

import pytest

from kentik_api.cloudexport.cloud_export import CloudExport, CloudExportType, CloudProviderType, GceProperties
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import clear_readonly_fields, client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_gce_crud() -> None:
    PLAN_ID = ID(os.environ["KTAPI_PLAN_ID"])
    PROPERTIES1 = GceProperties(
        project="testproject",
        subscription="testsubscription",
    )
    PROPERTIES2 = GceProperties(
        project="testprojectupdated",
        subscription="testsubscriptionupdated",
    )
    GCE = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-gce-cloudexport",
        description="E2E test GCE CloudExport description",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.GCE,
        gce=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(GCE)
        assert isinstance(created, CloudExport)
        assert created.id != ID()
        assert created.type == CloudExportType.CUSTOMER_MANAGED
        assert created.enabled == True
        assert created.name == "e2e-gce-cloudexport"
        assert created.description == "E2E test GCE CloudExport description"
        assert created.plan_id == PLAN_ID
        assert created.cloud_provider == CloudProviderType.GCE
        assert created.gce == PROPERTIES1

        # read
        received = client().cloud_export.get(created.id)
        assert clear_readonly_fields(received) == clear_readonly_fields(created)

        # update
        to_update = received
        to_update.type = CloudExportType.KENTIK_MANAGED
        # to_update.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        to_update.name = f"{received.name}-updated"
        to_update.description = f"{received.description} updated"
        to_update.gce = PROPERTIES2
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
