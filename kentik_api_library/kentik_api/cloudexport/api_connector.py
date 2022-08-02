from typing import Any, List, Tuple

from google.protobuf.field_mask_pb2 import FieldMask

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2_grpc import CloudExportAdminService
from kentik_api.internal.grpc import wrap_grpc_errors
from kentik_api.version import get_user_agent


class APICloudExportConnector:
    """
    APICloudExportConnector implements APICloudExportConnectorProtocol.
    Allows sending authorized gRPC requests to Kentik CloudExport API
    """

    def __init__(
        self,
        api_url: str,
        auth_email: str,
        auth_token: str,
        options: List[Tuple[str, Any]] = [],
    ):
        self._url = api_url
        self._options = tuple(options)
        self._admin = CloudExportAdminService()
        self._metadata = [
            ("x-ch-auth-email", auth_email),
            ("x-ch-auth-api-token", auth_token),
            ("user-agent", get_user_agent()),
        ]

    @wrap_grpc_errors
    def get_all(self) -> pb.ListCloudExportResponse:
        request = pb.ListCloudExportRequest()
        return self._admin.ListCloudExport(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        )

    @wrap_grpc_errors
    def get(self, export_id: str) -> pb.CloudExport:
        request = pb.GetCloudExportRequest(id=export_id)
        return self._admin.GetCloudExport(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).export

    @wrap_grpc_errors
    def create(self, export: pb.CloudExport) -> pb.CloudExport:
        request = pb.CreateCloudExportRequest(export=export)
        return self._admin.CreateCloudExport(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).export

    @wrap_grpc_errors
    def patch(self, export: pb.CloudExport, modified: str) -> pb.CloudExport:
        """modified example: export.name"""
        mask = FieldMask(paths=[modified])
        request = pb.PatchCloudExportRequest(export=export, mask=mask)
        return self._admin.PatchCloudExport(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).export

    @wrap_grpc_errors
    def update(self, export: pb.CloudExport) -> pb.CloudExport:
        request = pb.UpdateCloudExportRequest(export=export)
        return self._admin.UpdateCloudExport(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).export

    @wrap_grpc_errors
    def delete(self, export_id: str) -> None:
        request = pb.DeleteCloudExportRequest(id=export_id)
        self._admin.DeleteCloudExport(request=request, metadata=self._metadata, target=self._url, options=self._options)
