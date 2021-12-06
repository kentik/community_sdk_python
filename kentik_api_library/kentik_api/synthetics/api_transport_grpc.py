import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import grpc.experimental as _
from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.timestamp_pb2 import Timestamp

from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Agent as pbAgent
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentHealth as pbAgentHealth
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentStatus as pbAgentStatus
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentTaskConfig as pbAgentTaskConfig
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    CreateTestRequest,
    DeleteAgentRequest,
    DeleteTestRequest,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import DNSTaskDefinition as pbDNSTaskDefinition
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    GetAgentRequest,
    GetHealthForTestsRequest,
    GetTestRequest,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Health as pbHealth
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import HealthMoment as pbHealthMoment
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import HealthSettings as pbHealthSettings
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    HTTPTaskDefinition as pbHTTPTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ImplementType as pbAgentImpl
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import IPFamily as pbIPFamily
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    KnockTaskDefinition as pbKnockTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ListAgentsRequest, ListTestsRequest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import MeshColumn as pbMeshColumn
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import MeshMetric as pbMeshMetric
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import MeshMetrics as pbMeshMetrics
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import MeshResponse as pbMeshResponse
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import PatchAgentRequest, PatchTestRequest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    PingTaskDefinition as pbPingTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import SetTestStatusRequest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    ShakeTaskDefinition as pbShakeTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Task as pbTask
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TaskHealth as pbTaskHealth
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TaskState as pbTaskState
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Test as pbTest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TestHealth as pbTestHealth
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    TestMonitoringSettings as pbMonitoringSettings,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TestSettings as pbTestSettings
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TestStatus as pbTestStatus
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    TraceTaskDefinition as pbTraceTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2_grpc import (
    SyntheticsAdminService,
    SyntheticsDataService,
)
from kentik_api.public.types import ID, IP
from kentik_api.requests_payload.conversions import convert_or_none
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
from .api_transport import KentikAPITransport
from .health import (
    AgentHealth,
    AgentTaskConfig,
    Health,
    HealthMoment,
    MeshColumn,
    MeshMetric,
    MeshMetrics,
    MeshResponse,
    OverallHealth,
    TaskHealth,
)
from .task import (
    DNSTaskDefinition,
    HTTPTaskDefinition,
    KnockTaskDefinition,
    PingTaskDefinition,
    ShakeTaskDefinition,
    Task,
    TaskState,
    TraceTaskDefinition,
)

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
    pbAgentStatus.AGENT_STATUS_UNSPECIFIED: AgentStatus.UNSPECIFIED,
    pbAgentStatus.AGENT_STATUS_OK: AgentStatus.OK,
    pbAgentStatus.AGENT_STATUS_WAIT: AgentStatus.WAIT,
    pbAgentStatus.AGENT_STATUS_DELETED: AgentStatus.DELETED,
}

PB_AGENT_IMPL_TO_IMPL = {
    pbAgentImpl.IMPLEMENT_TYPE_UNSPECIFIED: AgentImplementType.UNSPECIFIED,
    pbAgentImpl.IMPLEMENT_TYPE_RUST: AgentImplementType.RUST,
    pbAgentImpl.IMPLEMENT_TYPE_NODE: AgentImplementType.NODE,
}

PB_TASK_STATE_TO_STATE = {
    pbTaskState.TASK_STATE_UNSPECIFIED: TaskState.UNSPECIFIED,
    pbTaskState.TASK_STATE_CREATED: TaskState.CREATED,
    pbTaskState.TASK_STATE_UPDATED: TaskState.UPDATED,
    pbTaskState.TASK_STATE_DELETED: TaskState.DELETED,
}


def reverse_map(src_map: Dict, value: Any) -> Any:
    for key, val in src_map.items():
        if val == value:
            return key
    raise RuntimeError(f"Value '{value}' not found in map")


