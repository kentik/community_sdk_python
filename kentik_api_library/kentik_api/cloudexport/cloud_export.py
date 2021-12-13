from dataclasses import dataclass, field
from typing import List, Optional

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb
from kentik_api.internal.grpc import DoNotSerializeMarker, SerializableEnum, _ConfigElement
from kentik_api.public.types import ID


class CloudExportType(SerializableEnum):
    UNSPECIFIED = pb.CLOUD_EXPORT_TYPE_UNSPECIFIED
    KENTIK_MANAGED = pb.CLOUD_EXPORT_TYPE_KENTIK_MANAGED
    CUSTOMER_MANAGED = pb.CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED


@dataclass
class AwsProperties(_ConfigElement):
    PB_TYPE = pb.AwsProperties

    bucket: str = ""
    iam_role_arn: str = ""
    region: str = ""
    delete_after_read: bool = False
    multiple_buckets: bool = False


@dataclass
class AzureProperties(_ConfigElement):
    PB_TYPE = pb.AzureProperties

    location: str = ""
    resource_group: str = ""
    storage_account: str = ""
    subscription_id: str = ""
    security_principal_enabled: bool = False


@dataclass
class GceProperties(_ConfigElement):
    PB_TYPE = pb.GceProperties

    project: str = ""
    subscription: str = ""


@dataclass
class IbmProperties(_ConfigElement):
    PB_TYPE = pb.IbmProperties

    bucket: str = ""


@dataclass
class BgpProperties(_ConfigElement):
    PB_TYPE = pb.BgpProperties

    apply_bgp: bool = False
    use_bgp_device_id: ID = ID()
    device_bgp_type: str = "none"  # device/other_device/none


@dataclass
class Status(_ConfigElement):
    PB_TYPE = DoNotSerializeMarker  # Status is read-only (provided by server)

    status: str = ""
    error_message: str = ""
    flow_found: bool = False
    api_access: bool = False
    storage_account_access: bool = False


@dataclass
class CloudExport(_ConfigElement):
    PB_TYPE = pb.CloudExport

    id: ID = ID()
    type: CloudExportType = CloudExportType.UNSPECIFIED
    enabled: bool = False
    name: str = ""
    description: str = ""
    api_root: str = ""
    flow_dest: str = ""
    plan_id: ID = ID()
    cloud_provider: str = ""  # not an enum as there will be more clouds supported. Currently: aws/azure/gce/ibm/bgp
    aws: Optional[AwsProperties] = None
    azure: Optional[AzureProperties] = None
    gce: Optional[GceProperties] = None
    ibm: Optional[IbmProperties] = None
    bgp: Optional[BgpProperties] = None
    current_status: Status = Status()


@dataclass
class ListCloudExportResponse(_ConfigElement):
    PB_TYPE = DoNotSerializeMarker  # response is read-only

    exports: List[CloudExport] = field(default_factory=list)
    invalid_exports_count: int = 0
