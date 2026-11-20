from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from . import kmeta_message_pb2 as _kmeta_message_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class ListServiceNowConfigsRequest(_message.Message):
    __slots__ = ("cid",)
    CID_FIELD_NUMBER: _ClassVar[int]
    cid: str
    def __init__(self, cid: _Optional[str] = ...) -> None: ...

class ListServiceNowConfigsResponse(_message.Message):
    __slots__ = ("configs",)
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[
        _kmeta_message_pb2.ServiceNowConfig
    ]
    def __init__(
        self,
        configs: _Optional[
            _Iterable[_Union[_kmeta_message_pb2.ServiceNowConfig, _Mapping]]
        ] = ...,
    ) -> None: ...

class GetServiceNowConfigRequest(_message.Message):
    __slots__ = ("cid", "id")
    CID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    cid: str
    id: str
    def __init__(self, cid: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetServiceNowConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _kmeta_message_pb2.ServiceNowConfig
    def __init__(
        self,
        config: _Optional[_Union[_kmeta_message_pb2.ServiceNowConfig, _Mapping]] = ...,
    ) -> None: ...

class CreateServiceNowConfigRequest(_message.Message):
    __slots__ = ("cid", "config")
    CID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    cid: str
    config: _kmeta_message_pb2.ServiceNowConfig
    def __init__(
        self,
        cid: _Optional[str] = ...,
        config: _Optional[_Union[_kmeta_message_pb2.ServiceNowConfig, _Mapping]] = ...,
    ) -> None: ...

class CreateServiceNowConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _kmeta_message_pb2.ServiceNowConfig
    def __init__(
        self,
        config: _Optional[_Union[_kmeta_message_pb2.ServiceNowConfig, _Mapping]] = ...,
    ) -> None: ...

class UpdateServiceNowConfigRequest(_message.Message):
    __slots__ = ("cid", "id", "config")
    CID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    cid: str
    id: str
    config: _kmeta_message_pb2.ServiceNowConfig
    def __init__(
        self,
        cid: _Optional[str] = ...,
        id: _Optional[str] = ...,
        config: _Optional[_Union[_kmeta_message_pb2.ServiceNowConfig, _Mapping]] = ...,
    ) -> None: ...

class UpdateServiceNowConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _kmeta_message_pb2.ServiceNowConfig
    def __init__(
        self,
        config: _Optional[_Union[_kmeta_message_pb2.ServiceNowConfig, _Mapping]] = ...,
    ) -> None: ...

class DeleteServiceNowConfigRequest(_message.Message):
    __slots__ = ("cid", "id")
    CID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    cid: str
    id: str
    def __init__(self, cid: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class DeleteServiceNowConfigResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
