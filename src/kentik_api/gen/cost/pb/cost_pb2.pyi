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

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[Status]
    STATUS_INCOMPLETE: _ClassVar[Status]
    STATUS_COMPLETE: _ClassVar[Status]

STATUS_UNSPECIFIED: Status
STATUS_INCOMPLETE: Status
STATUS_COMPLETE: Status

class CostProviderSummary(_message.Message):
    __slots__ = (
        "date",
        "status",
        "total_cost",
        "total_cost_variation",
        "total_cost_group_additional_cost",
        "total_cost_group_additional_interface_cost",
        "currency",
        "cost_per_mbps",
        "cost_per_mbps_variation",
        "provider_name",
        "cost_group_name",
        "cost_group_conn_type",
        "site_name",
        "site_market",
        "ingress_traffic_mbps",
        "ingress_traffic_variation",
        "egress_traffic_mbps",
        "egress_traffic_variation",
    )
    DATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_VARIATION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_GROUP_ADDITIONAL_COST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_GROUP_ADDITIONAL_INTERFACE_COST_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    COST_PER_MBPS_FIELD_NUMBER: _ClassVar[int]
    COST_PER_MBPS_VARIATION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    COST_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    COST_GROUP_CONN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SITE_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    INGRESS_TRAFFIC_MBPS_FIELD_NUMBER: _ClassVar[int]
    INGRESS_TRAFFIC_VARIATION_FIELD_NUMBER: _ClassVar[int]
    EGRESS_TRAFFIC_MBPS_FIELD_NUMBER: _ClassVar[int]
    EGRESS_TRAFFIC_VARIATION_FIELD_NUMBER: _ClassVar[int]
    date: str
    status: Status
    total_cost: float
    total_cost_variation: str
    total_cost_group_additional_cost: float
    total_cost_group_additional_interface_cost: float
    currency: str
    cost_per_mbps: float
    cost_per_mbps_variation: str
    provider_name: str
    cost_group_name: str
    cost_group_conn_type: str
    site_name: str
    site_market: str
    ingress_traffic_mbps: float
    ingress_traffic_variation: str
    egress_traffic_mbps: float
    egress_traffic_variation: str
    def __init__(
        self,
        date: _Optional[str] = ...,
        status: _Optional[_Union[Status, str]] = ...,
        total_cost: _Optional[float] = ...,
        total_cost_variation: _Optional[str] = ...,
        total_cost_group_additional_cost: _Optional[float] = ...,
        total_cost_group_additional_interface_cost: _Optional[float] = ...,
        currency: _Optional[str] = ...,
        cost_per_mbps: _Optional[float] = ...,
        cost_per_mbps_variation: _Optional[str] = ...,
        provider_name: _Optional[str] = ...,
        cost_group_name: _Optional[str] = ...,
        cost_group_conn_type: _Optional[str] = ...,
        site_name: _Optional[str] = ...,
        site_market: _Optional[str] = ...,
        ingress_traffic_mbps: _Optional[float] = ...,
        ingress_traffic_variation: _Optional[str] = ...,
        egress_traffic_mbps: _Optional[float] = ...,
        egress_traffic_variation: _Optional[str] = ...,
    ) -> None: ...

class CostProviderConcise(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(
        self, id: _Optional[str] = ..., name: _Optional[str] = ...
    ) -> None: ...

class ListCostProvidersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCostProvidersResponse(_message.Message):
    __slots__ = ("providers", "invalid_count")
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[CostProviderConcise]
    invalid_count: int
    def __init__(
        self,
        providers: _Optional[_Iterable[_Union[CostProviderConcise, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class ListCostProviderSummariesRequest(_message.Message):
    __slots__ = ("date",)
    DATE_FIELD_NUMBER: _ClassVar[int]
    date: str
    def __init__(self, date: _Optional[str] = ...) -> None: ...

class ListCostProviderSummariesResponse(_message.Message):
    __slots__ = ("providers", "invalid_count")
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[CostProviderSummary]
    invalid_count: int
    def __init__(
        self,
        providers: _Optional[_Iterable[_Union[CostProviderSummary, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetCostProviderSummaryRequest(_message.Message):
    __slots__ = ("id", "date")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    date: str
    def __init__(
        self, id: _Optional[str] = ..., date: _Optional[str] = ...
    ) -> None: ...

class GetCostProviderSummaryResponse(_message.Message):
    __slots__ = ("providers", "invalid_count")
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[CostProviderSummary]
    invalid_count: int
    def __init__(
        self,
        providers: _Optional[_Iterable[_Union[CostProviderSummary, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...
