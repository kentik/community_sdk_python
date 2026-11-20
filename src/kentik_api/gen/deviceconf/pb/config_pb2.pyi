import datetime
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import device_pb2 as _device_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONFIG_ENCODING_UNSPECIFIED: _ClassVar[ConfigEncoding]
    CONFIG_ENCODING_PLAIN: _ClassVar[ConfigEncoding]
    CONFIG_ENCODING_BZIP2: _ClassVar[ConfigEncoding]

CONFIG_ENCODING_UNSPECIFIED: ConfigEncoding
CONFIG_ENCODING_PLAIN: ConfigEncoding
CONFIG_ENCODING_BZIP2: ConfigEncoding

class Revision(_message.Message):
    __slots__ = ("id", "last_fetched", "first_fetched", "device_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAST_FETCHED_FIELD_NUMBER: _ClassVar[int]
    FIRST_FETCHED_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    last_fetched: _timestamp_pb2.Timestamp
    first_fetched: _timestamp_pb2.Timestamp
    device_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        last_fetched: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        first_fetched: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        device_id: _Optional[str] = ...,
    ) -> None: ...

class CommitDetails(_message.Message):
    __slots__ = ("time", "user", "method", "comment")
    TIME_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    time: _timestamp_pb2.Timestamp
    user: str
    method: str
    comment: str
    def __init__(
        self,
        time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        user: _Optional[str] = ...,
        method: _Optional[str] = ...,
        comment: _Optional[str] = ...,
    ) -> None: ...

class Snapshot(_message.Message):
    __slots__ = (
        "agent_id",
        "device_id",
        "revision",
        "fetch_error",
        "encoding",
        "config_data",
        "digest",
        "diff_data",
        "diff_revision",
        "first_fetched",
        "commit_details",
        "platform",
    )
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    FETCH_ERROR_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    DIFF_DATA_FIELD_NUMBER: _ClassVar[int]
    DIFF_REVISION_FIELD_NUMBER: _ClassVar[int]
    FIRST_FETCHED_FIELD_NUMBER: _ClassVar[int]
    COMMIT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    device_id: str
    revision: Revision
    fetch_error: bool
    encoding: ConfigEncoding
    config_data: bytes
    digest: str
    diff_data: bytes
    diff_revision: Revision
    first_fetched: _timestamp_pb2.Timestamp
    commit_details: CommitDetails
    platform: _device_pb2.DevicePlatform
    def __init__(
        self,
        agent_id: _Optional[str] = ...,
        device_id: _Optional[str] = ...,
        revision: _Optional[_Union[Revision, _Mapping]] = ...,
        fetch_error: _Optional[bool] = ...,
        encoding: _Optional[_Union[ConfigEncoding, str]] = ...,
        config_data: _Optional[bytes] = ...,
        digest: _Optional[str] = ...,
        diff_data: _Optional[bytes] = ...,
        diff_revision: _Optional[_Union[Revision, _Mapping]] = ...,
        first_fetched: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        commit_details: _Optional[_Union[CommitDetails, _Mapping]] = ...,
        platform: _Optional[_Union[_device_pb2.DevicePlatform, str]] = ...,
    ) -> None: ...

class ChangeEvent(_message.Message):
    __slots__ = ("agent_id", "device_id", "revision", "fetch_error", "commit_details")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    FETCH_ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMIT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    device_id: str
    revision: Revision
    fetch_error: bool
    commit_details: CommitDetails
    def __init__(
        self,
        agent_id: _Optional[str] = ...,
        device_id: _Optional[str] = ...,
        revision: _Optional[_Union[Revision, _Mapping]] = ...,
        fetch_error: _Optional[bool] = ...,
        commit_details: _Optional[_Union[CommitDetails, _Mapping]] = ...,
    ) -> None: ...
