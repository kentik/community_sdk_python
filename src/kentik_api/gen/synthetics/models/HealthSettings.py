# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ActivationSettings import ActivationSettings
from .DisabledMetrics import DisabledMetrics


class HealthSettings(BaseModel):
    """
    HealthSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    latencyCritical: Optional[float] = Field(
        validation_alias="latencyCritical",
        default=None,
        description="Threshold for ping response latency (in microseconds) to trigger critical alarm",
    )

    latencyWarning: Optional[float] = Field(
        validation_alias="latencyWarning",
        default=None,
        description="Threshold for ping response latency (in microseconds) to trigger warning alarm",
    )

    packetLossCritical: Optional[float] = Field(
        validation_alias="packetLossCritical",
        default=None,
        description="Threshold for ping packet loss (in %) to trigger critical alarm",
    )

    packetLossWarning: Optional[float] = Field(
        validation_alias="packetLossWarning",
        default=None,
        description="Threshold for ping packet loss (in %) to trigger warning alarm",
    )

    jitterCritical: Optional[float] = Field(
        validation_alias="jitterCritical",
        default=None,
        description="Threshold for ping jitter (in microseconds) to trigger critical alarm",
    )

    jitterWarning: Optional[float] = Field(
        validation_alias="jitterWarning",
        default=None,
        description="Threshold for ping jitter (in microseconds) to trigger critical alarm",
    )

    httpLatencyCritical: Optional[float] = Field(
        validation_alias="httpLatencyCritical",
        default=None,
        description="Threshold for HTTP response latency (in microseconds) to trigger critical alarm",
    )

    httpLatencyWarning: Optional[float] = Field(
        validation_alias="httpLatencyWarning",
        default=None,
        description="Threshold for HTTP response latency (in microseconds) to trigger warning alarm",
    )

    httpValidCodes: Optional[List[int]] = Field(
        validation_alias="httpValidCodes",
        default=None,
        description="List of HTTP status codes indicating healthy state",
    )

    dnsValidCodes: Optional[List[int]] = Field(
        validation_alias="dnsValidCodes",
        default=None,
        description="List of DNS status codes indicating healthy state",
    )

    latencyCriticalStddev: Optional[float] = Field(
        validation_alias="latencyCriticalStddev",
        default=None,
        description="Threshold for standard deviation (in microseconds) of ping response latency to trigger critical alarm",
    )

    latencyWarningStddev: Optional[float] = Field(
        validation_alias="latencyWarningStddev",
        default=None,
        description="Threshold for standard deviation (in microseconds) of ping response latency to trigger warning alarm",
    )

    jitterCriticalStddev: Optional[float] = Field(
        validation_alias="jitterCriticalStddev",
        default=None,
        description="Threshold for standard deviation of ping jitter (in microseconds) to trigger critical alarm",
    )

    jitterWarningStddev: Optional[float] = Field(
        validation_alias="jitterWarningStddev",
        default=None,
        description="Threshold for standard deviation of ping jitter (in microseconds) to trigger warning alarm",
    )

    httpLatencyCriticalStddev: Optional[float] = Field(
        validation_alias="httpLatencyCriticalStddev",
        default=None,
        description="Threshold for standard deviation of HTTP response latency (in microseconds) to trigger critical alarm",
    )

    httpLatencyWarningStddev: Optional[float] = Field(
        validation_alias="httpLatencyWarningStddev",
        default=None,
        description="Threshold for standard deviation of HTTP response latency (in microseconds) to trigger warning alarm",
    )

    unhealthySubtestThreshold: Optional[int] = Field(
        validation_alias="unhealthySubtestThreshold",
        default=None,
        description="Number of tasks (across all agents) that must report unhealthy status in order for alarm to be triggered",
    )

    activation: Optional[ActivationSettings] = Field(
        validation_alias="activation", default=None
    )

    certExpiryWarning: Optional[int] = Field(
        validation_alias="certExpiryWarning",
        default=None,
        description="Threshold for remaining validity of TLS certificate (in days) to trigger warning alarm",
    )

    certExpiryCritical: Optional[int] = Field(
        validation_alias="certExpiryCritical",
        default=None,
        description="Threshold for remaining validity of TLS certificate (in days) to trigger critical alarm",
    )

    dnsValidIps: Optional[str] = Field(
        validation_alias="dnsValidIps",
        default=None,
        description="Comma separated list of IP addresses expected to be received in response to DNS A or AAAA query",
    )

    dnsLatencyCritical: Optional[float] = Field(
        validation_alias="dnsLatencyCritical",
        default=None,
        description="Threshold for DNS response latency (in microseconds) to trigger critical alarm",
    )

    dnsLatencyWarning: Optional[float] = Field(
        validation_alias="dnsLatencyWarning",
        default=None,
        description="Threshold for DNS response latency (in microseconds) to trigger warning alarm",
    )

    dnsLatencyCriticalStddev: Optional[float] = Field(
        validation_alias="dnsLatencyCriticalStddev",
        default=None,
        description="Threshold for standard deviation (in microseconds) of DNS response latency to trigger critical alarm",
    )

    dnsLatencyWarningStddev: Optional[float] = Field(
        validation_alias="dnsLatencyWarningStddev",
        default=None,
        description="Threshold for standard deviation (in microseconds) of DNS response latency to trigger warning alarm",
    )

    perAgentAlerting: Optional[bool] = Field(
        validation_alias="perAgentAlerting",
        default=None,
        description="Boolean value indicating whether to use per-agent alerting",
    )

    disabledMetrics: Optional[DisabledMetrics] = Field(
        validation_alias="disabledMetrics", default=None
    )

    healthDisabled: Optional[bool] = Field(
        validation_alias="healthDisabled",
        default=None,
        description="Disable all health evaluation for this test",
    )

    throughputCritical: Optional[float] = Field(
        validation_alias="throughputCritical",
        default=None,
        description="Threshold for throughput bandwidth (in mbps) to trigger critical alarm",
    )

    throughputWarning: Optional[float] = Field(
        validation_alias="throughputWarning",
        default=None,
        description="Threshold for throughput bandwidth (in mbps) to trigger warning alarm",
    )

    throughputCriticalStddev: Optional[float] = Field(
        validation_alias="throughputCriticalStddev",
        default=None,
        description="Threshold for standard deviation (in mbps) of throughput bandwidth to trigger critical alarm",
    )

    throughputWarningStddev: Optional[float] = Field(
        validation_alias="throughputWarningStddev",
        default=None,
        description="Threshold for standard deviation (in mbps) of throughput bandwidth to trigger warning alarm",
    )

    disableAlerts: Optional[bool] = Field(
        validation_alias="disableAlerts",
        default=None,
        description="Boolean value indicating whether to disable all alerts for this test",
    )
