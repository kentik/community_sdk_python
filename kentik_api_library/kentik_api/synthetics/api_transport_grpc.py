import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import grpc.experimental as _
from google.protobuf.field_mask_pb2 import FieldMask

from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Agent as pbAgent
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentStatus as pbAgentStatus
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    CreateTestRequest,
    DeleteAgentRequest,
    DeleteTestRequest,
    GetAgentRequest,
    GetTestRequest,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import HealthSettings as pbHealthSettings
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import HostnameTest as pbHostnameTest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ImplementType as pbAgentImpl
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import IPFamily as pbIPFamily
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import IpTest as pbIpTest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    ListAgentsRequest,
    ListTestsRequest,
    PatchAgentRequest,
    PatchTestRequest,
    SetTestStatusRequest,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Test as pbTest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    TestMonitoringSettings as pbMonitoringSettings,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TestSettings as pbTestSettings
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TestStatus as pbTestStatus
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2_grpc import SyntheticsAdminService
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests import (
    HealthSettings,
    IPFamily,
    MeshTest,
    MonitoringSettings,
    PingTask,
    PingTraceTest,
    PingTraceTestSettings,
    Protocol,
    SynTest,
    SynTestSettings,
    TestStatus,
    TestType,
    TraceTask,
)

from .agent import Agent, AgentImplementType, AgentStatus
from .api_transport import KentikAPIRequestError, KentikAPITransport

log = logging.getLogger("api_transport_grpc")

PB_TEST_STATUS_TO_STATUS = {
    pbTestStatus.TEST_STATUS_UNSPECIFIED: TestStatus.none,
    pbTestStatus.TEST_STATUS_ACTIVE: TestStatus.active,
    pbTestStatus.TEST_STATUS_PAUSED: TestStatus.paused,
    pbTestStatus.TEST_STATUS_DELETED: TestStatus.deleted,
}

PB_FAMILY_TO_FAMILY = {
    pbIPFamily.IP_FAMILY_UNSPECIFIED: IPFamily.unspecified,
    pbIPFamily.IP_FAMILY_V4: IPFamily.v4,
    pbIPFamily.IP_FAMILY_V6: IPFamily.v6,
    pbIPFamily.IP_FAMILY_DUAL: IPFamily.dual,
}

PB_AGENT_STATUS_TO_STATUS = {
    pbAgentStatus.AGENT_STATUS_UNSPECIFIED: AgentStatus.unspecified,
    pbAgentStatus.AGENT_STATUS_OK: AgentStatus.ok,
    pbAgentStatus.AGENT_STATUS_WAIT: AgentStatus.wait,
    pbAgentStatus.AGENT_STATUS_DELETED: AgentStatus.deleted,
}

PB_AGENT_IMPL_TO_IMPL = {
    pbAgentImpl.IMPLEMENT_TYPE_UNSPECIFIED: AgentImplementType.unspecified,
    pbAgentImpl.IMPLEMENT_TYPE_RUST: AgentImplementType.rust,
    pbAgentImpl.IMPLEMENT_TYPE_NODE: AgentImplementType.node,
}


def reverse_map(map: Dict, value: Any) -> Any:
    for key, val in map.items():
        if val == value:
            return key
    raise RuntimeError(f"Value '{value}' not found in map")


