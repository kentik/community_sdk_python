from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from kentik_api.gen.user.pb import user_pb2 as _user_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Alert(_message.Message):
    __slots__ = (
        "saved",
        "policy_id",
        "thresholds",
        "primary_metric",
        "secondary_metrics",
        "is_template",
        "subpolicy_id",
    )
    SAVED_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_METRIC_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_METRICS_FIELD_NUMBER: _ClassVar[int]
    IS_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SUBPOLICY_ID_FIELD_NUMBER: _ClassVar[int]
    saved: bool
    policy_id: str
    thresholds: _containers.RepeatedCompositeFieldContainer[Threshold]
    primary_metric: str
    secondary_metrics: _containers.RepeatedScalarFieldContainer[str]
    is_template: bool
    subpolicy_id: str
    def __init__(
        self,
        saved: _Optional[bool] = ...,
        policy_id: _Optional[str] = ...,
        thresholds: _Optional[_Iterable[_Union[Threshold, _Mapping]]] = ...,
        primary_metric: _Optional[str] = ...,
        secondary_metrics: _Optional[_Iterable[str]] = ...,
        is_template: _Optional[bool] = ...,
        subpolicy_id: _Optional[str] = ...,
    ) -> None: ...

class Asset(_message.Message):
    __slots__ = ("reports", "default_report")
    class Report(_message.Message):
        __slots__ = ("id", "type")
        ID_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        id: str
        type: str
        def __init__(
            self, id: _Optional[str] = ..., type: _Optional[str] = ...
        ) -> None: ...

    REPORTS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REPORT_FIELD_NUMBER: _ClassVar[int]
    reports: _containers.RepeatedCompositeFieldContainer[Asset.Report]
    default_report: Asset.Report
    def __init__(
        self,
        reports: _Optional[_Iterable[_Union[Asset.Report, _Mapping]]] = ...,
        default_report: _Optional[_Union[Asset.Report, _Mapping]] = ...,
    ) -> None: ...

class Threshold(_message.Message):
    __slots__ = (
        "id",
        "activate",
        "severity",
        "conditions",
        "mitigations",
        "notification_channels",
        "threshold_ack_required",
        "enable_tenant_notifications",
        "receive_landlord_notifications",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    MITIGATIONS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_ACK_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    ENABLE_TENANT_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_LANDLORD_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    activate: Activate
    severity: str
    conditions: _containers.RepeatedCompositeFieldContainer[Condition]
    mitigations: _containers.RepeatedCompositeFieldContainer[Mitigation]
    notification_channels: _containers.RepeatedCompositeFieldContainer[
        NotificationChannel
    ]
    threshold_ack_required: bool
    enable_tenant_notifications: bool
    receive_landlord_notifications: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        activate: _Optional[_Union[Activate, _Mapping]] = ...,
        severity: _Optional[str] = ...,
        conditions: _Optional[_Iterable[_Union[Condition, _Mapping]]] = ...,
        mitigations: _Optional[_Iterable[_Union[Mitigation, _Mapping]]] = ...,
        notification_channels: _Optional[
            _Iterable[_Union[NotificationChannel, _Mapping]]
        ] = ...,
        threshold_ack_required: _Optional[bool] = ...,
        enable_tenant_notifications: _Optional[bool] = ...,
        receive_landlord_notifications: _Optional[bool] = ...,
    ) -> None: ...

class Activate(_message.Message):
    __slots__ = ("times", "operator", "time_window_seconds", "grace_period_seconds")
    TIMES_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_SECONDS_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    times: int
    operator: str
    time_window_seconds: int
    grace_period_seconds: int
    def __init__(
        self,
        times: _Optional[int] = ...,
        operator: _Optional[str] = ...,
        time_window_seconds: _Optional[int] = ...,
        grace_period_seconds: _Optional[int] = ...,
    ) -> None: ...

