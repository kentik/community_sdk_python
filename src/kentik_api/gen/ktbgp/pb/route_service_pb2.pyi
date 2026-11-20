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
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class InetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INET_TYPE_UNSPECIFIED: _ClassVar[InetType]
    INET_TYPE_IPV4: _ClassVar[InetType]
    INET_TYPE_IPV6: _ClassVar[InetType]

class ExtendedCommunityRouteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXTENDED_COMMUNITY_ROUTE_TYPE_UNSPECIFIED: _ClassVar[ExtendedCommunityRouteType]
    EXTENDED_COMMUNITY_ROUTE_TYPE_TARGET: _ClassVar[ExtendedCommunityRouteType]
    EXTENDED_COMMUNITY_ROUTE_TYPE_ORIGIN: _ClassVar[ExtendedCommunityRouteType]

class Fragment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FRAGMENT_UNSPECIFIED: _ClassVar[Fragment]
    FRAGMENT_DF: _ClassVar[Fragment]
    FRAGMENT_ISF: _ClassVar[Fragment]
    FRAGMENT_FF: _ClassVar[Fragment]
    FRAGMENT_LF: _ClassVar[Fragment]

class TCPFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TCP_FLAG_UNSPECIFIED: _ClassVar[TCPFlag]
    TCP_FLAG_FIN: _ClassVar[TCPFlag]
    TCP_FLAG_SYN: _ClassVar[TCPFlag]
    TCP_FLAG_RST: _ClassVar[TCPFlag]
    TCP_FLAG_PSH: _ClassVar[TCPFlag]
    TCP_FLAG_ACK: _ClassVar[TCPFlag]
    TCP_FLAG_URG: _ClassVar[TCPFlag]
    TCP_FLAG_ECE: _ClassVar[TCPFlag]
    TCP_FLAG_CWR: _ClassVar[TCPFlag]

class NumericOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NUMERIC_OP_UNSPECIFIED: _ClassVar[NumericOp]
    NUMERIC_OP_EQUALS: _ClassVar[NumericOp]
    NUMERIC_OP_NOT_EQUALS: _ClassVar[NumericOp]
    NUMERIC_OP_LESS_THAN: _ClassVar[NumericOp]
    NUMERIC_OP_GREATER_THAN: _ClassVar[NumericOp]
    NUMERIC_OP_LESS_THAN_OR_EQUALS: _ClassVar[NumericOp]
    NUMERIC_OP_GREATER_THAN_OR_EQUALS: _ClassVar[NumericOp]

class BitwiseOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BITWISE_OP_UNSPECIFIED: _ClassVar[BitwiseOp]
    BITWISE_OP_ANY: _ClassVar[BitwiseOp]
    BITWISE_OP_NONE: _ClassVar[BitwiseOp]
    BITWISE_OP_ALL: _ClassVar[BitwiseOp]
    BITWISE_OP_NOT_ALL: _ClassVar[BitwiseOp]

class AdvertStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADVERT_STATUS_UNSPECIFIED: _ClassVar[AdvertStatus]
    ADVERT_STATUS_ANNOUNCED: _ClassVar[AdvertStatus]
    ADVERT_STATUS_WITHDRAWN: _ClassVar[AdvertStatus]
    ADVERT_STATUS_NO_SESSION: _ClassVar[AdvertStatus]
    ADVERT_STATUS_FAILED: _ClassVar[AdvertStatus]

