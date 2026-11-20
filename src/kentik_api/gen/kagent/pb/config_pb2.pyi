from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import agent_config_pb2 as _agent_config_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ("name", "capability", "version", "runtime", "telemetry", "layers")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    capability: str
    version: str
    runtime: RuntimeConfig
    telemetry: _agent_config_pb2.TelemetryConfig
    layers: _containers.RepeatedCompositeFieldContainer[ConfigLayer]
    def __init__(
        self,
        name: _Optional[str] = ...,
        capability: _Optional[str] = ...,
        version: _Optional[str] = ...,
        runtime: _Optional[_Union[RuntimeConfig, _Mapping]] = ...,
        telemetry: _Optional[_Union[_agent_config_pb2.TelemetryConfig, _Mapping]] = ...,
        layers: _Optional[_Iterable[_Union[ConfigLayer, _Mapping]]] = ...,
    ) -> None: ...

class ConfigLayer(_message.Message):
    __slots__ = ("name", "type")
    class LayerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LAYER_TYPE_UNSPECIFIED: _ClassVar[ConfigLayer.LayerType]
        LAYER_TYPE_SEED: _ClassVar[ConfigLayer.LayerType]
        LAYER_TYPE_GROUP: _ClassVar[ConfigLayer.LayerType]
        LAYER_TYPE_AGENT: _ClassVar[ConfigLayer.LayerType]

    LAYER_TYPE_UNSPECIFIED: ConfigLayer.LayerType
    LAYER_TYPE_SEED: ConfigLayer.LayerType
    LAYER_TYPE_GROUP: ConfigLayer.LayerType
    LAYER_TYPE_AGENT: ConfigLayer.LayerType
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: ConfigLayer.LayerType
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[ConfigLayer.LayerType, str]] = ...,
    ) -> None: ...

class RuntimeConfig(_message.Message):
    __slots__ = ("args", "env", "binary", "linux_capabilities")
    class EnvVar(_message.Message):
        __slots__ = ("name", "value", "origin")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        origin: str
        def __init__(
            self,
            name: _Optional[str] = ...,
            value: _Optional[str] = ...,
            origin: _Optional[str] = ...,
        ) -> None: ...

    ARGS_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    BINARY_FIELD_NUMBER: _ClassVar[int]
    LINUX_CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    args: _containers.RepeatedScalarFieldContainer[str]
    env: _containers.RepeatedCompositeFieldContainer[RuntimeConfig.EnvVar]
    binary: str
    linux_capabilities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        args: _Optional[_Iterable[str]] = ...,
        env: _Optional[_Iterable[_Union[RuntimeConfig.EnvVar, _Mapping]]] = ...,
        binary: _Optional[str] = ...,
        linux_capabilities: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetConfigRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: Config
    def __init__(self, config: _Optional[_Union[Config, _Mapping]] = ...) -> None: ...

class DeleteConfigRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteConfigResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateConfigRequest(_message.Message):
    __slots__ = ("config", "mask")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    config: Config
    mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        config: _Optional[_Union[Config, _Mapping]] = ...,
        mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: Config
    def __init__(self, config: _Optional[_Union[Config, _Mapping]] = ...) -> None: ...

class CreateConfigRequest(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: Config
    def __init__(self, config: _Optional[_Union[Config, _Mapping]] = ...) -> None: ...

class CreateConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: Config
    def __init__(self, config: _Optional[_Union[Config, _Mapping]] = ...) -> None: ...
