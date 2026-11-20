from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class UserInfo(_message.Message):
    __slots__ = ("id", "email", "full_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    full_name: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        email: _Optional[str] = ...,
        full_name: _Optional[str] = ...,
    ) -> None: ...
