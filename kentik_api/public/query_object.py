import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Type, TypeVar

from kentik_api.internal import mandatory_dataclass_attributes
from kentik_api.public.saved_filter import Filters, SavedFilter
from kentik_api.public.types import PermissiveEnumMeta


class ImageType(Enum):
    png = "png"
    jpg = "jpeg"
    svg = "svg"
    pdf = "pdf"


class DimensionType(Enum, metaclass=PermissiveEnumMeta):
    AS_src = "AS_src"
    Geography_src = "Geography_src"
    InterfaceID_src = "InterfaceID_src"
    Port_src = "Port_src"
    src_eth_mac = "src_eth_mac"
    VLAN_src = "VLAN_src"
    IP_src = "IP_src"
    AS_dst = "AS_dst"
    Geography_dst = "Geography_dst"
    InterfaceID_dst = "InterfaceID_dst"
    Port_dst = "Port_dst"
    dst_eth_mac = "dst_eth_mac"
    VLAN_dst = "VLAN_dst"
    IP_dst = "IP_dst"
    TopFlow = "TopFlow"
    Proto = "Proto"
    Traffic = "Traffic"
    ASTopTalkers = "ASTopTalkers"
    InterfaceTopTalkers = "InterfaceTopTalkers"
    PortPortTalkers = "PortPortTalkers"
    TopFlowsIP = "TopFlowsIP"
    src_geo_region = "src_geo_region"
    src_geo_city = "src_geo_city"
    dst_geo_region = "dst_geo_region"
    dst_geo_city = "dst_geo_city"
    RegionTopTalkers = "RegionTopTalkers"
    i_device_id = "i_device_id"
    i_device_site_name = "i_device_site_name"
    i_output_interface_speed = "i_output_interface_speed"
    src_route_prefix_len = "src_route_prefix_len"
    src_route_length = "src_route_length"
    src_bgp_community = "src_bgp_community"
    src_bgp_aspath = "src_bgp_aspath"
    src_nexthop_ip = "src_nexthop_ip"
    src_nexthop_asn = "src_nexthop_asn"
    src_second_asn = "src_second_asn"
    src_third_asn = "src_third_asn"
    src_proto_port = "src_proto_port"
    dst_route_prefix_len = "dst_route_prefix_len"
    dst_route_length = "dst_route_length"
    dst_bgp_community = "dst_bgp_community"
    dst_bgp_aspath = "dst_bgp_aspath"
    dst_nexthop_ip = "dst_nexthop_ip"
    dst_nexthop_asn = "dst_nexthop_asn"
    dst_second_asn = "dst_second_asn"
    dst_third_asn = "dst_third_asn"
    dst_proto_port = "dst_proto_port"
    inet_family = "inet_family"
    TOS = "TOS"
    tcp_flags = "tcp_flags"


class ChartViewType(Enum, metaclass=PermissiveEnumMeta):
    stackedArea = "stackedArea"
    line = "line"
    stackedBar = "stackedBar"
    bar = "bar"
    pie = "pie"
    sankey = "sankey"
    table = "table"
    matrix = "matrix"


class MetricType(Enum, metaclass=PermissiveEnumMeta):
    bytes = "bytes"
    in_bytes = "in_bytes"
    out_bytes = "out_bytes"
    packets = "packets"
    in_packets = "in_packets"
    out_packets = "out_packets"
    tcp_retransmit = "tcp_retransmit"
    perc_retransmit = "perc_retransmit"
    retransmits_in = "retransmits_in"
    perc_retransmits_in = "perc_retransmits_in"
    out_of_order_in = "out_of_order_in"
    perc_out_of_order_in = "perc_out_of_order_in"
    fragments = "fragments"
    perc_fragments = "perc_fragments"
    client_latency = "client_latency"
    server_latency = "server_latency"
    appl_latency = "appl_latency"
    fps = "fps"
    unique_src_ip = "unique_src_ip"
    unique_dst_ip = "unique_dst_ip"
    unique_src_as = "unique_src_as"
    unique_dst_as = "unique_dst_as"
    unique_dst_nexthop_asn = "unique_dst_nexthop_asn"


class FastDataType(Enum):
    auto = "Auto"
    fast = "Fast"
    full = "Full"


class TimeFormat(Enum):
    utc = "UTC"
    local = "Local"


class AggregateFunctionType(Enum, metaclass=PermissiveEnumMeta):
    sum = "sum"
    average = "average"
    percentile = "percentile"
    max = "max"
    composite = "composite"
    exponent = "exponent"
    modulus = "modulus"
    greaterThan = "greaterThan"
    greaterThanEquals = "greaterThanEquals"
    lessThan = "lessThan"
    lessThanEquals = "lessThanEquals"
    equals = "equals"
    notEquals = "notEquals"


