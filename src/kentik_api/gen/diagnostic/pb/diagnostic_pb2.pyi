from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class EchoRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class EchoResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ChatRequest(_message.Message):
    __slots__ = ("message_id", "echo_request", "echo_response")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ECHO_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ECHO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    echo_request: EchoRequest
    echo_response: EchoResponse
    def __init__(
        self,
        message_id: _Optional[str] = ...,
        echo_request: _Optional[_Union[EchoRequest, _Mapping]] = ...,
        echo_response: _Optional[_Union[EchoResponse, _Mapping]] = ...,
    ) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ("message_id", "echo_request", "echo_response")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    ECHO_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ECHO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    echo_request: EchoRequest
    echo_response: EchoResponse
    def __init__(
        self,
        message_id: _Optional[str] = ...,
        echo_request: _Optional[_Union[EchoRequest, _Mapping]] = ...,
        echo_response: _Optional[_Union[EchoResponse, _Mapping]] = ...,
    ) -> None: ...
