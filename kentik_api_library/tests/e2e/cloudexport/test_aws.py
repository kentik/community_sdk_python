import os

import pytest

from kentik_api.cloudexport.cloud_export import AwsProperties, CloudExport, CloudExportType, CloudProviderType
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import clear_readonly_fields, client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_aws_crud() -> None:
    PLAN_ID = ID(os.environ["KTAPI_PLAN_ID"])
    PROPERTIES1 = AwsProperties(
        bucket="cloudexport-src-s3-bucket",
        iam_role_arn="arn:aws:iam::177634097045:role/test-cloudexport-IngestRole",
        region="eu-central-1",
        delete_after_read=True,
        multiple_buckets=True,
    )
    PROPERTIES2 = AwsProperties(
        bucket="cloudexport-src-s3-bucket-updated",
        iam_role_arn="arn:aws:iam::177634097045:role/test-cloudexport-IngestRole-updated",
        region="us-east-1",
        delete_after_read=False,
        multiple_buckets=False,
    )
    AWS = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-aws-cloudexport",
        description="E2E test AWS CloudExport description",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.AWS,
        aws=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(AWS)
        assert isinstance(created, CloudExport)
        assert created.id != ID()
        assert created.type == AWS.type
        assert created.enabled == AWS.enabled
        assert created.name == AWS.name
        assert created.description == AWS.description
        assert created.plan_id == AWS.plan_id
        assert created.cloud_provider == AWS.cloud_provider
        assert created.aws == AWS.aws

        # read
        received = client().cloud_export.get(created.id)
        assert clear_readonly_fields(received) == clear_readonly_fields(created)

        # update
        to_update = received
        to_update.type = CloudExportType.KENTIK_MANAGED
        # to_update.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        to_update.name = f"{received.name}-updated"
        to_update.description = f"{received.description} updated"
        to_update.aws = PROPERTIES2
        updated = client().cloud_export.update(to_update)
        assert clear_readonly_fields(updated) == clear_readonly_fields(to_update)

        # patch
        to_patch = received
        to_patch.name = f"{received.name}-patched"
        patched = client().cloud_export.patch(to_patch, "export.name")
        assert clear_readonly_fields(patched) == clear_readonly_fields(to_patch)
    finally:
        # delete (even if assertion failed)
        client().cloud_export.delete(created.id)
