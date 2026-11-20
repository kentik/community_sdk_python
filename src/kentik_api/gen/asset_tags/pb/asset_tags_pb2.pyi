from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class AssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_TYPE_UNSPECIFIED: _ClassVar[AssetType]
    ASSET_TYPE_DEVICE: _ClassVar[AssetType]

ASSET_TYPE_UNSPECIFIED: AssetType
ASSET_TYPE_DEVICE: AssetType

class TagKey(_message.Message):
    __slots__ = ("id", "name", "display_name", "color", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    color: str
    description: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        color: _Optional[str] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class TagValue(_message.Message):
    __slots__ = ("tag_id", "asset_type", "asset_id", "value")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    tag_id: str
    asset_type: AssetType
    asset_id: str
    value: str
    def __init__(
        self,
        tag_id: _Optional[str] = ...,
        asset_type: _Optional[_Union[AssetType, str]] = ...,
        asset_id: _Optional[str] = ...,
        value: _Optional[str] = ...,
    ) -> None: ...

class ListTagKeysRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTagKeysResponse(_message.Message):
    __slots__ = ("tag_keys",)
    TAG_KEYS_FIELD_NUMBER: _ClassVar[int]
    tag_keys: _containers.RepeatedCompositeFieldContainer[TagKey]
    def __init__(
        self, tag_keys: _Optional[_Iterable[_Union[TagKey, _Mapping]]] = ...
    ) -> None: ...

class GetTagKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTagKeyResponse(_message.Message):
    __slots__ = ("tag_key",)
    TAG_KEY_FIELD_NUMBER: _ClassVar[int]
    tag_key: TagKey
    def __init__(self, tag_key: _Optional[_Union[TagKey, _Mapping]] = ...) -> None: ...

class CreateTagKeyRequest(_message.Message):
    __slots__ = ("name", "display_name", "color", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    color: str
    description: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        color: _Optional[str] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class CreateTagKeyResponse(_message.Message):
    __slots__ = ("tag_key",)
    TAG_KEY_FIELD_NUMBER: _ClassVar[int]
    tag_key: TagKey
    def __init__(self, tag_key: _Optional[_Union[TagKey, _Mapping]] = ...) -> None: ...

class UpdateTagKeyRequest(_message.Message):
    __slots__ = ("id", "display_name", "color", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    color: str
    description: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        color: _Optional[str] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class UpdateTagKeyResponse(_message.Message):
    __slots__ = ("tag_key",)
    TAG_KEY_FIELD_NUMBER: _ClassVar[int]
    tag_key: TagKey
    def __init__(self, tag_key: _Optional[_Union[TagKey, _Mapping]] = ...) -> None: ...

class DeleteTagKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTagKeyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTagValuesRequest(_message.Message):
    __slots__ = ("tag_id", "asset_type")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    tag_id: str
    asset_type: AssetType
    def __init__(
        self,
        tag_id: _Optional[str] = ...,
        asset_type: _Optional[_Union[AssetType, str]] = ...,
    ) -> None: ...

class ListTagValuesResponse(_message.Message):
    __slots__ = ("tag_values",)
    TAG_VALUES_FIELD_NUMBER: _ClassVar[int]
    tag_values: _containers.RepeatedCompositeFieldContainer[TagValue]
    def __init__(
        self, tag_values: _Optional[_Iterable[_Union[TagValue, _Mapping]]] = ...
    ) -> None: ...

class GetTagValuesRequest(_message.Message):
    __slots__ = ("asset_type", "asset_id")
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    asset_type: AssetType
    asset_id: str
    def __init__(
        self,
        asset_type: _Optional[_Union[AssetType, str]] = ...,
        asset_id: _Optional[str] = ...,
    ) -> None: ...

class GetTagValuesResponse(_message.Message):
    __slots__ = ("tag_values",)
    TAG_VALUES_FIELD_NUMBER: _ClassVar[int]
    tag_values: _containers.RepeatedCompositeFieldContainer[TagValue]
    def __init__(
        self, tag_values: _Optional[_Iterable[_Union[TagValue, _Mapping]]] = ...
    ) -> None: ...

class SetTagValuesRequest(_message.Message):
    __slots__ = ("tag_id", "asset_type", "asset_ids", "value")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    tag_id: str
    asset_type: AssetType
    asset_ids: _containers.RepeatedScalarFieldContainer[str]
    value: str
    def __init__(
        self,
        tag_id: _Optional[str] = ...,
        asset_type: _Optional[_Union[AssetType, str]] = ...,
        asset_ids: _Optional[_Iterable[str]] = ...,
        value: _Optional[str] = ...,
    ) -> None: ...

class SetTagValuesResponse(_message.Message):
    __slots__ = ("tag_values",)
    TAG_VALUES_FIELD_NUMBER: _ClassVar[int]
    tag_values: _containers.RepeatedCompositeFieldContainer[TagValue]
    def __init__(
        self, tag_values: _Optional[_Iterable[_Union[TagValue, _Mapping]]] = ...
    ) -> None: ...

class DeleteTagValuesRequest(_message.Message):
    __slots__ = ("tag_id", "asset_type", "asset_ids")
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_IDS_FIELD_NUMBER: _ClassVar[int]
    tag_id: str
    asset_type: AssetType
    asset_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        tag_id: _Optional[str] = ...,
        asset_type: _Optional[_Union[AssetType, str]] = ...,
        asset_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class DeleteTagValuesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
