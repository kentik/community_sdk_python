import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb

# This class implements APICloudExportConnectorProtocol protocol, but doesn't use most of it's arguments
# pragma pylint: disable=unused-argument


class StubAPICloudExportConnector:
    """
    StubAPICloudExportConnector implements APICloudExportConnectorProtocol.
    Allows for recording the requests and returning stubbed API responses.
    """

    def __init__(
        self,
        export_response: pb.CloudExport = pb.CloudExport(),
        exports_response: pb.ListCloudExportResponse = pb.ListCloudExportResponse(),
    ) -> None:
        self._export_response = export_response
        self._exports_response = exports_response
        self.last_payload: pb.CloudExport = pb.CloudExport()

    def get_all(self) -> pb.ListCloudExportResponse:
        return self._exports_response

    def get(self, export_id: str) -> pb.CloudExport:
        return self._export_response

    def create(self, export: pb.CloudExport) -> pb.CloudExport:
        self.last_payload = export
        return export

    def patch(self, export: pb.CloudExport, modified: str) -> pb.CloudExport:
        self.last_payload = export
        return export

    def update(self, export: pb.CloudExport) -> pb.CloudExport:
        self.last_payload = export
        return export

    def delete(self, export_id: str) -> None:
        pass


# pragma pylint: enable=unused-argument
