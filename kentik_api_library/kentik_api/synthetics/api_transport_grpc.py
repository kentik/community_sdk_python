import logging
from typing import Any, Optional, Tuple, List
from datetime import datetime, timezone

import grpc.experimental as _

from .api_transport import KentikAPIRequestError, KentikAPITransport

from generated.kentik.synthetics.v202101beta1.synthetics_pb2_grpc import SyntheticsAdminService
from generated.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    ListTestsRequest,
    Test as pbTest,
    TestStatus as pbTestStatus,
    TestSettings as pbTestSettings,
    IPFamily as pbIPFamily,
    HealthSettings as pbHealthSettings,
    TestMonitoringSettings as pbMonitoringSettings,
)

from kentik_api.synthetics.synth_tests import (
    MeshTest,
    PingTask,
    SynTest,
    PingTraceTest,
    TestType,
    SynTestSettings,
    TestStatus,
    HealthSettings,
    MonitoringSettings,
    PingTraceTestSettings,
    Protocol,
    IPFamily,
    TraceTask,
)

log = logging.getLogger("api_transport_grpc")


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
            pbTests = self._client.ListTests(ListTestsRequest(), metadata=self._credentials, target=self._url).tests
            for pbt in pbTests:
                if pbt.type in [TestType.none.value, TestType.bgp_monitor.value]:
                    test = SynTest("[empty]")
                    populate_test_from_pb(pbt, test)
                    results.append(test)
                if pbt.type == TestType.mesh.value:
                    test = MeshTest("[empty]")
                    populate_mesh_test_from_pb(pbt, test)
                    results.append(test)
                else:
                    log.warning('Skipping test "%s" of unsupported type "%s"', pbt.name, pbt.type)
            return results
        raise NotImplementedError


def populate_test_from_pb(v: pbTest, out: SynTest) -> None:
    STATUS = {
        pbTestStatus.TEST_STATUS_UNSPECIFIED: TestStatus.none,
        pbTestStatus.TEST_STATUS_ACTIVE: TestStatus.active,
        pbTestStatus.TEST_STATUS_PAUSED: TestStatus.paused,
        pbTestStatus.TEST_STATUS_DELETED: TestStatus.deleted,
    }

    out.name = v.name
    out.type = TestType(v.type)
    out.status = STATUS[v.status]
    out.deviceId = v.device_id
    out._id = v.id
    out._cdate = datetime.fromtimestamp(v.cdate.seconds + v.cdate.nanos / 1e9, timezone.utc)
    out._edate = datetime.fromtimestamp(v.edate.seconds + v.edate.nanos / 1e9, timezone.utc)

    settings = SynTestSettings()
    pupulate_settings_from_pb(v.settings, settings)
    out.settings = settings


def pupulate_ping_trace_test_from_pb(v: pbTest, out: PingTraceTest) -> None:
    populate_test_from_pb(v, out)
    populate_ping_test_settings_from_pb(v.settings, out.settings)


def populate_mesh_test_from_pb(v: pbTest, out: MeshTest) -> None:
    pupulate_ping_trace_test_from_pb(v, out)
    # nothing more to populate


def pupulate_settings_from_pb(v: pbTestSettings, out: SynTestSettings) -> None:
    FAMILY = {
        pbIPFamily.IP_FAMILY_UNSPECIFIED: IPFamily.unspecified,
        pbIPFamily.IP_FAMILY_V4: IPFamily.v4,
        pbIPFamily.IP_FAMILY_V6: IPFamily.v6,
        pbIPFamily.IP_FAMILY_DUAL: IPFamily.dual,
    }
    out.agentIds = v.agent_ids
    out.tasks = v.tasks
    out.healthSettings = health_settings_from_pb(v.health_settings)
    out.monitoringSettings = monitoring_settings_from_pb(v.monitoring_settings)
    out.port = v.port
    out.period = v.period
    out.count = v.count
    out.expiry = v.expiry
    out.limit = v.limit
    out.protocol = Protocol(v.protocol)
    out.family = FAMILY[v.family]
    out.rollupLevel = v.rollup_level
    out.servers = v.servers


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


def monitoring_settings_from_pb(v: pbMonitoringSettings) -> MonitoringSettings:
    return MonitoringSettings(
        activationGracePeriod=v.activation_grace_period,
        activationTimeUnit=v.activation_time_unit,
        activationTimeWindow=v.activation_time_window,
        activationTimes=v.activation_times,
        notificationChannels=v.notification_channels,
    )
