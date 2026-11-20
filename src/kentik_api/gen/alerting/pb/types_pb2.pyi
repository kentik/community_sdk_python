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

class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SEVERITY_UNSPECIFIED: _ClassVar[Severity]
    SEVERITY_CLEAR: _ClassVar[Severity]
    SEVERITY_MINOR: _ClassVar[Severity]
    SEVERITY_WARNING: _ClassVar[Severity]
    SEVERITY_MAJOR: _ClassVar[Severity]
    SEVERITY_SEVERE: _ClassVar[Severity]
    SEVERITY_CRITICAL: _ClassVar[Severity]

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ORDER_UNSPECIFIED: _ClassVar[SortOrder]
    SORT_ORDER_ASCENDING: _ClassVar[SortOrder]
    SORT_ORDER_DESCENDING: _ClassVar[SortOrder]

SEVERITY_UNSPECIFIED: Severity
SEVERITY_CLEAR: Severity
SEVERITY_MINOR: Severity
SEVERITY_WARNING: Severity
SEVERITY_MAJOR: Severity
SEVERITY_SEVERE: Severity
SEVERITY_CRITICAL: Severity
SORT_ORDER_UNSPECIFIED: SortOrder
SORT_ORDER_ASCENDING: SortOrder
SORT_ORDER_DESCENDING: SortOrder

class MultiAttributeFilter(_message.Message):
    __slots__ = ("filter", "filters", "strict")
    class FilterEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AttributeFilter
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[AttributeFilter, _Mapping]] = ...,
        ) -> None: ...

    FILTER_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    filter: _containers.MessageMap[str, AttributeFilter]
    filters: _containers.RepeatedCompositeFieldContainer[KeyValueFilter]
    strict: bool
    def __init__(
        self,
        filter: _Optional[_Mapping[str, AttributeFilter]] = ...,
        filters: _Optional[_Iterable[_Union[KeyValueFilter, _Mapping]]] = ...,
        strict: _Optional[bool] = ...,
    ) -> None: ...

class AttributeFilter(_message.Message):
    __slots__ = (
        "empty",
        "equals",
        "starts_with",
        "ends_with",
        "contains",
        "matches_regex",
        "any",
    )
    class StringArray(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

    NOT_FIELD_NUMBER: _ClassVar[int]
    EMPTY_FIELD_NUMBER: _ClassVar[int]
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    STARTS_WITH_FIELD_NUMBER: _ClassVar[int]
    ENDS_WITH_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    MATCHES_REGEX_FIELD_NUMBER: _ClassVar[int]
    ANY_FIELD_NUMBER: _ClassVar[int]
    empty: bool
    equals: str
    starts_with: str
    ends_with: str
    contains: str
    matches_regex: str
    any: bool
    def __init__(
        self,
        empty: _Optional[bool] = ...,
        equals: _Optional[str] = ...,
        starts_with: _Optional[str] = ...,
        ends_with: _Optional[str] = ...,
        contains: _Optional[str] = ...,
        matches_regex: _Optional[str] = ...,
        any: _Optional[bool] = ...,
        **kwargs,
    ) -> None: ...

class SimpleAttributeFilter(_message.Message):
    __slots__ = (
        "equals",
        "starts_with",
        "ends_with",
        "contains",
        "matches_regex",
        "any",
    )
    class StringArray(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

    EQUALS_FIELD_NUMBER: _ClassVar[int]
    STARTS_WITH_FIELD_NUMBER: _ClassVar[int]
    ENDS_WITH_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    MATCHES_REGEX_FIELD_NUMBER: _ClassVar[int]
    ANY_FIELD_NUMBER: _ClassVar[int]
    equals: str
    starts_with: str
    ends_with: str
    contains: str
    matches_regex: str
    any: bool
    def __init__(
        self,
        equals: _Optional[str] = ...,
        starts_with: _Optional[str] = ...,
        ends_with: _Optional[str] = ...,
        contains: _Optional[str] = ...,
        matches_regex: _Optional[str] = ...,
        any: _Optional[bool] = ...,
        **kwargs,
    ) -> None: ...

class KeyValueFilter(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: SimpleAttributeFilter
    value: AttributeFilter
    def __init__(
        self,
        key: _Optional[_Union[SimpleAttributeFilter, _Mapping]] = ...,
        value: _Optional[_Union[AttributeFilter, _Mapping]] = ...,
    ) -> None: ...

class PaginationConfig(_message.Message):
    __slots__ = ("limit", "offset", "include_total_count")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    include_total_count: bool
    def __init__(
        self,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        include_total_count: _Optional[bool] = ...,
    ) -> None: ...

class PaginationInfo(_message.Message):
    __slots__ = ("total_count", "has_more_results")
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_RESULTS_FIELD_NUMBER: _ClassVar[int]
    total_count: int
    has_more_results: bool
    def __init__(
        self, total_count: _Optional[int] = ..., has_more_results: _Optional[bool] = ...
    ) -> None: ...

class SortingConfig(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[SortingField]
    def __init__(
        self, fields: _Optional[_Iterable[_Union[SortingField, _Mapping]]] = ...
    ) -> None: ...

class SortingField(_message.Message):
    __slots__ = ("name", "order", "values")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    name: str
    order: SortOrder
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        order: _Optional[_Union[SortOrder, str]] = ...,
        values: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class TimeRange(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    def __init__(
        self,
        start: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("value",)
    class ValueEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.ScalarMap[str, str]
    def __init__(self, value: _Optional[_Mapping[str, str]] = ...) -> None: ...
