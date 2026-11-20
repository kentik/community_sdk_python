# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Live checks of the V5 query calls, read-only POSTs the auto-discovered suite skips.

The query API needs a device name even when all_selected is true. The chart
endpoint gave no response in a live check on 2026-10-16, so its test expects a
timeout until Kentik confirms the endpoint (spec 005, FR-004 and FR-028).
"""

from __future__ import annotations

import pytest

from kentik_api.errors import TransportError
from kentik_api.gen.v5.models import ChartRequest, Query, QueryItem, QueryRequest
from kentik_api.v5_tools import decode_chart


def _query_item(client) -> QueryItem:
    devices = client.device.list().devices or []
    names = [d.deviceName for d in devices if d is not None and d.deviceName]
    if not names:
        pytest.skip("The account has no device to query.")
    query = Query(
        metric="bytes",
        dimension=["Proto"],
        device_name=",".join(names),
        lookback_seconds=3600,
        topx=8,
        depth=25,
        fastData="Auto",
        outsort="avg_bits_per_sec",
        hostname_lookup=False,
    )
    return QueryItem(query=query, bucket="Left +Y Axis", bucketIndex=0)


@pytest.mark.e2e
def test_top_x_data_returns_result_rows(real_client):
    response = real_client.v5.top_x_data(
        data=QueryRequest(queries=[_query_item(real_client)])
    )

    assert response.results is not None
    assert response.results[0].bucket == "Left +Y Axis"


@pytest.mark.e2e
def test_query_url_returns_a_portal_link(real_client):
    url = real_client.v5.query_url(
        data=QueryRequest(queries=[_query_item(real_client)])
    )

    assert url.startswith("https://portal.kentik")


@pytest.mark.e2e_grpc
def test_top_x_data_on_a_grpc_client_goes_over_rest(grpc_real_client):
    response = grpc_real_client.v5.top_x_data(
        data=QueryRequest(queries=[_query_item(grpc_real_client)])
    )

    assert response.results is not None


# Last on purpose: a chart call that never answers keeps one of the Query API's
# 4 concurrent slots busy on the server, and later queries can time out.
@pytest.mark.e2e
@pytest.mark.xfail(
    raises=TransportError,
    strict=False,
    reason="query/topXchart gave no response in the 2026-10-16 live check.",
)
def test_top_x_chart_returns_an_image(real_client):
    response = real_client.v5.top_x_chart(
        data=ChartRequest(queries=[_query_item(real_client)], imageType="svg"),
        api_config_override=real_client.v5_api_config.with_timeout(60),
    )

    assert decode_chart(response).data
