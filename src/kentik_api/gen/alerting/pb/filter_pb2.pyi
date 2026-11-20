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

class NetworkScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NETWORK_SCOPE_UNSPECIFIED: _ClassVar[NetworkScope]
    NETWORK_SCOPE_ANY: _ClassVar[NetworkScope]
    NETWORK_SCOPE_ROOT: _ClassVar[NetworkScope]
    NETWORK_SCOPE_SOURCE: _ClassVar[NetworkScope]
    NETWORK_SCOPE_DESTINATION: _ClassVar[NetworkScope]
    NETWORK_SCOPE_ADJACENT: _ClassVar[NetworkScope]

NETWORK_SCOPE_UNSPECIFIED: NetworkScope
NETWORK_SCOPE_ANY: NetworkScope
NETWORK_SCOPE_ROOT: NetworkScope
NETWORK_SCOPE_SOURCE: NetworkScope
NETWORK_SCOPE_DESTINATION: NetworkScope
NETWORK_SCOPE_ADJACENT: NetworkScope

class ContextFilter(_message.Message):
    __slots__ = ("conjunctions",)
    class Conjunction(_message.Message):
        __slots__ = ("clauses", "producer_predicates")
        CLAUSES_FIELD_NUMBER: _ClassVar[int]
        PRODUCER_PREDICATES_FIELD_NUMBER: _ClassVar[int]
        clauses: _containers.RepeatedCompositeFieldContainer[ScopedClause]
        producer_predicates: ProducerPredicates
        def __init__(
            self,
            clauses: _Optional[_Iterable[_Union[ScopedClause, _Mapping]]] = ...,
            producer_predicates: _Optional[_Union[ProducerPredicates, _Mapping]] = ...,
        ) -> None: ...

    CONJUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    conjunctions: _containers.RepeatedCompositeFieldContainer[ContextFilter.Conjunction]
    def __init__(
        self,
        conjunctions: _Optional[
            _Iterable[_Union[ContextFilter.Conjunction, _Mapping]]
        ] = ...,
    ) -> None: ...

class ScopedClause(_message.Message):
    __slots__ = ("network_scope", "predicates")
    NETWORK_SCOPE_FIELD_NUMBER: _ClassVar[int]
    PREDICATES_FIELD_NUMBER: _ClassVar[int]
    network_scope: _containers.RepeatedScalarFieldContainer[NetworkScope]
    predicates: SubjectPredicates
    def __init__(
        self,
        network_scope: _Optional[_Iterable[_Union[NetworkScope, str]]] = ...,
        predicates: _Optional[_Union[SubjectPredicates, _Mapping]] = ...,
    ) -> None: ...

class ProducerPredicates(_message.Message):
    __slots__ = ("origin_id", "origin_name", "origin_labels")
    ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_LABELS_FIELD_NUMBER: _ClassVar[int]
    origin_id: IdentityPredicate
    origin_name: StringPredicate
    origin_labels: LabelPredicate
    def __init__(
        self,
        origin_id: _Optional[_Union[IdentityPredicate, _Mapping]] = ...,
        origin_name: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        origin_labels: _Optional[_Union[LabelPredicate, _Mapping]] = ...,
    ) -> None: ...

class SubjectPredicates(_message.Message):
    __slots__ = (
        "device_id",
        "device_name",
        "device_labels",
        "site_id",
        "site_name",
        "interface_id",
        "interface_index",
        "interface_name",
        "interface_description",
        "ip_address",
        "mac_address",
    )
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_LABELS_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_INDEX_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    device_id: IdentityPredicate
    device_name: StringPredicate
    device_labels: LabelPredicate
    site_id: IdentityPredicate
    site_name: StringPredicate
    interface_id: IdentityPredicate
    interface_index: StringPredicate
    interface_name: StringPredicate
    interface_description: StringPredicate
    ip_address: IpPredicate
    mac_address: StringPredicate
    def __init__(
        self,
        device_id: _Optional[_Union[IdentityPredicate, _Mapping]] = ...,
        device_name: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        device_labels: _Optional[_Union[LabelPredicate, _Mapping]] = ...,
        site_id: _Optional[_Union[IdentityPredicate, _Mapping]] = ...,
        site_name: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        interface_id: _Optional[_Union[IdentityPredicate, _Mapping]] = ...,
        interface_index: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        interface_name: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        interface_description: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        ip_address: _Optional[_Union[IpPredicate, _Mapping]] = ...,
        mac_address: _Optional[_Union[StringPredicate, _Mapping]] = ...,
    ) -> None: ...

class IdentityPredicate(_message.Message):
    __slots__ = ("equals",)
    class IdentityList(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

    NOT_FIELD_NUMBER: _ClassVar[int]
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    equals: str
    def __init__(self, equals: _Optional[str] = ..., **kwargs) -> None: ...

class StringPredicate(_message.Message):
    __slots__ = ("equals", "contains", "starts_with", "ends_with", "matches_regex")
    class StringList(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

    NOT_FIELD_NUMBER: _ClassVar[int]
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_FIELD_NUMBER: _ClassVar[int]
    STARTS_WITH_FIELD_NUMBER: _ClassVar[int]
    ENDS_WITH_FIELD_NUMBER: _ClassVar[int]
    MATCHES_REGEX_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    equals: str
    contains: str
    starts_with: str
    ends_with: str
    matches_regex: str
    def __init__(
        self,
        equals: _Optional[str] = ...,
        contains: _Optional[str] = ...,
        starts_with: _Optional[str] = ...,
        ends_with: _Optional[str] = ...,
        matches_regex: _Optional[str] = ...,
        **kwargs,
    ) -> None: ...

class LabelPredicate(_message.Message):
    __slots__ = ("equals", "contains_all")
    class StringList(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

    NOT_FIELD_NUMBER: _ClassVar[int]
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_ALL_FIELD_NUMBER: _ClassVar[int]
    equals: str
    contains_all: LabelPredicate.StringList
    def __init__(
        self,
        equals: _Optional[str] = ...,
        contains_all: _Optional[_Union[LabelPredicate.StringList, _Mapping]] = ...,
        **kwargs,
    ) -> None: ...

class TagPredicate(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: StringPredicate
    value: StringPredicate
    def __init__(
        self,
        key: _Optional[_Union[StringPredicate, _Mapping]] = ...,
        value: _Optional[_Union[StringPredicate, _Mapping]] = ...,
    ) -> None: ...

class IpPredicate(_message.Message):
    __slots__ = ("equals", "within", "within_any")
    class StringList(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

    NOT_FIELD_NUMBER: _ClassVar[int]
    EQUALS_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    WITHIN_FIELD_NUMBER: _ClassVar[int]
    WITHIN_ANY_FIELD_NUMBER: _ClassVar[int]
    equals: str
    within: str
    within_any: IpPredicate.StringList
    def __init__(
        self,
        equals: _Optional[str] = ...,
        within: _Optional[str] = ...,
        within_any: _Optional[_Union[IpPredicate.StringList, _Mapping]] = ...,
        **kwargs,
    ) -> None: ...
