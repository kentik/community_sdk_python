from google.protobuf.wrappers_pb2 import BoolValue

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.cloudexport.client import KentikCloudExportClient
from kentik_api.cloudexport.cloud_export import (
    AwsProperties,
    BgpProperties,
    CloudExport,
    CloudExportType,
    CloudProviderType,
    DeviceBGPType,
    Status,
)
from kentik_api.public.types import ID
from tests.unit.cloudexport import clear_readonly_fields
from tests.unit.cloudexport.stub_api_connector import StubAPICloudExportConnector
from tests.unit.synthetics import protobuf_assert_equal

PB_AWS = pb.CloudExport(
    id="1234",
    type=CloudExportType.KENTIK_MANAGED.value,
    enabled=True,
    name="test_aws_cloudexport",
    description="Test AWS CloudExport description",
    api_root="https://api.kentik.com",
    flow_dest="https://flow.kentik.com",
    plan_id="5678",
    current_status=pb.Status(
        status="OK",
        error_message="NO ERROR",
        flow_found=BoolValue(value=True),
        api_access=BoolValue(value=True),
        storage_account_access=BoolValue(value=True),
    ),
    cloud_provider="aws",
    aws=pb.AwsProperties(
        bucket="cloudexport-src-s3-bucket",
        iam_role_arn="arn:aws:iam::177634097045:role/test-cloudexport-IngestRole",
        region="eu-central-1",
        delete_after_read=True,
        multiple_buckets=True,
    ),
    bgp=pb.BgpProperties(
        apply_bgp=True,
        use_bgp_device_id="42",
        device_bgp_type=DeviceBGPType.DEVICE.value,
    ),
)

AWS = CloudExport(
    id=ID("1234"),
    type=CloudExportType.KENTIK_MANAGED,
    enabled=True,
    name="test_aws_cloudexport",
    description="Test AWS CloudExport description",
    plan_id=ID("5678"),
    _api_root="https://api.kentik.com",
    _flow_dest="https://flow.kentik.com",
    _current_status=Status(
        status="OK",
        error_message="NO ERROR",
        flow_found=True,
        api_access=True,
        storage_account_access=True,
    ),
    cloud_provider=CloudProviderType.AWS,
    aws=AwsProperties(
        bucket="cloudexport-src-s3-bucket",
        iam_role_arn="arn:aws:iam::177634097045:role/test-cloudexport-IngestRole",
        region="eu-central-1",
        delete_after_read=True,
        multiple_buckets=True,
    ),
    bgp=BgpProperties(
        apply_bgp=True,
        use_bgp_device_id="42",
        device_bgp_type=DeviceBGPType.DEVICE,
    ),
)


def test_get_aws_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector(export_response=PB_AWS)
    client = KentikCloudExportClient(connector)

    # when
    export = client.get(ID("1234"))

    # then
    assert export == AWS


def test_create_aws_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.create(AWS)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AWS), "CloudExport")


def test_patch_aws_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.patch(AWS, "export.name")

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AWS), "CloudExport")


def test_update_aws_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.update(AWS)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AWS), "CloudExport")
