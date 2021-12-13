from google.protobuf.wrappers_pb2 import BoolValue

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.cloudexport.client import KentikCloudExportClient
from kentik_api.cloudexport.cloud_export import CloudExport, CloudExportType, GceProperties, Status
from kentik_api.public.types import ID
from tests.unit.cloudexport import clear_readonly_fields
from tests.unit.cloudexport.stub_api_connector import StubAPICloudExportConnector
from tests.unit.synthetics import protobuf_assert_equal

PB_GCE = pb.CloudExport(
    id="1234",
    type=CloudExportType.CUSTOMER_MANAGED.value,
    enabled=True,
    name="test_gce_cloudexport",
    description="Test GCE CloudExport description",
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
    cloud_provider="gce",
    gce=pb.GceProperties(project="testproject", subscription="gcesubscription"),
)

GCE = CloudExport(
    id=ID("1234"),
    type=CloudExportType.CUSTOMER_MANAGED,
    enabled=True,
    name="test_gce_cloudexport",
    description="Test GCE CloudExport description",
    api_root="https://api.kentik.com",
    flow_dest="https://flow.kentik.com",
    plan_id=ID("5678"),
    current_status=Status(
        status="OK",
        error_message="NO ERROR",
        flow_found=True,
        api_access=True,
        storage_account_access=True,
    ),
    cloud_provider="gce",
    gce=GceProperties(project="testproject", subscription="gcesubscription"),
)


def test_get_gce_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector(export_response=PB_GCE)
    client = KentikCloudExportClient(connector)

    # when
    export = client.get(ID("1234"))

    # then
    assert export == GCE


def test_create_gce_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.create(GCE)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_GCE), "CloudExport")


def test_patch_gce_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.patch(GCE, "export.name")

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_GCE), "CloudExport")


def test_update_gce_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.update(GCE)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_GCE), "CloudExport")