class Condition(_message.Message):
    __slots__ = ("type", "value", "metric", "operator", "value_type", "value_select")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_SELECT_FIELD_NUMBER: _ClassVar[int]
    type: str
    value: str
    metric: str
    operator: str
    value_type: str
    value_select: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        value: _Optional[str] = ...,
        metric: _Optional[str] = ...,
        operator: _Optional[str] = ...,
        value_type: _Optional[str] = ...,
        value_select: _Optional[str] = ...,
    ) -> None: ...

class Mitigation(_message.Message):
    __slots__ = (
        "id",
        "status",
        "company_id",
        "pairing_id",
        "threshold_id",
        "is_method_overridable",
        "mitigation_apply_type",
        "mitigation_clear_type",
        "mitigation_apply_timer",
        "mitigation_clear_timer",
        "is_platform_overridable",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    PAIRING_ID_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_ID_FIELD_NUMBER: _ClassVar[int]
    IS_METHOD_OVERRIDABLE_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_APPLY_TYPE_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_CLEAR_TYPE_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_APPLY_TIMER_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_CLEAR_TIMER_FIELD_NUMBER: _ClassVar[int]
    IS_PLATFORM_OVERRIDABLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    company_id: str
    pairing_id: str
    threshold_id: str
    is_method_overridable: bool
    mitigation_apply_type: str
    mitigation_clear_type: str
    mitigation_apply_timer: int
    mitigation_clear_timer: int
    is_platform_overridable: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        pairing_id: _Optional[str] = ...,
        threshold_id: _Optional[str] = ...,
        is_method_overridable: _Optional[bool] = ...,
        mitigation_apply_type: _Optional[str] = ...,
        mitigation_clear_type: _Optional[str] = ...,
        mitigation_apply_timer: _Optional[int] = ...,
        mitigation_clear_timer: _Optional[int] = ...,
        is_platform_overridable: _Optional[bool] = ...,
    ) -> None: ...

