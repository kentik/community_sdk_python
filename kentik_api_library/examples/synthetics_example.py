"""
Examples of using the Synthetics API
"""

import logging
from typing import Any

from kentik_api import KentikAPI
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ListTestsRequest, ListTestsResponse, Test
from kentik_api.synthetics.synth_tests import HealthSettings, MonitoringSettings, SynTest, SynTestSettings
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def pretty_print(v: Any, level: int = 1) -> None:
    INDENT = " " * level * 2

    for field_name, field in v.__dict__.items():
        if callable(field):
            continue
        if not hasattr(field, "__dict__"):
            print(f"{INDENT}{field_name}: {field}")
        else:
            print(f"{INDENT}{field_name}")
            pretty_print(field, level + 1)


def list_tests() -> None:
    print("### TESTS LIST")
    email, token = get_credentials()
    client = KentikAPI(email, token)

    items = client.synthetics.tests
    for test in items:
        print(test.id)
        pretty_print(test)
        print()


def crud_test() -> None:
    health = HealthSettings(
        latencyCritical=90,
        latencyWarning=60,
        latencyCriticalStddev=9,
        latencyWarningStddev=6,
        packetLossCritical=80,
        packetLossWarning=50,
        jitterCritical=20,
        jitterWarning=10,
        jitterCriticalStddev=2,
        jitterWarningStddev=1,
        httpLatencyCritical=250,
        httpLatencyWarning=150,
        httpLatencyCriticalStddev=25,
        httpLatencyWarningStddev=15,
        httpValidCodes=[200, 201],
        dnsValidCodes=[5, 6, 7],
    )
    monitoring = MonitoringSettings(
        activationGracePeriod="2",
        activationTimeUnit="m",
        activationTimeWindow="5",
        activationTimes="3",
        notificationChannels=[],
    )
    settings = SynTestSettings(
        agentIds=["616", "650", "754"],
        tasks=["ping", "traceroute"],
        healthSettings=health,
        monitoringSettings=monitoring,
        port=443,
        period=60,
        count=3,
        expiry=30,
        limit=20,
        family=IPFamily.v4,
        servers=["server1", "server2"],
    )
    settings.protocol = Protocol.icmp
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### TEST CREATE")
    test = SynTest(name="python-synthclient-test", status=TestStatus.active, settings=settings)
    test.type = TestType.mesh
    test.deviceId = "75702"
    created_test = client.synthetics.create_test(test)
    pretty_print(created_test)

    print("### TEST SET STATUS")
    client.synthetics.set_test_status(created_test.id, TestStatus.paused)

    print("### TEST GET")
    received_test = client.synthetics.test(created_test.id)
    pretty_print(received_test)

    print("### TEST UPDATE")
    created_test.settings.port = 640
    updated_test = client.synthetics.patch_test(created_test, "test.settings.port")
    pretty_print(updated_test)

    print("### TEST DELETE")
    client.synthetics.delete_test(created_test.id)


def list_agents() -> None:
    print("### AGENTS LIST")
    email, token = get_credentials()
    client = KentikAPI(email, token)

    agents = client.synthetics.agents
    for agent in agents:
        print(agent.id)
        pretty_print(agent)
        print()


def crud_agent() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### AGENT GET")
    received_agent = client.synthetics.agent("574")
    pretty_print(received_agent)


if __name__ == "__main__":
    list_tests()
    crud_test()
    list_agents()
    crud_agent()