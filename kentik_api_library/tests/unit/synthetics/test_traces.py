from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_client import KentikSynthClient
from kentik_api.synthetics.synth_tests.traces import Location, NetNode, Path, PathTrace, Stats, TraceHop, TraceResponse
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector

PB_TRACES = pb.GetTraceForTestResponse(
    nodes={
        "10.100.20.200": pb.NetNode(
            ip="10.100.20.200",
            asn=1,
            as_name="as_name",
            location=pb.Location(latitude=18.0, longitude=54.0, country="Poland", region="Pomeranian", city="Gdańsk"),
            dns_name="aws.route53.com",
            device_id="50",
            site_id="100",
        )
    },
    paths=[
        pb.Path(
            agent_id="1000",
            target_ip="10.100.20.200",
            hop_count=pb.Stats(average=50, min=10, max=90),
            max_as_path_length=11,
            traces=[
                pb.PathTrace(
                    as_path=[1000, 2000], is_complete=True, hops=[pb.TraceHop(latency=15, node_id="10.100.20.200")]
                )
            ],
            time=Timestamp(seconds=1649057685, nanos=0),
        ),
    ],
)
TRACES = TraceResponse(
    nodes={
        "10.100.20.200": NetNode(
            ip=IP("10.100.20.200"),
            asn=1,
            as_name="as_name",
            location=Location(latitude=18.0, longitude=54.0, country="Poland", region="Pomeranian", city="Gdańsk"),
            dns_name="aws.route53.com",
            device_id=ID("50"),
            site_id=ID("100"),
        )
    },
    paths=[
        Path(
            agent_id=ID("1000"),
            target_ip=IP("10.100.20.200"),
            hop_count=Stats(average=50, min=10, max=90),
            max_as_path_length=11,
            traces=[
                PathTrace(as_path=[1000, 2000], is_complete=True, hops=[TraceHop(latency=15, node_id="10.100.20.200")])
            ],
            time=datetime.fromtimestamp(1649057685, timezone.utc),
        )
    ],
)


def test_results_for_tests() -> None:
    # given
    connector = StubAPISyntheticsConnector(traces_response=PB_TRACES)
    client = KentikSynthClient(connector)

    # when
    traces = client.trace_for_test(
        test_id=ID("1234"), start=datetime(1970, 1, 1), end=datetime.now(), agent_ids=[], target_ips=[]
    )

    # then
    assert traces == TRACES
