# pylint: disable=redefined-outer-name
"""
Examples of using the typed Query API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, SQLQuery
from kentik_api.public.query_object import (
    QueryObject,
    QueryArrayItem,
    Query,
    Aggregate,
    AggregateFunctionType,
    FastDataType,
    MetricType,
    DimensionType,
    ImageType,
    ChartViewType,
)

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_query_data() -> None:
    """
    Expected response is subsequent result items
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    agg1 = Aggregate(name="avg_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.average, raw=True)
    agg2 = Aggregate(name="p95th_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.percentile, rank=95)
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    query = Query(
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=MetricType.bytes,
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=3600,
        hostname_lookup=True,
        device_name=[],
        all_selected=True,
        filters_obj=None,
        descriptor="",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis")
    query_object = QueryObject(queries=[query_item])

    print("Sending query for data...")
    result = client.query.data(query_object)

    print("Results:")
    for item in result.results:
        print(item.__dict__)


def run_query_chart() -> None:
    """
    Expected response is image type and base64 encoded image data
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    agg1 = Aggregate(name="avg_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.average, raw=True)
    agg2 = Aggregate(name="p95th_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.percentile, rank=95)
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    query = Query(
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=MetricType.bytes,
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
        filters_obj=None,
        descriptor="",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis", isOverlay=False)
    query_object = QueryObject(queries=[query_item], imageType=ImageType.png)

    print("Sending query for chart...")
    result = client.query.chart(query_object)

    print("Result:")
    print(result.__dict__)


def run_query_sql() -> None:
    """
    Expected response is rows containing SQL query result
    """

    email, token = get_auth_email_token()
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

    sql_query = SQLQuery(query_string)

    print("Sending SQL query...")
    result = client.query.sql(sql_query)

    print("Result:")
    print(result.rows)


if __name__ == "__main__":
    run_query_chart()
