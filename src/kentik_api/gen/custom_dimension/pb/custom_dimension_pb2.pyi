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

DESCRIPTOR: _descriptor.FileDescriptor

class CustomDimension(_message.Message):
    __slots__ = (
        "id",
        "name",
        "type",
        "description",
        "populators",
        "company_id",
        "created_date",
        "updated_date",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POPULATORS_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    description: str
    populators: _containers.RepeatedCompositeFieldContainer[Populator]
    company_id: str
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        type: _Optional[str] = ...,
        description: _Optional[str] = ...,
        populators: _Optional[_Iterable[_Union[Populator, _Mapping]]] = ...,
        company_id: _Optional[str] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class Populator(_message.Message):
    __slots__ = (
        "id",
        "value",
        "direction",
        "device_name",
        "device_type",
        "site",
        "interface_name",
        "addr",
        "port",
        "tcp_flags",
        "protocol",
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
        "user",
        "created_date",
        "updated_date",
        "addr_count",
        "mac_count",
        "extended_fields",
    )
    class ExtendedFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ExtendedField
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[ExtendedField, _Mapping]] = ...,
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDR_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TCP_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
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
    USER_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    ADDR_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAC_COUNT_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    value: str
    direction: str
    device_name: _containers.RepeatedScalarFieldContainer[str]
    device_type: _containers.RepeatedScalarFieldContainer[str]
    site: _containers.RepeatedScalarFieldContainer[str]
    interface_name: _containers.RepeatedScalarFieldContainer[str]
    addr: _containers.RepeatedScalarFieldContainer[str]
    port: _containers.RepeatedScalarFieldContainer[int]
    tcp_flags: int
    protocol: _containers.RepeatedScalarFieldContainer[int]
    asn: _containers.RepeatedScalarFieldContainer[int]
    lasthop_as_name: _containers.RepeatedScalarFieldContainer[str]
    nexthop_asn: _containers.RepeatedScalarFieldContainer[int]
    nexthop_as_name: _containers.RepeatedScalarFieldContainer[str]
    nexthop: _containers.RepeatedScalarFieldContainer[str]
    bgp_aspath: _containers.RepeatedScalarFieldContainer[str]
    bgp_community: _containers.RepeatedScalarFieldContainer[str]
    mac: _containers.RepeatedScalarFieldContainer[str]
    country: _containers.RepeatedScalarFieldContainer[str]
    vlans: _containers.RepeatedScalarFieldContainer[str]
    user: str
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    addr_count: int
    mac_count: int
    extended_fields: _containers.MessageMap[str, ExtendedField]
    def __init__(
        self,
        id: _Optional[str] = ...,
        value: _Optional[str] = ...,
        direction: _Optional[str] = ...,
        device_name: _Optional[_Iterable[str]] = ...,
        device_type: _Optional[_Iterable[str]] = ...,
        site: _Optional[_Iterable[str]] = ...,
        interface_name: _Optional[_Iterable[str]] = ...,
        addr: _Optional[_Iterable[str]] = ...,
        port: _Optional[_Iterable[int]] = ...,
        tcp_flags: _Optional[int] = ...,
        protocol: _Optional[_Iterable[int]] = ...,
        asn: _Optional[_Iterable[int]] = ...,
        lasthop_as_name: _Optional[_Iterable[str]] = ...,
        nexthop_asn: _Optional[_Iterable[int]] = ...,
        nexthop_as_name: _Optional[_Iterable[str]] = ...,
        nexthop: _Optional[_Iterable[str]] = ...,
        bgp_aspath: _Optional[_Iterable[str]] = ...,
        bgp_community: _Optional[_Iterable[str]] = ...,
        mac: _Optional[_Iterable[str]] = ...,
        country: _Optional[_Iterable[str]] = ...,
        vlans: _Optional[_Iterable[str]] = ...,
        user: _Optional[str] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        addr_count: _Optional[int] = ...,
        mac_count: _Optional[int] = ...,
        extended_fields: _Optional[_Mapping[str, ExtendedField]] = ...,
    ) -> None: ...

class ExtendedField(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, value: _Optional[_Iterable[str]] = ...) -> None: ...

class ListCustomDimensionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCustomDimensionsResponse(_message.Message):
    __slots__ = ("dimensions",)
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    dimensions: _containers.RepeatedCompositeFieldContainer[CustomDimension]
    def __init__(
        self, dimensions: _Optional[_Iterable[_Union[CustomDimension, _Mapping]]] = ...
    ) -> None: ...

class GetCustomDimensionInfoRequest(_message.Message):
    __slots__ = ("custom_dimension_id",)
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    def __init__(self, custom_dimension_id: _Optional[str] = ...) -> None: ...

class GetCustomDimensionInfoResponse(_message.Message):
    __slots__ = ("dimension",)
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    dimension: CustomDimension
    def __init__(
        self, dimension: _Optional[_Union[CustomDimension, _Mapping]] = ...
    ) -> None: ...

