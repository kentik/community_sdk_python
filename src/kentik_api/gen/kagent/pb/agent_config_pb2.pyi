import datetime
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class AgentConfig(_message.Message):
    __slots__ = (
        "created",
        "edited",
        "site_id",
        "name",
        "description",
        "release_channel",
        "os_distribution",
    )
    CREATED_FIELD_NUMBER: _ClassVar[int]
    EDITED_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RELEASE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    OS_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    created: _timestamp_pb2.Timestamp
    edited: _timestamp_pb2.Timestamp
    site_id: str
    name: str
    description: str
    release_channel: str
    os_distribution: str
    def __init__(
        self,
        created: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edited: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        site_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        release_channel: _Optional[str] = ...,
        os_distribution: _Optional[str] = ...,
    ) -> None: ...

class TelemetryConfig(_message.Message):
    __slots__ = (
        "logs_endpoint",
        "metrics_endpoint",
        "kmetrics_endpoint",
        "sentry_endpoint",
    )
    LOGS_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    METRICS_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    KMETRICS_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    SENTRY_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    logs_endpoint: str
    metrics_endpoint: str
    kmetrics_endpoint: str
    sentry_endpoint: str
    def __init__(
        self,
        logs_endpoint: _Optional[str] = ...,
        metrics_endpoint: _Optional[str] = ...,
        kmetrics_endpoint: _Optional[str] = ...,
        sentry_endpoint: _Optional[str] = ...,
    ) -> None: ...
