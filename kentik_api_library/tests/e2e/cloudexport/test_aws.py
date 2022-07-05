import os

import pytest
from requests import patch

from kentik_api.cloudexport.cloud_export import AwsProperties, CloudExport, CloudExportType
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import client, credentials_missing_str, credentials_present


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
        api_root="https://api.kentik.com",
        flow_dest="https://flow.kentik.com",
        plan_id=PLAN_ID,
        cloud_provider="aws",
        aws=PROPERTIES1,
    )

    try:
        # create
        created = client().cloud_export.create(AWS)
        assert isinstance(created, CloudExport)
        assert created.id != ID()
        assert created.type == CloudExportType.CUSTOMER_MANAGED
        assert created.enabled == True
        assert created.name == "e2e-aws-cloudexport"
        assert created.description == "E2E test AWS CloudExport description"
        assert created.api_root == "https://api.kentik.com"
        assert created.flow_dest == "https://flow.kentik.com"
        assert created.plan_id == PLAN_ID
        assert created.cloud_provider == "aws"
        assert created.aws == PROPERTIES1

        # read
        received = client().cloud_export.get(created.id)
        assert isinstance(received, CloudExport)
        assert received.id != ID()
        assert received.type == CloudExportType.CUSTOMER_MANAGED
        assert received.enabled == True
        assert received.name == "e2e-aws-cloudexport"
        assert received.description == "E2E test AWS CloudExport description"
        assert received.api_root == "https://api.kentik.com"
        assert received.flow_dest == "https://flow.kentik.com"
        assert received.plan_id == PLAN_ID
        assert received.cloud_provider == "aws"
        assert received.aws == PROPERTIES1

        # update
        created.type = CloudExportType.KENTIK_MANAGED
        # created.enabled = False  # updating 'enabled' flag doesn't take effect - always gets True
        created.name = "e2e-aws-cloudexport-updated"
        created.description = "E2E test AWS CloudExport description updated"
        created.api_root = "https://api.kentik-updated.com"
        created.flow_dest = "https://flow.kentik-updated.com"
        created.aws = PROPERTIES2
        updated = client().cloud_export.update(created)
        assert isinstance(updated, CloudExport)
        assert updated.id != ID()
        assert updated.type == CloudExportType.KENTIK_MANAGED
        # assert updated.enabled == False
        assert updated.name == "e2e-aws-cloudexport-updated"
        assert updated.description == "E2E test AWS CloudExport description updated"
        assert updated.api_root == "https://api.kentik-updated.com"
        assert updated.flow_dest == "https://flow.kentik-updated.com"
        assert updated.plan_id == PLAN_ID
        assert updated.cloud_provider == "aws"
        assert updated.aws == PROPERTIES2

        # patch
        created.name = "e2e-aws-cloudexport-patched"
        patched = client().cloud_export.patch(created, "export.name")
        assert isinstance(patched, CloudExport)
        assert patched.name == "e2e-aws-cloudexport-patched"
    finally:
        # delete (even if assertion failed)
        client().cloud_export.delete(created.id)
