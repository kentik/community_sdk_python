from google.protobuf.wrappers_pb2 import BoolValue

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.cloudexport.client import KentikCloudExportClient
from kentik_api.cloudexport.cloud_export import (
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

PB_BGP = pb.CloudExport(
    id="1234",
    type=CloudExportType.CUSTOMER_MANAGED.value,
    enabled=True,
    name="test_bgp_cloudexport",
    description="Test BGP CloudExport description",
    plan_id="5678",
    api_root="https://api.kentik.com",
    flow_dest="https://flow.kentik.com",
    current_status=pb.Status(
        status="ERROR",
        error_message="Flow not found",
        flow_found=BoolValue(value=False),
        api_access=BoolValue(value=False),
        storage_account_access=BoolValue(value=False),
    ),
    cloud_provider="bgp",
    bgp=pb.BgpProperties(
        apply_bgp=True,
        use_bgp_device_id="42",
        device_bgp_type=DeviceBGPType.DEVICE.value,
    ),
)

BGP = CloudExport(
    id=ID("1234"),
    type=CloudExportType.CUSTOMER_MANAGED,
    enabled=True,
    name="test_bgp_cloudexport",
    description="Test BGP CloudExport description",
    plan_id=ID("5678"),
    _api_root="https://api.kentik.com",
    _flow_dest="https://flow.kentik.com",
    _current_status=Status(
        status="ERROR",
        error_message="Flow not found",
        flow_found=False,
        api_access=False,
        storage_account_access=False,
    ),
    cloud_provider=CloudProviderType.BGP,
    bgp=BgpProperties(
        apply_bgp=True,
        use_bgp_device_id="42",
        device_bgp_type=DeviceBGPType.DEVICE,
    ),
)


def test_get_bgp_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector(export_response=PB_BGP)
    client = KentikCloudExportClient(connector)

    # when
    export = client.get(ID("1234"))

    # then
    assert export == BGP


def test_create_bgp_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.create(BGP)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_BGP), "CloudExport")


def test_patch_bgp_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.patch(BGP, "export.name")

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_BGP), "CloudExport")


def test_update_bgp_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.update(BGP)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_BGP), "CloudExport")
