import copy
from datetime import timezone
from typing import List

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.agent import Agent, AgentImplementType, AgentOwnershipType, AgentStatus
from kentik_api.synthetics.synth_client import KentikSynthClient
from kentik_api.synthetics.synth_tests.base import DateTime
from kentik_api.synthetics.types import IPFamily
from tests.unit.synthetics import protobuf_assert_equal
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector

PB_AGENTS: List[pb.Agent] = [
    pb.Agent(
        id="1234",
        site_name="site name",
        status=AgentStatus.OK.value,
        alias="agent alias",
        type=AgentOwnershipType.PRIVATE.value,
        os="SVR4",
        ip="100.10.200.20",
        lat=54.0,
        long=18.0,
        last_authed=Timestamp(seconds=649057685, nanos=0),
        family=IPFamily.V4.value,
        asn=1500,
        site_id="7",
        version="2.0.0",
        city="Gdańsk",
        region="Pomeranian",
        country="PL",
        test_ids=["100", "200", "300"],
        local_ip="150.15.250.25",
        cloud_region="eu-central-1",
        cloud_provider="aws",
        agent_impl=AgentImplementType.RUST.value,
    )
]

AGENTS: List[Agent] = [
    Agent(
        id=ID("1234"),
        site_name="site name",
        status=AgentStatus.OK,
        alias="agent alias",
        ip=IP("100.10.200.20"),
        lat=54.0,
        long=18.0,
        family=IPFamily.V4,
        asn=1500,
        site_id=ID("7"),
        city="Gdańsk",
        region="Pomeranian",
        country="PL",
        local_ip=IP("150.15.250.25"),
        cloud_region="eu-central-1",
        cloud_provider="aws",
        _os="SVR4",
        _version="2.0.0",
        _test_ids=[ID("100"), ID("200"), ID("300")],
        _type=AgentOwnershipType.PRIVATE,
        _agent_impl=AgentImplementType.RUST,
        _last_authed=DateTime.fromtimestamp(649057685, timezone.utc),
    )
]


def test_get_all_agents() -> None:
    # given
    connector = StubAPISyntheticsConnector(agents_response=PB_AGENTS)
    client = KentikSynthClient(connector)

    # when
    agents = client.get_all_agents()

    # then
    assert agents == AGENTS


def test_get_agent() -> None:
    # given
    connector = StubAPISyntheticsConnector(agents_response=PB_AGENTS[0])
    client = KentikSynthClient(connector)

    # when
    agent = client.get_agent(ID("1234"))

    # then
    assert agent == AGENTS[0]


def test_update_agent() -> None:
    # given
    connector = StubAPISyntheticsConnector()
    client = KentikSynthClient(connector)

    # when
    client.update_agent(AGENTS[0])

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(PB_AGENTS[0]), "Agent")


def clear_readonly_fields(agent: pb.Agent) -> pb.Agent:
    """For sending a request - clear the server-generated fields"""

    agent = copy.deepcopy(agent)
    agent.ClearField("type")
    agent.ClearField("os")
    agent.ClearField("last_authed")
    agent.ClearField("version")
    agent.ClearField("test_ids")
    agent.ClearField("agent_impl")
    return agent
