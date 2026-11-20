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

class SortingConfig(_message.Message):
    __slots__ = ("fields",)
    class Order(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ORDER_UNSPECIFIED: _ClassVar[SortingConfig.Order]
        ORDER_ASCENDING: _ClassVar[SortingConfig.Order]
        ORDER_DESCENDING: _ClassVar[SortingConfig.Order]

    ORDER_UNSPECIFIED: SortingConfig.Order
    ORDER_ASCENDING: SortingConfig.Order
    ORDER_DESCENDING: SortingConfig.Order
    class Field(_message.Message):
        __slots__ = ("by", "order")
        class By(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            BY_UNSPECIFIED: _ClassVar[SortingConfig.Field.By]
            BY_ID: _ClassVar[SortingConfig.Field.By]
            BY_NAME: _ClassVar[SortingConfig.Field.By]
            BY_CREATED_AT: _ClassVar[SortingConfig.Field.By]
            BY_UPDATED_AT: _ClassVar[SortingConfig.Field.By]
            BY_SEVERITY: _ClassVar[SortingConfig.Field.By]
            BY_STATUS: _ClassVar[SortingConfig.Field.By]
            BY_POLICY_TYPE: _ClassVar[SortingConfig.Field.By]
            BY_START_TIME: _ClassVar[SortingConfig.Field.By]
            BY_END_TIME: _ClassVar[SortingConfig.Field.By]
            BY_ALARM_STATE: _ClassVar[SortingConfig.Field.By]
            BY_ALARM_POLICY_NAME: _ClassVar[SortingConfig.Field.By]
            BY_ALARM_PRIMARY_DIMENSION: _ClassVar[SortingConfig.Field.By]

        BY_UNSPECIFIED: SortingConfig.Field.By
        BY_ID: SortingConfig.Field.By
        BY_NAME: SortingConfig.Field.By
        BY_CREATED_AT: SortingConfig.Field.By
        BY_UPDATED_AT: SortingConfig.Field.By
        BY_SEVERITY: SortingConfig.Field.By
        BY_STATUS: SortingConfig.Field.By
        BY_POLICY_TYPE: SortingConfig.Field.By
        BY_START_TIME: SortingConfig.Field.By
        BY_END_TIME: SortingConfig.Field.By
        BY_ALARM_STATE: SortingConfig.Field.By
        BY_ALARM_POLICY_NAME: SortingConfig.Field.By
        BY_ALARM_PRIMARY_DIMENSION: SortingConfig.Field.By
        BY_FIELD_NUMBER: _ClassVar[int]
        ORDER_FIELD_NUMBER: _ClassVar[int]
        by: SortingConfig.Field.By
        order: SortingConfig.Order
        def __init__(
            self,
            by: _Optional[_Union[SortingConfig.Field.By, str]] = ...,
            order: _Optional[_Union[SortingConfig.Order, str]] = ...,
        ) -> None: ...

    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[SortingConfig.Field]
    def __init__(
        self, fields: _Optional[_Iterable[_Union[SortingConfig.Field, _Mapping]]] = ...
    ) -> None: ...
