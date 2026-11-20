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

class NmsConditionConnector(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NMS_CONDITION_CONNECTOR_UNSPECIFIED: _ClassVar[NmsConditionConnector]
    NMS_CONDITION_CONNECTOR_ANY: _ClassVar[NmsConditionConnector]
    NMS_CONDITION_CONNECTOR_ALL: _ClassVar[NmsConditionConnector]

class NmsConditionOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NMS_CONDITION_OPERATOR_UNSPECIFIED: _ClassVar[NmsConditionOperator]
    NMS_CONDITION_OPERATOR_EQUALS: _ClassVar[NmsConditionOperator]
    NMS_CONDITION_OPERATOR_LESS_THAN: _ClassVar[NmsConditionOperator]
    NMS_CONDITION_OPERATOR_GREATER_THAN: _ClassVar[NmsConditionOperator]
    NMS_CONDITION_OPERATOR_LESS_THAN_OR_EQUALS: _ClassVar[NmsConditionOperator]
    NMS_CONDITION_OPERATOR_GREATER_THAN_OR_EQUALS: _ClassVar[NmsConditionOperator]

NMS_CONDITION_CONNECTOR_UNSPECIFIED: NmsConditionConnector
NMS_CONDITION_CONNECTOR_ANY: NmsConditionConnector
NMS_CONDITION_CONNECTOR_ALL: NmsConditionConnector
NMS_CONDITION_OPERATOR_UNSPECIFIED: NmsConditionOperator
NMS_CONDITION_OPERATOR_EQUALS: NmsConditionOperator
NMS_CONDITION_OPERATOR_LESS_THAN: NmsConditionOperator
NMS_CONDITION_OPERATOR_GREATER_THAN: NmsConditionOperator
NMS_CONDITION_OPERATOR_LESS_THAN_OR_EQUALS: NmsConditionOperator
NMS_CONDITION_OPERATOR_GREATER_THAN_OR_EQUALS: NmsConditionOperator

class NmsStateSet(_message.Message):
    __slots__ = ("states",)
    NOT_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, states: _Optional[_Iterable[str]] = ..., **kwargs) -> None: ...

class NmsCondition(_message.Message):
    __slots__ = (
        "measurement",
        "metric",
        "threshold",
        "state_change",
        "state_in_condition",
    )
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    STATE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    STATE_IN_CONDITION_FIELD_NUMBER: _ClassVar[int]
    measurement: str
    metric: str
    threshold: NmsThresholdCondition
    state_change: NmsStateChangeCondition
    state_in_condition: NmsStateSet
    def __init__(
        self,
        measurement: _Optional[str] = ...,
        metric: _Optional[str] = ...,
        threshold: _Optional[_Union[NmsThresholdCondition, _Mapping]] = ...,
        state_change: _Optional[_Union[NmsStateChangeCondition, _Mapping]] = ...,
        state_in_condition: _Optional[_Union[NmsStateSet, _Mapping]] = ...,
    ) -> None: ...

class NmsThresholdCondition(_message.Message):
    __slots__ = ("operator", "condition_value")
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    CONDITION_VALUE_FIELD_NUMBER: _ClassVar[int]
    operator: NmsConditionOperator
    condition_value: str
    def __init__(
        self,
        operator: _Optional[_Union[NmsConditionOperator, str]] = ...,
        condition_value: _Optional[str] = ...,
    ) -> None: ...

class NmsStateChangeCondition(_message.Message):
    __slots__ = ("to",)
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    to: NmsStateSet
    def __init__(
        self, to: _Optional[_Union[NmsStateSet, _Mapping]] = ..., **kwargs
    ) -> None: ...

class NmsConditionGroup(_message.Message):
    __slots__ = ("connector", "conditions", "condition_groups")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    CONDITION_GROUPS_FIELD_NUMBER: _ClassVar[int]
    connector: NmsConditionConnector
    conditions: _containers.RepeatedCompositeFieldContainer[NmsCondition]
    condition_groups: _containers.RepeatedCompositeFieldContainer[NmsConditionGroup]
    def __init__(
        self,
        connector: _Optional[_Union[NmsConditionConnector, str]] = ...,
        conditions: _Optional[_Iterable[_Union[NmsCondition, _Mapping]]] = ...,
        condition_groups: _Optional[
            _Iterable[_Union[NmsConditionGroup, _Mapping]]
        ] = ...,
        **kwargs,
    ) -> None: ...

class NmsActivateOrClearConditions(_message.Message):
    __slots__ = ("connector", "condition_groups")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    CONDITION_GROUPS_FIELD_NUMBER: _ClassVar[int]
    connector: NmsConditionConnector
    condition_groups: _containers.RepeatedCompositeFieldContainer[NmsConditionGroup]
    def __init__(
        self,
        connector: _Optional[_Union[NmsConditionConnector, str]] = ...,
        condition_groups: _Optional[
            _Iterable[_Union[NmsConditionGroup, _Mapping]]
        ] = ...,
    ) -> None: ...