class CreateCustomDimensionRequest(_message.Message):
    __slots__ = ("dimension",)
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    dimension: CustomDimension
    def __init__(
        self, dimension: _Optional[_Union[CustomDimension, _Mapping]] = ...
    ) -> None: ...

class CreateCustomDimensionResponse(_message.Message):
    __slots__ = ("dimension",)
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    dimension: CustomDimension
    def __init__(
        self, dimension: _Optional[_Union[CustomDimension, _Mapping]] = ...
    ) -> None: ...

class UpdateCustomDimensionRequest(_message.Message):
    __slots__ = ("custom_dimension_id", "dimension")
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    dimension: CustomDimension
    def __init__(
        self,
        custom_dimension_id: _Optional[str] = ...,
        dimension: _Optional[_Union[CustomDimension, _Mapping]] = ...,
    ) -> None: ...

class UpdateCustomDimensionResponse(_message.Message):
    __slots__ = ("dimension",)
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    dimension: CustomDimension
    def __init__(
        self, dimension: _Optional[_Union[CustomDimension, _Mapping]] = ...
    ) -> None: ...

class DeleteCustomDimensionRequest(_message.Message):
    __slots__ = ("custom_dimension_id",)
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    def __init__(self, custom_dimension_id: _Optional[str] = ...) -> None: ...

class DeleteCustomDimensionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPopulatorRequest(_message.Message):
    __slots__ = ("custom_dimension_id", "populator_id", "field_limit")
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_LIMIT_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    populator_id: str
    field_limit: int
    def __init__(
        self,
        custom_dimension_id: _Optional[str] = ...,
        populator_id: _Optional[str] = ...,
        field_limit: _Optional[int] = ...,
    ) -> None: ...

class GetPopulatorResponse(_message.Message):
    __slots__ = ("populator",)
    POPULATOR_FIELD_NUMBER: _ClassVar[int]
    populator: Populator
    def __init__(
        self, populator: _Optional[_Union[Populator, _Mapping]] = ...
    ) -> None: ...

class GetPopulatorFieldRequest(_message.Message):
    __slots__ = ("custom_dimension_id", "populator_id", "field_name", "offset", "limit")
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    populator_id: str
    field_name: str
    offset: int
    limit: int
    def __init__(
        self,
        custom_dimension_id: _Optional[str] = ...,
        populator_id: _Optional[str] = ...,
        field_name: _Optional[str] = ...,
        offset: _Optional[int] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class GetPopulatorFieldResponse(_message.Message):
    __slots__ = ("total_count", "offset", "limit", "extended_fields")
    class ExtendedFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ExtendedField
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[ExtendedField, _Mapping]] = ...,
        ) -> None: ...

    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    total_count: int
    offset: int
    limit: int
    extended_fields: _containers.MessageMap[str, ExtendedField]
    def __init__(
        self,
        total_count: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        limit: _Optional[int] = ...,
        extended_fields: _Optional[_Mapping[str, ExtendedField]] = ...,
    ) -> None: ...

class CreatePopulatorRequest(_message.Message):
    __slots__ = ("custom_dimension_id", "populator")
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    populator: Populator
    def __init__(
        self,
        custom_dimension_id: _Optional[str] = ...,
        populator: _Optional[_Union[Populator, _Mapping]] = ...,
    ) -> None: ...

class CreatePopulatorResponse(_message.Message):
    __slots__ = ("populator",)
    POPULATOR_FIELD_NUMBER: _ClassVar[int]
    populator: Populator
    def __init__(
        self, populator: _Optional[_Union[Populator, _Mapping]] = ...
    ) -> None: ...

class UpdatePopulatorRequest(_message.Message):
    __slots__ = ("custom_dimension_id", "populator_id", "populator")
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_ID_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    populator_id: str
    populator: Populator
    def __init__(
        self,
        custom_dimension_id: _Optional[str] = ...,
        populator_id: _Optional[str] = ...,
        populator: _Optional[_Union[Populator, _Mapping]] = ...,
    ) -> None: ...

class UpdatePopulatorResponse(_message.Message):
    __slots__ = ("populator",)
    POPULATOR_FIELD_NUMBER: _ClassVar[int]
    populator: Populator
    def __init__(
        self, populator: _Optional[_Union[Populator, _Mapping]] = ...
    ) -> None: ...

class DeletePopulatorRequest(_message.Message):
    __slots__ = ("custom_dimension_id", "populator_id")
    CUSTOM_DIMENSION_ID_FIELD_NUMBER: _ClassVar[int]
    POPULATOR_ID_FIELD_NUMBER: _ClassVar[int]
    custom_dimension_id: str
    populator_id: str
    def __init__(
        self,
        custom_dimension_id: _Optional[str] = ...,
        populator_id: _Optional[str] = ...,
    ) -> None: ...

class DeletePopulatorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
