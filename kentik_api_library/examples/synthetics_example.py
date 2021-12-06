"""
Examples of using the Synthetics API
"""

import logging
from datetime import datetime, timezone
from typing import Any

from kentik_api import KentikAPI
from kentik_api.public.types import ID
from kentik_api.synthetics.synth_tests import HealthSettings, MonitoringSettings, SynTest, SynTestSettings
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def pretty_print(v: Any, level: int = 1) -> None:
    indent = " " * level * 2

    if hasattr(v, "__dict__"):
        for field_name, field in v.__dict__.items():
            if callable(field):
                continue
            print(f"\n{indent}{field_name}: ", end="")
            pretty_print(field, level + 1)
    elif isinstance(v, list) and len(v) > 0 and hasattr(v[0], "__dict__"):
        for i, item in enumerate(v):
            print(f"\n{indent}[{i}]", end="")
            pretty_print(item, level + 1)
    else:
        print(f"{v}", end="")


def list_tests() -> None:
    print("### TESTS LIST")
    email, token = get_credentials()
    client = KentikAPI(email, token)

    items = client.synthetics.tests
    for test in items:
        pretty_print(test.id)
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
    test.deviceId = ID("75702")
    created_test = client.synthetics.create_test(test)
    pretty_print(created_test)
    print()

    print("### TEST SET STATUS")
    client.synthetics.set_test_status(created_test.id, TestStatus.paused)
    print("OK")
    print()

    print("### TEST GET")
    received_test = client.synthetics.test(created_test.id)
    pretty_print(received_test)
    print()

    print("### TEST PATCH")
    created_test.settings.port = 640
    patched_test = client.synthetics.patch_test(created_test, "test.settings.port")
    pretty_print(patched_test)
    print()

    print("### TEST DELETE")
    client.synthetics.delete_test(created_test.id)
    print("OK")
    print()


def list_agents() -> None:
    print("### AGENTS LIST")
    email, token = get_credentials()
    client = KentikAPI(email, token)

    agents = client.synthetics.agents
    for agent in agents:
        pretty_print(agent.id)
        pretty_print(agent)
        print()


def crud_agent() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### AGENT GET")
    received_agent = client.synthetics.agent(ID("1717"))
    pretty_print(received_agent)

    # print("### AGENT PATCH")
    # received_agent.alias = received_agent.alias + "!"
    # patched_agent = client.synthetics.patch_agent(received_agent, "agent.alias")
    # pretty_print(patched_agent)

    # print("### AGENT DELETE")
    # client.synthetics.delete_agent(ID("1717"))


def get_health() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    test_id = ID("3541")
    start = datetime(2021, 11, 8, 7, 15, 3, 0, timezone.utc)
    end = datetime(2021, 11, 8, 7, 20, 3, 0, timezone.utc)

    print("### GET HEALTH FOR TESTS")
    health_items = client.synthetics.health(
        test_ids=[test_id],
        start=start,
        end=end,
        augment=True,
        agent_ids=None,
        task_ids=None,
    )
    for health in health_items:
        pretty_print(health.test_id)
        pretty_print(health)
    print()


if __name__ == "__main__":
    list_tests()
    crud_test()
    list_agents()
    crud_agent()
    get_health()
