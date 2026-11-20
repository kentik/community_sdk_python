import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import nms_common_pb2 as _nms_common_pb2
from . import policy_datasources_pb2 as _policy_datasources_pb2
from . import policy_filters_pb2 as _policy_filters_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class NmsPolicySettings(_message.Message):
    __slots__ = ("dataset", "evaluation")
    class DatasetConfig(_message.Message):
        __slots__ = ("sources", "filters", "measurements", "custom_dimensions")
        SOURCES_FIELD_NUMBER: _ClassVar[int]
        FILTERS_FIELD_NUMBER: _ClassVar[int]
        MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
        CUSTOM_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
        sources: _policy_datasources_pb2.PolicyDataSources
        filters: _policy_filters_pb2.PolicyFilters
        measurements: _containers.RepeatedScalarFieldContainer[str]
        custom_dimensions: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            sources: _Optional[
                _Union[_policy_datasources_pb2.PolicyDataSources, _Mapping]
            ] = ...,
            filters: _Optional[
                _Union[_policy_filters_pb2.PolicyFilters, _Mapping]
            ] = ...,
            measurements: _Optional[_Iterable[str]] = ...,
            custom_dimensions: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class EvaluationConfig(_message.Message):
        __slots__ = ("activation_delay", "clearance_delay")
        ACTIVATION_DELAY_FIELD_NUMBER: _ClassVar[int]
        CLEARANCE_DELAY_FIELD_NUMBER: _ClassVar[int]
        activation_delay: _duration_pb2.Duration
        clearance_delay: _duration_pb2.Duration
        def __init__(
            self,
            activation_delay: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            clearance_delay: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
        ) -> None: ...

    DATASET_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    dataset: NmsPolicySettings.DatasetConfig
    evaluation: NmsPolicySettings.EvaluationConfig
    def __init__(
        self,
        dataset: _Optional[_Union[NmsPolicySettings.DatasetConfig, _Mapping]] = ...,
        evaluation: _Optional[
            _Union[NmsPolicySettings.EvaluationConfig, _Mapping]
        ] = ...,
    ) -> None: ...

class NmsPolicyLevelSettings(_message.Message):
    __slots__ = ("activate", "clear_type", "conditional")
    class ClearType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CLEAR_TYPE_UNSPECIFIED: _ClassVar[NmsPolicyLevelSettings.ClearType]
        CLEAR_TYPE_CLEAR_MANUAL: _ClassVar[NmsPolicyLevelSettings.ClearType]
        CLEAR_TYPE_CLEAR_UNLESS_ACTIVATED: _ClassVar[NmsPolicyLevelSettings.ClearType]

    CLEAR_TYPE_UNSPECIFIED: NmsPolicyLevelSettings.ClearType
    CLEAR_TYPE_CLEAR_MANUAL: NmsPolicyLevelSettings.ClearType
    CLEAR_TYPE_CLEAR_UNLESS_ACTIVATED: NmsPolicyLevelSettings.ClearType
    ACTIVATE_FIELD_NUMBER: _ClassVar[int]
    CLEAR_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONDITIONAL_FIELD_NUMBER: _ClassVar[int]
    activate: _nms_common_pb2.NmsActivateOrClearConditions
    clear_type: NmsPolicyLevelSettings.ClearType
    conditional: _nms_common_pb2.NmsActivateOrClearConditions
    def __init__(
        self,
        activate: _Optional[
            _Union[_nms_common_pb2.NmsActivateOrClearConditions, _Mapping]
        ] = ...,
        clear_type: _Optional[_Union[NmsPolicyLevelSettings.ClearType, str]] = ...,
        conditional: _Optional[
            _Union[_nms_common_pb2.NmsActivateOrClearConditions, _Mapping]
        ] = ...,
    ) -> None: ...
