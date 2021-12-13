from kentik_api.public.types import ID

from .api_transport_grpc import CloudExportGRPCTransport
from .cloud_export import CloudExport, ListCloudExportResponse


class CloudExportClient:
    """CloudExportClient can use gRPC or HTTP transport (to be implemented if needed)"""

    def __init__(self, auth_email: str, auth_token: str, api_url: str) -> None:
        self._transport = CloudExportGRPCTransport(auth_email, auth_token, api_url)

    def get_all(self) -> ListCloudExportResponse:
        return self._transport.get_all()

    def get(self, id: ID) -> CloudExport:
        return self._transport.get(id)

    def create(self, export: CloudExport) -> CloudExport:
        return self._transport.create(export)

    def patch(self, export: CloudExport, modified: str) -> CloudExport:
        """modified: eg. export.name"""
        return self._transport.patch(export, modified)

    def update(self, export: CloudExport) -> CloudExport:
        return self._transport.update(export)

    def delete(self, id: ID) -> None:
        return self._transport.delete(id)