INET_TYPE_UNSPECIFIED: InetType
INET_TYPE_IPV4: InetType
INET_TYPE_IPV6: InetType
EXTENDED_COMMUNITY_ROUTE_TYPE_UNSPECIFIED: ExtendedCommunityRouteType
EXTENDED_COMMUNITY_ROUTE_TYPE_TARGET: ExtendedCommunityRouteType
EXTENDED_COMMUNITY_ROUTE_TYPE_ORIGIN: ExtendedCommunityRouteType
FRAGMENT_UNSPECIFIED: Fragment
FRAGMENT_DF: Fragment
FRAGMENT_ISF: Fragment
FRAGMENT_FF: Fragment
FRAGMENT_LF: Fragment
TCP_FLAG_UNSPECIFIED: TCPFlag
TCP_FLAG_FIN: TCPFlag
TCP_FLAG_SYN: TCPFlag
TCP_FLAG_RST: TCPFlag
TCP_FLAG_PSH: TCPFlag
TCP_FLAG_ACK: TCPFlag
TCP_FLAG_URG: TCPFlag
TCP_FLAG_ECE: TCPFlag
TCP_FLAG_CWR: TCPFlag
NUMERIC_OP_UNSPECIFIED: NumericOp
NUMERIC_OP_EQUALS: NumericOp
NUMERIC_OP_NOT_EQUALS: NumericOp
NUMERIC_OP_LESS_THAN: NumericOp
NUMERIC_OP_GREATER_THAN: NumericOp
NUMERIC_OP_LESS_THAN_OR_EQUALS: NumericOp
NUMERIC_OP_GREATER_THAN_OR_EQUALS: NumericOp
BITWISE_OP_UNSPECIFIED: BitwiseOp
BITWISE_OP_ANY: BitwiseOp
BITWISE_OP_NONE: BitwiseOp
BITWISE_OP_ALL: BitwiseOp
BITWISE_OP_NOT_ALL: BitwiseOp
ADVERT_STATUS_UNSPECIFIED: AdvertStatus
ADVERT_STATUS_ANNOUNCED: AdvertStatus
ADVERT_STATUS_WITHDRAWN: AdvertStatus
ADVERT_STATUS_NO_SESSION: AdvertStatus
ADVERT_STATUS_FAILED: AdvertStatus

class RouteServiceAnnounceRequest(_message.Message):
    __slots__ = ("device_ids", "flowspec", "rtbh")
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    RTBH_FIELD_NUMBER: _ClassVar[int]
    device_ids: _containers.RepeatedScalarFieldContainer[int]
    flowspec: FlowspecUpdate
    rtbh: RTBHUpdate
    def __init__(
        self,
        device_ids: _Optional[_Iterable[int]] = ...,
        flowspec: _Optional[_Union[FlowspecUpdate, _Mapping]] = ...,
        rtbh: _Optional[_Union[RTBHUpdate, _Mapping]] = ...,
    ) -> None: ...

class RouteServiceAnnounceResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[UpdateResult]
    def __init__(
        self, results: _Optional[_Iterable[_Union[UpdateResult, _Mapping]]] = ...
    ) -> None: ...

class RouteServiceWithdrawRequest(_message.Message):
    __slots__ = ("device_ids", "withdraw")
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    WITHDRAW_FIELD_NUMBER: _ClassVar[int]
    device_ids: _containers.RepeatedScalarFieldContainer[int]
    withdraw: Withdraw
    def __init__(
        self,
        device_ids: _Optional[_Iterable[int]] = ...,
        withdraw: _Optional[_Union[Withdraw, _Mapping]] = ...,
    ) -> None: ...

class Withdraw(_message.Message):
    __slots__ = ("flowspec", "rtbh")
    FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    RTBH_FIELD_NUMBER: _ClassVar[int]
    flowspec: FlowspecMatch
    rtbh: RTBHMatch
    def __init__(
        self,
        flowspec: _Optional[_Union[FlowspecMatch, _Mapping]] = ...,
        rtbh: _Optional[_Union[RTBHMatch, _Mapping]] = ...,
    ) -> None: ...

class RouteServiceWithdrawResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[UpdateResult]
    def __init__(
        self, results: _Optional[_Iterable[_Union[UpdateResult, _Mapping]]] = ...
    ) -> None: ...

