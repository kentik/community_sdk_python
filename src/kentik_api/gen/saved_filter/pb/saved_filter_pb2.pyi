from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from . import saved_filter_message_pb2 as _saved_filter_message_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSavedFilterRequest(_message.Message):
    __slots__ = ("filter",)
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: _saved_filter_message_pb2.SavedFilter
    def __init__(
        self,
        filter: _Optional[
            _Union[_saved_filter_message_pb2.SavedFilter, _Mapping]
        ] = ...,
    ) -> None: ...

class CreateSavedFilterResponse(_message.Message):
    __slots__ = ("filter",)
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: _saved_filter_message_pb2.SavedFilter
    def __init__(
        self,
        filter: _Optional[
            _Union[_saved_filter_message_pb2.SavedFilter, _Mapping]
        ] = ...,
    ) -> None: ...

class UpdateSavedFilterRequest(_message.Message):
    __slots__ = ("id", "filter")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    id: str
    filter: _saved_filter_message_pb2.SavedFilter
    def __init__(
        self,
        id: _Optional[str] = ...,
        filter: _Optional[
            _Union[_saved_filter_message_pb2.SavedFilter, _Mapping]
        ] = ...,
    ) -> None: ...

class UpdateSavedFilterResponse(_message.Message):
    __slots__ = ("filter",)
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: _saved_filter_message_pb2.SavedFilter
    def __init__(
        self,
        filter: _Optional[
            _Union[_saved_filter_message_pb2.SavedFilter, _Mapping]
        ] = ...,
    ) -> None: ...

class ListSavedFiltersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSavedFiltersAllRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSavedFiltersResponse(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.RepeatedCompositeFieldContainer[
        _saved_filter_message_pb2.SavedFilter
    ]
    def __init__(
        self,
        filters: _Optional[
            _Iterable[_Union[_saved_filter_message_pb2.SavedFilter, _Mapping]]
        ] = ...,
    ) -> None: ...

class ListSavedFiltersAllResponse(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.RepeatedCompositeFieldContainer[
        _saved_filter_message_pb2.SavedFilter
    ]
    def __init__(
        self,
        filters: _Optional[
            _Iterable[_Union[_saved_filter_message_pb2.SavedFilter, _Mapping]]
        ] = ...,
    ) -> None: ...

class GetSavedFilterRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSavedFilterResponse(_message.Message):
    __slots__ = ("filter",)
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: _saved_filter_message_pb2.SavedFilter
    def __init__(
        self,
        filter: _Optional[
            _Union[_saved_filter_message_pb2.SavedFilter, _Mapping]
        ] = ...,
    ) -> None: ...

class DeleteSavedFilterRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSavedFilterResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
