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

class FilterField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILTER_FIELD_UNSPECIFIED: _ClassVar[FilterField]
    FILTER_FIELD_DST_AS: _ClassVar[FilterField]
    FILTER_FIELD_DST_NEXTHOP_AS: _ClassVar[FilterField]
    FILTER_FIELD_DST_SECOND_ASN: _ClassVar[FilterField]
    FILTER_FIELD_DST_THIRD_ASN: _ClassVar[FilterField]
    FILTER_FIELD_DST_BGP_ASPATH: _ClassVar[FilterField]
    FILTER_FIELD_DST_BGP_COMMUNITY: _ClassVar[FilterField]
    FILTER_FIELD_DST_ETH_MAC: _ClassVar[FilterField]
    FILTER_FIELD_DST_FLOW_TAGS: _ClassVar[FilterField]
    FILTER_FIELD_DST_GEO: _ClassVar[FilterField]
    FILTER_FIELD_DST_GEO_REGION: _ClassVar[FilterField]
    FILTER_FIELD_DST_GEO_CITY: _ClassVar[FilterField]
    FILTER_FIELD_DST_ROUTE_LENGTH: _ClassVar[FilterField]
    FILTER_FIELD_INET_DST_ADDR: _ClassVar[FilterField]
    FILTER_FIELD_IPV4_DST_ROUTE_PREFIX: _ClassVar[FilterField]
    FILTER_FIELD_IPV4_DST_NEXT_HOP: _ClassVar[FilterField]
    FILTER_FIELD_L4_DST_PORT: _ClassVar[FilterField]
    FILTER_FIELD_OUTPUT_PORT: _ClassVar[FilterField]
    FILTER_FIELD_I_OUTPUT_SNMP_ALIAS: _ClassVar[FilterField]
    FILTER_FIELD_I_OUTPUT_INTERFACE_DESCRIPTION: _ClassVar[FilterField]
    FILTER_FIELD_SRC_AS: _ClassVar[FilterField]
    FILTER_FIELD_SRC_NEXTHOP_AS: _ClassVar[FilterField]
    FILTER_FIELD_SRC_SECOND_ASN: _ClassVar[FilterField]
    FILTER_FIELD_SRC_THIRD_ASN: _ClassVar[FilterField]
    FILTER_FIELD_SRC_BGP_ASPATH: _ClassVar[FilterField]
    FILTER_FIELD_SRC_BGP_COMMUNITY: _ClassVar[FilterField]
    FILTER_FIELD_SRC_ETH_MAC: _ClassVar[FilterField]
    FILTER_FIELD_SRC_FLOW_TAGS: _ClassVar[FilterField]
    FILTER_FIELD_SRC_GEO: _ClassVar[FilterField]
    FILTER_FIELD_SRC_GEO_REGION: _ClassVar[FilterField]
    FILTER_FIELD_SRC_GEO_CITY: _ClassVar[FilterField]
    FILTER_FIELD_SRC_ROUTE_LENGTH: _ClassVar[FilterField]
    FILTER_FIELD_INET_SRC_ADDR: _ClassVar[FilterField]
    FILTER_FIELD_IPV4_SRC_ROUTE_PREFIX: _ClassVar[FilterField]
    FILTER_FIELD_IPV4_SRC_NEXT_HOP: _ClassVar[FilterField]
    FILTER_FIELD_L4_SRC_PORT: _ClassVar[FilterField]
    FILTER_FIELD_INPUT_PORT: _ClassVar[FilterField]
    FILTER_FIELD_I_INPUT_SNMP_ALIAS: _ClassVar[FilterField]
    FILTER_FIELD_I_INPUT_INTERFACE_DESCRIPTION: _ClassVar[FilterField]
    FILTER_FIELD_BOTH_PKTS: _ClassVar[FilterField]
    FILTER_FIELD_I_DEVICE_NAME: _ClassVar[FilterField]
    FILTER_FIELD_PROTOCOL: _ClassVar[FilterField]
    FILTER_FIELD_TCP_FLAGS: _ClassVar[FilterField]
    FILTER_FIELD_TCP_FLAGS_RAW: _ClassVar[FilterField]
    FILTER_FIELD_TCP_RETRANSMIT: _ClassVar[FilterField]
    FILTER_FIELD_TOS: _ClassVar[FilterField]
    FILTER_FIELD_VLAN_IN: _ClassVar[FilterField]
    FILTER_FIELD_VLAN_OUT: _ClassVar[FilterField]

class FilterOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILTER_OPERATOR_UNSPECIFIED: _ClassVar[FilterOperator]
    FILTER_OPERATOR_EQUAL: _ClassVar[FilterOperator]
    FILTER_OPERATOR_NOT_EQUAL: _ClassVar[FilterOperator]
    FILTER_OPERATOR_CONTAINS: _ClassVar[FilterOperator]
    FILTER_OPERATOR_NOT_CONTAINS: _ClassVar[FilterOperator]
    FILTER_OPERATOR_REGEX_CONTAINS: _ClassVar[FilterOperator]
    FILTER_OPERATOR_REGEX_NOT_CONTAINS: _ClassVar[FilterOperator]
    FILTER_OPERATOR_GREATER_THAN: _ClassVar[FilterOperator]
    FILTER_OPERATOR_LESS_THAN: _ClassVar[FilterOperator]
    FILTER_OPERATOR_BITWISE_AND: _ClassVar[FilterOperator]

class FilterLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILTER_LEVEL_UNSPECIFIED: _ClassVar[FilterLevel]
    FILTER_LEVEL_COMPANY: _ClassVar[FilterLevel]
    FILTER_LEVEL_GLOBAL: _ClassVar[FilterLevel]
    FILTER_LEVEL_USER: _ClassVar[FilterLevel]

FILTER_FIELD_UNSPECIFIED: FilterField
FILTER_FIELD_DST_AS: FilterField
FILTER_FIELD_DST_NEXTHOP_AS: FilterField
FILTER_FIELD_DST_SECOND_ASN: FilterField
FILTER_FIELD_DST_THIRD_ASN: FilterField
FILTER_FIELD_DST_BGP_ASPATH: FilterField
FILTER_FIELD_DST_BGP_COMMUNITY: FilterField
FILTER_FIELD_DST_ETH_MAC: FilterField
FILTER_FIELD_DST_FLOW_TAGS: FilterField
FILTER_FIELD_DST_GEO: FilterField
FILTER_FIELD_DST_GEO_REGION: FilterField
FILTER_FIELD_DST_GEO_CITY: FilterField
FILTER_FIELD_DST_ROUTE_LENGTH: FilterField
FILTER_FIELD_INET_DST_ADDR: FilterField
FILTER_FIELD_IPV4_DST_ROUTE_PREFIX: FilterField
FILTER_FIELD_IPV4_DST_NEXT_HOP: FilterField
FILTER_FIELD_L4_DST_PORT: FilterField
FILTER_FIELD_OUTPUT_PORT: FilterField
FILTER_FIELD_I_OUTPUT_SNMP_ALIAS: FilterField
FILTER_FIELD_I_OUTPUT_INTERFACE_DESCRIPTION: FilterField
FILTER_FIELD_SRC_AS: FilterField
FILTER_FIELD_SRC_NEXTHOP_AS: FilterField
FILTER_FIELD_SRC_SECOND_ASN: FilterField
FILTER_FIELD_SRC_THIRD_ASN: FilterField
FILTER_FIELD_SRC_BGP_ASPATH: FilterField
FILTER_FIELD_SRC_BGP_COMMUNITY: FilterField
FILTER_FIELD_SRC_ETH_MAC: FilterField
FILTER_FIELD_SRC_FLOW_TAGS: FilterField
FILTER_FIELD_SRC_GEO: FilterField
FILTER_FIELD_SRC_GEO_REGION: FilterField
FILTER_FIELD_SRC_GEO_CITY: FilterField
FILTER_FIELD_SRC_ROUTE_LENGTH: FilterField
FILTER_FIELD_INET_SRC_ADDR: FilterField
FILTER_FIELD_IPV4_SRC_ROUTE_PREFIX: FilterField
FILTER_FIELD_IPV4_SRC_NEXT_HOP: FilterField
FILTER_FIELD_L4_SRC_PORT: FilterField
FILTER_FIELD_INPUT_PORT: FilterField
FILTER_FIELD_I_INPUT_SNMP_ALIAS: FilterField
FILTER_FIELD_I_INPUT_INTERFACE_DESCRIPTION: FilterField
FILTER_FIELD_BOTH_PKTS: FilterField
FILTER_FIELD_I_DEVICE_NAME: FilterField
FILTER_FIELD_PROTOCOL: FilterField
FILTER_FIELD_TCP_FLAGS: FilterField
FILTER_FIELD_TCP_FLAGS_RAW: FilterField
FILTER_FIELD_TCP_RETRANSMIT: FilterField
FILTER_FIELD_TOS: FilterField
FILTER_FIELD_VLAN_IN: FilterField
FILTER_FIELD_VLAN_OUT: FilterField
FILTER_OPERATOR_UNSPECIFIED: FilterOperator
FILTER_OPERATOR_EQUAL: FilterOperator
FILTER_OPERATOR_NOT_EQUAL: FilterOperator
FILTER_OPERATOR_CONTAINS: FilterOperator
FILTER_OPERATOR_NOT_CONTAINS: FilterOperator
FILTER_OPERATOR_REGEX_CONTAINS: FilterOperator
FILTER_OPERATOR_REGEX_NOT_CONTAINS: FilterOperator
FILTER_OPERATOR_GREATER_THAN: FilterOperator
FILTER_OPERATOR_LESS_THAN: FilterOperator
FILTER_OPERATOR_BITWISE_AND: FilterOperator
FILTER_LEVEL_UNSPECIFIED: FilterLevel
FILTER_LEVEL_COMPANY: FilterLevel
FILTER_LEVEL_GLOBAL: FilterLevel
FILTER_LEVEL_USER: FilterLevel