class FlowspecAction(_message.Message):
    __slots__ = (
        "accept",
        "discard",
        "rate_bytes",
        "mark_dscp",
        "rt_redirect",
        "ip_redirect",
        "action_type",
        "rt_copy",
        "regular_community",
        "extended_community",
        "large_community",
    )
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    DISCARD_FIELD_NUMBER: _ClassVar[int]
    RATE_BYTES_FIELD_NUMBER: _ClassVar[int]
    MARK_DSCP_FIELD_NUMBER: _ClassVar[int]
    RT_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    IP_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    RT_COPY_FIELD_NUMBER: _ClassVar[int]
    REGULAR_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    LARGE_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    accept: FlowspecActionAccept
    discard: FlowspecActionDiscard
    rate_bytes: FlowspecActionTrafficRateBytes
    mark_dscp: FlowspecActionMarkDSCP
    rt_redirect: FlowspecActionRouteTargetRedirect
    ip_redirect: FlowspecActionIPNextHopRedirect
    action_type: FlowspecActionTerminalSample
    rt_copy: FlowspecActionIPNextHopCopy
    regular_community: FlowspecActionRegularCommunity
    extended_community: FlowspecActionExtendedCommunity
    large_community: FlowspecActionLargeCommunity
    def __init__(
        self,
        accept: _Optional[_Union[FlowspecActionAccept, _Mapping]] = ...,
        discard: _Optional[_Union[FlowspecActionDiscard, _Mapping]] = ...,
        rate_bytes: _Optional[_Union[FlowspecActionTrafficRateBytes, _Mapping]] = ...,
        mark_dscp: _Optional[_Union[FlowspecActionMarkDSCP, _Mapping]] = ...,
        rt_redirect: _Optional[
            _Union[FlowspecActionRouteTargetRedirect, _Mapping]
        ] = ...,
        ip_redirect: _Optional[_Union[FlowspecActionIPNextHopRedirect, _Mapping]] = ...,
        action_type: _Optional[_Union[FlowspecActionTerminalSample, _Mapping]] = ...,
        rt_copy: _Optional[_Union[FlowspecActionIPNextHopCopy, _Mapping]] = ...,
        regular_community: _Optional[
            _Union[FlowspecActionRegularCommunity, _Mapping]
        ] = ...,
        extended_community: _Optional[
            _Union[FlowspecActionExtendedCommunity, _Mapping]
        ] = ...,
        large_community: _Optional[
            _Union[FlowspecActionLargeCommunity, _Mapping]
        ] = ...,
    ) -> None: ...

class FlowspecUpdate(_message.Message):
    __slots__ = (
        "match",
        "creation_time",
        "inet",
        "inet_type",
        "key",
        "rate_bytes",
        "discard",
        "mark_dscp",
        "rt_redirect",
        "ip_redirect",
        "accept",
        "action_type",
        "rt_copy",
        "regular_community",
        "extended_community",
        "large_community",
        "actions",
        "terminal",
        "sample",
    )
    MATCH_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    INET_FIELD_NUMBER: _ClassVar[int]
    INET_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    RATE_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISCARD_FIELD_NUMBER: _ClassVar[int]
    MARK_DSCP_FIELD_NUMBER: _ClassVar[int]
    RT_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    IP_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    RT_COPY_FIELD_NUMBER: _ClassVar[int]
    REGULAR_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    LARGE_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    TERMINAL_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FIELD_NUMBER: _ClassVar[int]
    match: FlowspecMatch
    creation_time: _timestamp_pb2.Timestamp
    inet: str
    inet_type: InetType
    key: str
    rate_bytes: FlowspecActionTrafficRateBytes
    discard: FlowspecActionDiscard
    mark_dscp: FlowspecActionMarkDSCP
    rt_redirect: FlowspecActionRouteTargetRedirect
    ip_redirect: FlowspecActionIPNextHopRedirect
    accept: FlowspecActionAccept
    action_type: FlowspecActionTerminalSample
    rt_copy: FlowspecActionIPNextHopCopy
    regular_community: FlowspecActionRegularCommunity
    extended_community: FlowspecActionExtendedCommunity
    large_community: FlowspecActionLargeCommunity
    actions: _containers.RepeatedCompositeFieldContainer[FlowspecAction]
    terminal: bool
    sample: bool
    def __init__(
        self,
        match: _Optional[_Union[FlowspecMatch, _Mapping]] = ...,
        creation_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        inet: _Optional[str] = ...,
        inet_type: _Optional[_Union[InetType, str]] = ...,
        key: _Optional[str] = ...,
        rate_bytes: _Optional[_Union[FlowspecActionTrafficRateBytes, _Mapping]] = ...,
        discard: _Optional[_Union[FlowspecActionDiscard, _Mapping]] = ...,
        mark_dscp: _Optional[_Union[FlowspecActionMarkDSCP, _Mapping]] = ...,
        rt_redirect: _Optional[
            _Union[FlowspecActionRouteTargetRedirect, _Mapping]
        ] = ...,
        ip_redirect: _Optional[_Union[FlowspecActionIPNextHopRedirect, _Mapping]] = ...,
        accept: _Optional[_Union[FlowspecActionAccept, _Mapping]] = ...,
        action_type: _Optional[_Union[FlowspecActionTerminalSample, _Mapping]] = ...,
        rt_copy: _Optional[_Union[FlowspecActionIPNextHopCopy, _Mapping]] = ...,
        regular_community: _Optional[
            _Union[FlowspecActionRegularCommunity, _Mapping]
        ] = ...,
        extended_community: _Optional[
            _Union[FlowspecActionExtendedCommunity, _Mapping]
        ] = ...,
        large_community: _Optional[
            _Union[FlowspecActionLargeCommunity, _Mapping]
        ] = ...,
        actions: _Optional[_Iterable[_Union[FlowspecAction, _Mapping]]] = ...,
        terminal: _Optional[bool] = ...,
        sample: _Optional[bool] = ...,
    ) -> None: ...

