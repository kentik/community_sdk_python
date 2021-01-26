from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum

from kentik_api.public.types import ID
from kentik_api.public.saved_filter import Filters


class ImageType(Enum):
    png = "png"
    jpg = "jpeg"
    svg = "svg"
    pdf = "pdf"


class DimensionType(Enum):
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


class ChartViewType(Enum):
    stackedArea = "stackedArea"
    line = "line"
    stackedBar = "stackedBar"
    bar = "bar"
    pie = "pie"
    sankey = "sankey"
    table = "table"
    matrix = "matrix"


class MetricType(Enum):
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


class FastDataType(Enum):
    auto = "Auto"
    fast = "Fast"
    full = "Full"


class TimeFormat(Enum):
    utc = "UTC"
    local = "Local"


@dataclass
class SavedFilter:
    filter_id: ID
    is_not: bool = False


class AggregateFunctionType(Enum):
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


@dataclass
class Aggregate:
    name: str
    column: str
    fn: AggregateFunctionType
    sample_rate: int = 1
    rank: Optional[int] = None  # valid: number 5..99; only used when fn == percentile
    raw: Optional[bool] = None  # required for topxchart queries


@dataclass
class Query:
    metric: MetricType
    dimension: List[DimensionType]
    filters_obj: Optional[Filters] = None
    saved_filters: List[SavedFilter] = field(default_factory=list)
    matrixBy: List[str] = field(default_factory=list)  # DimensionType or custom dimension
    cidr: Optional[int] = None  # valid: number 0..32
    cidr6: Optional[int] = None  # valid: number 0..128
    pps_threshold: Optional[int] = None  # valid number > 0
    topx: int = 8  # valid: number 1..40
    depth: int = 100  # valid: number 25..250
    fastData: FastDataType = FastDataType.auto
    time_format: TimeFormat = TimeFormat.utc
    hostname_lookup: bool = True
    lookback_seconds: int = 3600  # value != 0 overrides "starting_time" and "ending_time"
    starting_time: Optional[str] = None  # alternative with "lookback_seconds", format: YYYY-MM-DD HH:mm:00
    ending_time: Optional[str] = None  # alternative with "lookback_seconds", format: YYYY-MM-DD HH:mm:00
    all_selected: Optional[bool] = None  # overrides "device_name" if true (makes it ignored)
    device_name: List[str] = field(default_factory=list)  #  alternative with "all_selected"
    descriptor: str = ""  # only used when dimension is "Traffic"
    aggregates: List[Aggregate] = field(default_factory=list)  # if empty, will be auto-filled based on "metric" field
    outsort: Optional[str] = None  # name of aggregate object, required when more than 1 objects on "aggregates" list
    query_title: str = ""  # only used in QueryChart
    viz_type: Optional[ChartViewType] = None  # only used in QueryChart, QueryURL
    show_overlay: Optional[bool] = None  # only used in QueryChart, QueryURL
    overlay_day: Optional[int] = None  # only used in QueryChart, QueryURL
    sync_axes: Optional[bool] = None  # only used in QueryChart, QueryURL


@dataclass
class QueryArrayItem:
    query: Query
    bucket: str
    bucketIndex: Optional[int] = None
    isOverlay: Optional[bool] = None  # used in QueryChart, QueryURL


@dataclass
class QueryObject:
    queries: List[QueryArrayItem]
    imageType: Optional[ImageType] = None  # used in QueryChart


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