class SavedFilterFilter(_message.Message):
    __slots__ = (
        "filter_field",
        "operator",
        "filter_value",
        "filter_field_string",
        "metric",
        "aggregate",
        "right_filter_field",
    )
    FILTER_FIELD_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    FILTER_VALUE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_STRING_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FILTER_FIELD_FIELD_NUMBER: _ClassVar[int]
    filter_field: FilterField
    operator: FilterOperator
    filter_value: str
    filter_field_string: str
    metric: str
    aggregate: str
    right_filter_field: str
    def __init__(
        self,
        filter_field: _Optional[_Union[FilterField, str]] = ...,
        operator: _Optional[_Union[FilterOperator, str]] = ...,
        filter_value: _Optional[str] = ...,
        filter_field_string: _Optional[str] = ...,
        metric: _Optional[str] = ...,
        aggregate: _Optional[str] = ...,
        right_filter_field: _Optional[str] = ...,
    ) -> None: ...

class SavedFilterFilterId(_message.Message):
    __slots__ = ("filter_id", "is_not")
    FILTER_ID_FIELD_NUMBER: _ClassVar[int]
    IS_NOT_FIELD_NUMBER: _ClassVar[int]
    filter_id: str
    is_not: bool
    def __init__(
        self, filter_id: _Optional[str] = ..., is_not: _Optional[bool] = ...
    ) -> None: ...

class SavedFilterFilterGroup(_message.Message):
    __slots__ = ("any", "filters", "saved_filter_ids", "nested_filter_groups")
    ANY_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    SAVED_FILTER_IDS_FIELD_NUMBER: _ClassVar[int]
    NESTED_FILTER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    any: bool
    filters: _containers.RepeatedCompositeFieldContainer[SavedFilterFilter]
    saved_filter_ids: _containers.RepeatedCompositeFieldContainer[SavedFilterFilterId]
    nested_filter_groups: _containers.RepeatedCompositeFieldContainer[
        SavedFilterFilterGroup
    ]
    def __init__(
        self,
        any: _Optional[bool] = ...,
        filters: _Optional[_Iterable[_Union[SavedFilterFilter, _Mapping]]] = ...,
        saved_filter_ids: _Optional[
            _Iterable[_Union[SavedFilterFilterId, _Mapping]]
        ] = ...,
        nested_filter_groups: _Optional[
            _Iterable[_Union[SavedFilterFilterGroup, _Mapping]]
        ] = ...,
        **kwargs,
    ) -> None: ...

class SavedFilterFilters(_message.Message):
    __slots__ = ("any", "filter_groups")
    ANY_FIELD_NUMBER: _ClassVar[int]
    FILTER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    any: bool
    filter_groups: _containers.RepeatedCompositeFieldContainer[SavedFilterFilterGroup]
    def __init__(
        self,
        any: _Optional[bool] = ...,
        filter_groups: _Optional[
            _Iterable[_Union[SavedFilterFilterGroup, _Mapping]]
        ] = ...,
    ) -> None: ...

class SavedFilter(_message.Message):
    __slots__ = (
        "id",
        "filter_name",
        "filter_description",
        "filters",
        "filter_level",
        "created_date",
        "updated_date",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_NAME_FIELD_NUMBER: _ClassVar[int]
    FILTER_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    FILTER_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    filter_name: str
    filter_description: str
    filters: SavedFilterFilters
    filter_level: FilterLevel
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        filter_name: _Optional[str] = ...,
        filter_description: _Optional[str] = ...,
        filters: _Optional[_Union[SavedFilterFilters, _Mapping]] = ...,
        filter_level: _Optional[_Union[FilterLevel, str]] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...
