import pytest

from kentik_api.cloudexport.cloud_export import CloudExport, CloudExportType, CloudProviderType, GceProperties
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import credentials_missing_str, credentials_present, execute_cloud_export_crud_steps


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_gce_crud() -> None:
    ce = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-gce-test",
        description="E2E GCE CloudExport test",
        plan_id=ID(),  # set to a valid value in execute_cloud_export_crud_steps
        cloud_provider=CloudProviderType.GCE,
        gce=GceProperties(
            project="test-project",
            subscription="test-subscription",
        ),
    )
    update_properties = GceProperties(
        project=ce.gce.project + "-updated",  # type: ignore
        subscription=ce.gce.subscription + "-updated",  # type: ignore
    )

    execute_cloud_export_crud_steps(ce, update_properties)
