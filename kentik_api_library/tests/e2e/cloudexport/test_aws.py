import pytest

from kentik_api.cloudexport.cloud_export import AwsProperties, CloudExport, CloudExportType, CloudProviderType
from kentik_api.public.types import ID
from tests.e2e.cloudexport.utils import credentials_missing_str, credentials_present, execute_cloud_export_crud_steps


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_aws_crud() -> None:
    ce = CloudExport(
        type=CloudExportType.CUSTOMER_MANAGED,
        enabled=True,
        name="e2e-aws-test",
        description="E2E AWS CloudExport test",
        plan_id=ID(),  # set to a valid value in execute_cloud_export_crud_steps
        cloud_provider=CloudProviderType.AWS,
        aws=AwsProperties(
            bucket="e2e-aws-test-bucket",
            iam_role_arn="arn:aws:iam::177634097045:role/test-IngestRole",
            region="eu-central-1",
            delete_after_read=True,
            multiple_buckets=True,
        ),
    )
    update_properties = AwsProperties(
        bucket=ce.aws.bucket + "-updated",  # type: ignore
        iam_role_arn=ce.aws.iam_role_arn + "-updated",  # type: ignore
        region="us-east-1",
        delete_after_read=False,
        multiple_buckets=False,
    )
    execute_cloud_export_crud_steps(ce, update_properties)