class SynthGRPCTransport(KentikAPITransport):
    def __init__(
        self, credentials: Tuple[str, str], url: str = "synthetics.api.kentik.com:443", proxy: Optional[str] = None
    ) -> None:
        (email, token) = credentials
        self._url = url
        self._client = SyntheticsAdminService()
        self._credentials = [
            ("x-ch-auth-email", email),
            ("x-ch-auth-api-token", token),
        ]

    def req(self, op: str, **kwargs) -> Any:
        # to be refactored
        if op == "TestsList":
            results: List[SynTest] = []
            pbAgents = self._client.ListTests(ListTestsRequest(), metadata=self._credentials, target=self._url).tests
            for pbt in pbAgents:
                if pbt.type in [TestType.none.value, TestType.bgp_monitor.value]:
                    pb_test = SynTest("[empty]")
                    populate_test_from_pb(pbt, pb_test)
                    results.append(pb_test)
                if pbt.type == TestType.mesh.value:
                    pb_test = MeshTest("[empty]")
                    populate_mesh_test_from_pb(pbt, pb_test)
                    results.append(pb_test)
                else:
                    log.warning('Skipping test "%s" of unsupported type "%s"', pbt.name, pbt.type)
            return results

        elif op == "TestCreate":
            test: SynTest = kwargs["test"]
            test._id = ID("")  # TestCreate doesn't accept id
            pb_test = test_to_pb(test)
            result = self._client.CreateTest(
                CreateTestRequest(test=pb_test), metadata=self._credentials, target=self._url
            )
            out = SynTest("[empty]")
            populate_test_from_pb(result.test, out)
            return out

        elif op == "TestGet":
            id = str(kwargs["id"])
            result = self._client.GetTest(GetTestRequest(id=id), metadata=self._credentials, target=self._url)
            out = SynTest("[empty]")
            populate_test_from_pb(result.test, out)
            return out

        elif op == "TestPatch":
            pb_test = test_to_pb(kwargs["test"])
            mask = FieldMask(paths=[kwargs["mask"]])
            result = self._client.PatchTest(
                PatchTestRequest(test=pb_test, mask=mask), metadata=self._credentials, target=self._url
            )
            out = SynTest("[empty]")
            populate_test_from_pb(result.test, out)
            return out

        elif op == "TestDelete":
            id = str(kwargs["id"])
            self._client.DeleteTest(DeleteTestRequest(id=id), metadata=self._credentials, target=self._url)
            return None

        elif op == "TestStatusUpdate":
            id = str(kwargs["id"])
            status: TestStatus = kwargs["status"]
            pb_status = reverse_map(PB_TEST_STATUS_TO_STATUS, status)
            self._client.SetTestStatus(
                SetTestStatusRequest(id=id, status=pb_status), metadata=self._credentials, target=self._url
            )
            return None

        elif op == "AgentsList":
            pbAgents = self._client.ListAgents(ListAgentsRequest(), metadata=self._credentials, target=self._url).agents
            return [pb_to_agent(agent) for agent in pbAgents]

        elif op == "AgentGet":
            id = str(kwargs["id"])
            result = self._client.GetAgent(GetAgentRequest(id=id), metadata=self._credentials, target=self._url).agent
            return pb_to_agent(result)

        elif op == "AgentPatch":
            pb_agent = agent_to_pb(kwargs["agent"])
            pb_agent.name = ""  # AgentPatch doesn't accept name
            mask = FieldMask(paths=[kwargs["mask"]])
            result = self._client.PatchAgent(
                PatchAgentRequest(agent=pb_agent, mask=mask), metadata=self._credentials, target=self._url
            )
            return pb_to_agent(result.agent)

        elif op == "AgentDelete":
            id = str(kwargs["id"])
            self._client.DeleteAgent(DeleteAgentRequest(id=id), metadata=self._credentials, target=self._url)
            return None

        else:
            raise NotImplementedError(op)


def populate_test_from_pb(v: pbTest, out: SynTest) -> None:
    out.name = v.name
    out.type = TestType(v.type)
    out.status = PB_TEST_STATUS_TO_STATUS[v.status]
    out.deviceId = ID(v.device_id)
    out._id = ID(v.id)
    out._cdate = datetime.fromtimestamp(v.cdate.seconds + v.cdate.nanos / 1e9, timezone.utc).isoformat()
    out._edate = datetime.fromtimestamp(v.edate.seconds + v.edate.nanos / 1e9, timezone.utc).isoformat()

    settings = SynTestSettings()
    pupulate_settings_from_pb(v.settings, settings)
    out.settings = settings


