from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyDataSources(_message.Message):
    __slots__ = (
        "all_devices",
        "device_ids",
        "label_ids",
        "site_ids",
        "types",
        "device_tags",
    )
    class DeviceTag(_message.Message):
        __slots__ = ("id", "values")
        ID_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        id: str
        values: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self, id: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...
        ) -> None: ...

    ALL_DEVICES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    LABEL_IDS_FIELD_NUMBER: _ClassVar[int]
    SITE_IDS_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TAGS_FIELD_NUMBER: _ClassVar[int]
    all_devices: bool
    device_ids: _containers.RepeatedScalarFieldContainer[str]
    label_ids: _containers.RepeatedScalarFieldContainer[str]
    site_ids: _containers.RepeatedScalarFieldContainer[str]
    types: _containers.RepeatedScalarFieldContainer[str]
    device_tags: _containers.RepeatedCompositeFieldContainer[
        PolicyDataSources.DeviceTag
    ]
    def __init__(
        self,
        all_devices: _Optional[bool] = ...,
        device_ids: _Optional[_Iterable[str]] = ...,
        label_ids: _Optional[_Iterable[str]] = ...,
        site_ids: _Optional[_Iterable[str]] = ...,
        types: _Optional[_Iterable[str]] = ...,
        device_tags: _Optional[
            _Iterable[_Union[PolicyDataSources.DeviceTag, _Mapping]]
        ] = ...,
    ) -> None: ...
