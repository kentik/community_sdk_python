import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

from . import command_pb2 as _command_pb2
from . import config_pb2 as _config_pb2
from . import device_pb2 as _device_pb2
from . import signature_pb2 as _signature_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class GetDeviceAssignmentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDeviceAssignmentsResponse(_message.Message):
    __slots__ = ("devices",)
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[_device_pb2.Device]
    def __init__(
        self, devices: _Optional[_Iterable[_Union[_device_pb2.Device, _Mapping]]] = ...
    ) -> None: ...

class UpdateDeviceConfigurationRequest(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _config_pb2.Snapshot
    def __init__(
        self, config: _Optional[_Union[_config_pb2.Snapshot, _Mapping]] = ...
    ) -> None: ...

class UpdateDeviceConfigurationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDeviceConfigurationRequest(_message.Message):
    __slots__ = (
        "fetch_time",
        "revision",
        "ref_revision",
        "device_id",
        "exclude_config_data",
        "exclude_diff_data",
    )
    FETCH_TIME_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    REF_REVISION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DIFF_DATA_FIELD_NUMBER: _ClassVar[int]
    fetch_time: _timestamp_pb2.Timestamp
    revision: str
    ref_revision: str
    device_id: str
    exclude_config_data: bool
    exclude_diff_data: bool
    def __init__(
        self,
        fetch_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        revision: _Optional[str] = ...,
        ref_revision: _Optional[str] = ...,
        device_id: _Optional[str] = ...,
        exclude_config_data: _Optional[bool] = ...,
        exclude_diff_data: _Optional[bool] = ...,
    ) -> None: ...

class GetDeviceConfigurationResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _config_pb2.Snapshot
    def __init__(
        self, config: _Optional[_Union[_config_pb2.Snapshot, _Mapping]] = ...
    ) -> None: ...

class GetLatestDeviceConfigurationsRequest(_message.Message):
    __slots__ = ("device_ids", "exclude_config_data", "exclude_diff_data")
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DIFF_DATA_FIELD_NUMBER: _ClassVar[int]
    device_ids: _containers.RepeatedScalarFieldContainer[str]
    exclude_config_data: bool
    exclude_diff_data: bool
    def __init__(
        self,
        device_ids: _Optional[_Iterable[str]] = ...,
        exclude_config_data: _Optional[bool] = ...,
        exclude_diff_data: _Optional[bool] = ...,
    ) -> None: ...

class GetLatestDeviceConfigurationsResponse(_message.Message):
    __slots__ = ("configs",)
    class ConfigsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _config_pb2.Snapshot
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[_config_pb2.Snapshot, _Mapping]] = ...,
        ) -> None: ...

    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.MessageMap[str, _config_pb2.Snapshot]
    def __init__(
        self, configs: _Optional[_Mapping[str, _config_pb2.Snapshot]] = ...
    ) -> None: ...

class ListDeviceConfigurationRevisionsRequest(_message.Message):
    __slots__ = ("from_time", "until_time", "limit", "device_id")
    FROM_TIME_FIELD_NUMBER: _ClassVar[int]
    UNTIL_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    from_time: _timestamp_pb2.Timestamp
    until_time: _timestamp_pb2.Timestamp
    limit: int
    device_id: str
    def __init__(
        self,
        from_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        until_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        limit: _Optional[int] = ...,
        device_id: _Optional[str] = ...,
    ) -> None: ...

class ListDeviceConfigurationRevisionsResponse(_message.Message):
    __slots__ = ("revisions",)
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    revisions: _containers.RepeatedCompositeFieldContainer[_config_pb2.Revision]
    def __init__(
        self,
        revisions: _Optional[_Iterable[_Union[_config_pb2.Revision, _Mapping]]] = ...,
    ) -> None: ...

class RequestDeviceConfigurationFetchRequest(_message.Message):
    __slots__ = ("device_id",)
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    def __init__(self, device_id: _Optional[str] = ...) -> None: ...

class RequestDeviceConfigurationFetchResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExecuteCommandRequest(_message.Message):
    __slots__ = ("device_command", "signature", "timeout")
    DEVICE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    device_command: _command_pb2.DeviceCommand
    signature: _signature_pb2.MessageSignature
    timeout: _duration_pb2.Duration
    def __init__(
        self,
        device_command: _Optional[_Union[_command_pb2.DeviceCommand, _Mapping]] = ...,
        signature: _Optional[_Union[_signature_pb2.MessageSignature, _Mapping]] = ...,
        timeout: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
    ) -> None: ...

class ExecuteCommandResponse(_message.Message):
    __slots__ = ("command_result",)
    COMMAND_RESULT_FIELD_NUMBER: _ClassVar[int]
    command_result: _command_pb2.CommandResult
    def __init__(
        self,
        command_result: _Optional[_Union[_command_pb2.CommandResult, _Mapping]] = ...,
    ) -> None: ...

class GetCommandAclsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCommandAclsResponse(_message.Message):
    __slots__ = ("acls",)
    ACLS_FIELD_NUMBER: _ClassVar[int]
    acls: _containers.RepeatedCompositeFieldContainer[_command_pb2.CommandAcl]
    def __init__(
        self,
        acls: _Optional[_Iterable[_Union[_command_pb2.CommandAcl, _Mapping]]] = ...,
    ) -> None: ...

class UpdateCommandAclsRequest(_message.Message):
    __slots__ = ("acls",)
    ACLS_FIELD_NUMBER: _ClassVar[int]
    acls: _containers.RepeatedCompositeFieldContainer[_command_pb2.CommandAcl]
    def __init__(
        self,
        acls: _Optional[_Iterable[_Union[_command_pb2.CommandAcl, _Mapping]]] = ...,
    ) -> None: ...

class UpdateCommandAclsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteDeviceConfigurationRequest(_message.Message):
    __slots__ = ("device_id", "revision")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    revision: str
    def __init__(
        self, device_id: _Optional[str] = ..., revision: _Optional[str] = ...
    ) -> None: ...

class DeleteDeviceConfigurationResponse(_message.Message):
    __slots__ = ("orphaned_revision",)
    ORPHANED_REVISION_FIELD_NUMBER: _ClassVar[int]
    orphaned_revision: _config_pb2.Revision
    def __init__(
        self, orphaned_revision: _Optional[_Union[_config_pb2.Revision, _Mapping]] = ...
    ) -> None: ...
