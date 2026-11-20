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

class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_TYPE_UNSPECIFIED: _ClassVar[ModelType]
    MODEL_TYPE_POPULATORS: _ClassVar[ModelType]
    MODEL_TYPE_TAGS: _ClassVar[ModelType]
    MODEL_TYPE_IP_ADDRESSES: _ClassVar[ModelType]

class LookupField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOOKUP_FIELD_UNSPECIFIED: _ClassVar[LookupField]
    LOOKUP_FIELD_VALUE: _ClassVar[LookupField]

class OrderDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_DIRECTION_UNSPECIFIED: _ClassVar[OrderDirection]
    ORDER_DIRECTION_ASC: _ClassVar[OrderDirection]
    ORDER_DIRECTION_DESC: _ClassVar[OrderDirection]

MODEL_TYPE_UNSPECIFIED: ModelType
MODEL_TYPE_POPULATORS: ModelType
MODEL_TYPE_TAGS: ModelType
MODEL_TYPE_IP_ADDRESSES: ModelType
LOOKUP_FIELD_UNSPECIFIED: LookupField
LOOKUP_FIELD_VALUE: LookupField
ORDER_DIRECTION_UNSPECIFIED: OrderDirection
ORDER_DIRECTION_ASC: OrderDirection
ORDER_DIRECTION_DESC: OrderDirection

