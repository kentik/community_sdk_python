import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.cloudexport.client import KentikCloudExportClient
from kentik_api.cloudexport.cloud_export import ListCloudExportResponse
from tests.unit.cloudexport.stub_api_connector import StubAPICloudExportConnector

from .test_aws import AWS, PB_AWS
from .test_azure import AZURE, PB_AZURE
from .test_gce import GCE, PB_GCE
from .test_ibm import IBM, PB_IBM


def test_get_all_tests() -> None:
    # given
    pb_cloudexports_response = pb.ListCloudExportResponse(
        exports=[PB_IBM, PB_AWS, PB_AZURE, PB_GCE],
        invalid_exports_count=1,
    )
    expected_cloudexports_response = ListCloudExportResponse(
        exports=[IBM, AWS, AZURE, GCE],
        invalid_exports_count=1,
    )

    connector = StubAPICloudExportConnector(exports_response=pb_cloudexports_response)
    client = KentikCloudExportClient(connector)

    # when
    tests = client.get_all()

    # then response properly parsed
    assert tests == expected_cloudexports_response
