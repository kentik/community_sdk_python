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

class SessionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SESSION_STATUS_UNSPECIFIED: _ClassVar[SessionStatus]
    SESSION_STATUS_PENDING: _ClassVar[SessionStatus]
    SESSION_STATUS_PROCESSING: _ClassVar[SessionStatus]
    SESSION_STATUS_COMPLETED: _ClassVar[SessionStatus]
    SESSION_STATUS_FAILED: _ClassVar[SessionStatus]
    SESSION_STATUS_AWAITING_APPROVAL: _ClassVar[SessionStatus]

SESSION_STATUS_UNSPECIFIED: SessionStatus
SESSION_STATUS_PENDING: SessionStatus
SESSION_STATUS_PROCESSING: SessionStatus
SESSION_STATUS_COMPLETED: SessionStatus
SESSION_STATUS_FAILED: SessionStatus
SESSION_STATUS_AWAITING_APPROVAL: SessionStatus

class CreateChatSessionRequest(_message.Message):
    __slots__ = ("prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    def __init__(self, prompt: _Optional[str] = ...) -> None: ...

class CreateChatSessionResponse(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: SessionStatus
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[SessionStatus, str]] = ...,
    ) -> None: ...

class UpdateChatSessionRequest(_message.Message):
    __slots__ = ("prompt", "id")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    id: str
    def __init__(
        self, prompt: _Optional[str] = ..., id: _Optional[str] = ...
    ) -> None: ...

class UpdateChatSessionResponse(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: SessionStatus
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[SessionStatus, str]] = ...,
    ) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = (
        "id",
        "status",
        "final_answer",
        "reasoning",
        "data",
        "error_message",
        "created_at",
        "updated_at",
        "prompt",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINAL_ANSWER_FIELD_NUMBER: _ClassVar[int]
    REASONING_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: SessionStatus
    final_answer: str
    reasoning: str
    data: str
    error_message: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    prompt: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[SessionStatus, str]] = ...,
        final_answer: _Optional[str] = ...,
        reasoning: _Optional[str] = ...,
        data: _Optional[str] = ...,
        error_message: _Optional[str] = ...,
        created_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        prompt: _Optional[str] = ...,
    ) -> None: ...

class GetChatSessionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetChatSessionResponse(_message.Message):
    __slots__ = ("id", "status", "messages")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: SessionStatus
    messages: _containers.RepeatedCompositeFieldContainer[ChatMessage]
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[SessionStatus, str]] = ...,
        messages: _Optional[_Iterable[_Union[ChatMessage, _Mapping]]] = ...,
    ) -> None: ...
