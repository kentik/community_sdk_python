from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ResultType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_TYPE_UNSPECIFIED: _ClassVar[ResultType]
    RESULT_TYPE_ERROR: _ClassVar[ResultType]
    RESULT_TYPE_DE_QUERY_OBJECT: _ClassVar[ResultType]
    RESULT_TYPE_ME_QUERY_OBJECT: _ClassVar[ResultType]
    RESULT_TYPE_KNOWLEDGE_BASE: _ClassVar[ResultType]
    RESULT_TYPE_DDOS_ALERTS: _ClassVar[ResultType]

class ResultFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULT_FORMAT_UNSPECIFIED: _ClassVar[ResultFormat]
    RESULT_FORMAT_JSON: _ClassVar[ResultFormat]
    RESULT_FORMAT_MARKDOWN: _ClassVar[ResultFormat]
    RESULT_FORMAT_PLAIN_TEXT: _ClassVar[ResultFormat]

RESULT_TYPE_UNSPECIFIED: ResultType
RESULT_TYPE_ERROR: ResultType
RESULT_TYPE_DE_QUERY_OBJECT: ResultType
RESULT_TYPE_ME_QUERY_OBJECT: ResultType
RESULT_TYPE_KNOWLEDGE_BASE: ResultType
RESULT_TYPE_DDOS_ALERTS: ResultType
RESULT_FORMAT_UNSPECIFIED: ResultFormat
RESULT_FORMAT_JSON: ResultFormat
RESULT_FORMAT_MARKDOWN: ResultFormat
RESULT_FORMAT_PLAIN_TEXT: ResultFormat

class GetJourneysNlqRequest(_message.Message):
    __slots__ = ("prompt",)
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    def __init__(self, prompt: _Optional[str] = ...) -> None: ...

class GetJourneysNlqResponse(_message.Message):
    __slots__ = ("result", "result_type", "result_format")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    result: str
    result_type: ResultType
    result_format: ResultFormat
    def __init__(
        self,
        result: _Optional[str] = ...,
        result_type: _Optional[_Union[ResultType, str]] = ...,
        result_format: _Optional[_Union[ResultFormat, str]] = ...,
    ) -> None: ...
