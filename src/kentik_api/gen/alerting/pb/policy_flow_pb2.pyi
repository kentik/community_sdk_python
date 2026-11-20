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

from . import common_pb2 as _common_pb2
from . import policy_datasources_pb2 as _policy_datasources_pb2
from . import policy_filters_pb2 as _policy_filters_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class FlowPolicySettings(_message.Message):
    __slots__ = ("dataset", "evaluation", "baseline")
    class DatasetConfig(_message.Message):
        __slots__ = ("sources", "filters", "dimensions", "metrics")
        SOURCES_FIELD_NUMBER: _ClassVar[int]
        FILTERS_FIELD_NUMBER: _ClassVar[int]
        DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
        METRICS_FIELD_NUMBER: _ClassVar[int]
        sources: _policy_datasources_pb2.PolicyDataSources
        filters: _policy_filters_pb2.PolicyFilters
        dimensions: _containers.RepeatedScalarFieldContainer[str]
        metrics: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            sources: _Optional[
                _Union[_policy_datasources_pb2.PolicyDataSources, _Mapping]
            ] = ...,
            filters: _Optional[
                _Union[_policy_filters_pb2.PolicyFilters, _Mapping]
            ] = ...,
            dimensions: _Optional[_Iterable[str]] = ...,
            metrics: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class EvaluationConfig(_message.Message):
        __slots__ = ("frequency", "key_count")
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        KEY_COUNT_FIELD_NUMBER: _ClassVar[int]
        frequency: _duration_pb2.Duration
        key_count: int
        def __init__(
            self,
            frequency: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            key_count: _Optional[int] = ...,
        ) -> None: ...

    class BaselineConfig(_message.Message):
        __slots__ = (
            "stored_key_count",
            "window_length",
            "window_start_offset",
            "rollup_aggregation",
            "compare_mode",
            "neighbourhood_radius",
            "neighbourhood_aggregation",
            "final_aggregation",
        )
        class CompareMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            COMPARE_MODE_UNSPECIFIED: _ClassVar[
                FlowPolicySettings.BaselineConfig.CompareMode
            ]
            COMPARE_MODE_PREVIOUS_HOURS: _ClassVar[
                FlowPolicySettings.BaselineConfig.CompareMode
            ]
            COMPARE_MODE_PREVIOUS_DAYS: _ClassVar[
                FlowPolicySettings.BaselineConfig.CompareMode
            ]
            COMPARE_MODE_PREVIOUS_DAYS_DISTINGUISH_WEEKENDS: _ClassVar[
                FlowPolicySettings.BaselineConfig.CompareMode
            ]
            COMPARE_MODE_PREVIOUS_WEEKS: _ClassVar[
                FlowPolicySettings.BaselineConfig.CompareMode
            ]

        COMPARE_MODE_UNSPECIFIED: FlowPolicySettings.BaselineConfig.CompareMode
        COMPARE_MODE_PREVIOUS_HOURS: FlowPolicySettings.BaselineConfig.CompareMode
        COMPARE_MODE_PREVIOUS_DAYS: FlowPolicySettings.BaselineConfig.CompareMode
        COMPARE_MODE_PREVIOUS_DAYS_DISTINGUISH_WEEKENDS: (
            FlowPolicySettings.BaselineConfig.CompareMode
        )
        COMPARE_MODE_PREVIOUS_WEEKS: FlowPolicySettings.BaselineConfig.CompareMode
        STORED_KEY_COUNT_FIELD_NUMBER: _ClassVar[int]
        WINDOW_LENGTH_FIELD_NUMBER: _ClassVar[int]
        WINDOW_START_OFFSET_FIELD_NUMBER: _ClassVar[int]
        ROLLUP_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
        COMPARE_MODE_FIELD_NUMBER: _ClassVar[int]
        NEIGHBOURHOOD_RADIUS_FIELD_NUMBER: _ClassVar[int]
        NEIGHBOURHOOD_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
        FINAL_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
        stored_key_count: int
        window_length: _duration_pb2.Duration
        window_start_offset: _duration_pb2.Duration
        rollup_aggregation: _common_pb2.AggregationType
        compare_mode: FlowPolicySettings.BaselineConfig.CompareMode
        neighbourhood_radius: _duration_pb2.Duration
        neighbourhood_aggregation: _common_pb2.AggregationType
        final_aggregation: _common_pb2.AggregationType
        def __init__(
            self,
            stored_key_count: _Optional[int] = ...,
            window_length: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            window_start_offset: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            rollup_aggregation: _Optional[
                _Union[_common_pb2.AggregationType, str]
            ] = ...,
            compare_mode: _Optional[
                _Union[FlowPolicySettings.BaselineConfig.CompareMode, str]
            ] = ...,
            neighbourhood_radius: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            neighbourhood_aggregation: _Optional[
                _Union[_common_pb2.AggregationType, str]
            ] = ...,
            final_aggregation: _Optional[
                _Union[_common_pb2.AggregationType, str]
            ] = ...,
        ) -> None: ...

    DATASET_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    BASELINE_FIELD_NUMBER: _ClassVar[int]
    dataset: FlowPolicySettings.DatasetConfig
    evaluation: FlowPolicySettings.EvaluationConfig
    baseline: FlowPolicySettings.BaselineConfig
    def __init__(
        self,
        dataset: _Optional[_Union[FlowPolicySettings.DatasetConfig, _Mapping]] = ...,
        evaluation: _Optional[
            _Union[FlowPolicySettings.EvaluationConfig, _Mapping]
        ] = ...,
        baseline: _Optional[_Union[FlowPolicySettings.BaselineConfig, _Mapping]] = ...,
    ) -> None: ...

