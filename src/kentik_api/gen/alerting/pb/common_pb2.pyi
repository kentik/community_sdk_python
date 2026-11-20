from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POLICY_TYPE_UNSPECIFIED: _ClassVar[PolicyType]
    POLICY_TYPE_AGENT: _ClassVar[PolicyType]
    POLICY_TYPE_COMPONENT: _ClassVar[PolicyType]
    POLICY_TYPE_DEVICE: _ClassVar[PolicyType]
    POLICY_TYPE_EVENT: _ClassVar[PolicyType]
    POLICY_TYPE_INTERFACE: _ClassVar[PolicyType]
    POLICY_TYPE_CUSTOM: _ClassVar[PolicyType]
    POLICY_TYPE_CLOUD: _ClassVar[PolicyType]
    POLICY_TYPE_PROTECT: _ClassVar[PolicyType]
    POLICY_TYPE_TRAFFIC: _ClassVar[PolicyType]
    POLICY_TYPE_KMETRICS: _ClassVar[PolicyType]

class ActivationMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVATION_MODE_UNSPECIFIED: _ClassVar[ActivationMode]
    ACTIVATION_MODE_ROLLING_WINDOW: _ClassVar[ActivationMode]
    ACTIVATION_MODE_TOGGLE: _ClassVar[ActivationMode]

class AggregationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGGREGATION_TYPE_UNSPECIFIED: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P05: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P10: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P25: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P50: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P75: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P80: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P90: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P95: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P98: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_P99: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_MAX: _ClassVar[AggregationType]
    AGGREGATION_TYPE_REL_MIN: _ClassVar[AggregationType]

class MitigationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MITIGATION_TYPE_UNSPECIFIED: _ClassVar[MitigationType]
    MITIGATION_TYPE_MANUAL: _ClassVar[MitigationType]
    MITIGATION_TYPE_AUTO: _ClassVar[MitigationType]

class MitigationPlatformType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MITIGATION_PLATFORM_TYPE_UNSPECIFIED: _ClassVar[MitigationPlatformType]
    MITIGATION_PLATFORM_TYPE_A10: _ClassVar[MitigationPlatformType]
    MITIGATION_PLATFORM_TYPE_FLOWSPEC: _ClassVar[MitigationPlatformType]
    MITIGATION_PLATFORM_TYPE_RADWARE: _ClassVar[MitigationPlatformType]
    MITIGATION_PLATFORM_TYPE_RTBH: _ClassVar[MitigationPlatformType]
    MITIGATION_PLATFORM_TYPE_CFMT: _ClassVar[MitigationPlatformType]
    MITIGATION_PLATFORM_TYPE_ADAPTIVE_FLOWSPEC: _ClassVar[MitigationPlatformType]

POLICY_TYPE_UNSPECIFIED: PolicyType
POLICY_TYPE_AGENT: PolicyType
POLICY_TYPE_COMPONENT: PolicyType
POLICY_TYPE_DEVICE: PolicyType
POLICY_TYPE_EVENT: PolicyType
POLICY_TYPE_INTERFACE: PolicyType
POLICY_TYPE_CUSTOM: PolicyType
POLICY_TYPE_CLOUD: PolicyType
POLICY_TYPE_PROTECT: PolicyType
POLICY_TYPE_TRAFFIC: PolicyType
POLICY_TYPE_KMETRICS: PolicyType
ACTIVATION_MODE_UNSPECIFIED: ActivationMode
ACTIVATION_MODE_ROLLING_WINDOW: ActivationMode
ACTIVATION_MODE_TOGGLE: ActivationMode
AGGREGATION_TYPE_UNSPECIFIED: AggregationType
AGGREGATION_TYPE_REL_P05: AggregationType
AGGREGATION_TYPE_REL_P10: AggregationType
AGGREGATION_TYPE_REL_P25: AggregationType
AGGREGATION_TYPE_REL_P50: AggregationType
AGGREGATION_TYPE_REL_P75: AggregationType
AGGREGATION_TYPE_REL_P80: AggregationType
AGGREGATION_TYPE_REL_P90: AggregationType
AGGREGATION_TYPE_REL_P95: AggregationType
AGGREGATION_TYPE_REL_P98: AggregationType
AGGREGATION_TYPE_REL_P99: AggregationType
AGGREGATION_TYPE_REL_MAX: AggregationType
AGGREGATION_TYPE_REL_MIN: AggregationType
MITIGATION_TYPE_UNSPECIFIED: MitigationType
MITIGATION_TYPE_MANUAL: MitigationType
MITIGATION_TYPE_AUTO: MitigationType
MITIGATION_PLATFORM_TYPE_UNSPECIFIED: MitigationPlatformType
MITIGATION_PLATFORM_TYPE_A10: MitigationPlatformType
MITIGATION_PLATFORM_TYPE_FLOWSPEC: MitigationPlatformType
MITIGATION_PLATFORM_TYPE_RADWARE: MitigationPlatformType
MITIGATION_PLATFORM_TYPE_RTBH: MitigationPlatformType
MITIGATION_PLATFORM_TYPE_CFMT: MitigationPlatformType
MITIGATION_PLATFORM_TYPE_ADAPTIVE_FLOWSPEC: MitigationPlatformType

class Source(_message.Message):
    __slots__ = ("policy_type", "id")
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    policy_type: PolicyType
    id: str
    def __init__(
        self,
        policy_type: _Optional[_Union[PolicyType, str]] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class NotificationChannelAssociation(_message.Message):
    __slots__ = ("channel_id",)
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    def __init__(self, channel_id: _Optional[str] = ...) -> None: ...
