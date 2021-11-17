import logging
from typing import Any, Optional, Tuple
from datetime import datetime, timezone

from .api_transport import KentikAPIRequestError, KentikAPITransport

import grpc.experimental as _
from kentik_api.grpc.kentik.synthetics.v202101beta1.synthetics_pb2_grpc import SyntheticsAdminService
from kentik_api.grpc.kentik.synthetics.v202101beta1.synthetics_pb2 import (
    ListTestsRequest,
    Test as pbTest,
    TestStatus as pbTestStatus,
    TestSettings as pbTestSettings,
    IPFamily as pbIPFamily,
    HealthSettings as pbHealthSettings,
    TestMonitoringSettings as pbMonitoringSettings,
)

from kentik_api.synthetics.synth_tests import (
    SynTest,
    TestType,
    SynTestSettings,
    TestStatus,
    HealthSettings,
    MonitoringSettings,
    Protocol,
    IPFamily,
)

log = logging.getLogger("api_transport_grpc")


class SynthGRPCTransport(KentikAPITransport):
    def __init__(
        self, credentials: Tuple[str, str], url: str = "synthetics.api.kentik.com:443", proxy: Optional[str] = None
    ):
        (email, token) = credentials
        self._url = url
        self._client = SyntheticsAdminService()
        self._credentials = [
            ("x-ch-auth-email", email),
            ("x-ch-auth-api-token", token),
        ]

    def req(self, op: str, **kwargs) -> Any:
        if op == "TestsList":
            return [
                test_from_pb(t)
                for t in self._client.ListTests(ListTestsRequest(), metadata=self._credentials, target=self._url).tests
            ]
        raise NotImplementedError


def test_from_pb(v: pbTest) -> SynTest:
    STATUS = {
        pbTestStatus.TEST_STATUS_UNSPECIFIED: TestStatus.none,
        pbTestStatus.TEST_STATUS_ACTIVE: TestStatus.active,
        pbTestStatus.TEST_STATUS_PAUSED: TestStatus.paused,
        pbTestStatus.TEST_STATUS_DELETED: TestStatus.deleted,
    }
    return SynTest(
        name=v.name,
        type=TestType(v.type),
        status=STATUS[v.status],
        deviceId=v.device_id,
        # _id=v.id,
        # _cdate=datetime.fromtimestamp(v.cdate.seconds + v.cdate.nanos / 1e9, timezone.utc).isoformat(),
        # _edate=datetime.fromtimestamp(v.edate.seconds + v.edate.nanos / 1e9, timezone.utc).isoformat(),
        settings=settings_from_pb(v.settings),
    )


def settings_from_pb(v: pbTestSettings) -> SynTestSettings:
    FAMILY = {
        pbIPFamily.IP_FAMILY_UNSPECIFIED: IPFamily.unspecified,
        pbIPFamily.IP_FAMILY_V4: IPFamily.v4,
        pbIPFamily.IP_FAMILY_V6: IPFamily.v6,
        pbIPFamily.IP_FAMILY_DUAL: IPFamily.dual,
    }
    return SynTestSettings(
        agentIds=v.agent_ids,
        tasks=v.tasks,
        healthSettings=health_settings_from_pb(v.health_settings),
        monitoringSettings=monitoring_settings_from_pb(v.monitoring_settings),
        port=v.port,
        period=v.period,
        count=v.count,
        expiry=v.expiry,
        limit=v.limit,
        protocol=Protocol(v.protocol),
        family=FAMILY[v.family],
        rollupLevel=v.rollup_level,
        servers=v.servers,
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
