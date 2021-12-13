from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from kentik_api.public.types import ID


class CloudExportType(Enum):
    CLOUD_EXPORT_TYPE_UNSPECIFIED = "CLOUD_EXPORT_TYPE_UNSPECIFIED"
    CLOUD_EXPORT_TYPE_KENTIK_MANAGED = "CLOUD_EXPORT_TYPE_KENTIK_MANAGED"
    CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED = "CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED"


@dataclass
class AwsProperties:
    bucket: str = ""
    iam_role_arn: str = ""
    region: str = ""
    delete_after_read: bool = False
    multiple_buckets: bool = False


@dataclass
class AzureProperties:
    location: str = ""
    resource_group: str = ""
    storage_account: str = ""
    subscription_id: ID = ID()
    security_principal_enabled: bool = False


@dataclass
class GceProperties:
    project: str = ""
    subscription: str = ""


@dataclass
class IbmProperties:
    bucket: str = ""


@dataclass
class BgpProperties:
    apply_bgp: bool = False
    use_bgp_device_id: ID = ID()
    device_bgp_type: str = "none"  # device/other_device/none


@dataclass
class Status:
    status: str = ""
    error_message: str = ""
    flow_found: bool = False
    api_access: bool = False
    storage_account_access: bool = False


@dataclass
class CloudExport:
    id: ID = ID()
    type: CloudExportType = CloudExportType.CLOUD_EXPORT_TYPE_UNSPECIFIED
    enabled: bool = False
    name: str = ""
    description: str = ""
    api_root: str = ""
    flow_dest: str = ""
    plan_id: ID = ID()
    cloud_provider: str = ""  # aws/azure/gce/ibm/bgp; see below
    aws: Optional[AwsProperties] = None
    azure: Optional[AzureProperties] = None
    gce: Optional[GceProperties] = None
    ibm: Optional[IbmProperties] = None
    bgp: Optional[BgpProperties] = None
    current_status: Status = Status()


@dataclass
class ListCloudExportResponse:
    exports: List[CloudExport] = field(default_factory=list)
    invalid_exports_count: int = 0
