from datetime import timezone
from typing import Tuple

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests import (
    agent,
    dns,
    dns_grid,
    flow,
    hostname,
    ip,
    network_grid,
    network_mesh,
    page_load,
    url,
)
from kentik_api.synthetics.synth_tests.base import (
    DateTime,
    PingTask,
    PingTraceTest,
    SynTest,
    SynTestSettings,
    TraceTask,
    UserInfo,
)
from kentik_api.synthetics.types import (
    DirectionType,
    DNSRecordType,
    FlowTestSubType,
    IPFamily,
    Protocol,
    TaskType,
    TestStatus,
    TestType,
)


def setup_syn_test(out_pb_test: pb.Test, out_test: SynTest) -> None:
    out_pb_test.id = "1234"
    out_pb_test.cdate.CopyFrom(Timestamp(seconds=1649057685, nanos=0))
    out_pb_test.edate.CopyFrom(Timestamp(seconds=1649058245, nanos=0))
    out_pb_test.created_by.CopyFrom(pb.UserInfo(id="67", email="creator@company.com", full_name="Bob Creator"))
    out_pb_test.last_updated_by.CopyFrom(pb.UserInfo(id="89", email="editor@company.com", full_name="Joe Editor"))
    out_pb_test.name = "example_test"
    out_pb_test.type = TestType.NONE.value  # to be set later - in target test type
    out_pb_test.status = TestStatus.ACTIVE.value

    # setup read-only fields for testing purpose
    # pragma pylint: disable=protected-access
    out_test._cdate = DateTime.fromtimestamp(1649057685, timezone.utc)
    out_test._created_by = UserInfo(id="67", email="creator@company.com", full_name="Bob Creator")
    out_test._last_updated_by = UserInfo(id="89", email="editor@company.com", full_name="Joe Editor")
    # pragma pylint: enable=protected-access
    out_test.id = ID("1234")
    out_test.name = "example_test"
    out_test.type = TestType.NONE  # to be set later - in target test type
    out_test.status = TestStatus.ACTIVE
    out_test.edate = DateTime.fromtimestamp(1649058245, timezone.utc)

    setup_syn_test_settings(out_pb_test.settings, out_test.settings)


def setup_syn_test_settings(out_pb_settings: pb.TestSettings, out_settings: SynTestSettings) -> None:
    out_pb_settings.family = IPFamily.DUAL.value
    out_pb_settings.period = 30
    out_pb_settings.agent_ids.extend(["757", "663", "559"])
    # out_pb_settings.tasks  # to be set later
    out_pb_settings.notification_channels.extend(["email", "slack"])
    out_pb_settings.health_settings.CopyFrom(
        pb.HealthSettings(
            latency_critical=100,
            latency_warning=50,
            latency_critical_stddev=3,
            latency_warning_stddev=1.5,
            packet_loss_critical=60,
            packet_loss_warning=30,
            jitter_critical=20,
            jitter_warning=10,
            jitter_critical_stddev=4.5,
            jitter_warning_stddev=2.25,
            http_latency_critical=500,
            http_latency_warning=250,
            http_latency_critical_stddev=7,
            http_latency_warning_stddev=3.5,
            http_valid_codes=[200, 201, 301],
            dns_valid_codes=[1, 2, 3],
            unhealthy_subtest_threshold=3,
            activation=pb.ActivationSettings(
                grace_period="3",
                time_unit="m",
                time_window="5",
                times="4",
            ),
        )
    )

    out_settings.family = IPFamily.DUAL
    out_settings.period = 30
    out_settings.agent_ids = [ID("757"), ID("663"), ID("559")]
    out_settings.tasks = []  # to be set later
    out_settings.notification_channels = ["email", "slack"]
    out_settings.health_settings.latency_critical = 100
    out_settings.health_settings.latency_warning = 50
    out_settings.health_settings.latency_critical_stddev = 3
    out_settings.health_settings.latency_warning_stddev = 1.5
    out_settings.health_settings.packet_loss_critical = 60
    out_settings.health_settings.packet_loss_warning = 30
    out_settings.health_settings.jitter_critical = 20
    out_settings.health_settings.jitter_warning = 10
    out_settings.health_settings.jitter_critical_stddev = 4.5
    out_settings.health_settings.jitter_warning_stddev = 2.25
    out_settings.health_settings.http_latency_critical = 500
    out_settings.health_settings.http_latency_warning = 250
    out_settings.health_settings.http_latency_critical_stddev = 7
    out_settings.health_settings.http_latency_warning_stddev = 3.5
    out_settings.health_settings.http_valid_codes = [200, 201, 301]
    out_settings.health_settings.dns_valid_codes = [1, 2, 3]
    out_settings.health_settings.unhealthy_subtest_threshold = 3
    out_settings.health_settings.activation.grace_period = "3"
    out_settings.health_settings.activation.time_unit = "m"
    out_settings.health_settings.activation.time_window = "5"
    out_settings.health_settings.activation.times = "4"


