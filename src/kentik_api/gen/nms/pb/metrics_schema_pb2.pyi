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

class FieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_TYPE_UNSPECIFIED: _ClassVar[FieldType]
    FIELD_TYPE_INT: _ClassVar[FieldType]
    FIELD_TYPE_FLOAT: _ClassVar[FieldType]
    FIELD_TYPE_STRING: _ClassVar[FieldType]

class Usage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USAGE_UNSPECIFIED: _ClassVar[Usage]
    USAGE_QUERY: _ClassVar[Usage]
    USAGE_KMETRICS_ALERT: _ClassVar[Usage]
    USAGE_FLOW_ALERT: _ClassVar[Usage]

FIELD_TYPE_UNSPECIFIED: FieldType
FIELD_TYPE_INT: FieldType
FIELD_TYPE_FLOAT: FieldType
FIELD_TYPE_STRING: FieldType
USAGE_UNSPECIFIED: Usage
USAGE_QUERY: Usage
USAGE_KMETRICS_ALERT: Usage
USAGE_FLOW_ALERT: Usage

class FieldDisplay(_message.Message):
    __slots__ = ("precision",)
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    precision: int
    def __init__(self, precision: _Optional[int] = ...) -> None: ...

class FieldSchema(_message.Message):
    __slots__ = (
        "type",
        "column",
        "mask",
        "description",
        "unit",
        "label",
        "values",
        "last_seen",
        "supported_usages",
        "query_column",
        "enrichment",
        "display",
        "is_primary_key",
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

    TYPE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_USAGES_FIELD_NUMBER: _ClassVar[int]
    QUERY_COLUMN_FIELD_NUMBER: _ClassVar[int]
    ENRICHMENT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_KEY_FIELD_NUMBER: _ClassVar[int]
    type: FieldType
    column: str
    mask: int
    description: str
    unit: str
    label: str
    values: _containers.ScalarMap[str, str]
    last_seen: _timestamp_pb2.Timestamp
    supported_usages: _containers.RepeatedScalarFieldContainer[Usage]
    query_column: str
    enrichment: str
    display: FieldDisplay
    is_primary_key: bool
    def __init__(
        self,
        type: _Optional[_Union[FieldType, str]] = ...,
        column: _Optional[str] = ...,
        mask: _Optional[int] = ...,
        description: _Optional[str] = ...,
        unit: _Optional[str] = ...,
        label: _Optional[str] = ...,
        values: _Optional[_Mapping[str, str]] = ...,
        last_seen: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        supported_usages: _Optional[_Iterable[_Union[Usage, str]]] = ...,
        query_column: _Optional[str] = ...,
        enrichment: _Optional[str] = ...,
        display: _Optional[_Union[FieldDisplay, _Mapping]] = ...,
        is_primary_key: _Optional[bool] = ...,
    ) -> None: ...

class MeasurementSchema(_message.Message):
    __slots__ = (
        "id",
        "entity_type",
        "description",
        "app_protocol",
        "source_timestamp_column",
        "dimensions",
        "metrics",
        "last_seen",
        "tags",
    )
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FieldSchema
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[FieldSchema, _Mapping]] = ...,
        ) -> None: ...

    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FieldSchema
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[FieldSchema, _Mapping]] = ...,
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    APP_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TIMESTAMP_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    entity_type: str
    description: str
    app_protocol: int
    source_timestamp_column: str
    dimensions: _containers.MessageMap[str, FieldSchema]
    metrics: _containers.MessageMap[str, FieldSchema]
    last_seen: _timestamp_pb2.Timestamp
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[int] = ...,
        entity_type: _Optional[str] = ...,
        description: _Optional[str] = ...,
        app_protocol: _Optional[int] = ...,
        source_timestamp_column: _Optional[str] = ...,
        dimensions: _Optional[_Mapping[str, FieldSchema]] = ...,
        metrics: _Optional[_Mapping[str, FieldSchema]] = ...,
        last_seen: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MetricsSchema(_message.Message):
    __slots__ = ("measurements",)
    class MeasurementsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: MeasurementSchema
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[MeasurementSchema, _Mapping]] = ...,
        ) -> None: ...

    MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
    measurements: _containers.MessageMap[str, MeasurementSchema]
    def __init__(
        self, measurements: _Optional[_Mapping[str, MeasurementSchema]] = ...
    ) -> None: ...

class GetMetricsSchemaRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMetricsSchemaResponse(_message.Message):
    __slots__ = ("schema",)
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: MetricsSchema
    def __init__(
        self, schema: _Optional[_Union[MetricsSchema, _Mapping]] = ...
    ) -> None: ...
