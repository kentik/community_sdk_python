import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CloudExportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_EXPORT_TYPE_UNSPECIFIED: _ClassVar[CloudExportType]
    CLOUD_EXPORT_TYPE_KENTIK_MANAGED: _ClassVar[CloudExportType]
    CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED: _ClassVar[CloudExportType]

class CloudProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_PROVIDER_UNSPECIFIED: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_AWS: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_AZURE: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_GCE: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_OCI: _ClassVar[CloudProvider]

class CloudExportSamplingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_EXPORT_SAMPLING_TYPE_UNSPECIFIED: _ClassVar[CloudExportSamplingType]
    CLOUD_EXPORT_SAMPLING_TYPE_RATE: _ClassVar[CloudExportSamplingType]
    CLOUD_EXPORT_SAMPLING_TYPE_UNSAMPLED: _ClassVar[CloudExportSamplingType]

CLOUD_EXPORT_TYPE_UNSPECIFIED: CloudExportType
CLOUD_EXPORT_TYPE_KENTIK_MANAGED: CloudExportType
CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED: CloudExportType
CLOUD_PROVIDER_UNSPECIFIED: CloudProvider
CLOUD_PROVIDER_AWS: CloudProvider
CLOUD_PROVIDER_AZURE: CloudProvider
CLOUD_PROVIDER_GCE: CloudProvider
CLOUD_PROVIDER_OCI: CloudProvider
CLOUD_EXPORT_SAMPLING_TYPE_UNSPECIFIED: CloudExportSamplingType
CLOUD_EXPORT_SAMPLING_TYPE_RATE: CloudExportSamplingType
CLOUD_EXPORT_SAMPLING_TYPE_UNSAMPLED: CloudExportSamplingType

