import os
from typing import List

from kentik_api import KentikAPI
from kentik_api.public.types import ID
from kentik_api.synthetics.agent import AgentImplementType
from kentik_api.synthetics.synth_tests.base import ActivationSettings, HealthSettings
from kentik_api.synthetics.types import IPFamily
from kentik_api.utils import get_credentials

HEALTH1 = HealthSettings(
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

HEALTH2 = HealthSettings(
    latency_critical=180,
    latency_warning=120,
    latency_critical_stddev=18,
    latency_warning_stddev=12,
    packet_loss_critical=90,
    packet_loss_warning=60,
    jitter_critical=30,
    jitter_warning=20,
    jitter_critical_stddev=3,
    jitter_warning_stddev=2,
    http_latency_critical=500,
    http_latency_warning=300,
    http_latency_critical_stddev=35,
    http_latency_warning_stddev=25,
    http_valid_codes=[200, 302],
    dns_valid_codes=[4, 5, 6],
    unhealthy_subtest_threshold=2,
    activation=ActivationSettings(grace_period="2", time_unit="h", time_window="1", times="4"),
)

credentials_missing_str = "KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN env variables are required to run the test"
credentials_present = "KTAPI_AUTH_EMAIL" in os.environ and "KTAPI_AUTH_TOKEN" in os.environ


def client() -> KentikAPI:
    """Get KentikAPI client"""

    email, token = get_credentials()
    return KentikAPI(email, token)


def pick_agent_ids(count: int = 1, page_load_support: bool = False) -> List[ID]:
    """Pick requested number of Agent IDs from the list of available agents"""

    # test types that an Agent supports depend on agent_impl attribute:
    #   for page_load tests - use AgentImplementType.NODE
    #   for all other tests - use AgentImplementType.RUST
    # select only tests with IPFamily.DUAL to ensure IPv4 and IPv6 support
    required_impl = AgentImplementType.NODE if page_load_support else AgentImplementType.RUST
    agents = [
        agent
        for agent in client().synthetics.get_all_agents()
        if agent.agent_impl == required_impl and agent.family == IPFamily.DUAL
    ]
    num_agents = len(agents)
    if num_agents < count:
        raise RuntimeError(
            f"No enough agents for synthetic testing are available. Requested: {count}, available: {num_agents}"
        )
    requested_agents = agents[0:count]
    ids = [a.id for a in requested_agents]
    print("### Selected Agent IDs:", ids)
    return ids
