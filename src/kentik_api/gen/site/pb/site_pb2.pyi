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

class SiteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SITE_TYPE_UNSPECIFIED: _ClassVar[SiteType]
    SITE_TYPE_DATA_CENTER: _ClassVar[SiteType]
    SITE_TYPE_CLOUD: _ClassVar[SiteType]
    SITE_TYPE_BRANCH: _ClassVar[SiteType]
    SITE_TYPE_CONNECTIVITY: _ClassVar[SiteType]
    SITE_TYPE_CUSTOMER: _ClassVar[SiteType]
    SITE_TYPE_OTHER: _ClassVar[SiteType]

SITE_TYPE_UNSPECIFIED: SiteType
SITE_TYPE_DATA_CENTER: SiteType
SITE_TYPE_CLOUD: SiteType
SITE_TYPE_BRANCH: SiteType
SITE_TYPE_CONNECTIVITY: SiteType
SITE_TYPE_CUSTOMER: SiteType
SITE_TYPE_OTHER: SiteType

class SiteIpAddressClassification(_message.Message):
    __slots__ = ("infrastructure_networks", "user_access_networks", "other_networks")
    INFRASTRUCTURE_NETWORKS_FIELD_NUMBER: _ClassVar[int]
    USER_ACCESS_NETWORKS_FIELD_NUMBER: _ClassVar[int]
    OTHER_NETWORKS_FIELD_NUMBER: _ClassVar[int]
    infrastructure_networks: _containers.RepeatedScalarFieldContainer[str]
    user_access_networks: _containers.RepeatedScalarFieldContainer[str]
    other_networks: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        infrastructure_networks: _Optional[_Iterable[str]] = ...,
        user_access_networks: _Optional[_Iterable[str]] = ...,
        other_networks: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Layer(_message.Message):
    __slots__ = ("name", "device_ids")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    device_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, name: _Optional[str] = ..., device_ids: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class LayerSet(_message.Message):
    __slots__ = ("layers",)
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedCompositeFieldContainer[Layer]
    def __init__(
        self, layers: _Optional[_Iterable[_Union[Layer, _Mapping]]] = ...
    ) -> None: ...

class PostalAddress(_message.Message):
    __slots__ = ("address", "city", "region", "postal_code", "country")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    def __init__(
        self,
        address: _Optional[str] = ...,
        city: _Optional[str] = ...,
        region: _Optional[str] = ...,
        postal_code: _Optional[str] = ...,
        country: _Optional[str] = ...,
    ) -> None: ...

class PeeringDBSiteMapping(_message.Message):
    __slots__ = ("id", "site_id", "peeringdb_fac_id", "edate", "cdate", "company_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    PEERINGDB_FAC_ID_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    site_id: str
    peeringdb_fac_id: str
    edate: _timestamp_pb2.Timestamp
    cdate: _timestamp_pb2.Timestamp
    company_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        site_id: _Optional[str] = ...,
        peeringdb_fac_id: _Optional[str] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        company_id: _Optional[str] = ...,
    ) -> None: ...

class Site(_message.Message):
    __slots__ = (
        "id",
        "title",
        "lat",
        "lon",
        "postal_address",
        "type",
        "address_classification",
        "architecture",
        "site_market",
        "peeringdb_site_mapping",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    POSTAL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    ARCHITECTURE_FIELD_NUMBER: _ClassVar[int]
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    PEERINGDB_SITE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    lat: float
    lon: float
    postal_address: PostalAddress
    type: SiteType
    address_classification: SiteIpAddressClassification
    architecture: _containers.RepeatedCompositeFieldContainer[LayerSet]
    site_market: SiteMarket
    peeringdb_site_mapping: _containers.RepeatedCompositeFieldContainer[
        PeeringDBSiteMapping
    ]
    def __init__(
        self,
        id: _Optional[str] = ...,
        title: _Optional[str] = ...,
        lat: _Optional[float] = ...,
        lon: _Optional[float] = ...,
        postal_address: _Optional[_Union[PostalAddress, _Mapping]] = ...,
        type: _Optional[_Union[SiteType, str]] = ...,
        address_classification: _Optional[
            _Union[SiteIpAddressClassification, _Mapping]
        ] = ...,
        architecture: _Optional[_Iterable[_Union[LayerSet, _Mapping]]] = ...,
        site_market: _Optional[_Union[SiteMarket, _Mapping]] = ...,
        peeringdb_site_mapping: _Optional[
            _Iterable[_Union[PeeringDBSiteMapping, _Mapping]]
        ] = ...,
    ) -> None: ...

class ListSitesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSitesResponse(_message.Message):
    __slots__ = ("sites", "invalid_count")
    SITES_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    sites: _containers.RepeatedCompositeFieldContainer[Site]
    invalid_count: int
    def __init__(
        self,
        sites: _Optional[_Iterable[_Union[Site, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetSiteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSiteResponse(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: Site
    def __init__(self, site: _Optional[_Union[Site, _Mapping]] = ...) -> None: ...

class CreateSiteRequest(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: Site
    def __init__(self, site: _Optional[_Union[Site, _Mapping]] = ...) -> None: ...

class CreateSiteResponse(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: Site
    def __init__(self, site: _Optional[_Union[Site, _Mapping]] = ...) -> None: ...

class UpdateSiteRequest(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: Site
    def __init__(self, site: _Optional[_Union[Site, _Mapping]] = ...) -> None: ...

class UpdateSiteResponse(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: Site
    def __init__(self, site: _Optional[_Union[Site, _Mapping]] = ...) -> None: ...

class DeleteSiteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSiteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SiteMarket(_message.Message):
    __slots__ = ("id", "name", "description", "number_of_sites", "cdate", "edate")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_SITES_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    number_of_sites: int
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        number_of_sites: _Optional[int] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class ListSiteMarketsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSiteMarketsResponse(_message.Message):
    __slots__ = ("site_markets", "invalid_count")
    SITE_MARKETS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    site_markets: _containers.RepeatedCompositeFieldContainer[SiteMarket]
    invalid_count: int
    def __init__(
        self,
        site_markets: _Optional[_Iterable[_Union[SiteMarket, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetSiteMarketRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSiteMarketResponse(_message.Message):
    __slots__ = ("site_market",)
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    site_market: SiteMarket
    def __init__(
        self, site_market: _Optional[_Union[SiteMarket, _Mapping]] = ...
    ) -> None: ...

class CreateSiteMarketRequest(_message.Message):
    __slots__ = ("site_market",)
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    site_market: SiteMarket
    def __init__(
        self, site_market: _Optional[_Union[SiteMarket, _Mapping]] = ...
    ) -> None: ...

class CreateSiteMarketResponse(_message.Message):
    __slots__ = ("site_market",)
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    site_market: SiteMarket
    def __init__(
        self, site_market: _Optional[_Union[SiteMarket, _Mapping]] = ...
    ) -> None: ...

class UpdateSiteMarketRequest(_message.Message):
    __slots__ = ("site_market",)
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    site_market: SiteMarket
    def __init__(
        self, site_market: _Optional[_Union[SiteMarket, _Mapping]] = ...
    ) -> None: ...

class UpdateSiteMarketResponse(_message.Message):
    __slots__ = ("site_market",)
    SITE_MARKET_FIELD_NUMBER: _ClassVar[int]
    site_market: SiteMarket
    def __init__(
        self, site_market: _Optional[_Union[SiteMarket, _Mapping]] = ...
    ) -> None: ...

class DeleteSiteMarketRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSiteMarketResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