def test_to_pb(v: SynTest) -> pbTest:
    out = pbTest()
    out.name = v.name
    out.device_id = str(v.deviceId)
    out.id = str(v.id)
    out.type = v.type.value
    out.status = reverse_map(PB_TEST_STATUS_TO_STATUS, v.status)
    out.settings.CopyFrom(settings_to_pb(v.settings))
    return out


def pupulate_ping_trace_test_from_pb(v: pbTest, out: PingTraceTest) -> None:
    populate_test_from_pb(v, out)
    populate_ping_test_settings_from_pb(v.settings, out.settings)


def populate_mesh_test_from_pb(v: pbTest, out: MeshTest) -> None:
    pupulate_ping_trace_test_from_pb(v, out)
    # nothing more to populate


def pupulate_settings_from_pb(v: pbTestSettings, out: SynTestSettings) -> None:
    out.agentIds = [ID(id) for id in v.agent_ids]
    out.tasks = v.tasks
    out.healthSettings = health_settings_from_pb(v.health_settings)
    out.monitoringSettings = monitoring_settings_from_pb(v.monitoring_settings)
    out.port = v.port
    out.period = v.period
    out.count = v.count
    out.expiry = v.expiry
    out.limit = v.limit
    out.protocol = Protocol(v.protocol)
    out.family = PB_FAMILY_TO_FAMILY[v.family]
    out.rollupLevel = v.rollup_level
    out.servers = v.servers


def settings_to_pb(v: SynTestSettings) -> pbTestSettings:
    out = pbTestSettings()

    # TODO: add missing fields to SynTestSettings
    out.ping.period = 60
    out.ping.count = 5
    out.ping.expiry = 3000
    out.trace.period = 60
    out.trace.count = 3
    out.trace.protocol = "udp"
    out.trace.port = 33434
    out.trace.expiry = 22500
    out.trace.limit = 30

    out.agent_ids.extend([str(id) for id in v.agentIds])
    out.tasks.extend(v.tasks)
    out.health_settings.CopyFrom(health_settings_to_pb(v.healthSettings))
    out.monitoring_settings.CopyFrom(monitoring_settings_to_pb(v.monitoringSettings))
    out.port = v.port
    out.period = v.period
    out.count = v.count
    out.expiry = v.expiry
    out.limit = v.limit
    out.protocol = v.protocol.value
    out.family = reverse_map(PB_FAMILY_TO_FAMILY, v.family)
    out.rollup_level = v.rollupLevel
    out.servers.extend(v.servers)
    return out


def populate_ping_test_settings_from_pb(v: pbTestSettings, out: PingTraceTestSettings):
    out.ping = PingTask(expiry=v.ping.expiry, period=v.ping.period, count=v.ping.count)
    out.trace = TraceTask(
        expiry=v.trace.expiry,
        period=v.trace.period,
        count=v.trace.count,
        limit=v.trace.limit,
        protocol=Protocol(v.trace.protocol),
        port=v.trace.port,
    )


def health_settings_from_pb(v: pbHealthSettings) -> HealthSettings:
    return HealthSettings(
        latencyCritical=v.latency_critical,
        latencyWarning=v.latency_warning,
        latencyCriticalStddev=v.latency_critical_stddev,
        latencyWarningStddev=v.latency_warning_stddev,
        packetLossCritical=v.packet_loss_critical,
        packetLossWarning=v.packet_loss_warning,
        jitterCritical=v.jitter_critical,
        jitterWarning=v.jitter_warning,
        jitterCriticalStddev=v.jitter_critical_stddev,
        jitterWarningStddev=v.jitter_warning_stddev,
        httpLatencyCritical=v.http_latency_critical,
        httpLatencyWarning=v.http_latency_warning,
        httpLatencyCriticalStddev=v.http_latency_critical_stddev,
        httpLatencyWarningStddev=v.http_latency_warning_stddev,
        httpValidCodes=v.http_valid_codes,
        dnsValidCodes=v.dns_valid_codes,
    )


