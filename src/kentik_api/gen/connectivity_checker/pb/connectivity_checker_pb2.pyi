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

class CloudProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_PROVIDER_UNSPECIFIED: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_AWS: _ClassVar[CloudProvider]
    CLOUD_PROVIDER_AZURE: _ClassVar[CloudProvider]

class EntityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTITY_TYPE_UNSPECIFIED: _ClassVar[EntityType]
    ENTITY_TYPE_SUBNET: _ClassVar[EntityType]
    ENTITY_TYPE_INSTANCE: _ClassVar[EntityType]
    ENTITY_TYPE_NETWORK_INTERFACE: _ClassVar[EntityType]

CLOUD_PROVIDER_UNSPECIFIED: CloudProvider
CLOUD_PROVIDER_AWS: CloudProvider
CLOUD_PROVIDER_AZURE: CloudProvider
ENTITY_TYPE_UNSPECIFIED: EntityType
ENTITY_TYPE_SUBNET: EntityType
ENTITY_TYPE_INSTANCE: EntityType
ENTITY_TYPE_NETWORK_INTERFACE: EntityType

class CreateConnectivityReportRequest(_message.Message):
    __slots__ = (
        "cloud_provider",
        "src",
        "dst",
        "dst_port",
        "protocol",
        "src_type",
        "dst_type",
        "start_time",
        "end_time",
        "name",
    )
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SRC_FIELD_NUMBER: _ClassVar[int]
    DST_FIELD_NUMBER: _ClassVar[int]
    DST_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SRC_TYPE_FIELD_NUMBER: _ClassVar[int]
    DST_TYPE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    cloud_provider: CloudProvider
    src: str
    dst: str
    dst_port: str
    protocol: str
    src_type: EntityType
    dst_type: EntityType
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    name: str
    def __init__(
        self,
        cloud_provider: _Optional[_Union[CloudProvider, str]] = ...,
        src: _Optional[str] = ...,
        dst: _Optional[str] = ...,
        dst_port: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        src_type: _Optional[_Union[EntityType, str]] = ...,
        dst_type: _Optional[_Union[EntityType, str]] = ...,
        start_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class CreateConnectivityReportResponse(_message.Message):
    __slots__ = (
        "reachable",
        "return_reachable",
        "query_status",
        "report_url",
        "paths",
        "return_paths",
        "last_metadata_fetch",
    )
    REACHABLE_FIELD_NUMBER: _ClassVar[int]
    RETURN_REACHABLE_FIELD_NUMBER: _ClassVar[int]
    QUERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    REPORT_URL_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    RETURN_PATHS_FIELD_NUMBER: _ClassVar[int]
    LAST_METADATA_FETCH_FIELD_NUMBER: _ClassVar[int]
    reachable: bool
    return_reachable: bool
    query_status: str
    report_url: str
    paths: _containers.RepeatedScalarFieldContainer[str]
    return_paths: _containers.RepeatedScalarFieldContainer[str]
    last_metadata_fetch: str
    def __init__(
        self,
        reachable: _Optional[bool] = ...,
        return_reachable: _Optional[bool] = ...,
        query_status: _Optional[str] = ...,
        report_url: _Optional[str] = ...,
        paths: _Optional[_Iterable[str]] = ...,
        return_paths: _Optional[_Iterable[str]] = ...,
        last_metadata_fetch: _Optional[str] = ...,
    ) -> None: ...
