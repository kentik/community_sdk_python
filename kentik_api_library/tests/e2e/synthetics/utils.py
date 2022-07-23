import os
from copy import deepcopy
from datetime import datetime, timezone
from typing import List
from urllib.parse import urlparse

from kentik_api import KentikAPI
from kentik_api.public.types import ID
from kentik_api.synthetics.agent import AgentImplementType
from kentik_api.synthetics.synth_tests.base import ActivationSettings, HealthSettings, SynTest, SynTestSettings
from kentik_api.synthetics.types import IPFamily, TestStatus, TestType
from kentik_api.utils import get_credentials, get_url

INITIAL_HEALTH_SETTINGS = HealthSettings(
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

UPDATE_HEALTH_SETTINGS = HealthSettings(
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

required_env_variables = ["KTAPI_AUTH_EMAIL", "KTAPI_AUTH_TOKEN"]
credentials_missing_str = f"{','.join(required_env_variables)} env variables are required to run the test"
credentials_present = all(v in os.environ for v in required_env_variables)


def make_e2e_test_name(test_type: TestType) -> str:
    now = datetime.now(tz=timezone.utc)
    return f"pysdk_e2e-{now.isoformat()}-{test_type.value}"


def client() -> KentikAPI:
    """Get KentikAPI client"""

    email, token = get_credentials()
    url = get_url()
    if url:
        api_host = urlparse(url).netloc
        if not api_host:
            api_host = urlparse(url).path
    else:
        api_host = None
    return KentikAPI(email, token, api_host=api_host)


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


def normalize_settings(s: SynTestSettings) -> SynTestSettings:
    out = deepcopy(s)
    if out.health_settings.activation.time_unit == "h":
        out.health_settings.activation.time_window = str(int(out.health_settings.activation.time_window) * 60)
        out.health_settings.activation.time_unit = "m"
    out.notification_channels.sort()
    return out


def execute_test_crud_steps(
    test: SynTest,
    update_settings: SynTestSettings,
    pause_after_creation: bool = False,
) -> None:
    test_id = ID()
    try:
        # create
        created_test = client().synthetics.create_test(test)
        test_id = created_test.id
        assert isinstance(created_test, type(test))
        assert created_test.name == test.name
        assert created_test.type == test.type
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == normalize_settings(test.settings)
        assert created_test.labels == sorted(test.labels)

        # set status
        if pause_after_creation:
            client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)

        # read
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, type(test))
        assert received_test.name == created_test.name
        assert received_test.type == created_test.type
        assert received_test.status == TestStatus.PAUSED if pause_after_creation else TestStatus.ACTIVE
        assert received_test.settings == normalize_settings(test.settings)
        assert received_test.labels == created_test.labels

        # update
        received_test.name = f"{test.name}-updated"
        received_test.status = TestStatus.ACTIVE
        received_test.settings = update_settings
        # test resetting labels, if any were provided
        if received_test.labels:
            received_test.labels = []

        updated_test = client().synthetics.update_test(received_test)
        assert isinstance(updated_test, type(test))
        assert updated_test.name == received_test.name
        assert updated_test.type == received_test.type
        assert updated_test.status == received_test.status
        assert updated_test.settings == normalize_settings(received_test.settings)
        assert updated_test.labels == received_test.labels

    finally:
        # delete the created test, if any, even if an assertion failed or other problem has occurred
        if test_id:
            print(f"deleting test id: {test_id}")
            client().synthetics.delete_test(test_id)
