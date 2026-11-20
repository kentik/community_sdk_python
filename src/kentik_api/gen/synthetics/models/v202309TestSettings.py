# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .v202309AgentTest import v202309AgentTest
from .v202309AlertingSettings import v202309AlertingSettings
from .v202309DnsTest import v202309DnsTest
from .v202309FlowTest import v202309FlowTest
from .v202309HealthSettings import v202309HealthSettings
from .v202309HostnameTest import v202309HostnameTest
from .v202309IPFamily import v202309IPFamily
from .v202309IpTest import v202309IpTest
from .v202309NetworkMeshTest import v202309NetworkMeshTest
from .v202309PageLoadTest import v202309PageLoadTest
from .v202309ScheduleSettings import v202309ScheduleSettings
from .v202309TestPingSettings import v202309TestPingSettings
from .v202309TestThroughputSettings import v202309TestThroughputSettings
from .v202309TestTraceSettings import v202309TestTraceSettings
from .v202309UrlTest import v202309UrlTest


class v202309TestSettings(BaseModel):
    """
    TestSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    hostname: Optional[v202309HostnameTest] = Field(
        validation_alias="hostname", default=None
    )

    ip: Optional[v202309IpTest] = Field(validation_alias="ip", default=None)

    agent: Optional[v202309AgentTest] = Field(validation_alias="agent", default=None)

    flow: Optional[v202309FlowTest] = Field(validation_alias="flow", default=None)

    dns: Optional[v202309DnsTest] = Field(validation_alias="dns", default=None)

    url: Optional[v202309UrlTest] = Field(validation_alias="url", default=None)

    networkGrid: Optional[v202309IpTest] = Field(
        validation_alias="networkGrid", default=None
    )

    pageLoad: Optional[v202309PageLoadTest] = Field(
        validation_alias="pageLoad", default=None
    )

    dnsGrid: Optional[v202309DnsTest] = Field(validation_alias="dnsGrid", default=None)

    networkMesh: Optional[v202309NetworkMeshTest] = Field(
        validation_alias="networkMesh", default=None
    )

    agentIds: Optional[List[str]] = Field(
        validation_alias="agentIds",
        default=None,
        description="IDs of agents assigned to run tasks on behalf of the test",
    )

    tasks: Optional[List[str]] = Field(
        validation_alias="tasks",
        default=None,
        description="List of task names to run for the test",
    )

    healthSettings: Optional[v202309HealthSettings] = Field(
        validation_alias="healthSettings", default=None
    )

    ping: Optional[v202309TestPingSettings] = Field(
        validation_alias="ping", default=None
    )

    trace: Optional[v202309TestTraceSettings] = Field(
        validation_alias="trace", default=None
    )

    period: Optional[int] = Field(
        validation_alias="period",
        default=None,
        description="Test evaluation period (in seconds)",
    )

    family: Optional[v202309IPFamily] = Field(validation_alias="family", default=None)

    notificationChannels: Optional[List[str]] = Field(
        validation_alias="notificationChannels",
        default=None,
        description="List of IDs of notification channels for alarms triggered by the test",
    )

    notes: Optional[str] = Field(
        validation_alias="notes",
        default=None,
        description="Add a note or comment for this test",
    )

    throughput: Optional[v202309TestThroughputSettings] = Field(
        validation_alias="throughput", default=None
    )

    schedule: Optional[v202309ScheduleSettings] = Field(
        validation_alias="schedule", default=None
    )

    alerting: Optional[v202309AlertingSettings] = Field(
        validation_alias="alerting", default=None
    )
