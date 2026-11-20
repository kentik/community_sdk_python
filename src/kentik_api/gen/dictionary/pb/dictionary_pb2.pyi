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

class FieldDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_DATA_TYPE_UNSPECIFIED: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_STRING: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_INT: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_UINT32: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_FLOAT: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_INET: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_BYTES: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_ENUM: _ClassVar[FieldDataType]
    FIELD_DATA_TYPE_BOOL: _ClassVar[FieldDataType]

class OperatorSetKey(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATOR_SET_KEY_UNSPECIFIED: _ClassVar[OperatorSetKey]
    OPERATOR_SET_KEY_INT: _ClassVar[OperatorSetKey]
    OPERATOR_SET_KEY_STRING: _ClassVar[OperatorSetKey]
    OPERATOR_SET_KEY_STRING_REGEX: _ClassVar[OperatorSetKey]
    OPERATOR_SET_KEY_INET: _ClassVar[OperatorSetKey]
    OPERATOR_SET_KEY_ENUM: _ClassVar[OperatorSetKey]
    OPERATOR_SET_KEY_FIELD_REFERENCE: _ClassVar[OperatorSetKey]

class MeasurementFamily(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEASUREMENT_FAMILY_UNSPECIFIED: _ClassVar[MeasurementFamily]
    MEASUREMENT_FAMILY_TRAFFIC: _ClassVar[MeasurementFamily]
    MEASUREMENT_FAMILY_NMS: _ClassVar[MeasurementFamily]
    MEASUREMENT_FAMILY_NMS_INTERFACES: _ClassVar[MeasurementFamily]
    MEASUREMENT_FAMILY_SYNTHETICS: _ClassVar[MeasurementFamily]
    MEASUREMENT_FAMILY_BGP: _ClassVar[MeasurementFamily]
    MEASUREMENT_FAMILY_EVENTS: _ClassVar[MeasurementFamily]

class FieldDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_DIRECTION_UNSPECIFIED: _ClassVar[FieldDirection]
    FIELD_DIRECTION_SRC: _ClassVar[FieldDirection]
    FIELD_DIRECTION_DST: _ClassVar[FieldDirection]
    FIELD_DIRECTION_BI: _ClassVar[FieldDirection]
    FIELD_DIRECTION_NONE: _ClassVar[FieldDirection]

class MetricQuantity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_QUANTITY_UNSPECIFIED: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_THROUGHPUT: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_PACKET_RATE: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_FLOW_RATE: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_BYTE_TOTAL: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_PACKET_TOTAL: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_FLOW_TOTAL: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_CARDINALITY: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_UTILIZATION_PCT: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_ERROR_RATE: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_LATENCY: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_JITTER: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_LOSS_PCT: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_SAMPLE_RATE: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_GAUGE: _ClassVar[MetricQuantity]
    METRIC_QUANTITY_SCORE: _ClassVar[MetricQuantity]

class BaseUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BASE_UNIT_UNSPECIFIED: _ClassVar[BaseUnit]
    BASE_UNIT_BITS_PER_SECOND: _ClassVar[BaseUnit]
    BASE_UNIT_PACKETS_PER_SECOND: _ClassVar[BaseUnit]
    BASE_UNIT_FLOWS_PER_SECOND: _ClassVar[BaseUnit]
    BASE_UNIT_BYTES: _ClassVar[BaseUnit]
    BASE_UNIT_PACKETS: _ClassVar[BaseUnit]
    BASE_UNIT_FLOWS: _ClassVar[BaseUnit]
    BASE_UNIT_COUNT: _ClassVar[BaseUnit]
    BASE_UNIT_PERCENT: _ClassVar[BaseUnit]
    BASE_UNIT_MILLISECONDS: _ClassVar[BaseUnit]
    BASE_UNIT_RATIO: _ClassVar[BaseUnit]
    BASE_UNIT_SCORE: _ClassVar[BaseUnit]

FIELD_DATA_TYPE_UNSPECIFIED: FieldDataType
FIELD_DATA_TYPE_STRING: FieldDataType
FIELD_DATA_TYPE_INT: FieldDataType
FIELD_DATA_TYPE_UINT32: FieldDataType
FIELD_DATA_TYPE_FLOAT: FieldDataType
FIELD_DATA_TYPE_INET: FieldDataType
FIELD_DATA_TYPE_BYTES: FieldDataType
FIELD_DATA_TYPE_ENUM: FieldDataType
FIELD_DATA_TYPE_BOOL: FieldDataType
OPERATOR_SET_KEY_UNSPECIFIED: OperatorSetKey
OPERATOR_SET_KEY_INT: OperatorSetKey
OPERATOR_SET_KEY_STRING: OperatorSetKey
OPERATOR_SET_KEY_STRING_REGEX: OperatorSetKey
OPERATOR_SET_KEY_INET: OperatorSetKey
OPERATOR_SET_KEY_ENUM: OperatorSetKey
OPERATOR_SET_KEY_FIELD_REFERENCE: OperatorSetKey
MEASUREMENT_FAMILY_UNSPECIFIED: MeasurementFamily
MEASUREMENT_FAMILY_TRAFFIC: MeasurementFamily
MEASUREMENT_FAMILY_NMS: MeasurementFamily
MEASUREMENT_FAMILY_NMS_INTERFACES: MeasurementFamily
MEASUREMENT_FAMILY_SYNTHETICS: MeasurementFamily
MEASUREMENT_FAMILY_BGP: MeasurementFamily
MEASUREMENT_FAMILY_EVENTS: MeasurementFamily
FIELD_DIRECTION_UNSPECIFIED: FieldDirection
FIELD_DIRECTION_SRC: FieldDirection
FIELD_DIRECTION_DST: FieldDirection
FIELD_DIRECTION_BI: FieldDirection
FIELD_DIRECTION_NONE: FieldDirection
METRIC_QUANTITY_UNSPECIFIED: MetricQuantity
METRIC_QUANTITY_THROUGHPUT: MetricQuantity
METRIC_QUANTITY_PACKET_RATE: MetricQuantity
METRIC_QUANTITY_FLOW_RATE: MetricQuantity
METRIC_QUANTITY_BYTE_TOTAL: MetricQuantity
METRIC_QUANTITY_PACKET_TOTAL: MetricQuantity
METRIC_QUANTITY_FLOW_TOTAL: MetricQuantity
METRIC_QUANTITY_CARDINALITY: MetricQuantity
METRIC_QUANTITY_UTILIZATION_PCT: MetricQuantity
METRIC_QUANTITY_ERROR_RATE: MetricQuantity
METRIC_QUANTITY_LATENCY: MetricQuantity
METRIC_QUANTITY_JITTER: MetricQuantity
METRIC_QUANTITY_LOSS_PCT: MetricQuantity
METRIC_QUANTITY_SAMPLE_RATE: MetricQuantity
METRIC_QUANTITY_GAUGE: MetricQuantity
METRIC_QUANTITY_SCORE: MetricQuantity
BASE_UNIT_UNSPECIFIED: BaseUnit
BASE_UNIT_BITS_PER_SECOND: BaseUnit
BASE_UNIT_PACKETS_PER_SECOND: BaseUnit
BASE_UNIT_FLOWS_PER_SECOND: BaseUnit
BASE_UNIT_BYTES: BaseUnit
BASE_UNIT_PACKETS: BaseUnit
BASE_UNIT_FLOWS: BaseUnit
BASE_UNIT_COUNT: BaseUnit
BASE_UNIT_PERCENT: BaseUnit
BASE_UNIT_MILLISECONDS: BaseUnit
BASE_UNIT_RATIO: BaseUnit
BASE_UNIT_SCORE: BaseUnit

class Operator(_message.Message):
    __slots__ = ("key", "label")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    def __init__(
        self, key: _Optional[str] = ..., label: _Optional[str] = ...
    ) -> None: ...

class OperatorSet(_message.Message):
    __slots__ = ("key", "operators")
    KEY_FIELD_NUMBER: _ClassVar[int]
    OPERATORS_FIELD_NUMBER: _ClassVar[int]
    key: OperatorSetKey
    operators: _containers.RepeatedCompositeFieldContainer[Operator]
    def __init__(
        self,
        key: _Optional[_Union[OperatorSetKey, str]] = ...,
        operators: _Optional[_Iterable[_Union[Operator, _Mapping]]] = ...,
    ) -> None: ...

class MetricFamilyDef(_message.Message):
    __slots__ = (
        "key",
        "label",
        "quantity",
        "base_unit",
        "dual_axis_compatible",
        "incompatible_with",
    )
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    BASE_UNIT_FIELD_NUMBER: _ClassVar[int]
    DUAL_AXIS_COMPATIBLE_FIELD_NUMBER: _ClassVar[int]
    INCOMPATIBLE_WITH_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    quantity: MetricQuantity
    base_unit: BaseUnit
    dual_axis_compatible: _containers.RepeatedScalarFieldContainer[str]
    incompatible_with: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        key: _Optional[str] = ...,
        label: _Optional[str] = ...,
        quantity: _Optional[_Union[MetricQuantity, str]] = ...,
        base_unit: _Optional[_Union[BaseUnit, str]] = ...,
        dual_axis_compatible: _Optional[_Iterable[str]] = ...,
        incompatible_with: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class AssetTag(_message.Message):
    __slots__ = ("name", "display_name")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    def __init__(
        self, name: _Optional[str] = ..., display_name: _Optional[str] = ...
    ) -> None: ...

class AppProtocolMetadata(_message.Message):
    __slots__ = ("full_data_only",)
    FULL_DATA_ONLY_FIELD_NUMBER: _ClassVar[int]
    full_data_only: bool
    def __init__(self, full_data_only: _Optional[bool] = ...) -> None: ...

class AppProtocol(_message.Message):
    __slots__ = ("id", "display_name", "add_to_standard_fields", "status", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ADD_TO_STANDARD_FIELDS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: int
    display_name: str
    add_to_standard_fields: bool
    status: str
    metadata: AppProtocolMetadata
    def __init__(
        self,
        id: _Optional[int] = ...,
        display_name: _Optional[str] = ...,
        add_to_standard_fields: _Optional[bool] = ...,
        status: _Optional[str] = ...,
        metadata: _Optional[_Union[AppProtocolMetadata, _Mapping]] = ...,
    ) -> None: ...

class DimensionField(_message.Message):
    __slots__ = (
        "key",
        "label",
        "data_type",
        "category",
        "column",
        "direction",
        "inverse",
        "values",
        "last_seen",
        "operator_set_key",
        "filter_only",
        "filter_column",
        "query_column",
        "can_count",
        "shared",
    )
    class ValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INVERSE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_SET_KEY_FIELD_NUMBER: _ClassVar[int]
    FILTER_ONLY_FIELD_NUMBER: _ClassVar[int]
    FILTER_COLUMN_FIELD_NUMBER: _ClassVar[int]
    QUERY_COLUMN_FIELD_NUMBER: _ClassVar[int]
    CAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    SHARED_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    data_type: FieldDataType
    category: str
    column: str
    direction: FieldDirection
    inverse: str
    values: _containers.ScalarMap[str, str]
    last_seen: str
    operator_set_key: OperatorSetKey
    filter_only: bool
    filter_column: str
    query_column: str
    can_count: bool
    shared: bool
    def __init__(
        self,
        key: _Optional[str] = ...,
        label: _Optional[str] = ...,
        data_type: _Optional[_Union[FieldDataType, str]] = ...,
        category: _Optional[str] = ...,
        column: _Optional[str] = ...,
        direction: _Optional[_Union[FieldDirection, str]] = ...,
        inverse: _Optional[str] = ...,
        values: _Optional[_Mapping[str, str]] = ...,
        last_seen: _Optional[str] = ...,
        operator_set_key: _Optional[_Union[OperatorSetKey, str]] = ...,
        filter_only: _Optional[bool] = ...,
        filter_column: _Optional[str] = ...,
        query_column: _Optional[str] = ...,
        can_count: _Optional[bool] = ...,
        shared: _Optional[bool] = ...,
    ) -> None: ...

class MetricField(_message.Message):
    __slots__ = (
        "key",
        "label",
        "data_type",
        "category",
        "column",
        "direction",
        "inverse",
        "values",
        "last_seen",
        "window_fn",
        "aggregate_fn",
        "expression",
        "depends_on",
        "to_bits",
        "rollup",
        "healthy_value",
        "family_key",
        "base_unit",
        "shared",
    )
    class ValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INVERSE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FN_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_FN_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    DEPENDS_ON_FIELD_NUMBER: _ClassVar[int]
    TO_BITS_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_VALUE_FIELD_NUMBER: _ClassVar[int]
    FAMILY_KEY_FIELD_NUMBER: _ClassVar[int]
    BASE_UNIT_FIELD_NUMBER: _ClassVar[int]
    SHARED_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    data_type: FieldDataType
    category: str
    column: str
    direction: FieldDirection
    inverse: str
    values: _containers.ScalarMap[str, str]
    last_seen: str
    window_fn: str
    aggregate_fn: str
    expression: str
    depends_on: _containers.RepeatedScalarFieldContainer[str]
    to_bits: bool
    rollup: bool
    healthy_value: str
    family_key: str
    base_unit: BaseUnit
    shared: bool
    def __init__(
        self,
        key: _Optional[str] = ...,
        label: _Optional[str] = ...,
        data_type: _Optional[_Union[FieldDataType, str]] = ...,
        category: _Optional[str] = ...,
        column: _Optional[str] = ...,
        direction: _Optional[_Union[FieldDirection, str]] = ...,
        inverse: _Optional[str] = ...,
        values: _Optional[_Mapping[str, str]] = ...,
        last_seen: _Optional[str] = ...,
        window_fn: _Optional[str] = ...,
        aggregate_fn: _Optional[str] = ...,
        expression: _Optional[str] = ...,
        depends_on: _Optional[_Iterable[str]] = ...,
        to_bits: _Optional[bool] = ...,
        rollup: _Optional[bool] = ...,
        healthy_value: _Optional[str] = ...,
        family_key: _Optional[str] = ...,
        base_unit: _Optional[_Union[BaseUnit, str]] = ...,
        shared: _Optional[bool] = ...,
    ) -> None: ...

class MeasurementDetail(_message.Message):
    __slots__ = (
        "name",
        "display_name",
        "family",
        "description",
        "last_seen",
        "dimensions",
        "metrics",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    family: MeasurementFamily
    description: str
    last_seen: str
    dimensions: _containers.RepeatedCompositeFieldContainer[DimensionField]
    metrics: _containers.RepeatedCompositeFieldContainer[MetricField]
    def __init__(
        self,
        name: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        family: _Optional[_Union[MeasurementFamily, str]] = ...,
        description: _Optional[str] = ...,
        last_seen: _Optional[str] = ...,
        dimensions: _Optional[_Iterable[_Union[DimensionField, _Mapping]]] = ...,
        metrics: _Optional[_Iterable[_Union[MetricField, _Mapping]]] = ...,
    ) -> None: ...

class GetDictionaryRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDictionaryResponse(_message.Message):
    __slots__ = (
        "measurements",
        "operator_sets",
        "metric_families",
        "asset_tags",
        "app_protocols",
    )
    class AppProtocolsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AppProtocol
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[AppProtocol, _Mapping]] = ...,
        ) -> None: ...

    MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_SETS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FAMILIES_FIELD_NUMBER: _ClassVar[int]
    ASSET_TAGS_FIELD_NUMBER: _ClassVar[int]
    APP_PROTOCOLS_FIELD_NUMBER: _ClassVar[int]
    measurements: _containers.RepeatedCompositeFieldContainer[MeasurementDetail]
    operator_sets: _containers.RepeatedCompositeFieldContainer[OperatorSet]
    metric_families: _containers.RepeatedCompositeFieldContainer[MetricFamilyDef]
    asset_tags: _containers.RepeatedCompositeFieldContainer[AssetTag]
    app_protocols: _containers.MessageMap[str, AppProtocol]
    def __init__(
        self,
        measurements: _Optional[_Iterable[_Union[MeasurementDetail, _Mapping]]] = ...,
        operator_sets: _Optional[_Iterable[_Union[OperatorSet, _Mapping]]] = ...,
        metric_families: _Optional[_Iterable[_Union[MetricFamilyDef, _Mapping]]] = ...,
        asset_tags: _Optional[_Iterable[_Union[AssetTag, _Mapping]]] = ...,
        app_protocols: _Optional[_Mapping[str, AppProtocol]] = ...,
    ) -> None: ...
