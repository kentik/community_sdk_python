from google.protobuf.wrappers_pb2 import BoolValue

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.cloudexport.client import KentikCloudExportClient
from kentik_api.cloudexport.cloud_export import (
    BgpProperties,
    CloudExport,
    CloudExportType,
    CloudProviderType,
    DeviceBGPType,
    IbmProperties,
    Status,
)
from kentik_api.public.types import ID
from tests.unit.cloudexport import clear_readonly_fields
from tests.unit.cloudexport.stub_api_connector import StubAPICloudExportConnector
from tests.unit.synthetics import protobuf_assert_equal

PB_IBM = pb.CloudExport(
    id="1234",
    type=CloudExportType.CUSTOMER_MANAGED.value,
    enabled=True,
    name="test_ibm_cloudexport",
    description="Test IBM CloudExport description",
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
    cloud_provider="ibm",
    ibm=pb.IbmProperties(bucket="cloudexport-bucket"),
    bgp=pb.BgpProperties(
        apply_bgp=True,
        use_bgp_device_id="42",
        device_bgp_type=DeviceBGPType.NONE.value,
    ),
)

IBM = CloudExport(
    id=ID("1234"),
    type=CloudExportType.CUSTOMER_MANAGED,
    enabled=True,
    name="test_ibm_cloudexport",
    description="Test IBM CloudExport description",
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
    cloud_provider=CloudProviderType.IBM,
    ibm=IbmProperties(bucket="cloudexport-bucket"),
    bgp=BgpProperties(
        apply_bgp=True,
        use_bgp_device_id="42",
        device_bgp_type=DeviceBGPType.NONE,
    ),
)


def test_get_ibm_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector(export_response=PB_IBM)
    client = KentikCloudExportClient(connector)

    # when
    export = client.get(ID("1234"))

    # then
    assert export == IBM


def test_create_ibm_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.create(IBM)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_IBM), "CloudExport")


def test_patch_ibm_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.patch(IBM, "export.name")

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_IBM), "CloudExport")


def test_update_ibm_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.update(IBM)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_IBM), "CloudExport")
