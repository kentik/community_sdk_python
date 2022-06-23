from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_client import KentikSynthClient
from kentik_api.synthetics.synth_tests.base import DateTime
from kentik_api.synthetics.synth_tests.traces import Location, NetNode, Path, PathTrace, Stats, TraceHop, TraceResponse
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector

PB_TRACES = pb.GetTraceForTestResponse(
    nodes={
        "10.100.20.200": pb.NetNode(
            ip="10.100.20.200",
            asn=1,
            as_name="Gdansk,PL",
            location=pb.Location(
                latitude=18.6466,
                longitude=54.3520,
                country="Poland",
                region="Pomeranian",
                city="Gdańsk",
            ),
            dns_name="aws.route53.com",
            device_id="50",
            site_id="100",
        ),
        "45.11.183.168": pb.NetNode(
            ip="45.11.183.168",
            asn=2,
            as_name="SERVINGA-EE,DE",
            location=pb.Location(
                latitude=59.436958,
                longitude=24.753531,
                country="Estonia",
                region="Harjumaa",
                city="Tallinn",
            ),
            dns_name=" - ",
            device_id="",
            site_id="",
        ),
        "62.219.189.226": pb.NetNode(
            ip="62.219.189.226",
            asn=3,
            as_name="Bezeq International,IL",
            location=pb.Location(
                latitude=32.09174,
                longitude=34.885029,
                country="Israel",
                region="HaMerkaz",
                city="Petah Tikva",
            ),
            dns_name="bzq-219-189-226.cablep.bezeqint.net",
            device_id="",
            site_id="",
        ),
        "154.54.39.225": pb.NetNode(
            ip="154.54.39.225",
            asn=4,
            as_name="Cogent,US",
            location=pb.Location(
                latitude=44.804008,
                longitude=20.46513,
                country="Serbia",
                region="Beograd",
                city="Belgrade",
            ),
            dns_name="be3077.ccr31.bio02.atlas.cogentco.com",
            device_id="",
            site_id="",
        ),
        "151.139.44.19": pb.NetNode(
            ip="151.139.44.19",
            asn=5,
            as_name="Stackpath (Highwinds),US",
            location=pb.Location(
                latitude=39.04372,
                longitude=-77.487488,
                country="United States",
                region="Virginia",
                city="Ashburn",
            ),
            dns_name=" - ",
            device_id="",
            site_id="",
        ),
    },
    paths=[
        pb.Path(
            agent_id="1000",
            target_ip="151.139.44.19",
            hop_count=pb.Stats(average=50, min=10, max=90),
            max_as_path_length=5,
            traces=[
                pb.PathTrace(
                    is_complete=True,
                    as_path=[
                        1,
                        2,
                        3,
                        4,
                        5,
                    ],
                    hops=[
                        pb.TraceHop(latency=15, node_id="10.100.20.200"),
                        pb.TraceHop(latency=23, node_id="145.11.183.168"),
                        pb.TraceHop(latency=17, node_id="62.219.189.226"),
                        pb.TraceHop(latency=14, node_id="154.54.39.225"),
                        pb.TraceHop(latency=34, node_id="151.139.44.19"),
                    ],
                ),
                pb.PathTrace(
                    is_complete=False,
                    as_path=[
                        1,
                        2,
                        3,
                    ],
                    hops=[
                        pb.TraceHop(latency=15, node_id="10.100.20.200"),
                        pb.TraceHop(latency=23, node_id="145.11.183.168"),
                        pb.TraceHop(latency=17, node_id="62.219.189.226"),
                    ],
                ),
            ],
            time=Timestamp(seconds=1577923200, nanos=0),
        ),
    ],
)
TRACES = TraceResponse(
    nodes={
        "10.100.20.200": NetNode(
            ip=IP("10.100.20.200"),
            asn=1,
            as_name="Gdansk,PL",
            location=Location(
                latitude=18.6466,
                longitude=54.3520,
                country="Poland",
                region="Pomeranian",
                city="Gdańsk",
            ),
            dns_name="aws.route53.com",
            device_id=ID("50"),
            site_id=ID("100"),
        ),
        "45.11.183.168": NetNode(
            ip=IP("45.11.183.168"),
            asn=2,
            as_name="SERVINGA-EE,DE",
            location=Location(
                latitude=59.436958,
                longitude=24.753531,
                country="Estonia",
                region="Harjumaa",
                city="Tallinn",
            ),
            dns_name=" - ",
            device_id=ID(""),
            site_id=ID(""),
        ),
        "62.219.189.226": NetNode(
            ip=IP("62.219.189.226"),
            asn=3,
            as_name="Bezeq International,IL",
            location=Location(
                latitude=32.09174,
                longitude=34.885029,
                country="Israel",
                region="HaMerkaz",
                city="Petah Tikva",
            ),
            dns_name="bzq-219-189-226.cablep.bezeqint.net",
            device_id=ID(""),
            site_id=ID(""),
        ),
        "154.54.39.225": NetNode(
            ip=IP("154.54.39.225"),
            asn=4,
            as_name="Cogent,US",
            location=Location(
                latitude=44.804008,
                longitude=20.46513,
                country="Serbia",
                region="Beograd",
                city="Belgrade",
            ),
            dns_name="be3077.ccr31.bio02.atlas.cogentco.com",
            device_id=ID(""),
            site_id=ID(""),
        ),
        "151.139.44.19": NetNode(
            ip=IP("151.139.44.19"),
            asn=5,
            as_name="Stackpath (Highwinds),US",
            location=Location(
                latitude=39.04372,
                longitude=-77.487488,
                country="United States",
                region="Virginia",
                city="Ashburn",
            ),
            dns_name=" - ",
            device_id=ID(""),
            site_id=ID(""),
        ),
    },
    paths=[
        Path(
            agent_id=ID("1000"),
            target_ip=IP("151.139.44.19"),
            hop_count=Stats(average=50, min=10, max=90),
            max_as_path_length=5,
            traces=[
                PathTrace(
                    is_complete=True,
                    as_path=[
                        1,
                        2,
                        3,
                        4,
                        5,
                    ],
                    hops=[
                        TraceHop(latency=15, node_id="10.100.20.200"),
                        TraceHop(latency=23, node_id="145.11.183.168"),
                        TraceHop(latency=17, node_id="62.219.189.226"),
                        TraceHop(latency=14, node_id="154.54.39.225"),
                        TraceHop(latency=34, node_id="151.139.44.19"),
                    ],
                ),
                PathTrace(
                    is_complete=False,
                    as_path=[
                        1,
                        2,
                        3,
                    ],
                    hops=[
                        TraceHop(latency=15, node_id="10.100.20.200"),
                        TraceHop(latency=23, node_id="145.11.183.168"),
                        TraceHop(latency=17, node_id="62.219.189.226"),
                    ],
                ),
            ],
            time=DateTime.fromtimestamp(1577923200, timezone.utc),
        ),
    ],
)


def test_results_for_tests() -> None:
    # given
    connector = StubAPISyntheticsConnector(traces_response=PB_TRACES)
    client = KentikSynthClient(connector)

    # when
    traces = client.trace_for_test(
        test_id=ID("1234"),
        start=datetime(2020, 1, 1),
        end=datetime(2020, 1, 2),
        agent_ids=[],
        target_ips=[],
    )

    # then
    assert traces == TRACES