class FlowspecUpdates(_message.Message):
    __slots__ = ("update",)
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    update: _containers.RepeatedCompositeFieldContainer[FlowspecUpdate]
    def __init__(
        self, update: _Optional[_Iterable[_Union[FlowspecUpdate, _Mapping]]] = ...
    ) -> None: ...

class RTBHUpdate(_message.Message):
    __slots__ = ("match", "action", "creation_time", "inet", "inet_type", "key")
    MATCH_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    INET_FIELD_NUMBER: _ClassVar[int]
    INET_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    match: RTBHMatch
    action: RTBHAction
    creation_time: _timestamp_pb2.Timestamp
    inet: str
    inet_type: InetType
    key: str
    def __init__(
        self,
        match: _Optional[_Union[RTBHMatch, _Mapping]] = ...,
        action: _Optional[_Union[RTBHAction, _Mapping]] = ...,
        creation_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        inet: _Optional[str] = ...,
        inet_type: _Optional[_Union[InetType, str]] = ...,
        key: _Optional[str] = ...,
    ) -> None: ...

class RTBHUpdates(_message.Message):
    __slots__ = ("update",)
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    update: _containers.RepeatedCompositeFieldContainer[RTBHUpdate]
    def __init__(
        self, update: _Optional[_Iterable[_Union[RTBHUpdate, _Mapping]]] = ...
    ) -> None: ...

