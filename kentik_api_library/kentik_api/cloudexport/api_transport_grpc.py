from typing import Any, Callable, Optional

from google.protobuf.field_mask_pb2 import FieldMask
from grpc import RpcError

import kentik_api.generated.google.api as _
from kentik_api.api_connection.grpc_errors import new_api_error
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import AwsProperties as pbAwsProperties
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import AzureProperties as pbAzureProperties
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import BgpProperties as pbBgpProperties
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import CloudExport as pbCloudExport
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import CloudExportType as pbCloudExportType
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import (
    CreateCloudExportRequest,
    DeleteCloudExportRequest,
)
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import GceProperties as pbGceProperties
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import GetCloudExportRequest
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import IbmProperties as pbIbmProperties
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import ListCloudExportRequest
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import (
    ListCloudExportResponse as pbListCloudExportResponse,
)
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import PatchCloudExportRequest
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import Status as pbStatus
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 import UpdateCloudExportRequest
from kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2_grpc import CloudExportAdminService
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, convert_or_none
from kentik_api.synthetics.api_transport_grpc import reverse_map

from .cloud_export import (
    AwsProperties,
    AzureProperties,
    BgpProperties,
    CloudExport,
    CloudExportType,
    GceProperties,
    IbmProperties,
    ListCloudExportResponse,
    Status,
)

PB_TO_CLOUD_EXPORT_TYPE = {
    pbCloudExportType.CLOUD_EXPORT_TYPE_UNSPECIFIED: CloudExportType.CLOUD_EXPORT_TYPE_UNSPECIFIED,
    pbCloudExportType.CLOUD_EXPORT_TYPE_KENTIK_MANAGED: CloudExportType.CLOUD_EXPORT_TYPE_KENTIK_MANAGED,
    pbCloudExportType.CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED: CloudExportType.CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED,
}


class CloudExportGRPCTransport:
    def __init__(self, auth_email: str, auth_token: str, api_url: str) -> None:
        self._url = api_url
        self._admin = CloudExportAdminService()
        self._credentials = [
            ("x-ch-auth-email", auth_email),
            ("x-ch-auth-api-token", auth_token),
        ]

    def _rpc(self, method: Callable, request: Any) -> Any:
        """Wrap RPC call in RPC error handling"""
        try:
            return method(request=request, metadata=self._credentials, target=self._url)
        except RpcError as error:
            raise new_api_error(error) from error

    def get_all(self) -> ListCloudExportResponse:
        request = ListCloudExportRequest()
        response = self._rpc(self._admin.ListCloudExport, request)
        return pb_to_list_cloud_export_reponse(response)

    def get(self, id: ID) -> CloudExport:
        request = GetCloudExportRequest(id=str(id))
        response = self._rpc(self._admin.GetCloudExport, request)
        return pb_to_cloud_export(response.export)

    def create(self, export: CloudExport) -> CloudExport:
        pb_export = pb_from_cloud_export(export)
        request = CreateCloudExportRequest(export=pb_export)
        response = self._rpc(self._admin.CreateCloudExport, request)
        return pb_to_cloud_export(response.export)

    def patch(self, export: CloudExport, modified: str) -> CloudExport:
        """modified example: export.name"""
        pb_export = pb_from_cloud_export(export)
        mask = FieldMask(paths=[modified])
        request = PatchCloudExportRequest(export=pb_export, mask=mask)
        response = self._rpc(self._admin.PatchCloudExport, request)
        return pb_to_cloud_export(response.export)

    def update(self, export: CloudExport) -> CloudExport:
        pb_export = pb_from_cloud_export(export)
        request = UpdateCloudExportRequest(export=pb_export)
        response = self._rpc(self._admin.UpdateCloudExport, request)
        return pb_to_cloud_export(response.export)

    def delete(self, id: ID) -> None:
        request = DeleteCloudExportRequest(id=str(id))
        self._rpc(self._admin.DeleteCloudExport, request)


def convert_or_empty(attr: Any, convert_func) -> Optional[Any]:
    """Convert if input is not an empty object, else just return None. Raise DataFormatError on failure"""

    _class = attr.__class__
    empty_obj = _class()
    if attr == empty_obj:
        return None
    return convert(attr, convert_func)


def pb_to_list_cloud_export_reponse(v: pbListCloudExportResponse) -> ListCloudExportResponse:
    return ListCloudExportResponse(
        exports=[pb_to_cloud_export(export) for export in v.exports],
        invalid_exports_count=v.invalid_exports_count,
    )


