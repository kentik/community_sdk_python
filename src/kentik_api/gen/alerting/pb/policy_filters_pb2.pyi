from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyFilters(_message.Message):
    __slots__ = ("connector", "filters", "groups", "saved")
    class FilterConnector(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FILTER_CONNECTOR_UNSPECIFIED: _ClassVar[PolicyFilters.FilterConnector]
        FILTER_CONNECTOR_AND: _ClassVar[PolicyFilters.FilterConnector]
        FILTER_CONNECTOR_OR: _ClassVar[PolicyFilters.FilterConnector]

    FILTER_CONNECTOR_UNSPECIFIED: PolicyFilters.FilterConnector
    FILTER_CONNECTOR_AND: PolicyFilters.FilterConnector
    FILTER_CONNECTOR_OR: PolicyFilters.FilterConnector
    class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OPERATOR_UNSPECIFIED: _ClassVar[PolicyFilters.Operator]
        OPERATOR_EQUALS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_NOT_EQUALS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_BITWISE_AND: _ClassVar[PolicyFilters.Operator]
        OPERATOR_BITWISE_OR: _ClassVar[PolicyFilters.Operator]
        OPERATOR_LESS_THAN: _ClassVar[PolicyFilters.Operator]
        OPERATOR_GREATER_THAN: _ClassVar[PolicyFilters.Operator]
        OPERATOR_LESS_THAN_OR_EQUALS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_GREATER_THAN_OR_EQUALS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_NOT_CONTAINS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_CONTAINS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_NOT_CONTAINS_REGULAR_EXP: _ClassVar[PolicyFilters.Operator]
        OPERATOR_CONTAINS_REGULAR_EXP: _ClassVar[PolicyFilters.Operator]
        OPERATOR_NOT_CONTAINS_REGULAR_EXP_STAR: _ClassVar[PolicyFilters.Operator]
        OPERATOR_CONTAINS_REGULAR_EXP_STAR: _ClassVar[PolicyFilters.Operator]
        OPERATOR_BITWISE_ANY: _ClassVar[PolicyFilters.Operator]
        OPERATOR_BITWISE_NONE: _ClassVar[PolicyFilters.Operator]
        OPERATOR_BITWISE_ALL: _ClassVar[PolicyFilters.Operator]
        OPERATOR_BITWISE_NOT_ALL: _ClassVar[PolicyFilters.Operator]
        OPERATOR_EXISTS: _ClassVar[PolicyFilters.Operator]
        OPERATOR_NOT_EXISTS: _ClassVar[PolicyFilters.Operator]

    OPERATOR_UNSPECIFIED: PolicyFilters.Operator
    OPERATOR_EQUALS: PolicyFilters.Operator
    OPERATOR_NOT_EQUALS: PolicyFilters.Operator
    OPERATOR_BITWISE_AND: PolicyFilters.Operator
    OPERATOR_BITWISE_OR: PolicyFilters.Operator
    OPERATOR_LESS_THAN: PolicyFilters.Operator
    OPERATOR_GREATER_THAN: PolicyFilters.Operator
    OPERATOR_LESS_THAN_OR_EQUALS: PolicyFilters.Operator
    OPERATOR_GREATER_THAN_OR_EQUALS: PolicyFilters.Operator
    OPERATOR_NOT_CONTAINS: PolicyFilters.Operator
    OPERATOR_CONTAINS: PolicyFilters.Operator
    OPERATOR_NOT_CONTAINS_REGULAR_EXP: PolicyFilters.Operator
    OPERATOR_CONTAINS_REGULAR_EXP: PolicyFilters.Operator
    OPERATOR_NOT_CONTAINS_REGULAR_EXP_STAR: PolicyFilters.Operator
    OPERATOR_CONTAINS_REGULAR_EXP_STAR: PolicyFilters.Operator
    OPERATOR_BITWISE_ANY: PolicyFilters.Operator
    OPERATOR_BITWISE_NONE: PolicyFilters.Operator
    OPERATOR_BITWISE_ALL: PolicyFilters.Operator
    OPERATOR_BITWISE_NOT_ALL: PolicyFilters.Operator
    OPERATOR_EXISTS: PolicyFilters.Operator
    OPERATOR_NOT_EXISTS: PolicyFilters.Operator
    class FieldFilter(_message.Message):
        __slots__ = ("field", "operator", "value")
        FIELD_FIELD_NUMBER: _ClassVar[int]
        OPERATOR_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        field: str
        operator: PolicyFilters.Operator
        value: str
        def __init__(
            self,
            field: _Optional[str] = ...,
            operator: _Optional[_Union[PolicyFilters.Operator, str]] = ...,
            value: _Optional[str] = ...,
        ) -> None: ...

    class SavedFilter(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        NOT_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ..., **kwargs) -> None: ...

    NOT_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    SAVED_FIELD_NUMBER: _ClassVar[int]
    connector: PolicyFilters.FilterConnector
    filters: _containers.RepeatedCompositeFieldContainer[PolicyFilters.FieldFilter]
    groups: _containers.RepeatedCompositeFieldContainer[PolicyFilters]
    saved: _containers.RepeatedCompositeFieldContainer[PolicyFilters.SavedFilter]
    def __init__(
        self,
        connector: _Optional[_Union[PolicyFilters.FilterConnector, str]] = ...,
        filters: _Optional[
            _Iterable[_Union[PolicyFilters.FieldFilter, _Mapping]]
        ] = ...,
        groups: _Optional[_Iterable[_Union[PolicyFilters, _Mapping]]] = ...,
        saved: _Optional[_Iterable[_Union[PolicyFilters.SavedFilter, _Mapping]]] = ...,
        **kwargs,
    ) -> None: ...

class PolicyDimensionFilters(_message.Message):
    __slots__ = ("conjunctions",)
    class Conjunction(_message.Message):
        __slots__ = ("entries",)
        ENTRIES_FIELD_NUMBER: _ClassVar[int]
        entries: _containers.RepeatedCompositeFieldContainer[
            PolicyDimensionFilters.Entry
        ]
        def __init__(
            self,
            entries: _Optional[
                _Iterable[_Union[PolicyDimensionFilters.Entry, _Mapping]]
            ] = ...,
        ) -> None: ...

    class Entry(_message.Message):
        __slots__ = ("dimension", "equals_any", "matches_any")
        class StringArray(_message.Message):
            __slots__ = ("values",)
            VALUES_FIELD_NUMBER: _ClassVar[int]
            values: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

        NOT_FIELD_NUMBER: _ClassVar[int]
        DIMENSION_FIELD_NUMBER: _ClassVar[int]
        EQUALS_ANY_FIELD_NUMBER: _ClassVar[int]
        MATCHES_ANY_FIELD_NUMBER: _ClassVar[int]
        dimension: str
        equals_any: PolicyDimensionFilters.Entry.StringArray
        matches_any: PolicyDimensionFilters.Entry.StringArray
        def __init__(
            self,
            dimension: _Optional[str] = ...,
            equals_any: _Optional[
                _Union[PolicyDimensionFilters.Entry.StringArray, _Mapping]
            ] = ...,
            matches_any: _Optional[
                _Union[PolicyDimensionFilters.Entry.StringArray, _Mapping]
            ] = ...,
            **kwargs,
        ) -> None: ...

    CONJUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    conjunctions: _containers.RepeatedCompositeFieldContainer[
        PolicyDimensionFilters.Conjunction
    ]
    def __init__(
        self,
        conjunctions: _Optional[
            _Iterable[_Union[PolicyDimensionFilters.Conjunction, _Mapping]]
        ] = ...,
    ) -> None: ...