class SynthGRPCTransport(KentikAPITransport):
    def __init__(
        self, credentials: Tuple[str, str], url: str = "synthetics.api.kentik.com:443", proxy: Optional[str] = None
    ) -> None:
        (email, token) = credentials
        self._url = url
        self._admin = SyntheticsAdminService()
        self._data = SyntheticsDataService()
        self._credentials = [
            ("x-ch-auth-email", email),
            ("x-ch-auth-api-token", token),
        ]

    def req(self, op: str, **kwargs) -> Any:
        # to be refactored
        if op == "TestsList":
            results: List[SynTest] = []
            pb_agents = self._admin.ListTests(ListTestsRequest(), metadata=self._credentials, target=self._url).tests
            for pbt in pb_agents:
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

        if op == "TestCreate":
            test: SynTest = kwargs["test"]
            test._id = ID("")  # TestCreate doesn't accept id
            pb_test = test_to_pb(test)
            result = self._admin.CreateTest(
                CreateTestRequest(test=pb_test), metadata=self._credentials, target=self._url
            )
            out = SynTest("[empty]")
            populate_test_from_pb(result.test, out)
            return out

        if op == "TestGet":
            id = str(kwargs["id"])
            result = self._admin.GetTest(GetTestRequest(id=id), metadata=self._credentials, target=self._url)
            out = SynTest("[empty]")
            populate_test_from_pb(result.test, out)
            return out

        if op == "TestPatch":
            pb_test = test_to_pb(kwargs["test"])
            mask = FieldMask(paths=[kwargs["mask"]])
            result = self._admin.PatchTest(
                PatchTestRequest(test=pb_test, mask=mask), metadata=self._credentials, target=self._url
            )
            out = SynTest("[empty]")
            populate_test_from_pb(result.test, out)
            return out

        if op == "TestDelete":
            id = str(kwargs["id"])
            self._admin.DeleteTest(DeleteTestRequest(id=id), metadata=self._credentials, target=self._url)
            return None

        if op == "TestStatusUpdate":
            id = str(kwargs["id"])
            status: TestStatus = kwargs["status"]
            pb_status = reverse_map(PB_TEST_STATUS_TO_STATUS, status)
            self._admin.SetTestStatus(
                SetTestStatusRequest(id=id, status=pb_status), metadata=self._credentials, target=self._url
            )
            return None

        if op == "AgentsList":
            pb_agents = self._admin.ListAgents(ListAgentsRequest(), metadata=self._credentials, target=self._url).agents
            return [pb_to_agent(agent) for agent in pb_agents]

        if op == "AgentGet":
            id = str(kwargs["id"])
            result = self._admin.GetAgent(GetAgentRequest(id=id), metadata=self._credentials, target=self._url).agent
            return pb_to_agent(result)

        if op == "AgentPatch":
            pb_agent = agent_to_pb(kwargs["agent"])
            pb_agent.name = ""  # AgentPatch doesn't accept name
            mask = FieldMask(paths=[kwargs["mask"]])
            result = self._admin.PatchAgent(
                PatchAgentRequest(agent=pb_agent, mask=mask), metadata=self._credentials, target=self._url
            )
            return pb_to_agent(result.agent)

        if op == "AgentDelete":
            id = str(kwargs["id"])
            self._admin.DeleteAgent(DeleteAgentRequest(id=id), metadata=self._credentials, target=self._url)
            return None

        if op == "GetHealthForTests":
            ids = [str(id) for id in kwargs["test_ids"]]
            agents = [str(id) for id in kwargs["agent_ids"]]
            tasks = [str(id) for id in kwargs["task_ids"]]
            start = Timestamp(seconds=int(kwargs["start_time"].timestamp()))
            end = Timestamp(seconds=int(kwargs["end_time"].timestamp()))
            get_health_req = GetHealthForTestsRequest(
                ids=ids,
                start_time=start,
                end_time=end,
                agent_ids=agents,
                task_ids=tasks,
                augment=kwargs["augment"],
            )
            result = self._data.GetHealthForTests(
                request=get_health_req,
                metadata=self._credentials,
                target=self._url,
            )
            return pb_to_health(result.health)

        raise NotImplementedError(op)


def populate_test_from_pb(v: pbTest, out: SynTest) -> None:
    out.name = v.name
    out.type = TestType(v.type)
    out.status = PB_TEST_STATUS_TO_STATUS[v.status]
    out.deviceId = ID(v.device_id)
    out._id = ID(v.id)
    out._cdate = pb_to_datetime_iso(v.cdate)
    out._edate = pb_to_datetime_iso(v.edate)

    settings = SynTestSettings()
    pupulate_settings_from_pb(v.settings, settings)
    out.settings = settings


# disable no-member linting as gRPC structures are wrongly recognized as to have missing attributes
# pylint: disable=no-member
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


# disable no-member linting as gRPC structures are wrongly recognized as to have missing attributes
# pylint: disable=no-member
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


# disable no-member linting as gRPC structures are wrongly recognized as to have missing attributes
# pylint: disable=no-member
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
        last_authed=pb_to_datetime_iso(v.last_authed),
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


def pb_to_health(v: List[pbTestHealth]) -> List[Health]:
    return [pb_to_health_(health) for health in v]


def pb_to_health_(v: pbTestHealth) -> Health:
    return Health(
        test_id=ID(v.test_id),
        tasks=[pb_to_task_health(task) for task in v.tasks],
        overall_health=pb_to_overall_health(v.overall_health),
        health_ts=[pb_to_overall_health(health) for health in v.health_ts],
        agent_task_config=[pb_to_agent_task_config(config) for config in v.agent_task_config],
        mesh=[pb_to_mesh_response(item) for item in v.mesh],
    )


def pb_to_mesh_response(v: pbMeshResponse) -> MeshResponse:
    return MeshResponse(
        id=ID(v.id),
        name=v.name,
        local_ip=IP(v.local_ip),
        ip=IP(v.ip),
        alias=v.alias,
        columns=[pb_to_column(column) for column in v.columns],
    )


def pb_to_column(v: pbMeshColumn) -> MeshColumn:
    return MeshColumn(
        id=ID(v.id),
        name=v.name,
        alias=v.alias,
        target=IP(v.target),
        metrics=pb_to_metrics(v.metrics),
        health=[pb_to_metrics(metric) for metric in v.health],
    )


