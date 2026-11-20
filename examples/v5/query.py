# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Run the V5 top-X data, URL, and chart queries.

`client.v5` always uses REST, also on a client created with protocol="grpc".
"""

from kentik_api.client import KentikAPI
from kentik_api.errors import TransportError
from kentik_api.gen.v5.models import (
    Aggregate,
    ChartRequest,
    Query,
    QueryItem,
    QueryRequest,
)
from kentik_api.v5_tools import decode_chart


def _query_item(device_names: str) -> QueryItem:
    query = Query(
        metric="bytes",
        dimension=["Traffic"],
        device_name=device_names,
        cidr=32,
        cidr6=128,
        topx=8,
        depth=75,
        fastData="Auto",
        outsort="avg_bits_per_sec",
        lookback_seconds=3600,
        hostname_lookup=True,
        aggregates=[
            Aggregate(
                name="avg_bits_per_sec",
                column="f_sum_both_bytes",
                fn="average",
                raw=True,
            ),
            Aggregate(
                name="p95th_bits_per_sec",
                column="f_sum_both_bytes",
                fn="percentile",
                rank=95,
            ),
            Aggregate(
                name="max_bits_per_sec", column="f_sum_both_bytes", fn="max"
            ),
        ],
    )
    return QueryItem(query=query, bucket="Left +Y Axis")


def main() -> None:
    """Request top-X data, a Data Explorer URL, and a chart."""
    client = KentikAPI()  # loads KENTIK_EMAIL / KENTIK_API_TOKEN from .env
    devices = client.device.list().devices or []
    names = ",".join(
        d.deviceName for d in devices if d is not None and d.deviceName
    )
    item = _query_item(names)

    data = client.v5.top_x_data(data=QueryRequest(queries=[item]))
    for bucket in data.results or []:
        if bucket is not None:
            print(f"{bucket.bucket}: {len(bucket.data or [])} row(s)")

    url = client.v5.query_url(data=QueryRequest(queries=[item]))
    print(f"Data Explorer: {url}")

    try:
        chart = client.v5.top_x_chart(
            data=ChartRequest(queries=[item], imageType="png"),
            api_config_override=client.v5_api_config.with_timeout(60),
        )
    except TransportError:
        print("The chart endpoint did not answer in 60 seconds (not verified).")
        return
    image = decode_chart(chart)
    print(f"Chart: {image.image_type}, {len(image.data)} bytes")


if __name__ == "__main__":
    main()
