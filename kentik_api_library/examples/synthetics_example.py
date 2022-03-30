"""
Examples of using the Synthetics API
"""

from datetime import datetime, timezone

from utils import client, pretty_print

from kentik_api.public.types import ID
from kentik_api.synthetics.agent import AgentStatus
from kentik_api.synthetics.synth_tests import HealthSettings, SynTest, SynTestSettings
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType


def tests_list() -> None:
    print("### TESTS LIST")
    items = client().synthetics.tests
    for test in items:
        pretty_print(test.id)
        pretty_print(test)
        print()


def test_crud() -> None:
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
    settings = SynTestSettings(
        agentIds=["616", "650", "754"],
        tasks=["ping", "traceroute"],
        healthSettings=health,
        port=443,
        period=60,
        count=3,
        expiry=30,
        limit=20,
        family=IPFamily.v4,
        servers=["server1", "server2"],
    )
    settings.protocol = Protocol.icmp

    print("### TEST CREATE")
    test = SynTest(name="python-synthclient-test", status=TestStatus.active, settings=settings)
    test.type = TestType.mesh
    test.deviceId = ID("75702")
    created_test = client().synthetics.create_test(test)
    pretty_print(created_test)
    print()

    print("### TEST SET STATUS")
    client().synthetics.set_test_status(created_test.id, TestStatus.paused)
    print("OK")
    print()

    print("### TEST GET")
    received_test = client().synthetics.test(created_test.id)
    pretty_print(received_test)
    print()

    print("### TEST PATCH")
    created_test.settings.port = 640
    patched_test = client().synthetics.patch_test(created_test, "test.settings.port")
    pretty_print(patched_test)
    print()

    print("### TEST DELETE")
    client().synthetics.delete_test(created_test.id)
    print("OK")
    print()


def agents_list() -> None:
    print("### AGENTS LIST")
    agents = client().synthetics.agents
    for agent in agents:
        pretty_print(agent.id)
        pretty_print(agent)
        print()


def agent_crud() -> None:
    print("### AGENT GET")
    received_agent = client().synthetics.agent(ID("1717"))
    pretty_print(received_agent)
    print()

    # Note: it is only allowed to modify/delete Agent if Agent type is "private"

    # print("### AGENT PATCH")
    # received_agent.status = AgentStatus.OK
    # patched_agent = client().synthetics.patch_agent(received_agent, "agent.alias")
    # pretty_print(patched_agent)

    # print("### AGENT DELETE")
    # client().synthetics.delete_agent(ID("1717"))


def get_health() -> None:
    test_id = ID("6232")
    start = datetime(2021, 11, 8, 7, 15, 3, 0, timezone.utc)
    end = datetime(2021, 11, 8, 7, 20, 3, 0, timezone.utc)

    print("### GET HEALTH FOR TESTS")
    health_items = client().synthetics.health(
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


def get_trace() -> None:
    test_id = ID("6232")
    start = datetime(2021, 11, 8, 7, 15, 3, 0, timezone.utc)
    end = datetime(2021, 11, 8, 7, 20, 3, 0, timezone.utc)

    print("### GET TRACE FOR TESTS")
    trace = client().synthetics.trace(
        test_id=test_id,
        start=start,
        end=end,
        agent_ids=None,
        ips=None,
    )
    pretty_print(trace)
    print()


if __name__ == "__main__":
    tests_list()
    test_crud()
    agents_list()
    agent_crud()
    get_health()
    get_trace()
