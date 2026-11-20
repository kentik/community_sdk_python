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

class CapabilityRelease(_message.Message):
    __slots__ = (
        "capability",
        "semver",
        "download_urls",
        "checksum",
        "checksum_algorithm",
        "provenance",
        "supported_distros",
        "compatibility",
    )
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    SEMVER_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URLS_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    PROVENANCE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_DISTROS_FIELD_NUMBER: _ClassVar[int]
    COMPATIBILITY_FIELD_NUMBER: _ClassVar[int]
    capability: str
    semver: str
    download_urls: _containers.RepeatedScalarFieldContainer[str]
    checksum: str
    checksum_algorithm: str
    provenance: str
    supported_distros: _containers.RepeatedScalarFieldContainer[str]
    compatibility: CompatibilityInfo
    def __init__(
        self,
        capability: _Optional[str] = ...,
        semver: _Optional[str] = ...,
        download_urls: _Optional[_Iterable[str]] = ...,
        checksum: _Optional[str] = ...,
        checksum_algorithm: _Optional[str] = ...,
        provenance: _Optional[str] = ...,
        supported_distros: _Optional[_Iterable[str]] = ...,
        compatibility: _Optional[_Union[CompatibilityInfo, _Mapping]] = ...,
    ) -> None: ...

class CompatibilityInfo(_message.Message):
    __slots__ = ("tier", "tier_name", "requested_distro", "matched_distro", "message")
    TIER_FIELD_NUMBER: _ClassVar[int]
    TIER_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_DISTRO_FIELD_NUMBER: _ClassVar[int]
    MATCHED_DISTRO_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    tier: int
    tier_name: str
    requested_distro: str
    matched_distro: str
    message: str
    def __init__(
        self,
        tier: _Optional[int] = ...,
        tier_name: _Optional[str] = ...,
        requested_distro: _Optional[str] = ...,
        matched_distro: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class GetCapabilityReleaseRequest(_message.Message):
    __slots__ = ("os", "arch", "channel", "capability", "semver", "distro")
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    SEMVER_FIELD_NUMBER: _ClassVar[int]
    DISTRO_FIELD_NUMBER: _ClassVar[int]
    os: str
    arch: str
    channel: str
    capability: str
    semver: str
    distro: str
    def __init__(
        self,
        os: _Optional[str] = ...,
        arch: _Optional[str] = ...,
        channel: _Optional[str] = ...,
        capability: _Optional[str] = ...,
        semver: _Optional[str] = ...,
        distro: _Optional[str] = ...,
    ) -> None: ...

class GetCapabilityReleaseResponse(_message.Message):
    __slots__ = ("release",)
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    release: CapabilityRelease
    def __init__(
        self, release: _Optional[_Union[CapabilityRelease, _Mapping]] = ...
    ) -> None: ...

class GetCapabilityLatestReleasesRequest(_message.Message):
    __slots__ = ("os", "arch", "channel", "install_id", "capabilities", "distro")
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    INSTALL_ID_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    DISTRO_FIELD_NUMBER: _ClassVar[int]
    os: str
    arch: str
    channel: str
    install_id: str
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    distro: str
    def __init__(
        self,
        os: _Optional[str] = ...,
        arch: _Optional[str] = ...,
        channel: _Optional[str] = ...,
        install_id: _Optional[str] = ...,
        capabilities: _Optional[_Iterable[str]] = ...,
        distro: _Optional[str] = ...,
    ) -> None: ...

class GetCapabilitySupportedDistrosRequest(_message.Message):
    __slots__ = ("capabilities",)
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, capabilities: _Optional[_Iterable[str]] = ...) -> None: ...

class CapabilitySupportedDistro(_message.Message):
    __slots__ = ("capability", "distros")
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    DISTROS_FIELD_NUMBER: _ClassVar[int]
    capability: str
    distros: _containers.RepeatedCompositeFieldContainer[CapabilityDistro]
    def __init__(
        self,
        capability: _Optional[str] = ...,
        distros: _Optional[_Iterable[_Union[CapabilityDistro, _Mapping]]] = ...,
    ) -> None: ...

class CapabilityDistro(_message.Message):
    __slots__ = ("distro", "arch", "os")
    DISTRO_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    distro: str
    arch: str
    os: str
    def __init__(
        self,
        distro: _Optional[str] = ...,
        arch: _Optional[str] = ...,
        os: _Optional[str] = ...,
    ) -> None: ...

class GetCapabilitySupportedDistrosResponse(_message.Message):
    __slots__ = ("capabilities",)
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    capabilities: _containers.RepeatedCompositeFieldContainer[CapabilitySupportedDistro]
    def __init__(
        self,
        capabilities: _Optional[
            _Iterable[_Union[CapabilitySupportedDistro, _Mapping]]
        ] = ...,
    ) -> None: ...

class GetCapabilityLatestReleasesResponse(_message.Message):
    __slots__ = ("releases",)
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    releases: _containers.RepeatedCompositeFieldContainer[CapabilityRelease]
    def __init__(
        self, releases: _Optional[_Iterable[_Union[CapabilityRelease, _Mapping]]] = ...
    ) -> None: ...

class Capability(_message.Message):
    __slots__ = ("name", "display_name", "description", "seed_bundle_id", "seed_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SEED_BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
    SEED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    description: str
    seed_bundle_id: str
    seed_config: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        seed_bundle_id: _Optional[str] = ...,
        seed_config: _Optional[str] = ...,
    ) -> None: ...

class CreateCapabilityRequest(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    def __init__(
        self, capability: _Optional[_Union[Capability, _Mapping]] = ...
    ) -> None: ...

class CreateCapabilityResponse(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    def __init__(
        self, capability: _Optional[_Union[Capability, _Mapping]] = ...
    ) -> None: ...

class UpdateCapabilityRequest(_message.Message):
    __slots__ = ("capability", "update_mask")
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        capability: _Optional[_Union[Capability, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateCapabilityResponse(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    def __init__(
        self, capability: _Optional[_Union[Capability, _Mapping]] = ...
    ) -> None: ...

class DeleteCapabilityRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteCapabilityResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCapabilitiesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCapabilitiesResponse(_message.Message):
    __slots__ = ("capabilities",)
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    capabilities: _containers.RepeatedCompositeFieldContainer[Capability]
    def __init__(
        self, capabilities: _Optional[_Iterable[_Union[Capability, _Mapping]]] = ...
    ) -> None: ...

class GetCapabilityRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetCapabilityResponse(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    def __init__(
        self, capability: _Optional[_Union[Capability, _Mapping]] = ...
    ) -> None: ...