def setup_ping_trace_test(out_pb_test: pb.Test, out_test: PingTraceTest) -> None:
    setup_syn_test(out_pb_test, out_test)

    out_pb_test.settings.tasks.extend([TaskType.PING.value, TaskType.TRACE_ROUTE.value])
    out_pb_test.settings.ping.CopyFrom(
        pb.TestPingSettings(timeout=3000, count=10, delay=555, protocol=Protocol.TCP.value, port=333)
    )
    out_pb_test.settings.trace.CopyFrom(
        pb.TestTraceSettings(
            timeout=11222,
            count=10,
            limit=50,
            delay=25,
            protocol=Protocol.ICMP.value,
            port=33444,
        )
    )

    out_test.settings.tasks = [TaskType.PING, TaskType.TRACE_ROUTE]
    out_test.settings.ping = PingTask(timeout=3000, count=10, delay=555, protocol=Protocol.TCP, port=333)
    out_test.settings.trace = TraceTask(timeout=11222, count=10, limit=50, delay=25, protocol=Protocol.ICMP, port=33444)


def make_ip_test_pair() -> Tuple[pb.Test, ip.IPTest]:
    # general test config
    pb_test = pb.Test()
    test = ip.IPTest(name="", status=TestStatus.UNSPECIFIED, settings=ip.IPTestSettings())
    setup_ping_trace_test(pb_test, test)

    # IP-test specific config
    pb_test.type = TestType.IP.value
    pb_test.settings.ip.CopyFrom(pb.IpTest(targets=["54.161.222.85", "34.205.242.146"]))

    test.type = TestType.IP
    test.settings.ip = ip.IPTestSpecific(targets=[IP("54.161.222.85"), IP("34.205.242.146")])

    return (pb_test, test)


def make_agent_test_pair() -> Tuple[pb.Test, agent.AgentTest]:
    # general test config
    pb_test = pb.Test()
    test = agent.AgentTest(name="", status=TestStatus.UNSPECIFIED, settings=agent.AgentTestSettings())
    setup_ping_trace_test(pb_test, test)

    # Agent-test specific config
    pb_test.type = TestType.AGENT.value
    pb_test.settings.agent.CopyFrom(pb.AgentTest(target="38", use_local_ip=True))

    test.type = TestType.AGENT
    test.settings.agent = agent.AgentTestSpecific(target=ID("38"), use_local_ip=True)

    return (pb_test, test)


def make_hostname_test_pair() -> Tuple[pb.Test, hostname.HostnameTest]:
    # general test config
    pb_test = pb.Test()
    test = hostname.HostnameTest(name="", status=TestStatus.UNSPECIFIED, settings=hostname.HostnameTestSettings())
    setup_ping_trace_test(pb_test, test)

    # Hostname-test specific config
    pb_test.type = TestType.HOSTNAME.value
    pb_test.settings.hostname.CopyFrom(pb.HostnameTest(target="www.example.com"))

    test.type = TestType.HOSTNAME
    test.settings.hostname = hostname.HostnameTestSpecific(target="www.example.com")

    return (pb_test, test)


def make_url_test_pair() -> Tuple[pb.Test, url.UrlTest]:
    # general test config
    pb_test = pb.Test()
    test = url.UrlTest(name="", status=TestStatus.UNSPECIFIED, settings=url.UrlTestSettings())
    setup_ping_trace_test(pb_test, test)

    # Hostname-test specific config
    pb_test.type = TestType.URL.value
    pb_test.settings.url.CopyFrom(
        pb.UrlTest(
            target="www.example.com",
            timeout=7000,
            method="GET",
            headers={"origin": "url-test"},
            body="BODY",
            ignore_tls_errors=True,
        )
    )

    test.type = TestType.URL
    test.settings.url = url.URLTestSpecific(
        target="www.example.com",
        timeout=7000,
        method="GET",
        headers={"origin": "url-test"},
        body="BODY",
        ignore_tls_errors=True,
    )

    return (pb_test, test)


def make_page_load_test_pair() -> Tuple[pb.Test, page_load.PageLoadTest]:
    # general test config
    pb_test = pb.Test()
    test = page_load.PageLoadTest(
        name="",
        status=TestStatus.UNSPECIFIED,
        settings=page_load.PageLoadTestSettings(),
    )
    setup_ping_trace_test(pb_test, test)

    # PageLoad-test specific config
    pb_test.type = TestType.PAGE_LOAD.value
    pb_test.settings.page_load.CopyFrom(
        pb.PageLoadTest(
            target="www.example.com",
            timeout=7000,
            headers={"origin": "page-load-test"},
            ignore_tls_errors=True,
            css_selectors={"id": "#id", "class": ".class"},
        )
    )

    test.type = TestType.PAGE_LOAD
    test.settings.page_load = page_load.PageLoadTestSpecific(
        target="www.example.com",
        timeout=7000,
        headers={"origin": "page-load-test"},
        ignore_tls_errors=True,
        css_selectors={"id": "#id", "class": ".class"},
    )

    return (pb_test, test)


