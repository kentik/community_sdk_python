from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class PaginationConfig(_message.Message):
    __slots__ = ("limit", "offset", "include_total_count")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    include_total_count: bool
    def __init__(
        self,
        limit: _Optional[int] = ...,
        offset: _Optional[int] = ...,
        include_total_count: _Optional[bool] = ...,
    ) -> None: ...

class PaginationInfo(_message.Message):
    __slots__ = ("total_count", "has_more_results")
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_RESULTS_FIELD_NUMBER: _ClassVar[int]
    total_count: int
    has_more_results: bool
    def __init__(
        self, total_count: _Optional[int] = ..., has_more_results: _Optional[bool] = ...
    ) -> None: ...
