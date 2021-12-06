import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

import grpc.experimental as _
from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.timestamp_pb2 import Timestamp

from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ASN as pbASN
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Agent as pbAgent
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentHealth as pbAgentHealth
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentStatus as pbAgentStatus
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import AgentTaskConfig as pbAgentTaskConfig
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import City as pbCity
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Country as pbCountry
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    CreateTestRequest,
    DeleteAgentRequest,
    DeleteTestRequest,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import DNSTaskDefinition as pbDNSTaskDefinition
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Geo as pbGeo
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    GetAgentRequest,
    GetHealthForTestsRequest,
    GetTestRequest,
    GetTraceForTestRequest,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    GetTraceForTestResponse as pbGetTraceForTestResponse,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Health as pbHealth
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import HealthMoment as pbHealthMoment
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import HealthSettings as pbHealthSettings
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    HTTPTaskDefinition as pbHTTPTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import IDByIP as pbIDByIP
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ImplementType as pbAgentImpl
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import IPFamily as pbIPFamily
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import IPInfo as pbIPInfo
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
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Region as pbRegion
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import SetTestStatusRequest
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    ShakeTaskDefinition as pbShakeTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Stats as pbStats
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
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import Trace as pbTrace
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TraceHop as pbTraceHop
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TraceProbe as pbTraceProbe
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TracerouteInfo as pbTracerouteInfo
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TracerouteLookup as pbTracerouteLookup
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import TracerouteResult as pbTracerouteResult
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    TraceTaskDefinition as pbTraceTaskDefinition,
)
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2_grpc import (
    SyntheticsAdminService,
    SyntheticsDataService,
)
from kentik_api.public import device
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
    HealthMoment,
    MeshColumn,
    MeshMetric,
    MeshMetrics,
    MeshResponse,
    OverallHealth,
    TaskHealth,
    TestHealth,
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
from .trace import (
    ASN,
    DNS,
    City,
    Country,
    Geo,
    GetTraceForTestResponse,
    IDbyIP,
    IPInfo,
    Region,
    Stats,
    Trace,
    TraceHop,
    TraceProbe,
    TracerouteInfo,
    TracerouteLookup,
    TracerouteResult,
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
        OPS: Dict[str, Callable] = {
            "TestsList": self.tests_list,
            "TestCreate": self.test_create,
            "TestGet": self.test_get,
            "TestPatch": self.test_patch,
            "TestDelete": self.test_delete,
            "TestStatusUpdate": self.test_status_update,
            "AgentsList": self.agent_list,
            "AgentGet": self.agent_get,
            "AgentPatch": self.agent_patch,
            "AgentDelete": self.agent_delete,
            "GetHealthForTests": self.get_health_for_tests,
            "GetTraceForTest": self.get_trace_for_test,
        }

        try:
            svc = OPS[op]
        except KeyError:
            raise RuntimeError(f"Invalid operation '{op}'")

        return svc(**kwargs)

    def tests_list(self, **kwargs) -> List[SynTest]:
        tests: List[SynTest] = []
        pb_tests = self._admin.ListTests(ListTestsRequest(), metadata=self._credentials, target=self._url).tests
        for pbt in pb_tests:
            if pbt.type in [TestType.none.value, TestType.bgp_monitor.value]:
                pb_test = SynTest("[empty]")
                populate_test_from_pb(pbt, pb_test)
                tests.append(pb_test)
            if pbt.type == TestType.mesh.value:
                pb_test = MeshTest("[empty]")
                populate_mesh_test_from_pb(pbt, pb_test)
                tests.append(pb_test)
            else:
                log.warning('Skipping test "%s" of unsupported type "%s"', pbt.name, pbt.type)
        return tests

    def test_create(self, **kwargs) -> SynTest:
        test: SynTest = kwargs["test"]
        test._id = ID("")  # TestCreate doesn't accept id
        pb_test = pb_from_test(test)
        response = self._admin.CreateTest(CreateTestRequest(test=pb_test), metadata=self._credentials, target=self._url)
        out = SynTest("[empty]")
        populate_test_from_pb(response.test, out)
        return out

    def test_get(self, **kwargs) -> SynTest:
        id = str(kwargs["id"])
        response = self._admin.GetTest(GetTestRequest(id=id), metadata=self._credentials, target=self._url)
        out = SynTest("[empty]")
        populate_test_from_pb(response.test, out)
        return out

    def test_patch(self, **kwargs) -> SynTest:
        pb_test = pb_from_test(kwargs["test"])
        mask = FieldMask(paths=[kwargs["mask"]])
        patch_test_req = PatchTestRequest(test=pb_test, mask=mask)
        response = self._admin.PatchTest(request=patch_test_req, metadata=self._credentials, target=self._url)
        out = SynTest("[empty]")
        populate_test_from_pb(response.test, out)
        return out

    def test_delete(self, **kwargs) -> None:
        id = str(kwargs["id"])
        self._admin.DeleteTest(DeleteTestRequest(id=id), metadata=self._credentials, target=self._url)

    def test_status_update(self, **kwargs) -> None:
        id = str(kwargs["id"])
        status: TestStatus = kwargs["status"]
        pb_status = reverse_map(PB_TEST_STATUS_TO_STATUS, status)
        set_status_req = SetTestStatusRequest(id=id, status=pb_status)
        self._admin.SetTestStatus(request=set_status_req, metadata=self._credentials, target=self._url)

    def agent_list(self, **kwargs) -> List[Agent]:
        pb_agents = self._admin.ListAgents(ListAgentsRequest(), metadata=self._credentials, target=self._url).agents
        return [pb_to_agent(agent) for agent in pb_agents]

    def agent_get(self, **kwargs) -> Agent:
        id = str(kwargs["id"])
        response = self._admin.GetAgent(GetAgentRequest(id=id), metadata=self._credentials, target=self._url).agent
        return pb_to_agent(response)

    def agent_patch(self, **kwargs) -> Agent:
        pb_agent = pb_from_agent(kwargs["agent"])
        pb_agent.name = ""  # AgentPatch doesn't accept name
        mask = FieldMask(paths=[kwargs["mask"]])
        patch_agent_req = PatchAgentRequest(agent=pb_agent, mask=mask)
        response = self._admin.PatchAgent(request=patch_agent_req, metadata=self._credentials, target=self._url)
        return pb_to_agent(response.agent)

    def agent_delete(self, **kwargs) -> None:
        id = str(kwargs["id"])
        self._admin.DeleteAgent(DeleteAgentRequest(id=id), metadata=self._credentials, target=self._url)

    def get_health_for_tests(self, **kwargs) -> List[TestHealth]:
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
        response = self._data.GetHealthForTests(request=get_health_req, metadata=self._credentials, target=self._url)
        return pb_to_health_tests(response.health)

    def get_trace_for_test(self, **kwargs) -> GetTraceForTestResponse:
        id = str(kwargs["id"])
        agents = [str(id) for id in kwargs["agent_ids"]]
        ips = [str(ip) for ip in kwargs["target_ips"]]
        start = Timestamp(seconds=int(kwargs["start_time"].timestamp()))
        end = Timestamp(seconds=int(kwargs["end_time"].timestamp()))
        get_trace_req = GetTraceForTestRequest(
            id=id,
            start_time=start,
            end_time=end,
            agent_ids=agents,
            target_ips=ips,
        )
        response = self._data.GetTraceForTest(request=get_trace_req, metadata=self._credentials, target=self._url)
        return pb_to_trace_response(response)


def reverse_map(src_map: Dict[Any, Any], value: Any) -> Any:
    for key, val in src_map.items():
        if val == value:
            return key
    raise RuntimeError(f"Value '{value}' not found in map")


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
def pb_from_test(v: SynTest) -> pbTest:
    out = pbTest()
    out.name = v.name
    out.device_id = str(v.deviceId)
    out.id = str(v.id)
    out.type = v.type.value
    out.status = reverse_map(PB_TEST_STATUS_TO_STATUS, v.status)
    out.settings.CopyFrom(pb_from_settings(v.settings))
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
    out.healthSettings = pb_to_health_settings(v.health_settings)
    out.monitoringSettings = pb_to_monitoring_settings(v.monitoring_settings)
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
def pb_from_settings(v: SynTestSettings) -> pbTestSettings:
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
    out.health_settings.CopyFrom(pb_from_health_settings(v.healthSettings))
    out.monitoring_settings.CopyFrom(pb_from_monitoring_settings(v.monitoringSettings))
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


def pb_to_health_settings(v: pbHealthSettings) -> HealthSettings:
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
def pb_from_health_settings(v: HealthSettings) -> pbHealthSettings:
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


def pb_to_monitoring_settings(v: pbMonitoringSettings) -> MonitoringSettings:
    return MonitoringSettings(
        activationGracePeriod=v.activation_grace_period,
        activationTimeUnit=v.activation_time_unit,
        activationTimeWindow=v.activation_time_window,
        activationTimes=v.activation_times,
        notificationChannels=v.notification_channels,
    )


def pb_from_monitoring_settings(v: MonitoringSettings) -> pbMonitoringSettings:
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


def pb_from_agent(v: Agent) -> pbAgent:
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


def pb_to_health_tests(v: List[pbTestHealth]) -> List[TestHealth]:
    return [pb_to_health_test(health) for health in v]


def pb_to_health_test(v: pbTestHealth) -> TestHealth:
    return TestHealth(
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


def pb_to_trace_response(v: pbGetTraceForTestResponse) -> GetTraceForTestResponse:
    return GetTraceForTestResponse(
        lookups=pb_to_lookups(v.lookups),
        trace_routes=[pb_to_trace_routes(item) for item in v.trace_routes],
        trace_routes_info=pb_to_trace_route_info(v.trace_routes_info),
    )


def pb_to_trace_routes(v: pbTracerouteResult) -> TracerouteResult:
    return TracerouteResult(
        time=pb_to_datetime_iso(v.time),
        traces=[pb_to_trace(trace) for trace in v.traces],
        hop_count=v.hop_count,
        count=pb_to_stats(v.count),
        distance=pb_to_stats(v.distance),
    )


def pb_to_trace(v: pbTrace) -> Trace:
    return Trace(
        agent_id=ID(v.agent_id),
        agent_ip=IP(v.agent_ip),
        target_ip=IP(v.target_ip),
        hop_count=v.hop_count,
        probes=[pb_to_probe(probe) for probe in v.probes],
    )


def pb_to_probe(v: pbTraceProbe) -> TraceProbe:
    return TraceProbe(
        as_path=v.as_path,
        completed=v.completed,
        hop_count=v.hop_count,
        region_path=v.region_path,
        site_path=v.site_path,
        hops=[pb_to_trace_hop(hop) for hop in v.hops],
    )


def pb_to_trace_hop(v: pbTraceHop) -> TraceHop:
    return TraceHop(
        ttl=v.ttl,
        ip=IP(v.ip),
        timeout=v.timeout,
        latency=v.latency,
        min_expected_latency=v.min_expected_latency,
        asn=v.asn,
        site=v.site,
        region=v.region,
        target=v.target,
        trace_end=v.trace_end,
    )


def pb_to_stats(v: pbStats) -> Stats:
    return Stats(
        average=v.average,
        max=v.max,
        total=v.total,
    )


def pb_to_trace_route_info(v: pbTracerouteInfo) -> TracerouteInfo:
    return TracerouteInfo(
        is_trace_routes_truncated=v.is_trace_routes_truncated,
        max_asn_path_count=v.max_asn_path_count,
        max_site_path_count=v.max_site_path_count,
        max_region_path_count=v.max_region_path_count,
    )


def pb_to_lookups(v: pbTracerouteLookup) -> TracerouteLookup:
    return TracerouteLookup(
        agent_id_by_ip=[pb_to_id_by_ip(item) for item in v.agent_id_by_ip],
        agents=[pb_to_agent(agent) for agent in v.agents],
        asns=[pb_to_asn(asn) for asn in v.asns],
        device_id_by_ip=[pb_to_id_by_ip(item) for item in v.device_id_by_ip],
        site_id_by_ip=[pb_to_id_by_ip(item) for item in v.site_id_by_ip],
        ips=[pb_to_ipinfo(item) for item in v.ips],
    )


def pb_to_asn(v: pbASN) -> ASN:
    return ASN(
        id=ID(v.id),
        name=v.name,
    )


def pb_to_id_by_ip(v: pbIDByIP) -> IDbyIP:
    return IDbyIP(
        id=ID(v.id),
        ip=IP(v.ip),
    )


def pb_to_ipinfo(v: pbIPInfo) -> IPInfo:
    return IPInfo(
        ip=IP(v.ip),
        asn=pb_to_asn(v.asn),
        geo=pb_to_geo(v.geo),
        dns=DNS(v.dns.name),
        device_id=ID(v.device_id),
        site_id=ID(v.site_id),
        egress=v.egress,
    )


def pb_to_geo(v: pbGeo) -> Geo:
    return Geo(
        country=pb_to_country(v.country),
        city=pb_to_city(v.city),
        region=pb_to_region(v.region),
    )


def pb_to_country(v: pbCountry) -> Country:
    return Country(
        code=v.code,
        name=v.name,
    )


def pb_to_city(v: pbCity) -> City:
    return City(
        id=ID(v.id),
        name=v.name,
        longitude=v.longitude,
        latitude=v.latitude,
    )


def pb_to_region(v: pbRegion) -> Region:
    return Region(
        id=ID(v.id),
        name=v.name,
    )
