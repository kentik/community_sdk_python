from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class PtrResult(_message.Message):
    __slots__ = ("address", "answer", "error", "ttl", "resolver_ip")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_IP_FIELD_NUMBER: _ClassVar[int]
    address: str
    answer: str
    error: str
    ttl: int
    resolver_ip: str
    def __init__(
        self,
        address: _Optional[str] = ...,
        answer: _Optional[str] = ...,
        error: _Optional[str] = ...,
        ttl: _Optional[int] = ...,
        resolver_ip: _Optional[str] = ...,
    ) -> None: ...