class FlowspecMatch(_message.Message):
    __slots__ = (
        "dst_prefix",
        "src_prefix",
        "ip_protocol",
        "dst_port",
        "src_port",
        "icmp_type",
        "icmp_code",
        "tcp_flags",
        "packet_length",
        "dscp",
        "fragments",
    )
    DST_PREFIX_FIELD_NUMBER: _ClassVar[int]
    SRC_PREFIX_FIELD_NUMBER: _ClassVar[int]
    IP_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    DST_PORT_FIELD_NUMBER: _ClassVar[int]
    SRC_PORT_FIELD_NUMBER: _ClassVar[int]
    ICMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    ICMP_CODE_FIELD_NUMBER: _ClassVar[int]
    TCP_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PACKET_LENGTH_FIELD_NUMBER: _ClassVar[int]
    DSCP_FIELD_NUMBER: _ClassVar[int]
    FRAGMENTS_FIELD_NUMBER: _ClassVar[int]
    dst_prefix: str
    src_prefix: str
    ip_protocol: NumericFormula
    dst_port: NumericFormula
    src_port: NumericFormula
    icmp_type: NumericFormula
    icmp_code: NumericFormula
    tcp_flags: TCPFlagsFormula
    packet_length: NumericFormula
    dscp: NumericFormula
    fragments: FragmentFormula
    def __init__(
        self,
        dst_prefix: _Optional[str] = ...,
        src_prefix: _Optional[str] = ...,
        ip_protocol: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        dst_port: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        src_port: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        icmp_type: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        icmp_code: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        tcp_flags: _Optional[_Union[TCPFlagsFormula, _Mapping]] = ...,
        packet_length: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        dscp: _Optional[_Union[NumericFormula, _Mapping]] = ...,
        fragments: _Optional[_Union[FragmentFormula, _Mapping]] = ...,
    ) -> None: ...

class FlowspecActionTrafficRateBytes(_message.Message):
    __slots__ = ("bytes_per_second",)
    BYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    bytes_per_second: float
    def __init__(self, bytes_per_second: _Optional[float] = ...) -> None: ...