def make_network_mesh_test_pair() -> Tuple[pb.Test, network_mesh.NetworkMeshTest]:
    # general test config
    pb_test = pb.Test()
    test = network_mesh.NetworkMeshTest(
        name="",
        status=TestStatus.UNSPECIFIED,
        settings=network_mesh.NetworkMeshTestSettings(),
    )
    setup_ping_trace_test(pb_test, test)

    # Mesh-test specific config
    pb_test.type = TestType.NETWORK_MESH.value
    pb_test.settings.network_mesh.CopyFrom(pb.NetworkMeshTest(use_local_ip=True))

    test.type = TestType.NETWORK_MESH
    test.settings.network_mesh = network_mesh.NetworkMeshTestSpecific(use_local_ip=True)

    return (pb_test, test)


def make_network_grid_test_pair() -> Tuple[pb.Test, network_grid.NetworkGridTest]:
    # general test config
    pb_test = pb.Test()
    test = network_grid.NetworkGridTest(
        name="", status=TestStatus.UNSPECIFIED, settings=network_grid.GridTestSettings()
    )
    setup_ping_trace_test(pb_test, test)

    # Grid-test specific config
    pb_test.type = TestType.NETWORK_GRID.value
    pb_test.settings.network_grid.CopyFrom(pb.IpTest(targets=["54.161.222.85", "34.205.242.146"]))

    test.type = TestType.NETWORK_GRID
    test.settings.network_grid = network_grid.NetworkGridTestSpecific(
        targets=[IP("54.161.222.85"), IP("34.205.242.146")]
    )

    return (pb_test, test)


def make_flow_test_pair() -> Tuple[pb.Test, flow.FlowTest]:
    # general test config
    pb_test = pb.Test()
    test = flow.FlowTest(name="", status=TestStatus.UNSPECIFIED, settings=flow.FlowTestSettings())
    setup_ping_trace_test(pb_test, test)

    # Flow-test specific config
    pb_test.type = TestType.FLOW.value
    pb_test.settings.flow.CopyFrom(
        pb.FlowTest(
            target="456",
            target_refresh_interval_millis=333,
            max_providers=4,
            max_ip_targets=5,
            type=FlowTestSubType.CDN.value,
            inet_direction=DirectionType.DST.value,
            direction=DirectionType.DST.value,
        )
    )

    test.type = TestType.FLOW
    test.settings.flow = flow.FlowTestSpecific(
        target="456",
        target_refresh_interval_millis=333,
        max_providers=4,
        max_ip_targets=5,
        type=FlowTestSubType.CDN,
        inet_direction=DirectionType.DST,
        direction=DirectionType.DST,
    )

    return (pb_test, test)


def make_dns_test_pair() -> Tuple[pb.Test, dns.DNSTest]:
    # general test config
    pb_test = pb.Test()
    test = dns.DNSTest(name="", status=TestStatus.UNSPECIFIED, settings=dns.DNSTestSettings())
    setup_syn_test(pb_test, test)

    # DNS-test specific config
    pb_test.type = TestType.DNS.value
    pb_test.settings.dns.CopyFrom(
        pb.DnsTest(
            target="123",
            timeout=1600,
            record_type=DNSRecordType.A.value,
            servers=["1.1.1.1", "2.2.2.2"],
            port=2233,
        )
    )

    test.type = TestType.DNS
    test.settings.dns = dns.DNSTestSpecific(
        target="123",
        timeout=1600,
        record_type=DNSRecordType.A,
        servers=["1.1.1.1", "2.2.2.2"],
        port=2233,
    )

    return (pb_test, test)


def make_dns_grid_test_pair() -> Tuple[pb.Test, dns_grid.DNSGridTest]:
    # general test config
    pb_test = pb.Test()
    test = dns_grid.DNSGridTest(name="", status=TestStatus.UNSPECIFIED, settings=dns_grid.DNSGridTestSettings())
    setup_syn_test(pb_test, test)

    # DNSGrid-test specific config
    pb_test.type = TestType.DNS_GRID.value
    pb_test.settings.dns_grid.CopyFrom(
        pb.DnsTest(
            target="456",
            timeout=3200,
            record_type=DNSRecordType.AAAA.value,
            servers=["8.8.8.8", "4.4.4.4"],
            port=4455,
        )
    )

    test.type = TestType.DNS_GRID
    test.settings.dns_grid = dns_grid.DSNGridTestSpecific(
        target="456",
        timeout=3200,
        record_type=DNSRecordType.AAAA,
        servers=["8.8.8.8", "4.4.4.4"],
        port=4455,
    )

    return (pb_test, test)
