from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_client import KentikSynthClient
from kentik_api.synthetics.synth_tests.base import DateTime
from kentik_api.synthetics.synth_tests.results import (
    AgentResults,
    DnsResponseData,
    DnsTaskResults,
    HttpResponseData,
    HttpTaskResults,
    MetricData,
    PacketLossData,
    PingTaskResults,
    TaskResults,
    TestResults,
)
from kentik_api.synthetics.types import Health
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector

PB_RESULTS = [
    pb.TestResults(
        test_id="1234",
        time=Timestamp(seconds=1649057685, nanos=0),
        health="warning",
        agents=[
            pb.AgentResults(
                agent_id="100",
                health="healthy",
                tasks=[
                    pb.TaskResults(
                        health="healthy",
                        ping=pb.PingResults(
                            target="151.139.47.114",
                            packet_loss=pb.PacketLossData(current=0.1, health="healthy"),
                            latency=pb.MetricData(
                                current=400000,
                                rolling_avg=300000,
                                rolling_stddev=50000,
                                health="healthy",
                            ),
                            jitter=pb.MetricData(
                                current=40,
                                rolling_avg=150,
                                rolling_stddev=100,
                                health="healthy",
                            ),
                            dst_ip="39.101.222.33",
                        ),
                    ),
                ],
            ),
            pb.AgentResults(
                agent_id="200",
                health="warning",
                tasks=[
                    pb.TaskResults(
                        health="warning",
                        dns=pb.DNSResults(
                            target="151.139.47.114",
                            server="4.4.4.4",
                            latency=pb.MetricData(
                                current=400000,
                                rolling_avg=300000,
                                rolling_stddev=50000,
                                health="warning",
                            ),
                            response=pb.DNSResponseData(status=1, data="dns response data"),
                        ),
                    )
                ],
            ),
            pb.AgentResults(
                agent_id="300",
                health="critical",
                tasks=[
                    pb.TaskResults(
                        health="critical",
                        http=pb.HTTPResults(
                            target="151.139.47.114",
                            latency=pb.MetricData(
                                current=400000,
                                rolling_avg=300000,
                                rolling_stddev=50000,
                                health="critical",
                            ),
                            response=pb.HTTPResponseData(status=403, size=9, data="forbidden"),
                            dst_ip="39.101.222.33",
                        ),
                    )
                ],
            ),
        ],
    )
]
RESULTS = [
    TestResults(
        test_id=ID("1234"),
        time=DateTime.fromtimestamp(1649057685, timezone.utc),
        health=Health.WARNING,
        agents=[
            AgentResults(
                agent_id=ID("100"),
                health=Health.HEALTHY,
                tasks=[
                    TaskResults(
                        health=Health.HEALTHY,
                        task=PingTaskResults(
                            target="151.139.47.114",
                            packet_loss=PacketLossData(current=0.1, health=Health.HEALTHY),
                            latency=MetricData(
                                current=400000,
                                rolling_avg=300000,
                                rolling_stddev=50000,
                                health=Health.HEALTHY,
                            ),
                            jitter=MetricData(
                                current=40,
                                rolling_avg=150,
                                rolling_stddev=100,
                                health=Health.HEALTHY,
                            ),
                            dst_ip=IP("39.101.222.33"),
                        ),
                    )
                ],
            ),
            AgentResults(
                agent_id=ID("200"),
                health=Health.WARNING,
                tasks=[
                    TaskResults(
                        health=Health.WARNING,
                        task=DnsTaskResults(
                            target="151.139.47.114",
                            server="4.4.4.4",
                            latency=MetricData(
                                current=400000,
                                rolling_avg=300000,
                                rolling_stddev=50000,
                                health=Health.WARNING,
                            ),
                            response=DnsResponseData(status=1, data="dns response data"),
                        ),
                    )
                ],
            ),
            AgentResults(
                agent_id=ID("300"),
                health=Health.CRITICAL,
                tasks=[
                    TaskResults(
                        health=Health.CRITICAL,
                        task=HttpTaskResults(
                            target="151.139.47.114",
                            latency=MetricData(
                                current=400000,
                                rolling_avg=300000,
                                rolling_stddev=50000,
                                health=Health.CRITICAL,
                            ),
                            response=HttpResponseData(status=403, size=9, data="forbidden"),
                            dst_ip=IP("39.101.222.33"),
                        ),
                    )
                ],
            ),
        ],
    )
]


def test_results_for_tests() -> None:
    # given
    connector = StubAPISyntheticsConnector(results_response=pb.GetResultsForTestsResponse(results=PB_RESULTS))
    client = KentikSynthClient(connector)

    # when
    results = client.results_for_tests(test_ids=[ID("1234")], start=datetime(1970, 1, 1), end=datetime.now())

    # then
    assert results == RESULTS
