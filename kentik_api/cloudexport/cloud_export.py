from dataclasses import dataclass
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

    bucket: str
    iam_role_arn: str
    region: str
    delete_after_read: bool = False
    multiple_buckets: bool = False


@dataclass
class AzureProperties(_ConfigElement):
    PB_TYPE = pb.AzureProperties

    location: str
    resource_group: str
    storage_account: str
    subscription_id: str
    security_principal_enabled: bool


@dataclass
class GceProperties(_ConfigElement):
    PB_TYPE = pb.GceProperties

    project: str
    subscription: str


@dataclass
class IbmProperties(_ConfigElement):
    PB_TYPE = pb.IbmProperties

    bucket: str


class DeviceBGPType(SerializableEnum):
    NONE = "none"
    OTHER_DEVICE = "other_device"
    DEVICE = "device"


@dataclass
class BgpProperties(_ConfigElement):
    PB_TYPE = pb.BgpProperties

    apply_bgp: bool
    use_bgp_device_id: ID
    device_bgp_type: DeviceBGPType


@dataclass
class Status(_ConfigElement):
    PB_TYPE = DoNotSerializeMarker  # Status is read-only (provided by server)

    status: str = ""
    error_message: str = ""
    flow_found: bool = False
    api_access: bool = False
    storage_account_access: bool = False


class CloudProviderType(SerializableEnum):
    AWS = "aws"
    AZURE = "azure"
    GCE = "gce"
    IBM = "ibm"


@dataclass
class CloudExport(_ConfigElement):
    PB_TYPE = pb.CloudExport

    # read-write
    name: str
    description: str
    type: CloudExportType
    plan_id: ID
    cloud_provider: CloudProviderType
    aws: Optional[AwsProperties] = None
    azure: Optional[AzureProperties] = None
    gce: Optional[GceProperties] = None
    ibm: Optional[IbmProperties] = None
    bgp: Optional[BgpProperties] = None  # note: not a cloud provider type
    enabled: bool = True
    id: ID = ID()

    # read-only
    _api_root: str = ""
    _flow_dest: str = ""
    _current_status: Status = Status()

    @property
    def current_status(self) -> Status:
        return self._current_status


@dataclass
class ListCloudExportResponse(_ConfigElement):
    PB_TYPE = DoNotSerializeMarker  # response is read-only

    exports: List[CloudExport]
    invalid_exports_count: int
