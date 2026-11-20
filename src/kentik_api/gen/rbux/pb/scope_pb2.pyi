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

from kentik_api.gen.saved_filter.pb import (
    saved_filter_message_pb2 as _saved_filter_message_pb2,
)

DESCRIPTOR: _descriptor.FileDescriptor

class AssetTagSelector(_message.Message):
    __slots__ = ("tag_id", "values")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    tag_id: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, tag_id: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class ScopeDimensions(_message.Message):
    __slots__ = ("sites", "labels", "asset_tags")
    SITES_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ASSET_TAGS_FIELD_NUMBER: _ClassVar[int]
    sites: _containers.RepeatedScalarFieldContainer[int]
    labels: _containers.RepeatedScalarFieldContainer[int]
    asset_tags: _containers.RepeatedCompositeFieldContainer[AssetTagSelector]
    def __init__(
        self,
        sites: _Optional[_Iterable[int]] = ...,
        labels: _Optional[_Iterable[int]] = ...,
        asset_tags: _Optional[_Iterable[_Union[AssetTagSelector, _Mapping]]] = ...,
    ) -> None: ...

class ScopeConfig(_message.Message):
    __slots__ = ("dimensions", "filters")
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    dimensions: ScopeDimensions
    filters: _saved_filter_message_pb2.SavedFilterFilters
    def __init__(
        self,
        dimensions: _Optional[_Union[ScopeDimensions, _Mapping]] = ...,
        filters: _Optional[
            _Union[_saved_filter_message_pb2.SavedFilterFilters, _Mapping]
        ] = ...,
    ) -> None: ...

class Scope(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "scope",
        "created_by",
        "created_date",
        "updated_date",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    scope: ScopeConfig
    created_by: str
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        scope: _Optional[_Union[ScopeConfig, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class ListScopesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListScopesResponse(_message.Message):
    __slots__ = ("scopes",)
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    scopes: _containers.RepeatedCompositeFieldContainer[Scope]
    def __init__(
        self, scopes: _Optional[_Iterable[_Union[Scope, _Mapping]]] = ...
    ) -> None: ...

class GetScopeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetScopeResponse(_message.Message):
    __slots__ = ("scope",)
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    def __init__(self, scope: _Optional[_Union[Scope, _Mapping]] = ...) -> None: ...

class CreateScopeRequest(_message.Message):
    __slots__ = ("scope",)
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    def __init__(self, scope: _Optional[_Union[Scope, _Mapping]] = ...) -> None: ...

class CreateScopeResponse(_message.Message):
    __slots__ = ("scope",)
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    def __init__(self, scope: _Optional[_Union[Scope, _Mapping]] = ...) -> None: ...

class UpdateScopeRequest(_message.Message):
    __slots__ = ("scope",)
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    def __init__(self, scope: _Optional[_Union[Scope, _Mapping]] = ...) -> None: ...

class UpdateScopeResponse(_message.Message):
    __slots__ = ("scope",)
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    def __init__(self, scope: _Optional[_Union[Scope, _Mapping]] = ...) -> None: ...

class DeleteScopeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteScopeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