class FlowPolicyLevelSettings(_message.Message):
    __slots__ = ("conditions", "activation", "mitigation_associations")
    class ActivationSettings(_message.Message):
        __slots__ = ("match_times", "match_window", "reset_count_window")
        MATCH_TIMES_FIELD_NUMBER: _ClassVar[int]
        MATCH_WINDOW_FIELD_NUMBER: _ClassVar[int]
        RESET_COUNT_WINDOW_FIELD_NUMBER: _ClassVar[int]
        match_times: int
        match_window: _duration_pb2.Duration
        reset_count_window: _duration_pb2.Duration
        def __init__(
            self,
            match_times: _Optional[int] = ...,
            match_window: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            reset_count_window: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
        ) -> None: ...

    class Conditions(_message.Message):
        __slots__ = (
            "static",
            "baseline",
            "top_keys",
            "interface_capacity",
            "ratio",
            "forecast",
        )
        class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            OPERATOR_UNSPECIFIED: _ClassVar[FlowPolicyLevelSettings.Conditions.Operator]
            OPERATOR_GREATER_THAN_OR_EQUALS: _ClassVar[
                FlowPolicyLevelSettings.Conditions.Operator
            ]
            OPERATOR_GREATER_THAN: _ClassVar[
                FlowPolicyLevelSettings.Conditions.Operator
            ]
            OPERATOR_EQUALS: _ClassVar[FlowPolicyLevelSettings.Conditions.Operator]
            OPERATOR_NOT_EQUALS: _ClassVar[FlowPolicyLevelSettings.Conditions.Operator]
            OPERATOR_LESS_THAN: _ClassVar[FlowPolicyLevelSettings.Conditions.Operator]
            OPERATOR_LESS_THAN_OR_EQUALS: _ClassVar[
                FlowPolicyLevelSettings.Conditions.Operator
            ]
            OPERATOR_IN_SET: _ClassVar[FlowPolicyLevelSettings.Conditions.Operator]
            OPERATOR_NOT_IN_SET: _ClassVar[FlowPolicyLevelSettings.Conditions.Operator]

        OPERATOR_UNSPECIFIED: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_GREATER_THAN_OR_EQUALS: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_GREATER_THAN: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_EQUALS: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_NOT_EQUALS: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_LESS_THAN: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_LESS_THAN_OR_EQUALS: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_IN_SET: FlowPolicyLevelSettings.Conditions.Operator
        OPERATOR_NOT_IN_SET: FlowPolicyLevelSettings.Conditions.Operator
        class StaticCondition(_message.Message):
            __slots__ = ("metric", "operator", "value")
            METRIC_FIELD_NUMBER: _ClassVar[int]
            OPERATOR_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            metric: str
            operator: FlowPolicyLevelSettings.Conditions.Operator
            value: float
            def __init__(
                self,
                metric: _Optional[str] = ...,
                operator: _Optional[
                    _Union[FlowPolicyLevelSettings.Conditions.Operator, str]
                ] = ...,
                value: _Optional[float] = ...,
            ) -> None: ...

        class BaselineCondition(_message.Message):
            __slots__ = (
                "absolute",
                "percentage",
                "delta",
                "use_lowest",
                "use_highest",
                "use_trigger",
                "skip",
                "use_value",
            )
            class DeltaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                DELTA_TYPE_UNSPECIFIED: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
                ]
                DELTA_TYPE_ABOVE: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
                ]
                DELTA_TYPE_BELOW: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
                ]

            DELTA_TYPE_UNSPECIFIED: (
                FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
            )
            DELTA_TYPE_ABOVE: (
                FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
            )
            DELTA_TYPE_BELOW: (
                FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
            )
            ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
            PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
            DELTA_FIELD_NUMBER: _ClassVar[int]
            USE_LOWEST_FIELD_NUMBER: _ClassVar[int]
            USE_HIGHEST_FIELD_NUMBER: _ClassVar[int]
            USE_TRIGGER_FIELD_NUMBER: _ClassVar[int]
            SKIP_FIELD_NUMBER: _ClassVar[int]
            USE_VALUE_FIELD_NUMBER: _ClassVar[int]
            absolute: float
            percentage: int
            delta: FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType
            use_lowest: bool
            use_highest: bool
            use_trigger: bool
            skip: bool
            use_value: int
            def __init__(
                self,
                absolute: _Optional[float] = ...,
                percentage: _Optional[int] = ...,
                delta: _Optional[
                    _Union[
                        FlowPolicyLevelSettings.Conditions.BaselineCondition.DeltaType,
                        str,
                    ]
                ] = ...,
                use_lowest: _Optional[bool] = ...,
                use_highest: _Optional[bool] = ...,
                use_trigger: _Optional[bool] = ...,
                skip: _Optional[bool] = ...,
                use_value: _Optional[int] = ...,
            ) -> None: ...

        class TopKeysCondition(_message.Message):
            __slots__ = ("event", "count")
            class TopKeysEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                TOP_KEYS_EVENT_UNSPECIFIED: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
                ]
                TOP_KEYS_EVENT_JOINS: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
                ]
                TOP_KEYS_EVENT_LEAVES: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
                ]

            TOP_KEYS_EVENT_UNSPECIFIED: (
                FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
            )
            TOP_KEYS_EVENT_JOINS: (
                FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
            )
            TOP_KEYS_EVENT_LEAVES: (
                FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
            )
            EVENT_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            event: FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent
            count: int
            def __init__(
                self,
                event: _Optional[
                    _Union[
                        FlowPolicyLevelSettings.Conditions.TopKeysCondition.TopKeysEvent,
                        str,
                    ]
                ] = ...,
                count: _Optional[int] = ...,
            ) -> None: ...

        class InterfaceCapacityCondition(_message.Message):
            __slots__ = ("absolute", "percentage")
            ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
            PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
            absolute: float
            percentage: int
            def __init__(
                self, absolute: _Optional[float] = ..., percentage: _Optional[int] = ...
            ) -> None: ...

        class RatioCondition(_message.Message):
            __slots__ = (
                "lhs_metric",
                "rhs_metric",
                "lhs_proportion",
                "rhs_proportion",
                "margin",
                "direction",
            )
            class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                DIRECTION_UNSPECIFIED: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
                ]
                DIRECTION_BOTH: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
                ]
                DIRECTION_RIGHT: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
                ]
                DIRECTION_LEFT: _ClassVar[
                    FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
                ]

            DIRECTION_UNSPECIFIED: (
                FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
            )
            DIRECTION_BOTH: FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
            DIRECTION_RIGHT: FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
            DIRECTION_LEFT: FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
            LHS_METRIC_FIELD_NUMBER: _ClassVar[int]
            RHS_METRIC_FIELD_NUMBER: _ClassVar[int]
            LHS_PROPORTION_FIELD_NUMBER: _ClassVar[int]
            RHS_PROPORTION_FIELD_NUMBER: _ClassVar[int]
            MARGIN_FIELD_NUMBER: _ClassVar[int]
            DIRECTION_FIELD_NUMBER: _ClassVar[int]
            lhs_metric: str
            rhs_metric: str
            lhs_proportion: int
            rhs_proportion: int
            margin: float
            direction: FlowPolicyLevelSettings.Conditions.RatioCondition.Direction
            def __init__(
                self,
                lhs_metric: _Optional[str] = ...,
                rhs_metric: _Optional[str] = ...,
                lhs_proportion: _Optional[int] = ...,
                rhs_proportion: _Optional[int] = ...,
                margin: _Optional[float] = ...,
                direction: _Optional[
                    _Union[
                        FlowPolicyLevelSettings.Conditions.RatioCondition.Direction, str
                    ]
                ] = ...,
            ) -> None: ...

        class ForecastCondition(_message.Message):
            __slots__ = ("operator", "percentage_value")
            OPERATOR_FIELD_NUMBER: _ClassVar[int]
            PERCENTAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
            operator: FlowPolicyLevelSettings.Conditions.Operator
            percentage_value: int
            def __init__(
                self,
                operator: _Optional[
                    _Union[FlowPolicyLevelSettings.Conditions.Operator, str]
                ] = ...,
                percentage_value: _Optional[int] = ...,
            ) -> None: ...

        STATIC_FIELD_NUMBER: _ClassVar[int]
        BASELINE_FIELD_NUMBER: _ClassVar[int]
        TOP_KEYS_FIELD_NUMBER: _ClassVar[int]
        INTERFACE_CAPACITY_FIELD_NUMBER: _ClassVar[int]
        RATIO_FIELD_NUMBER: _ClassVar[int]
        FORECAST_FIELD_NUMBER: _ClassVar[int]
        static: FlowPolicyLevelSettings.Conditions.StaticCondition
        baseline: FlowPolicyLevelSettings.Conditions.BaselineCondition
        top_keys: FlowPolicyLevelSettings.Conditions.TopKeysCondition
        interface_capacity: (
            FlowPolicyLevelSettings.Conditions.InterfaceCapacityCondition
        )
        ratio: FlowPolicyLevelSettings.Conditions.RatioCondition
        forecast: FlowPolicyLevelSettings.Conditions.ForecastCondition
        def __init__(
            self,
            static: _Optional[
                _Union[FlowPolicyLevelSettings.Conditions.StaticCondition, _Mapping]
            ] = ...,
            baseline: _Optional[
                _Union[FlowPolicyLevelSettings.Conditions.BaselineCondition, _Mapping]
            ] = ...,
            top_keys: _Optional[
                _Union[FlowPolicyLevelSettings.Conditions.TopKeysCondition, _Mapping]
            ] = ...,
            interface_capacity: _Optional[
                _Union[
                    FlowPolicyLevelSettings.Conditions.InterfaceCapacityCondition,
                    _Mapping,
                ]
            ] = ...,
            ratio: _Optional[
                _Union[FlowPolicyLevelSettings.Conditions.RatioCondition, _Mapping]
            ] = ...,
            forecast: _Optional[
                _Union[FlowPolicyLevelSettings.Conditions.ForecastCondition, _Mapping]
            ] = ...,
        ) -> None: ...

    class MitigationAssociation(_message.Message):
        __slots__ = ("platform_id", "method_id")
        PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
        METHOD_ID_FIELD_NUMBER: _ClassVar[int]
        platform_id: str
        method_id: str
        def __init__(
            self, platform_id: _Optional[str] = ..., method_id: _Optional[str] = ...
        ) -> None: ...

    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_ASSOCIATIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[
        FlowPolicyLevelSettings.Conditions
    ]
    activation: FlowPolicyLevelSettings.ActivationSettings
    mitigation_associations: _containers.RepeatedCompositeFieldContainer[
        FlowPolicyLevelSettings.MitigationAssociation
    ]
    def __init__(
        self,
        conditions: _Optional[
            _Iterable[_Union[FlowPolicyLevelSettings.Conditions, _Mapping]]
        ] = ...,
        activation: _Optional[
            _Union[FlowPolicyLevelSettings.ActivationSettings, _Mapping]
        ] = ...,
        mitigation_associations: _Optional[
            _Iterable[_Union[FlowPolicyLevelSettings.MitigationAssociation, _Mapping]]
        ] = ...,
    ) -> None: ...
