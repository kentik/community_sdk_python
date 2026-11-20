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

class AutonomousSystem(_message.Message):
    __slots__ = ("asn", "name")
    ASN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    asn: int
    name: str
    def __init__(
        self, asn: _Optional[int] = ..., name: _Optional[str] = ...
    ) -> None: ...

class ASGroupConcise(_message.Message):
    __slots__ = ("id", "name", "asn", "created_date", "updated_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    asn: _containers.RepeatedScalarFieldContainer[str]
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        asn: _Optional[_Iterable[str]] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class ASGroupDetailed(_message.Message):
    __slots__ = ("id", "name", "asn", "created_date", "updated_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    asn: _containers.RepeatedCompositeFieldContainer[AutonomousSystem]
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        asn: _Optional[_Iterable[_Union[AutonomousSystem, _Mapping]]] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class ListASGroupsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListASGroupsResponse(_message.Message):
    __slots__ = ("as_groups", "invalid_count")
    AS_GROUPS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    as_groups: _containers.RepeatedCompositeFieldContainer[ASGroupDetailed]
    invalid_count: int
    def __init__(
        self,
        as_groups: _Optional[_Iterable[_Union[ASGroupDetailed, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetASGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetASGroupResponse(_message.Message):
    __slots__ = ("as_group",)
    AS_GROUP_FIELD_NUMBER: _ClassVar[int]
    as_group: ASGroupDetailed
    def __init__(
        self, as_group: _Optional[_Union[ASGroupDetailed, _Mapping]] = ...
    ) -> None: ...

class CreateASGroupRequest(_message.Message):
    __slots__ = ("as_group",)
    AS_GROUP_FIELD_NUMBER: _ClassVar[int]
    as_group: ASGroupConcise
    def __init__(
        self, as_group: _Optional[_Union[ASGroupConcise, _Mapping]] = ...
    ) -> None: ...

class CreateASGroupResponse(_message.Message):
    __slots__ = ("as_group",)
    AS_GROUP_FIELD_NUMBER: _ClassVar[int]
    as_group: ASGroupDetailed
    def __init__(
        self, as_group: _Optional[_Union[ASGroupDetailed, _Mapping]] = ...
    ) -> None: ...

class UpdateASGroupRequest(_message.Message):
    __slots__ = ("as_group",)
    AS_GROUP_FIELD_NUMBER: _ClassVar[int]
    as_group: ASGroupConcise
    def __init__(
        self, as_group: _Optional[_Union[ASGroupConcise, _Mapping]] = ...
    ) -> None: ...

class UpdateASGroupResponse(_message.Message):
    __slots__ = ("as_group",)
    AS_GROUP_FIELD_NUMBER: _ClassVar[int]
    as_group: ASGroupDetailed
    def __init__(
        self, as_group: _Optional[_Union[ASGroupDetailed, _Mapping]] = ...
    ) -> None: ...

class DeleteASGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteASGroupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