def pb_to_metrics(v: pbMeshMetrics) -> MeshMetrics:
    return MeshMetrics(
        time=pb_to_datetime_iso(v.time),
        latency=pb_to_metric(v.latency),
        packet_loss=pb_to_metric(v.packet_loss),
        jitter=pb_to_metric(v.jitter),
    )


def pb_to_metric(v: pbMeshMetric) -> MeshMetric:
    return MeshMetric(
        name=v.name,
        health=v.health,
        value=v.value,
    )


def pb_to_agent_task_config(v: pbAgentTaskConfig) -> AgentTaskConfig:
    return AgentTaskConfig(
        id=ID(v.id),
        targets=[IP(ip) for ip in v.targets],
    )


def pb_to_task_health(v: pbTaskHealth) -> TaskHealth:
    return TaskHealth(
        task=pb_to_task(v.task),
        agents=[pb_to_agent_health(agent) for agent in v.agents],
        overall_health=pb_to_overall_health(v.overall_health),
    )


def pb_to_agent_health(v: pbAgentHealth) -> AgentHealth:
    return AgentHealth(
        agent=pb_to_agent(v.agent),
        health=[pb_to_health_moment(health) for health in v.health],
        overall_health=pb_to_overall_health(v.overall_health),
    )


def pb_to_health_moment(v: pbHealthMoment) -> HealthMoment:
    return HealthMoment(
        time=pb_to_datetime_iso(v.time),
        src_ip=IP(v.src_ip),
        dst_ip=IP(v.dst_ip),
        packet_loss=v.packet_loss,
        avg_latency=v.avg_latency,
        avg_weighted_latency=v.avg_weighted_latency,
        rolling_avg_latency=v.rolling_avg_latency,
        rolling_stddev_latency=v.rolling_stddev_latency,
        rolling_avg_weighted_latency=v.rolling_avg_weighted_latency,
        latency_health=v.latency_health,
        packet_loss_health=v.packet_loss_health,
        overall_health=pb_to_overall_health(v.overall_health),
        avg_jitter=v.avg_jitter,
        rolling_avg_jitter=v.rolling_avg_jitter,
        rolling_std_jitter=v.rolling_std_jitter,
        jitter_health=v.jitter_health,
        data=v.data,
        size=v.size,
        status=v.status,
        task_type=v.task_type,
    )


def pb_to_overall_health(v: pbHealth) -> OverallHealth:
    return OverallHealth(
        health=v.health,
        time=pb_to_datetime_iso(v.time),
    )


def pb_to_task(v: pbTask) -> Task:
    return Task(
        id=ID(v.id),
        test_id=ID(v.test_id),
        device_id=ID(v.device_id),
        state=PB_TASK_STATE_TO_STATE[v.state],
        status=v.status,
        family=PB_FAMILY_TO_FAMILY[v.family],
        ping=pb_to_ping_task(v.ping),
        traceroute=pb_to_trace_task(v.traceroute),
        http=pb_to_http_task(v.http),
        knock=pb_to_knock_task(v.knock),
        dns=pb_to_dns_task(v.dns),
        shake=pb_to_shake_task(v.shake),
    )


def pb_to_ping_task(v: pbPingTaskDefinition) -> Optional[PingTaskDefinition]:
    if v == pbPingTaskDefinition():
        return None
    return PingTaskDefinition(
        target=IP(v.target),
        period=v.period,
        expiry=v.expiry,
        count=v.count,
    )


def pb_to_trace_task(v: pbTraceTaskDefinition) -> Optional[TraceTaskDefinition]:
    if v == pbTraceTaskDefinition():
        return None
    return TraceTaskDefinition(
        target=IP(v.target),
        period=v.period,
        expiry=v.expiry,
        limit=v.limit,
    )


def pb_to_http_task(v: pbHTTPTaskDefinition) -> Optional[HTTPTaskDefinition]:
    if v == pbHTTPTaskDefinition():
        return None
    return HTTPTaskDefinition(
        target=IP(v.target),
        period=v.period,
        expiry=v.expiry,
    )


def pb_to_knock_task(v: pbKnockTaskDefinition) -> Optional[KnockTaskDefinition]:
    if v == pbKnockTaskDefinition():
        return None
    return KnockTaskDefinition(
        target=IP(v.target),
        period=v.period,
        expiry=v.expiry,
        count=v.count,
        port=v.port,
    )


def pb_to_dns_task(v: pbDNSTaskDefinition) -> Optional[DNSTaskDefinition]:
    if v == pbDNSTaskDefinition():
        return None
    return DNSTaskDefinition(
        target=IP(v.target),
        period=v.period,
        expiry=v.expiry,
        count=v.count,
        port=v.count,
        type=v.type,
        resolver=v.resolver,
    )


def pb_to_shake_task(v: pbShakeTaskDefinition) -> Optional[ShakeTaskDefinition]:
    if v == pbShakeTaskDefinition():
        return None
    return ShakeTaskDefinition(
        target=IP(v.target),
        port=v.port,
        period=v.period,
        expiry=v.expiry,
    )


def pb_to_datetime_iso(v: Timestamp) -> str:
    return datetime.fromtimestamp(v.seconds + v.nanos / 1e9, timezone.utc).isoformat()
