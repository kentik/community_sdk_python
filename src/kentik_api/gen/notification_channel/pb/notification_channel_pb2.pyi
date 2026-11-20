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

class ChannelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHANNEL_TYPE_UNSPECIFIED: _ClassVar[ChannelType]
    CHANNEL_TYPE_XMATTERS: _ClassVar[ChannelType]
    CHANNEL_TYPE_SLACK: _ClassVar[ChannelType]
    CHANNEL_TYPE_SERVICENOW: _ClassVar[ChannelType]
    CHANNEL_TYPE_SYSLOG: _ClassVar[ChannelType]
    CHANNEL_TYPE_OPSGENIE: _ClassVar[ChannelType]
    CHANNEL_TYPE_CUSTOM_WEBHOOK: _ClassVar[ChannelType]
    CHANNEL_TYPE_SPLUNK: _ClassVar[ChannelType]
    CHANNEL_TYPE_MSTEAMS: _ClassVar[ChannelType]
    CHANNEL_TYPE_JSON: _ClassVar[ChannelType]
    CHANNEL_TYPE_EMAIL: _ClassVar[ChannelType]
    CHANNEL_TYPE_VICTOROPS: _ClassVar[ChannelType]
    CHANNEL_TYPE_PAGERDUTY: _ClassVar[ChannelType]

CHANNEL_TYPE_UNSPECIFIED: ChannelType
CHANNEL_TYPE_XMATTERS: ChannelType
CHANNEL_TYPE_SLACK: ChannelType
CHANNEL_TYPE_SERVICENOW: ChannelType
CHANNEL_TYPE_SYSLOG: ChannelType
CHANNEL_TYPE_OPSGENIE: ChannelType
CHANNEL_TYPE_CUSTOM_WEBHOOK: ChannelType
CHANNEL_TYPE_SPLUNK: ChannelType
CHANNEL_TYPE_MSTEAMS: ChannelType
CHANNEL_TYPE_JSON: ChannelType
CHANNEL_TYPE_EMAIL: ChannelType
CHANNEL_TYPE_VICTOROPS: ChannelType
CHANNEL_TYPE_PAGERDUTY: ChannelType

class NotificationChannel(_message.Message):
    __slots__ = ("id", "name", "type", "enabled", "cdate", "edate")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: ChannelType
    enabled: bool
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        type: _Optional[_Union[ChannelType, str]] = ...,
        enabled: _Optional[bool] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class ListNotificationChannelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListNotificationChannelsResponse(_message.Message):
    __slots__ = ("notification_channels", "invalid_count")
    NOTIFICATION_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    notification_channels: _containers.RepeatedCompositeFieldContainer[
        NotificationChannel
    ]
    invalid_count: int
    def __init__(
        self,
        notification_channels: _Optional[
            _Iterable[_Union[NotificationChannel, _Mapping]]
        ] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetNotificationChannelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetNotificationChannelResponse(_message.Message):
    __slots__ = ("notification_channel",)
    NOTIFICATION_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    notification_channel: NotificationChannel
    def __init__(
        self,
        notification_channel: _Optional[_Union[NotificationChannel, _Mapping]] = ...,
    ) -> None: ...

class SearchNotificationChannelsRequest(_message.Message):
    __slots__ = ("name_pattern", "types", "include_disabled")
    NAME_PATTERN_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISABLED_FIELD_NUMBER: _ClassVar[int]
    name_pattern: str
    types: _containers.RepeatedScalarFieldContainer[ChannelType]
    include_disabled: bool
    def __init__(
        self,
        name_pattern: _Optional[str] = ...,
        types: _Optional[_Iterable[_Union[ChannelType, str]]] = ...,
        include_disabled: _Optional[bool] = ...,
    ) -> None: ...

class SearchNotificationChannelsResponse(_message.Message):
    __slots__ = ("notification_channels", "invalid_count")
    NOTIFICATION_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    notification_channels: _containers.RepeatedCompositeFieldContainer[
        NotificationChannel
    ]
    invalid_count: int
    def __init__(
        self,
        notification_channels: _Optional[
            _Iterable[_Union[NotificationChannel, _Mapping]]
        ] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...
