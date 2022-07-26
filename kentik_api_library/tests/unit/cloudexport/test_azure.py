from google.protobuf.wrappers_pb2 import BoolValue

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.cloudexport.client import KentikCloudExportClient
from kentik_api.cloudexport.cloud_export import AzureProperties, CloudExport, CloudExportType, CloudProviderType, Status
from kentik_api.public.types import ID
from tests.unit.cloudexport import clear_readonly_fields
from tests.unit.cloudexport.stub_api_connector import StubAPICloudExportConnector
from tests.unit.synthetics import protobuf_assert_equal

PB_AZURE = pb.CloudExport(
    id="1234",
    type=CloudExportType.CUSTOMER_MANAGED.value,
    enabled=False,
    name="test_azure_cloudexport",
    description="Test AZURE CloudExport description",
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
    cloud_provider="azure",
    azure=pb.AzureProperties(
        location="Singapore",
        resource_group="testresourcegroup",
        storage_account="teststorageaccount",
        subscription_id="bda574ce-5d2e-5d2c-83da-0f7b0762e10c",
        security_principal_enabled=True,
    ),
    bgp=None,
)

AZURE = CloudExport(
    id=ID("1234"),
    type=CloudExportType.CUSTOMER_MANAGED,
    enabled=False,
    name="test_azure_cloudexport",
    description="Test AZURE CloudExport description",
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
    cloud_provider=CloudProviderType.AZURE,
    azure=AzureProperties(
        location="Singapore",
        resource_group="testresourcegroup",
        storage_account="teststorageaccount",
        subscription_id="bda574ce-5d2e-5d2c-83da-0f7b0762e10c",
        security_principal_enabled=True,
    ),
    bgp=None,
)


def test_get_azure_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector(export_response=PB_AZURE)
    client = KentikCloudExportClient(connector)

    # when
    export = client.get(ID("1234"))

    # then
    assert export == AZURE


def test_create_azure_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.create(AZURE)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AZURE), "CloudExport")


def test_patch_azure_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.patch(AZURE, "export.name")

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AZURE), "CloudExport")


def test_update_azure_cloudexport() -> None:
    # given
    connector = StubAPICloudExportConnector()
    client = KentikCloudExportClient(connector)

    # when
    client.update(AZURE)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AZURE), "CloudExport")
