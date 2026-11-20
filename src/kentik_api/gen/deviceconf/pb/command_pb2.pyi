from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class AclAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACL_ACTION_UNSPECIFIED: _ClassVar[AclAction]
    ACL_ACTION_ALLOW: _ClassVar[AclAction]
    ACL_ACTION_DENY: _ClassVar[AclAction]

class AclMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACL_MODE_UNSPECIFIED: _ClassVar[AclMode]
    ACL_MODE_EXACT: _ClassVar[AclMode]
    ACL_MODE_CONTAINS: _ClassVar[AclMode]
    ACL_MODE_REGEX: _ClassVar[AclMode]

ACL_ACTION_UNSPECIFIED: AclAction
ACL_ACTION_ALLOW: AclAction
ACL_ACTION_DENY: AclAction
ACL_MODE_UNSPECIFIED: AclMode
ACL_MODE_EXACT: AclMode
ACL_MODE_CONTAINS: AclMode
ACL_MODE_REGEX: AclMode

class DeviceCommand(_message.Message):
    __slots__ = ("device_id", "command")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    command: str
    def __init__(
        self, device_id: _Optional[str] = ..., command: _Optional[str] = ...
    ) -> None: ...

class CommandResult(_message.Message):
    __slots__ = ("success", "output")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    output: str
    def __init__(
        self, success: _Optional[bool] = ..., output: _Optional[str] = ...
    ) -> None: ...

class CommandAcl(_message.Message):
    __slots__ = ("action", "mode", "filter")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    action: AclAction
    mode: AclMode
    filter: str
    def __init__(
        self,
        action: _Optional[_Union[AclAction, str]] = ...,
        mode: _Optional[_Union[AclMode, str]] = ...,
        filter: _Optional[str] = ...,
    ) -> None: ...
