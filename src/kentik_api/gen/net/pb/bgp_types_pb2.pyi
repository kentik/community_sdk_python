from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class Afi(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AFI_UNSPECIFIED: _ClassVar[Afi]
    AFI_IP4: _ClassVar[Afi]
    AFI_IP6: _ClassVar[Afi]

class Safi(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SAFI_UNSPECIFIED: _ClassVar[Safi]
    SAFI_UNICAST: _ClassVar[Safi]
    SAFI_MPLS: _ClassVar[Safi]
    SAFI_L3VPN: _ClassVar[Safi]

class RpkiStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RPKI_STATUS_UNSPECIFIED: _ClassVar[RpkiStatus]
    RPKI_STATUS_NOT_FOUND: _ClassVar[RpkiStatus]
    RPKI_STATUS_EXPLICIT_INVALID: _ClassVar[RpkiStatus]
    RPKI_STATUS_INVALID_PREFIX: _ClassVar[RpkiStatus]
    RPKI_STATUS_INVALID: _ClassVar[RpkiStatus]
    RPKI_STATUS_VALID: _ClassVar[RpkiStatus]
    RPKI_STATUS_ERROR: _ClassVar[RpkiStatus]

AFI_UNSPECIFIED: Afi
AFI_IP4: Afi
AFI_IP6: Afi
SAFI_UNSPECIFIED: Safi
SAFI_UNICAST: Safi
SAFI_MPLS: Safi
SAFI_L3VPN: Safi
RPKI_STATUS_UNSPECIFIED: RpkiStatus
RPKI_STATUS_NOT_FOUND: RpkiStatus
RPKI_STATUS_EXPLICIT_INVALID: RpkiStatus
RPKI_STATUS_INVALID_PREFIX: RpkiStatus
RPKI_STATUS_INVALID: RpkiStatus
RPKI_STATUS_VALID: RpkiStatus
RPKI_STATUS_ERROR: RpkiStatus

class VantagePoint(_message.Message):
    __slots__ = ("dataset", "collector", "peer_asn", "peer_ip")
    DATASET_FIELD_NUMBER: _ClassVar[int]
    COLLECTOR_FIELD_NUMBER: _ClassVar[int]
    PEER_ASN_FIELD_NUMBER: _ClassVar[int]
    PEER_IP_FIELD_NUMBER: _ClassVar[int]
    dataset: str
    collector: str
    peer_asn: int
    peer_ip: str
    def __init__(
        self,
        dataset: _Optional[str] = ...,
        collector: _Optional[str] = ...,
        peer_asn: _Optional[int] = ...,
        peer_ip: _Optional[str] = ...,
    ) -> None: ...