class Model(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: ModelType
    def __init__(self, type: _Optional[_Union[ModelType, str]] = ...) -> None: ...

class OrderField(_message.Message):
    __slots__ = ("field", "direction")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    field: LookupField
    direction: OrderDirection
    def __init__(
        self,
        field: _Optional[_Union[LookupField, str]] = ...,
        direction: _Optional[_Union[OrderDirection, str]] = ...,
    ) -> None: ...

class FlowTagSearch(_message.Message):
    __slots__ = (
        "limit",
        "offset",
        "lookup_fields",
        "lookup_values",
        "order_by",
        "field_limit",
    )
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LOOKUP_FIELDS_FIELD_NUMBER: _ClassVar[int]
    LOOKUP_VALUES_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    FIELD_LIMIT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    lookup_fields: _containers.RepeatedScalarFieldContainer[LookupField]
    lookup_values: _containers.RepeatedScalarFieldContainer[str]
    order_by: _containers.RepeatedCompositeFieldContainer[OrderField]
    field_limit: int
    def __init__(
        self,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        lookup_fields: _Optional[_Iterable[_Union[LookupField, str]]] = ...,
        lookup_values: _Optional[_Iterable[str]] = ...,
        order_by: _Optional[_Iterable[_Union[OrderField, _Mapping]]] = ...,
        field_limit: _Optional[int] = ...,
    ) -> None: ...

class AddressInfo(_message.Message):
    __slots__ = ("addresses", "total_count")
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedScalarFieldContainer[str]
    total_count: int
    def __init__(
        self,
        addresses: _Optional[_Iterable[str]] = ...,
        total_count: _Optional[int] = ...,
    ) -> None: ...

class FlowTag(_message.Message):
    __slots__ = (
        "id",
        "name",
        "edited_by",
        "created_by",
        "cdate",
        "edate",
        "ip",
        "port",
        "tcp_flags",
        "protocol",
        "device_name",
        "device_type",
        "site",
        "interface_name",
        "asn",
        "lasthop_as_name",
        "nexthop_asn",
        "nexthop_as_name",
        "nexthop",
        "bgp_aspath",
        "bgp_community",
        "mac",
        "country",
        "vlans",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EDITED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TCP_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    LASTHOP_AS_NAME_FIELD_NUMBER: _ClassVar[int]
    NEXTHOP_ASN_FIELD_NUMBER: _ClassVar[int]
    NEXTHOP_AS_NAME_FIELD_NUMBER: _ClassVar[int]
    NEXTHOP_FIELD_NUMBER: _ClassVar[int]
    BGP_ASPATH_FIELD_NUMBER: _ClassVar[int]
    BGP_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    VLANS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    edited_by: str
    created_by: str
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    ip: AddressInfo
    port: _containers.RepeatedScalarFieldContainer[str]
    tcp_flags: int
    protocol: _containers.RepeatedScalarFieldContainer[int]
    device_name: _containers.RepeatedScalarFieldContainer[str]
    device_type: _containers.RepeatedScalarFieldContainer[str]
    site: _containers.RepeatedScalarFieldContainer[str]
    interface_name: _containers.RepeatedScalarFieldContainer[str]
    asn: _containers.RepeatedScalarFieldContainer[str]
    lasthop_as_name: _containers.RepeatedScalarFieldContainer[str]
    nexthop_asn: _containers.RepeatedScalarFieldContainer[str]
    nexthop_as_name: _containers.RepeatedScalarFieldContainer[str]
    nexthop: _containers.RepeatedScalarFieldContainer[str]
    bgp_aspath: _containers.RepeatedScalarFieldContainer[str]
    bgp_community: _containers.RepeatedScalarFieldContainer[str]
    mac: AddressInfo
    country: _containers.RepeatedScalarFieldContainer[str]
    vlans: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        edited_by: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        ip: _Optional[_Union[AddressInfo, _Mapping]] = ...,
        port: _Optional[_Iterable[str]] = ...,
        tcp_flags: _Optional[int] = ...,
        protocol: _Optional[_Iterable[int]] = ...,
        device_name: _Optional[_Iterable[str]] = ...,
        device_type: _Optional[_Iterable[str]] = ...,
        site: _Optional[_Iterable[str]] = ...,
        interface_name: _Optional[_Iterable[str]] = ...,
        asn: _Optional[_Iterable[str]] = ...,
        lasthop_as_name: _Optional[_Iterable[str]] = ...,
        nexthop_asn: _Optional[_Iterable[str]] = ...,
        nexthop_as_name: _Optional[_Iterable[str]] = ...,
        nexthop: _Optional[_Iterable[str]] = ...,
        bgp_aspath: _Optional[_Iterable[str]] = ...,
        bgp_community: _Optional[_Iterable[str]] = ...,
        mac: _Optional[_Union[AddressInfo, _Mapping]] = ...,
        country: _Optional[_Iterable[str]] = ...,
        vlans: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetFlowTagRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFlowTagResponse(_message.Message):
    __slots__ = ("flow_tag",)
    FLOW_TAG_FIELD_NUMBER: _ClassVar[int]
    flow_tag: FlowTag
    def __init__(
        self, flow_tag: _Optional[_Union[FlowTag, _Mapping]] = ...
    ) -> None: ...

class SearchFlowTagRequest(_message.Message):
    __slots__ = ("search",)
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    search: FlowTagSearch
    def __init__(
        self, search: _Optional[_Union[FlowTagSearch, _Mapping]] = ...
    ) -> None: ...

class SearchFlowTagResponse(_message.Message):
    __slots__ = ("flow_tags", "total_count", "invalid_count")
    FLOW_TAGS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    flow_tags: _containers.RepeatedCompositeFieldContainer[FlowTag]
    total_count: int
    invalid_count: int
    def __init__(
        self,
        flow_tags: _Optional[_Iterable[_Union[FlowTag, _Mapping]]] = ...,
        total_count: _Optional[int] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class CreateFlowTagRequest(_message.Message):
    __slots__ = ("flow_tag",)
    FLOW_TAG_FIELD_NUMBER: _ClassVar[int]
    flow_tag: FlowTag
    def __init__(
        self, flow_tag: _Optional[_Union[FlowTag, _Mapping]] = ...
    ) -> None: ...

class CreateFlowTagResponse(_message.Message):
    __slots__ = ("flow_tag",)
    FLOW_TAG_FIELD_NUMBER: _ClassVar[int]
    flow_tag: FlowTag
    def __init__(
        self, flow_tag: _Optional[_Union[FlowTag, _Mapping]] = ...
    ) -> None: ...

class UpdateFlowTagRequest(_message.Message):
    __slots__ = ("flow_tag",)
    FLOW_TAG_FIELD_NUMBER: _ClassVar[int]
    flow_tag: FlowTag
    def __init__(
        self, flow_tag: _Optional[_Union[FlowTag, _Mapping]] = ...
    ) -> None: ...

class UpdateFlowTagResponse(_message.Message):
    __slots__ = ("flow_tag",)
    FLOW_TAG_FIELD_NUMBER: _ClassVar[int]
    flow_tag: FlowTag
    def __init__(
        self, flow_tag: _Optional[_Union[FlowTag, _Mapping]] = ...
    ) -> None: ...

class DeleteFlowTagRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteFlowTagResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
