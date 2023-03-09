# pylint: disable=redefined-outer-name
"""
Examples of using the typed Query API
"""

import logging
from io import BytesIO

from PIL import Image  # type: ignore

from examples.utils import pretty_print
from kentik_api import (
    Aggregate,
    AggregateFunctionType,
    ChartViewType,
    DimensionType,
    FastDataType,
    ImageType,
    KentikAPI,
    MetricType,
    Query,
    QueryArrayItem,
    QueryObject,
    QuerySQL,
)
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_query_data() -> None:
    """
    Expected response is subsequent result items
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    agg1 = Aggregate(
        name="avg_bits_per_sec",
        column="f_sum_both_bytes",
        fn=AggregateFunctionType.average,
        raw=True,
    )
    agg2 = Aggregate(
        name="p95th_bits_per_sec",
        column="f_sum_both_bytes",
        fn=AggregateFunctionType.percentile,
        rank=95,
    )
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    query = Query(
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=[MetricType.bytes],
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=3600,
        hostname_lookup=True,
        device_name=[],
        all_selected=True,
        descriptor="",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis")
    query_object = QueryObject(queries=[query_item])

    print("Sending query for data...")
    result = client.query.data(query_object)

    print("Results:")
    pretty_print(result.results)
    print()


def run_query_chart() -> None:
    """
    Expected response is image type and base64 encoded image data
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    agg1 = Aggregate(
        name="avg_bits_per_sec",
        column="f_sum_both_bytes",
        fn=AggregateFunctionType.average,
        raw=True,
    )
    agg2 = Aggregate(
        name="p95th_bits_per_sec",
        column="f_sum_both_bytes",
        fn=AggregateFunctionType.percentile,
        rank=95,
    )
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    query = Query(
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=[MetricType.bytes],
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        overlay_day=-7,
        show_overlay=False,
        sync_axes=False,
        viz_type=ChartViewType.stackedArea,
        lookback_seconds=3600,
        hostname_lookup=True,
        device_name=[],
        matrixBy=[],
        all_selected=True,
        descriptor="",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis", isOverlay=False)
    query_object = QueryObject(queries=[query_item], imageType=ImageType.png)

    print("Sending query for chart...")
    result = client.query.chart(query_object)

    print("Result:")
    img = Image.open(BytesIO(result.get_data()))
    img.show()


def run_query_url() -> None:
    """
    Expected response is url to Data Explorer page with query params filled as specified in query
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    query = Query(
        viz_type=ChartViewType.stackedArea,
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=[MetricType.bytes],
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=3600,
        hostname_lookup=True,
        device_name=[],
        all_selected=True,
        descriptor="",
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis")
    query_object = QueryObject(queries=[query_item])

    print("Sending query for url...")
    result = client.query.url(query_object)

    print("Result:")
    pretty_print(result)
    print()


def run_query_sql() -> None:
    """
    Expected response is rows containing SQL query result
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    # Return kpps and kBps over the last hour,
    # grouped by minute (the first minute is skipped
    # as it is likely incomplete most of the time):
    query_string = (
        "SELECT i_start_time, "
        "round(sum(in_pkts)/(3600)/1000) AS f_sum_in_pkts, "
        "round(sum(in_bytes)/(3600)/1000)*8 AS f_sum_in_bytes "
        "FROM all_devices "
        "WHERE ctimestamp > 3660 "
        "AND ctimestamp < 60 "
        "GROUP by i_start_time "
        "ORDER by i_start_time DESC "
        "LIMIT 1000;"
    )

    sql_query = QuerySQL(query_string)

    print("Sending SQL query...")
    result = client.query.sql(sql_query)

    print("Result:")
    pretty_print(result.rows)
    print()


if __name__ == "__main__":
    # run_query_data()
    # run_query_chart()
    # run_query_url()
    run_query_sql()
