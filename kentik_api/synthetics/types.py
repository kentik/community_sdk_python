import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.internal.grpc import SerializableEnum


class TestType(SerializableEnum):
    __test__ = False  # mark class as "Not a test"; to avoid pytest warnings
    NONE = ""
    AGENT = "agent"
    BGP_MONITOR = "bgp_monitor"
    DNS = "dns"
    DNS_GRID = "dns_grid"
    FLOW = "flow"
    HOSTNAME = "hostname"
    IP = "ip"
    NETWORK_MESH = "network_mesh"
    NETWORK_GRID = "network_grid"
    PAGE_LOAD = "page_load"
    TRANSACTION = "transaction"
    URL = "url"


class TaskType(SerializableEnum):
    NONE = ""
    PING = "ping"
    TRACE_ROUTE = "traceroute"
    DNS = "dns"
    HTTP = "http"
    PAGE_LOAD = "page-load"
    TRANSACTION = "transaction"


class TestStatus(SerializableEnum):
    __test__ = False  # mark class as "Not a test"; to avoid pytest warnings
    UNSPECIFIED = pb.TestStatus.TEST_STATUS_UNSPECIFIED
    ACTIVE = pb.TestStatus.TEST_STATUS_ACTIVE
    PAUSED = pb.TestStatus.TEST_STATUS_PAUSED
    DELETED = pb.TestStatus.TEST_STATUS_DELETED


class IPFamily(SerializableEnum):
    UNSPECIFIED = pb.IPFamily.IP_FAMILY_UNSPECIFIED
    DUAL = pb.IPFamily.IP_FAMILY_DUAL
    V4 = pb.IPFamily.IP_FAMILY_V4
    V6 = pb.IPFamily.IP_FAMILY_V6


class Protocol(SerializableEnum):
    NONE = ""
    ICMP = "icmp"
    UDP = "udp"
    TCP = "tcp"


class FlowTestSubType(SerializableEnum):
    NONE = ""
    ASN = "asn"
    CDN = "cdn"
    COUNTRY = "country"
    REGION = "region"
    CITY = "city"


class DirectionType(SerializableEnum):
    NONE = ""
    DST = "dst"
    SRC = "src"


class DNSRecordType(SerializableEnum):
    UNSPECIFIED = pb.DNS_RECORD_UNSPECIFIED
    A = pb.DNS_RECORD_A
    AAAA = pb.DNS_RECORD_AAAA
    CNAME = pb.DNS_RECORD_CNAME
    DNAME = pb.DNS_RECORD_DNAME
    NS = pb.DNS_RECORD_NS
    MX = pb.DNS_RECORD_MX
    PTR = pb.DNS_RECORD_PTR
    SOA = pb.DNS_RECORD_SOA


class Health(SerializableEnum):
    NONE = ""
    HEALTHY = "healthy"
    WARNING = "warning"
    FAILING = "failing"
    CRITICAL = "critical"