def pb_to_cloud_export(v: pbCloudExport) -> CloudExport:
    return CloudExport(
        id=ID(v.id),
        type=PB_TO_CLOUD_EXPORT_TYPE[v.type],
        enabled=v.enabled,
        name=v.name,
        description=v.description,
        api_root=v.api_root,
        flow_dest=v.flow_dest,
        plan_id=ID(v.plan_id),
        cloud_provider=v.cloud_provider,
        aws=convert_or_empty(v.aws, pb_to_aws),
        azure=convert_or_empty(v.azure, pb_to_azure),
        gce=convert_or_empty(v.gce, pb_to_gce),
        ibm=convert_or_empty(v.ibm, pb_to_ibm),
        bgp=convert_or_empty(v.bgp, pb_to_bgp),
        current_status=pb_to_status(v.current_status),
    )


def pb_from_cloud_export(v: CloudExport) -> pbCloudExport:
    # current_status is generated on server side
    # id is necessary for patch/update operations
    return pbCloudExport(
        id=str(v.id),
        type=reverse_map(PB_TO_CLOUD_EXPORT_TYPE, v.type),
        enabled=v.enabled,
        name=v.name,
        description=v.description,
        api_root=v.api_root,
        flow_dest=v.flow_dest,
        plan_id=str(v.plan_id),
        cloud_provider=v.cloud_provider,
        aws=convert_or_none(v.aws, pb_from_aws),
        azure=convert_or_none(v.azure, pb_from_azure),
        gce=convert_or_none(v.gce, pb_from_gce),
        ibm=convert_or_none(v.ibm, pb_from_ibm),
        bgp=convert_or_none(v.bgp, pb_from_bgp),
    )


def pb_to_aws(v: pbAwsProperties) -> AwsProperties:
    return AwsProperties(
        bucket=v.bucket,
        iam_role_arn=v.iam_role_arn,
        region=v.region,
        delete_after_read=v.delete_after_read,
        multiple_buckets=v.multiple_buckets,
    )


def pb_from_aws(v: AwsProperties) -> pbAwsProperties:
    return pbAwsProperties(
        bucket=v.bucket,
        iam_role_arn=v.iam_role_arn,
        region=v.region,
        delete_after_read=v.delete_after_read,
        multiple_buckets=v.multiple_buckets,
    )


def pb_to_azure(v: pbAzureProperties) -> AzureProperties:
    return AzureProperties(
        location=v.location,
        resource_group=v.resource_group,
        storage_account=v.storage_account,
        subscription_id=ID(v.subscription_id),
        security_principal_enabled=v.security_principal_enabled,
    )


def pb_from_azure(v: AzureProperties) -> pbAzureProperties:
    return pbAzureProperties(
        location=v.location,
        resource_group=v.resource_group,
        storage_account=v.storage_account,
        subscription_id=str(v.subscription_id),
        security_principal_enabled=v.security_principal_enabled,
    )


def pb_to_gce(v: pbGceProperties) -> GceProperties:
    return GceProperties(
        project=v.project,
        subscription=v.subscription,
    )


def pb_from_gce(v: GceProperties) -> pbGceProperties:
    return pbGceProperties(
        project=v.project,
        subscription=v.subscription,
    )


def pb_to_ibm(v: pbIbmProperties) -> IbmProperties:
    return IbmProperties(bucket=v.bucket)


def pb_from_ibm(v: IbmProperties) -> pbIbmProperties:
    return pbIbmProperties(bucket=v.bucket)


def pb_to_bgp(v: pbBgpProperties) -> BgpProperties:
    return BgpProperties(
        apply_bgp=v.apply_bgp,
        use_bgp_device_id=ID(v.use_bgp_device_id),
        device_bgp_type=v.device_bgpp_type,
    )


def pb_from_bgp(v: BgpProperties) -> pbBgpProperties:
    return BgpProperties(
        apply_bgp=v.apply_bgp,
        use_bgp_device_id=str(v.use_bgp_device_id),
        device_bgp_type=v.device_bgp_type,
    )


def pb_to_status(v: pbStatus) -> Status:
    return Status(
        status=v.status,
        error_message=v.error_message,
        flow_found=v.flow_found,
        api_access=v.api_access,
        storage_account_access=v.storage_account_access,
    )