class FlowspecActionAccept(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FlowspecActionDiscard(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FlowspecActionTerminalSample(_message.Message):
    __slots__ = ("terminal", "sample")
    TERMINAL_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FIELD_NUMBER: _ClassVar[int]
    terminal: bool
    sample: bool
    def __init__(
        self, terminal: _Optional[bool] = ..., sample: _Optional[bool] = ...
    ) -> None: ...

class FlowspecActionMarkDSCP(_message.Message):
    __slots__ = ("dscp",)
    DSCP_FIELD_NUMBER: _ClassVar[int]
    dscp: int
    def __init__(self, dscp: _Optional[int] = ...) -> None: ...

class FlowspecActionRouteTargetRedirect(_message.Message):
    __slots__ = ("asn", "route_target")
    ASN_FIELD_NUMBER: _ClassVar[int]
    ROUTE_TARGET_FIELD_NUMBER: _ClassVar[int]
    asn: int
    route_target: int
    def __init__(
        self, asn: _Optional[int] = ..., route_target: _Optional[int] = ...
    ) -> None: ...

class FlowspecActionIPNextHopRedirect(_message.Message):
    __slots__ = ("next_hop",)
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    next_hop: str
    def __init__(self, next_hop: _Optional[str] = ...) -> None: ...

class FlowspecActionIPNextHopCopy(_message.Message):
    __slots__ = ("next_hop",)
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    next_hop: str
    def __init__(self, next_hop: _Optional[str] = ...) -> None: ...

class FlowspecActionRegularCommunity(_message.Message):
    __slots__ = ("asn1", "asn2")
    ASN1_FIELD_NUMBER: _ClassVar[int]
    ASN2_FIELD_NUMBER: _ClassVar[int]
    asn1: int
    asn2: int
    def __init__(
        self, asn1: _Optional[int] = ..., asn2: _Optional[int] = ...
    ) -> None: ...

class FlowspecActionExtendedCommunity(_message.Message):
    __slots__ = ("route_type", "asn1", "asn2")
    ROUTE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASN1_FIELD_NUMBER: _ClassVar[int]
    ASN2_FIELD_NUMBER: _ClassVar[int]
    route_type: ExtendedCommunityRouteType
    asn1: int
    asn2: int
    def __init__(
        self,
        route_type: _Optional[_Union[ExtendedCommunityRouteType, str]] = ...,
        asn1: _Optional[int] = ...,
        asn2: _Optional[int] = ...,
    ) -> None: ...

class FlowspecActionLargeCommunity(_message.Message):
    __slots__ = ("asn", "data1", "data2")
    ASN_FIELD_NUMBER: _ClassVar[int]
    DATA1_FIELD_NUMBER: _ClassVar[int]
    DATA2_FIELD_NUMBER: _ClassVar[int]
    asn: int
    data1: int
    data2: int
    def __init__(
        self,
        asn: _Optional[int] = ...,
        data1: _Optional[int] = ...,
        data2: _Optional[int] = ...,
    ) -> None: ...

class RTBHMatch(_message.Message):
    __slots__ = ("src_prefix",)
    SRC_PREFIX_FIELD_NUMBER: _ClassVar[int]
    src_prefix: str
    def __init__(self, src_prefix: _Optional[str] = ...) -> None: ...

class RTBHAction(_message.Message):
    __slots__ = ("bgp_communities", "next_hop", "local_preference")
    BGP_COMMUNITIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    LOCAL_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    bgp_communities: _containers.RepeatedScalarFieldContainer[int]
    next_hop: str
    local_preference: int
    def __init__(
        self,
        bgp_communities: _Optional[_Iterable[int]] = ...,
        next_hop: _Optional[str] = ...,
        local_preference: _Optional[int] = ...,
    ) -> None: ...

class NumericFormula(_message.Message):
    __slots__ = ()
    OR_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class NumericPredicateGroup(_message.Message):
    __slots__ = ()
    AND_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class NumericPredicate(_message.Message):
    __slots__ = ("operator", "value")
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    operator: NumericOp
    value: int
    def __init__(
        self,
        operator: _Optional[_Union[NumericOp, str]] = ...,
        value: _Optional[int] = ...,
    ) -> None: ...

class FragmentFormula(_message.Message):
    __slots__ = ()
    OR_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class FragmentPredicateGroup(_message.Message):
    __slots__ = ()
    AND_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class FragmentPredicate(_message.Message):
    __slots__ = ("operator", "values")
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    operator: BitwiseOp
    values: _containers.RepeatedScalarFieldContainer[Fragment]
    def __init__(
        self,
        operator: _Optional[_Union[BitwiseOp, str]] = ...,
        values: _Optional[_Iterable[_Union[Fragment, str]]] = ...,
    ) -> None: ...

class TCPFlagsFormula(_message.Message):
    __slots__ = ()
    OR_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class TCPFlagsPredicateGroup(_message.Message):
    __slots__ = ()
    AND_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, **kwargs) -> None: ...

class TCPFlagsPredicate(_message.Message):
    __slots__ = ("operator", "values")
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    operator: BitwiseOp
    values: _containers.RepeatedScalarFieldContainer[TCPFlag]
    def __init__(
        self,
        operator: _Optional[_Union[BitwiseOp, str]] = ...,
        values: _Optional[_Iterable[_Union[TCPFlag, str]]] = ...,
    ) -> None: ...

class UpdateResult(_message.Message):
    __slots__ = ("device_id", "status", "message")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    status: AdvertStatus
    message: str
    def __init__(
        self,
        device_id: _Optional[int] = ...,
        status: _Optional[_Union[AdvertStatus, str]] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class RouteServiceListRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: RoutesFilter
    def __init__(
        self, filters: _Optional[_Union[RoutesFilter, _Mapping]] = ...
    ) -> None: ...

class RoutesFilter(_message.Message):
    __slots__ = ("device_ids",)
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    device_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, device_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class RouteServiceListResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _containers.RepeatedCompositeFieldContainer[DeviceAdverts]
    def __init__(
        self, result: _Optional[_Iterable[_Union[DeviceAdverts, _Mapping]]] = ...
    ) -> None: ...

class DeviceAdverts(_message.Message):
    __slots__ = ("device_id", "flowspec", "rtbh")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    RTBH_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    flowspec: _containers.RepeatedCompositeFieldContainer[FlowspecUpdate]
    rtbh: _containers.RepeatedCompositeFieldContainer[RTBHUpdate]
    def __init__(
        self,
        device_id: _Optional[int] = ...,
        flowspec: _Optional[_Iterable[_Union[FlowspecUpdate, _Mapping]]] = ...,
        rtbh: _Optional[_Iterable[_Union[RTBHUpdate, _Mapping]]] = ...,
    ) -> None: ...