class CloudExport(_message.Message):
    __slots__ = (
        "id",
        "type",
        "enabled",
        "name",
        "description",
        "plan_id",
        "cloud_provider",
        "aws",
        "azure",
        "gce",
        "oci",
        "current_status",
        "cdate",
        "edate",
        "sampling",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    AWS_FIELD_NUMBER: _ClassVar[int]
    AZURE_FIELD_NUMBER: _ClassVar[int]
    GCE_FIELD_NUMBER: _ClassVar[int]
    OCI_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: CloudExportType
    enabled: bool
    name: str
    description: str
    plan_id: str
    cloud_provider: CloudProvider
    aws: AwsProperties
    azure: AzureProperties
    gce: GceProperties
    oci: OciProperties
    current_status: CloudExportStatus
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    sampling: CloudExportSamplingProperties
    def __init__(
        self,
        id: _Optional[str] = ...,
        type: _Optional[_Union[CloudExportType, str]] = ...,
        enabled: _Optional[bool] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        plan_id: _Optional[str] = ...,
        cloud_provider: _Optional[_Union[CloudProvider, str]] = ...,
        aws: _Optional[_Union[AwsProperties, _Mapping]] = ...,
        azure: _Optional[_Union[AzureProperties, _Mapping]] = ...,
        gce: _Optional[_Union[GceProperties, _Mapping]] = ...,
        oci: _Optional[_Union[OciProperties, _Mapping]] = ...,
        current_status: _Optional[_Union[CloudExportStatus, _Mapping]] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        sampling: _Optional[_Union[CloudExportSamplingProperties, _Mapping]] = ...,
    ) -> None: ...

class AwsProperties(_message.Message):
    __slots__ = (
        "iam_role_arn",
        "region",
        "metadata_only",
        "collect_flow_logs",
        "collect_firewall_logs",
        "collect_metrics",
        "bucket",
        "bucket_prefix",
        "delete_after_read",
        "aws_iam_role_arn_is_org",
        "secondary_aws_accounts",
        "secondary_aws_blocked_accounts",
        "secondary_aws_regions",
        "secondary_aws_suffix",
    )
    IAM_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    METADATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    COLLECT_FLOW_LOGS_FIELD_NUMBER: _ClassVar[int]
    COLLECT_FIREWALL_LOGS_FIELD_NUMBER: _ClassVar[int]
    COLLECT_METRICS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    BUCKET_PREFIX_FIELD_NUMBER: _ClassVar[int]
    DELETE_AFTER_READ_FIELD_NUMBER: _ClassVar[int]
    AWS_IAM_ROLE_ARN_IS_ORG_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_AWS_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_AWS_BLOCKED_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_AWS_REGIONS_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_AWS_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    iam_role_arn: str
    region: str
    metadata_only: bool
    collect_flow_logs: bool
    collect_firewall_logs: bool
    collect_metrics: bool
    bucket: str
    bucket_prefix: str
    delete_after_read: bool
    aws_iam_role_arn_is_org: bool
    secondary_aws_accounts: _containers.RepeatedScalarFieldContainer[str]
    secondary_aws_blocked_accounts: _containers.RepeatedScalarFieldContainer[str]
    secondary_aws_regions: _containers.RepeatedScalarFieldContainer[str]
    secondary_aws_suffix: str
    def __init__(
        self,
        iam_role_arn: _Optional[str] = ...,
        region: _Optional[str] = ...,
        metadata_only: _Optional[bool] = ...,
        collect_flow_logs: _Optional[bool] = ...,
        collect_firewall_logs: _Optional[bool] = ...,
        collect_metrics: _Optional[bool] = ...,
        bucket: _Optional[str] = ...,
        bucket_prefix: _Optional[str] = ...,
        delete_after_read: _Optional[bool] = ...,
        aws_iam_role_arn_is_org: _Optional[bool] = ...,
        secondary_aws_accounts: _Optional[_Iterable[str]] = ...,
        secondary_aws_blocked_accounts: _Optional[_Iterable[str]] = ...,
        secondary_aws_regions: _Optional[_Iterable[str]] = ...,
        secondary_aws_suffix: _Optional[str] = ...,
    ) -> None: ...

class AzureProperties(_message.Message):
    __slots__ = (
        "location",
        "resource_group",
        "storage_account",
        "subscription_id",
        "security_principal_enabled",
    )
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_PRINCIPAL_ENABLED_FIELD_NUMBER: _ClassVar[int]
    location: str
    resource_group: str
    storage_account: str
    subscription_id: str
    security_principal_enabled: bool
    def __init__(
        self,
        location: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        storage_account: _Optional[str] = ...,
        subscription_id: _Optional[str] = ...,
        security_principal_enabled: _Optional[bool] = ...,
    ) -> None: ...

class GceProperties(_message.Message):
    __slots__ = (
        "project",
        "subscription",
        "metadata_only",
        "collect_flow_logs",
        "collect_metrics",
    )
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    COLLECT_FLOW_LOGS_FIELD_NUMBER: _ClassVar[int]
    COLLECT_METRICS_FIELD_NUMBER: _ClassVar[int]
    project: str
    subscription: str
    metadata_only: bool
    collect_flow_logs: bool
    collect_metrics: bool
    def __init__(
        self,
        project: _Optional[str] = ...,
        subscription: _Optional[str] = ...,
        metadata_only: _Optional[bool] = ...,
        collect_flow_logs: _Optional[bool] = ...,
        collect_metrics: _Optional[bool] = ...,
    ) -> None: ...

class OciProperties(_message.Message):
    __slots__ = (
        "oci_user_id",
        "oci_tenancy_id",
        "oci_compartment_id",
        "oci_default_region",
        "oci_collect_flow_logs",
        "oci_bucket_name",
        "oci_bucket_namespace_name",
        "oci_service_connector_ocid",
        "oci_flow_object_name_prefix",
        "metadata_only",
    )
    OCI_USER_ID_FIELD_NUMBER: _ClassVar[int]
    OCI_TENANCY_ID_FIELD_NUMBER: _ClassVar[int]
    OCI_COMPARTMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OCI_DEFAULT_REGION_FIELD_NUMBER: _ClassVar[int]
    OCI_COLLECT_FLOW_LOGS_FIELD_NUMBER: _ClassVar[int]
    OCI_BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    OCI_BUCKET_NAMESPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    OCI_SERVICE_CONNECTOR_OCID_FIELD_NUMBER: _ClassVar[int]
    OCI_FLOW_OBJECT_NAME_PREFIX_FIELD_NUMBER: _ClassVar[int]
    METADATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    oci_user_id: str
    oci_tenancy_id: str
    oci_compartment_id: _containers.RepeatedScalarFieldContainer[str]
    oci_default_region: str
    oci_collect_flow_logs: bool
    oci_bucket_name: str
    oci_bucket_namespace_name: str
    oci_service_connector_ocid: str
    oci_flow_object_name_prefix: str
    metadata_only: bool
    def __init__(
        self,
        oci_user_id: _Optional[str] = ...,
        oci_tenancy_id: _Optional[str] = ...,
        oci_compartment_id: _Optional[_Iterable[str]] = ...,
        oci_default_region: _Optional[str] = ...,
        oci_collect_flow_logs: _Optional[bool] = ...,
        oci_bucket_name: _Optional[str] = ...,
        oci_bucket_namespace_name: _Optional[str] = ...,
        oci_service_connector_ocid: _Optional[str] = ...,
        oci_flow_object_name_prefix: _Optional[str] = ...,
        metadata_only: _Optional[bool] = ...,
    ) -> None: ...

class CloudExportSamplingProperties(_message.Message):
    __slots__ = ("sampling_enabled", "sampling_type", "sampling_rate")
    SAMPLING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_TYPE_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_RATE_FIELD_NUMBER: _ClassVar[int]
    sampling_enabled: bool
    sampling_type: CloudExportSamplingType
    sampling_rate: int
    def __init__(
        self,
        sampling_enabled: _Optional[bool] = ...,
        sampling_type: _Optional[_Union[CloudExportSamplingType, str]] = ...,
        sampling_rate: _Optional[int] = ...,
    ) -> None: ...

class CloudExportStatus(_message.Message):
    __slots__ = (
        "status",
        "error_message",
        "flow_found",
        "api_access",
        "storage_account_access",
    )
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FLOW_FOUND_FIELD_NUMBER: _ClassVar[int]
    API_ACCESS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_ACCESS_FIELD_NUMBER: _ClassVar[int]
    status: str
    error_message: str
    flow_found: bool
    api_access: bool
    storage_account_access: bool
    def __init__(
        self,
        status: _Optional[str] = ...,
        error_message: _Optional[str] = ...,
        flow_found: _Optional[bool] = ...,
        api_access: _Optional[bool] = ...,
        storage_account_access: _Optional[bool] = ...,
    ) -> None: ...

class CreateCloudExportRequest(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: CloudExport
    def __init__(
        self, export: _Optional[_Union[CloudExport, _Mapping]] = ...
    ) -> None: ...

class CreateCloudExportResponse(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: CloudExport
    def __init__(
        self, export: _Optional[_Union[CloudExport, _Mapping]] = ...
    ) -> None: ...

class ListCloudExportsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCloudExportsResponse(_message.Message):
    __slots__ = ("exports", "invalid_exports_count")
    EXPORTS_FIELD_NUMBER: _ClassVar[int]
    INVALID_EXPORTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    exports: _containers.RepeatedCompositeFieldContainer[CloudExport]
    invalid_exports_count: int
    def __init__(
        self,
        exports: _Optional[_Iterable[_Union[CloudExport, _Mapping]]] = ...,
        invalid_exports_count: _Optional[int] = ...,
    ) -> None: ...

class GetCloudExportRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCloudExportResponse(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: CloudExport
    def __init__(
        self, export: _Optional[_Union[CloudExport, _Mapping]] = ...
    ) -> None: ...

class UpdateCloudExportRequest(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: CloudExport
    def __init__(
        self, export: _Optional[_Union[CloudExport, _Mapping]] = ...
    ) -> None: ...

class UpdateCloudExportResponse(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: CloudExport
    def __init__(
        self, export: _Optional[_Union[CloudExport, _Mapping]] = ...
    ) -> None: ...

class DeleteCloudExportRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteCloudExportResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