class NotificationChannel(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TenantLink(_message.Message):
    __slots__ = ("id", "pivot_template_id", "pivot_user_group_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PIVOT_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    PIVOT_USER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    pivot_template_id: str
    pivot_user_group_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        pivot_template_id: _Optional[str] = ...,
        pivot_user_group_id: _Optional[str] = ...,
    ) -> None: ...

class Package(_message.Message):
    __slots__ = (
        "id",
        "company_id",
        "name",
        "description",
        "icon",
        "color",
        "alerts",
        "assets",
        "is_default",
        "tenants",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    TENANTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    name: str
    description: str
    icon: str
    color: str
    alerts: _containers.RepeatedCompositeFieldContainer[Alert]
    assets: Asset
    is_default: bool
    tenants: _containers.RepeatedCompositeFieldContainer[TenantLink]
    def __init__(
        self,
        id: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        icon: _Optional[str] = ...,
        color: _Optional[str] = ...,
        alerts: _Optional[_Iterable[_Union[Alert, _Mapping]]] = ...,
        assets: _Optional[_Union[Asset, _Mapping]] = ...,
        is_default: _Optional[bool] = ...,
        tenants: _Optional[_Iterable[_Union[TenantLink, _Mapping]]] = ...,
    ) -> None: ...

class CustomDimension(_message.Message):
    __slots__ = ("dimension", "populator")
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_FIELD_NUMBER: _ClassVar[int]
    dimension: str
    populator: str
    def __init__(
        self, dimension: _Optional[str] = ..., populator: _Optional[str] = ...
    ) -> None: ...

class Devices(_message.Message):
    __slots__ = (
        "all_devices",
        "device_types",
        "device_labels",
        "device_sites",
        "device_name",
    )
    ALL_DEVICES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_LABELS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SITES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    all_devices: bool
    device_types: _containers.RepeatedScalarFieldContainer[str]
    device_labels: _containers.RepeatedScalarFieldContainer[int]
    device_sites: _containers.RepeatedScalarFieldContainer[int]
    device_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        all_devices: _Optional[bool] = ...,
        device_types: _Optional[_Iterable[str]] = ...,
        device_labels: _Optional[_Iterable[int]] = ...,
        device_sites: _Optional[_Iterable[int]] = ...,
        device_name: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class FilterField(_message.Message):
    __slots__ = ("filter_field", "operator", "filter_value")
    FILTER_FIELD_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    FILTER_VALUE_FIELD_NUMBER: _ClassVar[int]
    filter_field: str
    operator: str
    filter_value: str
    def __init__(
        self,
        filter_field: _Optional[str] = ...,
        operator: _Optional[str] = ...,
        filter_value: _Optional[str] = ...,
    ) -> None: ...

class Filter(_message.Message):
    __slots__ = (
        "name",
        "named",
        "connector",
        "auto_added",
        "saved_filters",
        "filters",
        "filter_groups",
        "metric",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMED_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    AUTO_ADDED_FIELD_NUMBER: _ClassVar[int]
    SAVED_FILTERS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    FILTER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    name: str
    named: bool
    connector: str
    auto_added: str
    saved_filters: _containers.RepeatedScalarFieldContainer[str]
    filters: _containers.RepeatedCompositeFieldContainer[FilterField]
    filter_groups: _containers.RepeatedCompositeFieldContainer[Filter]
    metric: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        named: _Optional[bool] = ...,
        connector: _Optional[str] = ...,
        auto_added: _Optional[str] = ...,
        saved_filters: _Optional[_Iterable[str]] = ...,
        filters: _Optional[_Iterable[_Union[FilterField, _Mapping]]] = ...,
        filter_groups: _Optional[_Iterable[_Union[Filter, _Mapping]]] = ...,
        metric: _Optional[_Iterable[str]] = ...,
        **kwargs,
    ) -> None: ...

class TenantUser(_message.Message):
    __slots__ = ("id", "tenant_id", "user_full_name", "user_email")
    ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    tenant_id: str
    user_full_name: str
    user_email: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        tenant_id: _Optional[str] = ...,
        user_full_name: _Optional[str] = ...,
        user_email: _Optional[str] = ...,
    ) -> None: ...

class Tenant(_message.Message):
    __slots__ = (
        "id",
        "company_id",
        "name",
        "description",
        "type",
        "enabled",
        "alerts",
        "assets",
        "asn",
        "cidr",
        "custom_dimensions",
        "devices",
        "filters",
        "interface_name",
        "snmp_alias",
        "packages",
        "users",
        "template_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    CIDR_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    SNMP_ALIAS_FIELD_NUMBER: _ClassVar[int]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    name: str
    description: str
    type: str
    enabled: bool
    alerts: _containers.RepeatedCompositeFieldContainer[Alert]
    assets: Asset
    asn: str
    cidr: str
    custom_dimensions: _containers.RepeatedCompositeFieldContainer[CustomDimension]
    devices: Devices
    filters: Filter
    interface_name: str
    snmp_alias: str
    packages: _containers.RepeatedCompositeFieldContainer[Package]
    users: _containers.RepeatedCompositeFieldContainer[_user_pb2.User]
    template_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        type: _Optional[str] = ...,
        enabled: _Optional[bool] = ...,
        alerts: _Optional[_Iterable[_Union[Alert, _Mapping]]] = ...,
        assets: _Optional[_Union[Asset, _Mapping]] = ...,
        asn: _Optional[str] = ...,
        cidr: _Optional[str] = ...,
        custom_dimensions: _Optional[
            _Iterable[_Union[CustomDimension, _Mapping]]
        ] = ...,
        devices: _Optional[_Union[Devices, _Mapping]] = ...,
        filters: _Optional[_Union[Filter, _Mapping]] = ...,
        interface_name: _Optional[str] = ...,
        snmp_alias: _Optional[str] = ...,
        packages: _Optional[_Iterable[_Union[Package, _Mapping]]] = ...,
        users: _Optional[_Iterable[_Union[_user_pb2.User, _Mapping]]] = ...,
        template_id: _Optional[str] = ...,
    ) -> None: ...

class ListPackageRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListPackageResponse(_message.Message):
    __slots__ = ("packages", "invalid_count")
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    packages: _containers.RepeatedCompositeFieldContainer[Package]
    invalid_count: int
    def __init__(
        self,
        packages: _Optional[_Iterable[_Union[Package, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetPackageRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPackageResponse(_message.Message):
    __slots__ = ("package",)
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: Package
    def __init__(self, package: _Optional[_Union[Package, _Mapping]] = ...) -> None: ...

class CreatePackageRequest(_message.Message):
    __slots__ = ("package",)
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: Package
    def __init__(self, package: _Optional[_Union[Package, _Mapping]] = ...) -> None: ...

class CreatePackageResponse(_message.Message):
    __slots__ = ("package",)
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: Package
    def __init__(self, package: _Optional[_Union[Package, _Mapping]] = ...) -> None: ...

class UpdatePackageRequest(_message.Message):
    __slots__ = ("package",)
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: Package
    def __init__(self, package: _Optional[_Union[Package, _Mapping]] = ...) -> None: ...

class UpdatePackageResponse(_message.Message):
    __slots__ = ("package",)
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: Package
    def __init__(self, package: _Optional[_Union[Package, _Mapping]] = ...) -> None: ...

class DeletePackageRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePackageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTenantRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTenantResponse(_message.Message):
    __slots__ = ("tenants", "invalid_count")
    TENANTS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    tenants: _containers.RepeatedCompositeFieldContainer[Tenant]
    invalid_count: int
    def __init__(
        self,
        tenants: _Optional[_Iterable[_Union[Tenant, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetTenantRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTenantResponse(_message.Message):
    __slots__ = ("tenant",)
    TENANT_FIELD_NUMBER: _ClassVar[int]
    tenant: Tenant
    def __init__(self, tenant: _Optional[_Union[Tenant, _Mapping]] = ...) -> None: ...

class CreateTenantRequest(_message.Message):
    __slots__ = ("tenant",)
    TENANT_FIELD_NUMBER: _ClassVar[int]
    tenant: Tenant
    def __init__(self, tenant: _Optional[_Union[Tenant, _Mapping]] = ...) -> None: ...

class CreateTenantResponse(_message.Message):
    __slots__ = ("tenant",)
    TENANT_FIELD_NUMBER: _ClassVar[int]
    tenant: Tenant
    def __init__(self, tenant: _Optional[_Union[Tenant, _Mapping]] = ...) -> None: ...

class UpdateTenantRequest(_message.Message):
    __slots__ = ("tenant",)
    TENANT_FIELD_NUMBER: _ClassVar[int]
    tenant: Tenant
    def __init__(self, tenant: _Optional[_Union[Tenant, _Mapping]] = ...) -> None: ...

class UpdateTenantResponse(_message.Message):
    __slots__ = ("tenant",)
    TENANT_FIELD_NUMBER: _ClassVar[int]
    tenant: Tenant
    def __init__(self, tenant: _Optional[_Union[Tenant, _Mapping]] = ...) -> None: ...

class DeleteTenantRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTenantResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTenantUserRequest(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class ListTenantUserResponse(_message.Message):
    __slots__ = ("users", "invalid_count")
    USERS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[TenantUser]
    invalid_count: int
    def __init__(
        self,
        users: _Optional[_Iterable[_Union[TenantUser, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class CreateTenantUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: TenantUser
    def __init__(self, user: _Optional[_Union[TenantUser, _Mapping]] = ...) -> None: ...

class CreateTenantUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: TenantUser
    def __init__(self, user: _Optional[_Union[TenantUser, _Mapping]] = ...) -> None: ...

class UpdateTenantUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: TenantUser
    def __init__(self, user: _Optional[_Union[TenantUser, _Mapping]] = ...) -> None: ...

class UpdateTenantUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: TenantUser
    def __init__(self, user: _Optional[_Union[TenantUser, _Mapping]] = ...) -> None: ...

class DeleteTenantUserRequest(_message.Message):
    __slots__ = ("tenant_id", "id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    id: str
    def __init__(
        self, tenant_id: _Optional[str] = ..., id: _Optional[str] = ...
    ) -> None: ...

class DeleteTenantUserResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
