import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import agent_config_pb2 as _agent_config_pb2
from . import agent_state_pb2 as _agent_state_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class InstallerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INSTALLER_TYPE_UNSPECIFIED: _ClassVar[InstallerType]
    INSTALLER_TYPE_LINUX: _ClassVar[InstallerType]
    INSTALLER_TYPE_DOCKER: _ClassVar[InstallerType]
    INSTALLER_TYPE_RPM: _ClassVar[InstallerType]
    INSTALLER_TYPE_DEB: _ClassVar[InstallerType]

class ReleaseSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RELEASE_SOURCE_UNSPECIFIED: _ClassVar[ReleaseSource]
    RELEASE_SOURCE_MANAGED: _ClassVar[ReleaseSource]
    RELEASE_SOURCE_LOCAL: _ClassVar[ReleaseSource]

class ConfigSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONFIG_SOURCE_UNSPECIFIED: _ClassVar[ConfigSource]
    CONFIG_SOURCE_MANAGED: _ClassVar[ConfigSource]
    CONFIG_SOURCE_LOCAL: _ClassVar[ConfigSource]

class BundleSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUNDLE_SOURCE_UNSPECIFIED: _ClassVar[BundleSource]
    BUNDLE_SOURCE_MANAGED: _ClassVar[BundleSource]
    BUNDLE_SOURCE_LOCAL: _ClassVar[BundleSource]

INSTALLER_TYPE_UNSPECIFIED: InstallerType
INSTALLER_TYPE_LINUX: InstallerType
INSTALLER_TYPE_DOCKER: InstallerType
INSTALLER_TYPE_RPM: InstallerType
INSTALLER_TYPE_DEB: InstallerType
RELEASE_SOURCE_UNSPECIFIED: ReleaseSource
RELEASE_SOURCE_MANAGED: ReleaseSource
RELEASE_SOURCE_LOCAL: ReleaseSource
CONFIG_SOURCE_UNSPECIFIED: ConfigSource
CONFIG_SOURCE_MANAGED: ConfigSource
CONFIG_SOURCE_LOCAL: ConfigSource
BUNDLE_SOURCE_UNSPECIFIED: BundleSource
BUNDLE_SOURCE_MANAGED: BundleSource
BUNDLE_SOURCE_LOCAL: BundleSource

class HostMetadata(_message.Message):
    __slots__ = ("hostname", "machine_id", "public_ip", "private_ip", "os", "arch")
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_IP_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    machine_id: str
    public_ip: str
    private_ip: str
    os: str
    arch: str
    def __init__(
        self,
        hostname: _Optional[str] = ...,
        machine_id: _Optional[str] = ...,
        public_ip: _Optional[str] = ...,
        private_ip: _Optional[str] = ...,
        os: _Optional[str] = ...,
        arch: _Optional[str] = ...,
    ) -> None: ...

