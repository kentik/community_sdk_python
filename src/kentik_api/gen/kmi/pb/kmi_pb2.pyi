from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Market(_message.Message):
    __slots__ = ("market_id", "name")
    MARKET_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    market_id: str
    name: str
    def __init__(
        self, market_id: _Optional[str] = ..., name: _Optional[str] = ...
    ) -> None: ...

class Ranking(_message.Message):
    __slots__ = ("asn", "name", "rank", "rank_change", "score", "score_change")
    ASN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    RANK_CHANGE_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    SCORE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    asn: int
    name: str
    rank: int
    rank_change: int
    score: int
    score_change: int
    def __init__(
        self,
        asn: _Optional[int] = ...,
        name: _Optional[str] = ...,
        rank: _Optional[int] = ...,
        rank_change: _Optional[int] = ...,
        score: _Optional[int] = ...,
        score_change: _Optional[int] = ...,
    ) -> None: ...

class CustomerProvider(_message.Message):
    __slots__ = (
        "asn",
        "name",
        "score",
        "singlehomed_customer",
        "mutual_customer",
        "mutual_provider",
    )
    ASN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    SINGLEHOMED_CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    MUTUAL_CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    MUTUAL_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    asn: int
    name: str
    score: int
    singlehomed_customer: bool
    mutual_customer: bool
    mutual_provider: bool
    def __init__(
        self,
        asn: _Optional[int] = ...,
        name: _Optional[str] = ...,
        score: _Optional[int] = ...,
        singlehomed_customer: _Optional[bool] = ...,
        mutual_customer: _Optional[bool] = ...,
        mutual_provider: _Optional[bool] = ...,
    ) -> None: ...

class Peer(_message.Message):
    __slots__ = ("asn", "name", "pfx_count")
    ASN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PFX_COUNT_FIELD_NUMBER: _ClassVar[int]
    asn: int
    name: str
    pfx_count: int
    def __init__(
        self,
        asn: _Optional[int] = ...,
        name: _Optional[str] = ...,
        pfx_count: _Optional[int] = ...,
    ) -> None: ...

class ASNDetails(_message.Message):
    __slots__ = ("asn", "name", "country_name", "customers", "providers", "peers")
    ASN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    PEERS_FIELD_NUMBER: _ClassVar[int]
    asn: int
    name: str
    country_name: str
    customers: _containers.RepeatedCompositeFieldContainer[CustomerProvider]
    providers: _containers.RepeatedCompositeFieldContainer[CustomerProvider]
    peers: _containers.RepeatedCompositeFieldContainer[Peer]
    def __init__(
        self,
        asn: _Optional[int] = ...,
        name: _Optional[str] = ...,
        country_name: _Optional[str] = ...,
        customers: _Optional[_Iterable[_Union[CustomerProvider, _Mapping]]] = ...,
        providers: _Optional[_Iterable[_Union[CustomerProvider, _Mapping]]] = ...,
        peers: _Optional[_Iterable[_Union[Peer, _Mapping]]] = ...,
    ) -> None: ...

class Insight(_message.Message):
    __slots__ = ("asn", "name", "type", "message", "created_at")
    ASN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    asn: int
    name: str
    type: int
    message: str
    created_at: str
    def __init__(
        self,
        asn: _Optional[int] = ...,
        name: _Optional[str] = ...,
        type: _Optional[int] = ...,
        message: _Optional[str] = ...,
        created_at: _Optional[str] = ...,
    ) -> None: ...

class ListMarketsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMarketsResponse(_message.Message):
    __slots__ = ("markets",)
    MARKETS_FIELD_NUMBER: _ClassVar[int]
    markets: _containers.RepeatedCompositeFieldContainer[Market]
    def __init__(
        self, markets: _Optional[_Iterable[_Union[Market, _Mapping]]] = ...
    ) -> None: ...

class GetRankingsRequest(_message.Message):
    __slots__ = ("market_id", "rank_type", "ip", "limit")
    MARKET_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    market_id: str
    rank_type: str
    ip: str
    limit: int
    def __init__(
        self,
        market_id: _Optional[str] = ...,
        rank_type: _Optional[str] = ...,
        ip: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class GetRankingsResponse(_message.Message):
    __slots__ = ("rankings", "invalid_count")
    RANKINGS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    rankings: _containers.RepeatedCompositeFieldContainer[Ranking]
    invalid_count: int
    def __init__(
        self,
        rankings: _Optional[_Iterable[_Union[Ranking, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetASNDetailsRequest(_message.Message):
    __slots__ = (
        "market_id",
        "asn",
        "ip",
        "type",
        "mutual_provider",
        "mutual_customer",
        "singlehomed_customer",
    )
    MARKET_ID_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MUTUAL_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MUTUAL_CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    SINGLEHOMED_CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    market_id: str
    asn: str
    ip: str
    type: str
    mutual_provider: str
    mutual_customer: str
    singlehomed_customer: str
    def __init__(
        self,
        market_id: _Optional[str] = ...,
        asn: _Optional[str] = ...,
        ip: _Optional[str] = ...,
        type: _Optional[str] = ...,
        mutual_provider: _Optional[str] = ...,
        mutual_customer: _Optional[str] = ...,
        singlehomed_customer: _Optional[str] = ...,
    ) -> None: ...

class GetASNDetailsResponse(_message.Message):
    __slots__ = ("asn_details",)
    ASN_DETAILS_FIELD_NUMBER: _ClassVar[int]
    asn_details: ASNDetails
    def __init__(
        self, asn_details: _Optional[_Union[ASNDetails, _Mapping]] = ...
    ) -> None: ...

class GetGlobalInsightsRequest(_message.Message):
    __slots__ = ("limit", "market_id", "ip", "lookback", "types", "magnitude")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MARKET_ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    LOOKBACK_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    limit: int
    market_id: str
    ip: str
    lookback: int
    types: _containers.RepeatedScalarFieldContainer[str]
    magnitude: int
    def __init__(
        self,
        limit: _Optional[int] = ...,
        market_id: _Optional[str] = ...,
        ip: _Optional[str] = ...,
        lookback: _Optional[int] = ...,
        types: _Optional[_Iterable[str]] = ...,
        magnitude: _Optional[int] = ...,
    ) -> None: ...

class GetGlobalInsightsResponse(_message.Message):
    __slots__ = ("insights",)
    INSIGHTS_FIELD_NUMBER: _ClassVar[int]
    insights: _containers.RepeatedCompositeFieldContainer[Insight]
    def __init__(
        self, insights: _Optional[_Iterable[_Union[Insight, _Mapping]]] = ...
    ) -> None: ...

class GetASNInsightsRequest(_message.Message):
    __slots__ = ("asn", "limit", "market_id", "ip", "lookback", "types", "magnitude")
    ASN_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MARKET_ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    LOOKBACK_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    asn: str
    limit: int
    market_id: str
    ip: str
    lookback: int
    types: _containers.RepeatedScalarFieldContainer[str]
    magnitude: int
    def __init__(
        self,
        asn: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        market_id: _Optional[str] = ...,
        ip: _Optional[str] = ...,
        lookback: _Optional[int] = ...,
        types: _Optional[_Iterable[str]] = ...,
        magnitude: _Optional[int] = ...,
    ) -> None: ...

class GetASNInsightsResponse(_message.Message):
    __slots__ = ("insights",)
    INSIGHTS_FIELD_NUMBER: _ClassVar[int]
    insights: _containers.RepeatedCompositeFieldContainer[Insight]
    def __init__(
        self, insights: _Optional[_Iterable[_Union[Insight, _Mapping]]] = ...
    ) -> None: ...