def health_settings_to_pb(v: HealthSettings) -> pbHealthSettings:
    out = pbHealthSettings()
    out.latency_critical = v.latencyCritical
    out.latency_warning = v.latencyWarning
    out.latency_critical_stddev = v.latencyCriticalStddev
    out.latency_warning_stddev = v.latencyWarningStddev
    out.packet_loss_critical = v.packetLossCritical
    out.packet_loss_warning = v.packetLossWarning
    out.jitter_critical = v.jitterCritical
    out.jitter_warning = v.jitterWarning
    out.jitter_critical_stddev = v.jitterCriticalStddev
    out.jitter_warning_stddev = v.jitterWarningStddev
    out.http_latency_critical = v.httpLatencyCritical
    out.http_latency_warning = v.httpLatencyWarning
    out.http_latency_critical_stddev = v.httpLatencyCriticalStddev
    out.http_latency_warning_stddev = v.httpLatencyWarningStddev
    out.http_valid_codes.extend(v.httpValidCodes)
    out.dns_valid_codes.extend(v.dnsValidCodes)
    return out


def monitoring_settings_from_pb(v: pbMonitoringSettings) -> MonitoringSettings:
    return MonitoringSettings(
        activationGracePeriod=v.activation_grace_period,
        activationTimeUnit=v.activation_time_unit,
        activationTimeWindow=v.activation_time_window,
        activationTimes=v.activation_times,
        notificationChannels=v.notification_channels,
    )


def monitoring_settings_to_pb(v: MonitoringSettings) -> pbMonitoringSettings:
    out = pbMonitoringSettings()
    out.activation_grace_period = v.activationGracePeriod
    out.activation_time_unit = v.activationTimeUnit
    out.activation_time_window = v.activationTimeWindow
    out.activation_times = v.activationTimes
    out.notification_channels.extend(v.notificationChannels)
    return out


def pb_to_agent(v: pbAgent) -> Agent:
    return Agent(
        id=ID(v.id),
        name=v.name,
        status=PB_AGENT_STATUS_TO_STATUS[v.status],
        alias=v.alias,
        type=v.type,
        os=v.os,
        ip=IP(v.ip),
        lat=v.lat,
        long=v.long,
        last_authed=datetime.fromtimestamp(v.last_authed.seconds + v.last_authed.nanos / 1e9, timezone.utc).isoformat(),
        family=PB_FAMILY_TO_FAMILY[v.family],
        asn=v.asn,
        site_id=ID(v.site_id),
        version=v.version,
        challenge=v.challenge,
        city=v.city,
        region=v.region,
        country=v.country,
        test_ids=[ID(id) for id in v.test_ids],
        local_ip=IP(v.local_ip),
        cloud_vpc=v.cloud_vpc,
        agent_impl=PB_AGENT_IMPL_TO_IMPL[v.agent_impl],
    )


def agent_to_pb(v: Agent) -> pbAgent:
    return pbAgent(
        id=str(v.id),
        name=v.name,
        status=reverse_map(PB_AGENT_STATUS_TO_STATUS, v.status),
        alias=v.alias,
        type=v.type,
        os=v.os,
        ip=str(v.ip),
        lat=v.lat,
        long=v.long,
        family=reverse_map(PB_FAMILY_TO_FAMILY, v.family),
        asn=v.asn,
        site_id=str(v.site_id),
        version=v.version,
        challenge=v.challenge,
        city=v.city,
        region=v.region,
        country=v.country,
        test_ids=[str(id) for id in v.test_ids],
        local_ip=str(v.local_ip),
        cloud_vpc=v.cloud_vpc,
        agent_impl=reverse_map(PB_AGENT_IMPL_TO_IMPL, v.agent_impl),
    )