AggregateType = TypeVar("AggregateType", bound="Aggregate")


@dataclass
class Aggregate:
    name: str
    column: str
    fn: AggregateFunctionType
    value: Optional[str] = None
    label: Optional[str] = None
    origLabel: Optional[str] = None
    unit: Optional[str] = None
    group: Optional[str] = None
    sample_rate: int = 1
    rank: Optional[int] = None  # valid: number 5..99; only used when fn == percentile
    raw: Optional[bool] = None  # required for topxchart queries
    is_bytes: Optional[bool] = None
    is_count: Optional[bool] = None
    fix: Optional[int] = None

    @classmethod
    def from_dict(cls: Type[AggregateType], data: Dict) -> AggregateType:
        """
        Construct Aggregate object based on data in a dictionary. The dictionary must provide values for all mandatory
        Query attributes
        :param data: dictionary containing class attributes
        :return: instance of Aggregate
        """
        # verify that values are provided for all mandatory fields
        missing = [field_name for field_name in mandatory_dataclass_attributes(cls) if field_name not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        _d = dict()
        _d.update(data)
        _d["fn"] = AggregateFunctionType(data["fn"])
        return cls(**_d)


QueryType = TypeVar("QueryType", bound="Query")


@dataclass
class Query:
    # mandatory attributes
    dimension: List[DimensionType]
    metric: List[MetricType]
    # attributes with defaults (sorted alphabetically)
    aggregateFilters: Optional[dict] = None
    aggregateFiltersDimensionLabel: Optional[dict] = None
    aggregateFiltersEnabled: Optional[dict] = None
    aggregateThresholds: Optional[Dict[str, int]] = None
    aggregateTypes: Optional[List[str]] = None
    aggregates: List[Aggregate] = field(default_factory=list)  # if empty, will be auto-filled based on "metric" field
    all_devices: Optional[bool] = None
    all_selected: Optional[bool] = None  # overrides "device_name" if true (makes it ignored)
    bracketOptions: Optional[str] = None
    cidr6: Optional[int] = None  # valid: number 0..128
    cidr: Optional[int] = None  # valid: number 0..32
    customAsGroups: Optional[bool] = None
    cutFn: Optional[dict] = None
    cutFnRegex: Optional[dict] = None
    cutFnSelector: Optional[dict] = None
    depth: int = 100  # valid: number 25..250
    descriptor: str = ""  # only used when dimension is "Traffic"
    device_labels: Optional[dict] = None
    device_name: List[str] = field(default_factory=list)  # alternative with "all_selected"
    device_sites: Optional[dict] = None
    device_types: Optional[dict] = None
    ending_time: Optional[str] = None  # alternative with "lookback_seconds", format: YYYY-MM-DD HH:mm:00
    fastData: FastDataType = FastDataType.auto
    filterDimensionName: Optional[dict] = None
    filterDimensionOther: Optional[dict] = None
    filterDimensionSort: Optional[dict] = None
    filterDimensions: Optional[dict] = None
    filterDimensionsEnabled: Optional[dict] = None
    filters: Optional[Filters] = None
    forceMinsPolling: Optional[dict] = None
    from_to_lookback: Optional[dict] = None
    generatorColumns: Optional[dict] = None
    generatorDimensions: Optional[dict] = None
    generatorMode: Optional[dict] = None
    generatorPanelMinHeight: Optional[dict] = None
    generatorQueryTitle: Optional[dict] = None
    generatorTopx: Optional[dict] = None
    hideCidr: Optional[bool] = None
    hostname_lookup: bool = True
    isOverlay: Optional[dict] = None
    # "lookback_seconds" MUST be present and set to 0 in order for "starting_time" and "ending_time" to be honored
    # It defaults to 3600 seconds if absent and overrides "(starting|ending)_time"
    lookback_seconds: Optional[int] = 0
    matrixBy: List[str] = field(default_factory=list)  # DimensionType or custom dimension
    minsPolling: Optional[int] = None
    mirror: Optional[dict] = None
    mirrorUnits: Optional[dict] = None
    outsort: str = ""  # name of aggregate object, required when more than 1 objects on "aggregates" list
    overlay_day: Optional[int] = None  # only used in QueryChart, QueryURL
    overlay_timestamp_adjust: Optional[dict] = None
    pps_threshold: Optional[int] = None  # valid number > 0
    query_title: str = ""  # only used in QueryChart
    saved_filters: List[SavedFilter] = field(default_factory=list)
    secondaryOutsort: Optional[dict] = None
    secondaryTopxMirrored: Optional[dict] = None
    secondaryTopxSeparate: Optional[dict] = None
    show_overlay: Optional[bool] = None  # only used in QueryChart, QueryURL
    show_site_markers: Optional[dict] = None
    show_total_overlay: Optional[dict] = None
    starting_time: Optional[str] = None  # alternative with "lookback_seconds", format: YYYY-MM-DD HH:mm:00
    sync_all_axes: Optional[dict] = None
    sync_axes: Optional[bool] = None  # only used in QueryChart, QueryURL
    sync_extents: Optional[dict] = None
    time_format: TimeFormat = TimeFormat.utc
    topx: int = 125  # valid: number 1..40
    update_frequency: Optional[dict] = None
    use_log_axis: Optional[dict] = None
    use_secondary_log_axis: Optional[dict] = None
    viz_type: Optional[ChartViewType] = None  # only used in QueryChart, QueryURL

    @classmethod
    def from_dict(cls: Type[QueryType], data: Dict) -> QueryType:
        """
        Construct Query object based on data in a dictionary. The dictionary must provide values for all mandatory
        Query attributes
        :param data: dictionary
        :return: instance of Query
        """
        # verify that values are provided for all mandatory fields
        missing = [field_name for field_name in mandatory_dataclass_attributes(cls) if field_name not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        _d = dict()
        _d.update(data)
        if "fastData" in data:
            _d["fastData"] = FastDataType(data["fastData"])
        if "filters" in data:
            _d["filters"] = Filters.from_dict(data["filters"])
        _d["dimension"] = [DimensionType(f) for f in data["dimension"]]
        _d["metric"] = [MetricType(f) for f in data["metric"]]
        if "aggregates" in data:
            _d["aggregates"] = [Aggregate.from_dict(f) for f in data["aggregates"]]
        if "saved_filters" in data:
            _d["saved_filters"] = [SavedFilter.from_dict(f) for f in data["saved_filters"]]
        return cls(**_d)


QueryArrayItemType = TypeVar("QueryArrayItemType", bound="QueryArrayItem")


@dataclass
class QueryArrayItem:
    query: Query
    bucket: str
    bucketIndex: Optional[int] = None
    isOverlay: Optional[bool] = None  # used in QueryChart, QueryURL

    @classmethod
    def from_dict(cls: Type[QueryArrayItemType], data: Dict) -> QueryArrayItemType:
        """
        Construct QueryArrayItem based on data in a dictionary. The dictionary must provide values for all mandatory
        QueryArrayItem fields
        :param data: dictionary
        :return: instance of QueryArrayItem
        """
        # verify that values are provided for all mandatory fields
        missing = [field_name for field_name in mandatory_dataclass_attributes(cls) if field_name not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        # construct Query object
        _d = dict()
        _d.update(data)
        _d["query"] = Query.from_dict(data["query"])
        return cls(**_d)


QueryObjectType = TypeVar("QueryObjectType", bound="QueryObject")


@dataclass
class QueryObject:
    queries: List[QueryArrayItem]
    imageType: Optional[ImageType] = None  # used in QueryChart
    version: int = 4

    @classmethod
    def from_dict(cls: Type[QueryObjectType], data: Dict) -> QueryObjectType:
        """
        Construct QueryObject based on a dictionary. The dictionary must contain data for all mandatory query attributes
        :param data: dictionary
        :return: instance of QueryObject
        """
        # verify that all QueryObject data field without built-in default value are provided
        missing = [field_name for field_name in mandatory_dataclass_attributes(cls) if field_name not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        # construct List of QueryArrayItem objects
        _d = dict()
        _d.update(data)
        _d["queries"] = [QueryArrayItem.from_dict(item_data) for item_data in data["queries"]]
        return cls(**_d)

    @classmethod
    def from_json(cls: Type[QueryObjectType], file_name: str) -> QueryObjectType:
        with open(file_name) as f:
            return cls.from_dict(json.load(f))


@dataclass
class QueryDataResult:
    results: List[Dict]  # The elements included in the array depend on the query passed into the call


@dataclass
class QueryChartResult:
    image_type: ImageType
    image_data: bytes

    def save_image_as(self, file_path: str) -> None:
        data = self.get_data()
        with open(file_path, "wb") as file:
            file.write(data)

    def get_data(self) -> bytes:
        return self.image_data


@dataclass
class QueryURLResult:
    url: str
