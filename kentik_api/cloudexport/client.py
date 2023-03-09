from kentik_api.public.types import ID

from .api_connector_protocol import APICloudExportConnectorProtocol
from .cloud_export import CloudExport, ListCloudExportResponse


class KentikCloudExportClient:
    def __init__(self, connector: APICloudExportConnectorProtocol) -> None:
        self._connector = connector

    def get_all(self) -> ListCloudExportResponse:
        pb_exports = self._connector.get_all()
        return ListCloudExportResponse.from_pb(pb_exports)

    def get(self, export_id: ID) -> CloudExport:
        pb_export = self._connector.get(str(export_id))
        return CloudExport.from_pb(pb_export)

    def create(self, export: CloudExport) -> CloudExport:
        pb_input_export = export.to_pb()
        pb_output_export = self._connector.create(pb_input_export)
        return CloudExport.from_pb(pb_output_export)

    def patch(self, export: CloudExport, modified: str) -> CloudExport:
        """
        :param modified comma-separated list of fields to be modified, eg. "export.name,export.description"
        """

        pb_input_export = export.to_pb()
        pb_output_export = self._connector.patch(pb_input_export, modified)
        return CloudExport.from_pb(pb_output_export)

    def update(self, export: CloudExport) -> CloudExport:
        pb_input_export = export.to_pb()
        pb_output_export = self._connector.update(pb_input_export)
        return CloudExport.from_pb(pb_output_export)

    def delete(self, export_id: ID) -> None:
        return self._connector.delete(str(export_id))
