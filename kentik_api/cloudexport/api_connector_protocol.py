from typing_extensions import Protocol

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb


class APICloudExportConnectorProtocol(Protocol):
    def get_all(self) -> pb.ListCloudExportResponse:
        pass

    def get(self, export_id: str) -> pb.CloudExport:
        pass

    def create(self, export: pb.CloudExport) -> pb.CloudExport:
        pass

    def patch(self, export: pb.CloudExport, modified: str) -> pb.CloudExport:
        pass

    def update(self, export: pb.CloudExport) -> pb.CloudExport:
        pass

    def delete(self, export_id: str) -> None:
        pass
