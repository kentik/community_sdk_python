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

DESCRIPTOR: _descriptor.FileDescriptor

class Label(_message.Message):
    __slots__ = ("id", "name", "description", "color", "cdate", "edate")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    color: str
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        color: _Optional[str] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class ListLabelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListLabelsResponse(_message.Message):
    __slots__ = ("labels", "invalid_count")
    LABELS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[Label]
    invalid_count: int
    def __init__(
        self,
        labels: _Optional[_Iterable[_Union[Label, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class CreateLabelRequest(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: Label
    def __init__(self, label: _Optional[_Union[Label, _Mapping]] = ...) -> None: ...

class CreateLabelResponse(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: Label
    def __init__(self, label: _Optional[_Union[Label, _Mapping]] = ...) -> None: ...

class UpdateLabelRequest(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: Label
    def __init__(self, label: _Optional[_Union[Label, _Mapping]] = ...) -> None: ...

class UpdateLabelResponse(_message.Message):
    __slots__ = ("label",)
    LABEL_FIELD_NUMBER: _ClassVar[int]
    label: Label
    def __init__(self, label: _Optional[_Union[Label, _Mapping]] = ...) -> None: ...

class DeleteLabelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteLabelResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
