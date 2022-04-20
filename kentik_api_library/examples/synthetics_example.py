"""
Examples of using the Synthetics API
"""

from datetime import datetime, timezone

from examples.utils import client, pretty_print
from kentik_api.public.types import ID
from kentik_api.synthetics.synth_tests import HealthSettings, HostnameTest
from kentik_api.synthetics.synth_tests.base import ActivationSettings, PingTask, TraceTask
from kentik_api.synthetics.synth_tests.hostname import HostnameTestSettings, HostnameTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus


def tests_list() -> None:
    print("### TESTS LIST")
    items = client().synthetics.get_all_tests()
    for test in items:
        pretty_print(test.id)
        pretty_print(test)
        print()


def test_crud() -> None:
    health = HealthSettings(
        latency_critical=90,
        latency_warning=60,
        latency_critical_stddev=9,
        latency_warning_stddev=6,
        packet_loss_critical=80,
        packet_loss_warning=50,
        jitter_critical=20,
        jitter_warning=10,
        jitter_critical_stddev=2,
        jitter_warning_stddev=1,
        http_latency_critical=250,
        http_latency_warning=150,
        http_latency_critical_stddev=25,
        http_latency_warning_stddev=15,
        http_valid_codes=[200, 201],
        dns_valid_codes=[1, 2, 3],
        unhealthy_subtest_threshold=1,
        activation=ActivationSettings(grace_period="1", time_unit="m", time_window="5", times="3"),
    )
    settings = HostnameTestSettings(
        family=IPFamily.DUAL,
        period=60,
        agent_ids=["841"],
        health_settings=health,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP, port=2222),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        hostname=HostnameTestSpecific(target="www.example.com"),
    )

    print("### TEST CREATE")
    test = HostnameTest("PythonSdk-hostname-example", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    pretty_print(created_test)
    print()

    print("### TEST SET STATUS")
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    print("OK")
    print()

    print("### TEST GET")
    received_test = client().synthetics.get_test(created_test.id)
    pretty_print(received_test)
    print()

    print("### TEST UPDATE")
    created_test.name = "PythonSdk-hostname-example-updated"
    updated_test = client().synthetics.update_test(created_test)
    pretty_print(updated_test)
    print()

    print("### TEST DELETE")
    client().synthetics.delete_test(created_test.id)
    print("OK")
    print()


def agents_list() -> None:
    print("### AGENTS LIST")
    agents = client().synthetics.get_all_agents()
    pretty_print(agents)


def agent_crud() -> None:
    print("### AGENT GET")
    received_agent = client().synthetics.get_agent(ID("34004"))
    pretty_print(received_agent)
    print()

    # Note: it is only allowed to modify/delete Agent if Agent type is "private"

    # print("### AGENT UPDATE")
    # received_agent.status = AgentStatus.OK
    # updated_agent = client().synthetics.update_agent(received_agent)
    # pretty_print(updated_agent)

    # print("### AGENT DELETE")
    # client().synthetics.delete_agent(received_agent.id)


def get_results_for_tests() -> None:
    test_id = ID("6232")
    start = datetime(2022, 4, 13, 0, 0, 0, 0, timezone.utc)
    end = datetime.now(timezone.utc)

    print("### GET RESULTS FOR TESTS")
    results = client().synthetics.results_for_tests(
        test_ids=[test_id],
        start=start,
        end=end,
        agent_ids=None,
        task_ids=None,
    )
    for result in results:
        pretty_print(result)
    print()


def get_trace_for_test() -> None:
    test_id = ID("6232")
    start = datetime(2022, 4, 13, 12, 0, 0, 0, timezone.utc)
    end = datetime(2022, 4, 13, 12, 5, 0, 0, timezone.utc)

    print("### GET TRACE FOR TESTS")
    trace = client().synthetics.trace_for_test(
        test_id=test_id,
        start=start,
        end=end,
        agent_ids=None,
        target_ips=None,
    )
    pretty_print(trace)
    print()


if __name__ == "__main__":
    tests_list()
    test_crud()
    agents_list()
    agent_crud()
    get_results_for_tests()
    get_trace_for_test()