class InstallConfig(_message.Message):
    __slots__ = (
        "id",
        "type",
        "host_metadata",
        "release_source",
        "config_source",
        "bundle_source",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HOST_METADATA_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_SOURCE_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: InstallerType
    host_metadata: HostMetadata
    release_source: ReleaseSource
    config_source: ConfigSource
    bundle_source: BundleSource
    def __init__(
        self,
        id: _Optional[str] = ...,
        type: _Optional[_Union[InstallerType, str]] = ...,
        host_metadata: _Optional[_Union[HostMetadata, _Mapping]] = ...,
        release_source: _Optional[_Union[ReleaseSource, str]] = ...,
        config_source: _Optional[_Union[ConfigSource, str]] = ...,
        bundle_source: _Optional[_Union[BundleSource, str]] = ...,
    ) -> None: ...

class Agent(_message.Message):
    __slots__ = (
        "id",
        "running",
        "cluster_id",
        "public_key",
        "provisioning_token",
        "config",
        "install",
        "desired_state",
        "current_state",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    RUNNING_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    PROVISIONING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INSTALL_FIELD_NUMBER: _ClassVar[int]
    DESIRED_STATE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    running: bool
    cluster_id: str
    public_key: str
    provisioning_token: str
    config: _agent_config_pb2.AgentConfig
    install: InstallConfig
    desired_state: _agent_state_pb2.AgentDesiredState
    current_state: _agent_state_pb2.AgentCurrentState
    def __init__(
        self,
        id: _Optional[str] = ...,
        running: _Optional[bool] = ...,
        cluster_id: _Optional[str] = ...,
        public_key: _Optional[str] = ...,
        provisioning_token: _Optional[str] = ...,
        config: _Optional[_Union[_agent_config_pb2.AgentConfig, _Mapping]] = ...,
        install: _Optional[_Union[InstallConfig, _Mapping]] = ...,
        desired_state: _Optional[
            _Union[_agent_state_pb2.AgentDesiredState, _Mapping]
        ] = ...,
        current_state: _Optional[
            _Union[_agent_state_pb2.AgentCurrentState, _Mapping]
        ] = ...,
    ) -> None: ...

class GetAgentRequest(_message.Message):
    __slots__ = ("id", "unregistered")
    ID_FIELD_NUMBER: _ClassVar[int]
    UNREGISTERED_FIELD_NUMBER: _ClassVar[int]
    id: str
    unregistered: bool
    def __init__(
        self, id: _Optional[str] = ..., unregistered: _Optional[bool] = ...
    ) -> None: ...

class GetAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class ListAgentsRequest(_message.Message):
    __slots__ = ("unregistered", "ids", "capabilities", "include_desired_state")
    UNREGISTERED_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DESIRED_STATE_FIELD_NUMBER: _ClassVar[int]
    unregistered: bool
    ids: _containers.RepeatedScalarFieldContainer[str]
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    include_desired_state: bool
    def __init__(
        self,
        unregistered: _Optional[bool] = ...,
        ids: _Optional[_Iterable[str]] = ...,
        capabilities: _Optional[_Iterable[str]] = ...,
        include_desired_state: _Optional[bool] = ...,
    ) -> None: ...

class ListAgentsResponse(_message.Message):
    __slots__ = ("agents",)
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.RepeatedCompositeFieldContainer[Agent]
    def __init__(
        self, agents: _Optional[_Iterable[_Union[Agent, _Mapping]]] = ...
    ) -> None: ...

class UpdateAgentRequest(_message.Message):
    __slots__ = ("agent", "mask")
    AGENT_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        agent: _Optional[_Union[Agent, _Mapping]] = ...,
        mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class DeleteAgentRequest(_message.Message):
    __slots__ = ("id", "unregistered")
    ID_FIELD_NUMBER: _ClassVar[int]
    UNREGISTERED_FIELD_NUMBER: _ClassVar[int]
    id: str
    unregistered: bool
    def __init__(
        self, id: _Optional[str] = ..., unregistered: _Optional[bool] = ...
    ) -> None: ...

class DeleteAgentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AuthorizeRequest(_message.Message):
    __slots__ = ("install_id",)
    INSTALL_ID_FIELD_NUMBER: _ClassVar[int]
    install_id: str
    def __init__(self, install_id: _Optional[str] = ...) -> None: ...

class AuthorizeResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AgentRegistration(_message.Message):
    __slots__ = (
        "public_key",
        "site_id",
        "name",
        "description",
        "release_channel",
        "cluster_id",
    )
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RELEASE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    public_key: str
    site_id: str
    name: str
    description: str
    release_channel: str
    cluster_id: str
    def __init__(
        self,
        public_key: _Optional[str] = ...,
        site_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        release_channel: _Optional[str] = ...,
        cluster_id: _Optional[str] = ...,
    ) -> None: ...

class RegistrationConfig(_message.Message):
    __slots__ = ("expires_at", "allowed_private_cidrs", "allowed_public_cidrs")
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_PRIVATE_CIDRS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_PUBLIC_CIDRS_FIELD_NUMBER: _ClassVar[int]
    expires_at: _timestamp_pb2.Timestamp
    allowed_private_cidrs: _containers.RepeatedScalarFieldContainer[str]
    allowed_public_cidrs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        expires_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        allowed_private_cidrs: _Optional[_Iterable[str]] = ...,
        allowed_public_cidrs: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class CreateAgentRequest(_message.Message):
    __slots__ = ("agent", "config")
    AGENT_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    agent: AgentRegistration
    config: RegistrationConfig
    def __init__(
        self,
        agent: _Optional[_Union[AgentRegistration, _Mapping]] = ...,
        config: _Optional[_Union[RegistrationConfig, _Mapping]] = ...,
    ) -> None: ...

class BootstrapInfo(_message.Message):
    __slots__ = (
        "linux_install_command",
        "docker_install_command",
        "provisioning_token",
    )
    LINUX_INSTALL_COMMAND_FIELD_NUMBER: _ClassVar[int]
    DOCKER_INSTALL_COMMAND_FIELD_NUMBER: _ClassVar[int]
    PROVISIONING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    linux_install_command: str
    docker_install_command: str
    provisioning_token: str
    def __init__(
        self,
        linux_install_command: _Optional[str] = ...,
        docker_install_command: _Optional[str] = ...,
        provisioning_token: _Optional[str] = ...,
    ) -> None: ...

class CreateAgentResponse(_message.Message):
    __slots__ = ("agent", "bootstrap")
    AGENT_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    bootstrap: BootstrapInfo
    def __init__(
        self,
        agent: _Optional[_Union[Agent, _Mapping]] = ...,
        bootstrap: _Optional[_Union[BootstrapInfo, _Mapping]] = ...,
    ) -> None: ...

class GenerateInstallCommandsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GenerateInstallCommandsResponse(_message.Message):
    __slots__ = ("bootstrap",)
    BOOTSTRAP_FIELD_NUMBER: _ClassVar[int]
    bootstrap: BootstrapInfo
    def __init__(
        self, bootstrap: _Optional[_Union[BootstrapInfo, _Mapping]] = ...
    ) -> None: ...
