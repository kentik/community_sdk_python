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

class CloudType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_TYPE_UNSPECIFIED: _ClassVar[CloudType]
    CLOUD_TYPE_AWS: _ClassVar[CloudType]
    CLOUD_TYPE_AZURE: _ClassVar[CloudType]
    CLOUD_TYPE_GCE: _ClassVar[CloudType]
    CLOUD_TYPE_IBM: _ClassVar[CloudType]

CLOUD_TYPE_UNSPECIFIED: CloudType
CLOUD_TYPE_AWS: CloudType
CLOUD_TYPE_AZURE: CloudType
CLOUD_TYPE_GCE: CloudType
CLOUD_TYPE_IBM: CloudType

class CloudSubnet(_message.Message):
    __slots__ = ("type", "subnets")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    type: CloudType
    subnets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        type: _Optional[_Union[CloudType, str]] = ...,
        subnets: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class NetworkClass(_message.Message):
    __slots__ = (
        "internal_asns",
        "internal_ips",
        "use_private_asns",
        "use_private_subnets",
        "cloud_subnets",
    )
    INTERNAL_ASNS_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_IPS_FIELD_NUMBER: _ClassVar[int]
    USE_PRIVATE_ASNS_FIELD_NUMBER: _ClassVar[int]
    USE_PRIVATE_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    CLOUD_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    internal_asns: _containers.RepeatedScalarFieldContainer[str]
    internal_ips: _containers.RepeatedScalarFieldContainer[str]
    use_private_asns: bool
    use_private_subnets: bool
    cloud_subnets: _containers.RepeatedCompositeFieldContainer[CloudSubnet]
    def __init__(
        self,
        internal_asns: _Optional[_Iterable[str]] = ...,
        internal_ips: _Optional[_Iterable[str]] = ...,
        use_private_asns: _Optional[bool] = ...,
        use_private_subnets: _Optional[bool] = ...,
        cloud_subnets: _Optional[_Iterable[_Union[CloudSubnet, _Mapping]]] = ...,
    ) -> None: ...

class GetNetworkClassRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNetworkClassResponse(_message.Message):
    __slots__ = ("network_class",)
    NETWORK_CLASS_FIELD_NUMBER: _ClassVar[int]
    network_class: NetworkClass
    def __init__(
        self, network_class: _Optional[_Union[NetworkClass, _Mapping]] = ...
    ) -> None: ...

class UpdateNetworkClassRequest(_message.Message):
    __slots__ = ("network_class",)
    NETWORK_CLASS_FIELD_NUMBER: _ClassVar[int]
    network_class: NetworkClass
    def __init__(
        self, network_class: _Optional[_Union[NetworkClass, _Mapping]] = ...
    ) -> None: ...

class UpdateNetworkClassResponse(_message.Message):
    __slots__ = ("network_class",)
    NETWORK_CLASS_FIELD_NUMBER: _ClassVar[int]
    network_class: NetworkClass
    def __init__(
        self, network_class: _Optional[_Union[NetworkClass, _Mapping]] = ...
    ) -> None: ...
