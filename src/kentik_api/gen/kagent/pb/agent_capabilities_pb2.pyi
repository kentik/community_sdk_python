from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class AgentCapability(_message.Message):
    __slots__ = (
        "name",
        "bundle_id",
        "enabled",
        "version",
        "channel",
        "config_id",
        "group_id",
        "group_index",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_INDEX_FIELD_NUMBER: _ClassVar[int]
    name: str
    bundle_id: str
    enabled: bool
    version: str
    channel: str
    config_id: str
    group_id: str
    group_index: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        bundle_id: _Optional[str] = ...,
        enabled: _Optional[bool] = ...,
        version: _Optional[str] = ...,
        channel: _Optional[str] = ...,
        config_id: _Optional[str] = ...,
        group_id: _Optional[str] = ...,
        group_index: _Optional[int] = ...,
    ) -> None: ...

class AgentCapabilityGroup(_message.Message):
    __slots__ = ("group_id", "index", "running_count", "standby_count")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    RUNNING_COUNT_FIELD_NUMBER: _ClassVar[int]
    STANDBY_COUNT_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    index: int
    running_count: int
    standby_count: int
    def __init__(
        self,
        group_id: _Optional[str] = ...,
        index: _Optional[int] = ...,
        running_count: _Optional[int] = ...,
        standby_count: _Optional[int] = ...,
    ) -> None: ...

class UpsertAgentCapabilityRequest(_message.Message):
    __slots__ = ("agent_id", "capability", "mask")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    capability: AgentCapability
    mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        agent_id: _Optional[str] = ...,
        capability: _Optional[_Union[AgentCapability, _Mapping]] = ...,
        mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpsertAgentCapabilityResponse(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: AgentCapability
    def __init__(
        self, capability: _Optional[_Union[AgentCapability, _Mapping]] = ...
    ) -> None: ...

class ListAgentCapabilitiesRequest(_message.Message):
    __slots__ = ("agent_id",)
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    def __init__(self, agent_id: _Optional[str] = ...) -> None: ...

class ListAgentCapabilitiesResponse(_message.Message):
    __slots__ = ("capabilities",)
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    capabilities: _containers.RepeatedCompositeFieldContainer[AgentCapability]
    def __init__(
        self,
        capabilities: _Optional[_Iterable[_Union[AgentCapability, _Mapping]]] = ...,
    ) -> None: ...

class DeleteAgentCapabilityRequest(_message.Message):
    __slots__ = ("agent_id", "capability")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    capability: str
    def __init__(
        self, agent_id: _Optional[str] = ..., capability: _Optional[str] = ...
    ) -> None: ...

class DeleteAgentCapabilityResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAgentCapabilityRequest(_message.Message):
    __slots__ = ("agent_id", "capability")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    capability: str
    def __init__(
        self, agent_id: _Optional[str] = ..., capability: _Optional[str] = ...
    ) -> None: ...

class GetAgentCapabilityResponse(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: AgentCapability
    def __init__(
        self, capability: _Optional[_Union[AgentCapability, _Mapping]] = ...
    ) -> None: ...
