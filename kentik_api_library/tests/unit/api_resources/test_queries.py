from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.query_api import QueryAPI
from kentik_api.public.query_object import (
    Aggregate,
    AggregateFunctionType,
    ChartViewType,
    DimensionType,
    FastDataType,
    ImageType,
    MetricType,
    Query,
    QueryArrayItem,
    QueryObject,
    TimeFormat,
)
from kentik_api.public.query_sql import QuerySQL
from kentik_api.public.saved_filter import Filter, FilterGroups, Filters
from tests.unit.stub_api_connector import StubAPIConnector


def test_query_sql_success() -> None:
    # given
    query_sql = """
        SELECT i_start_time,
        round(sum(in_pkts)/(3600)/1000) AS f_sum_in_pkts,
        round(sum(in_bytes)/(3600)/1000)*8 AS f_sum_in_bytes
        FROM all_devices
        WHERE ctimestamp > 3660 AND ctimestamp < 60
        GROUP by i_start_time
        ORDER by i_start_time DESC
        LIMIT 1000;"""
    query_response_payload = """
    {
        "rows": [
            {
                "f_sum_in_bytes": 10,
                "f_sum_in_pkts": 20,
                "i_start_time": "2021-01-25T11:39:00Z"
            },
            {
                "f_sum_in_bytes": 50,
                "f_sum_in_pkts": 60,
                "i_start_time": "2021-01-25T11:38:00Z"
            },
            {
                "f_sum_in_bytes": 80,
                "f_sum_in_pkts": 90,
                "i_start_time": "2021-01-25T11:37:00Z"
            }
        ]
    }"""

    # when
    connector = StubAPIConnector(query_response_payload, HTTPStatus.OK)
    query_api = QueryAPI(connector)
    query = QuerySQL(query=query_sql)
    result = query_api.sql(query=query)

    # then request properly formed
    assert connector.last_url_path == "/query/sql"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["query"] == query_sql

    # and response properly parsed
    assert len(result.rows) == 3
    assert result.rows[0]["f_sum_in_bytes"] == 10
    assert result.rows[0]["f_sum_in_pkts"] == 20
    assert result.rows[0]["i_start_time"] == "2021-01-25T11:39:00Z"
    assert result.rows[1]["f_sum_in_bytes"] == 50
    assert result.rows[1]["f_sum_in_pkts"] == 60
    assert result.rows[1]["i_start_time"] == "2021-01-25T11:38:00Z"
    assert result.rows[2]["f_sum_in_bytes"] == 80
    assert result.rows[2]["f_sum_in_pkts"] == 90
    assert result.rows[2]["i_start_time"] == "2021-01-25T11:37:00Z"


def test_query_data_success() -> None:
    # given
    query_response_payload = """
    {
        "results": [
            {
                "bucket": "Left +Y Axis",
                "data": [
                    {
                        "key": "Total",
                        "avg_bits_per_sec": 19738.220765027323,
                        "p95th_bits_per_sec": 22745.466666666667,
                        "max_bits_per_sec": 25902.533333333333,
                        "name": "Total",
                        "timeSeries": {
                            "both_bits_per_sec": {
                                "flow": [
                                    [
                                        1608538980000,
                                        20751.333333333332,
                                        60
                                    ],
                                    [
                                        1608539040000,
                                        16364.133333333333,
                                        60
                                    ],
                                    [
                                        1608539100000,
                                        19316.933333333334,
                                        60
                                    ]
                                ]
                            }
                        }
                    }
                ]
            }
        ]
    }"""
    connector = StubAPIConnector(query_response_payload, HTTPStatus.OK)
    query_api = QueryAPI(connector)

    # when
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
        all_selected=True,
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis")
    query_object = QueryObject(queries=[query_item])
    result = query_api.data(query_object)

    # then request properly formed
    assert connector.last_url_path == "/query/topXdata"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert len(connector.last_payload["queries"]) == 1
    assert connector.last_payload["queries"][0]["bucket"] == "Left +Y Axis"
    query0 = connector.last_payload["queries"][0]["query"]
    assert len(query0["dimension"]) == 1
    assert query0["dimension"][0] == "Traffic"
    assert query0["cidr"] == 32
    assert query0["cidr6"] == 128
    assert query0["metric"] == ["bytes"]
    assert query0["topx"] == 8
    assert query0["depth"] == 75
    assert query0["fastData"] == "Auto"
    assert query0["outsort"] == "avg_bits_per_sec"
    assert query0["lookback_seconds"] == 3600
    assert query0["hostname_lookup"] == True
    assert query0["device_name"] == []
    assert query0["all_selected"] == True
    assert query0["descriptor"] == ""
    assert len(query0["aggregates"]) == 3
    assert query0["aggregates"][0]["name"] == "avg_bits_per_sec"
    assert query0["aggregates"][0]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][0]["fn"] == "average"
    assert query0["aggregates"][0]["raw"] == True
    assert query0["aggregates"][1]["name"] == "p95th_bits_per_sec"
    assert query0["aggregates"][1]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][1]["fn"] == "percentile"
    assert query0["aggregates"][1]["rank"] == 95
    assert query0["aggregates"][2]["name"] == "max_bits_per_sec"
    assert query0["aggregates"][2]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][2]["fn"] == "max"

    # and response properly parsed
    assert len(result.results) == 1
    assert result.results[0]["bucket"] == "Left +Y Axis"
    assert result.results[0]["data"] is not None


def test_query_chart_success() -> None:
    # given
    query_response_payload = """{"dataUri": "data:image/png;base64,ImageDataEncodedBase64=="}"""
    connector = StubAPIConnector(query_response_payload, HTTPStatus.OK)
    query_api = QueryAPI(connector)

    # when
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
    filter_ = Filter(filterField="dst_as", operator="=", filterValue="")
    filter_group = FilterGroups(connector="All", not_=False, filters=[filter_])
    filters = Filters(connector="", filterGroups=[filter_group])
    query = Query(
        viz_type=ChartViewType.stackedArea,
        show_overlay=False,
        overlay_day=-7,
        sync_axes=False,
        query_title="title",
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=[MetricType.bytes],
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=0,
        starting_time="2020-10-20 10:15:00",
        ending_time="2020-10-21 10:15:00",
        hostname_lookup=False,
        device_name=["dev1", "dev2"],
        all_selected=False,
        filters=filters,
        saved_filters=[],
        matrixBy=[DimensionType.src_geo_city.value, DimensionType.dst_geo_city.value],
        pps_threshold=1,
        time_format=TimeFormat.local,
        descriptor="descriptor",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis", isOverlay=False)
    query_object = QueryObject(queries=[query_item], imageType=ImageType.png)
    result = query_api.chart(query_object)

    # then request properly formed
    assert connector.last_url_path == "/query/topXchart"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert len(connector.last_payload["queries"]) == 1
    assert connector.last_payload["queries"][0]["bucket"] == "Left +Y Axis"
    query0 = connector.last_payload["queries"][0]["query"]
    assert query0["viz_type"] == "stackedArea"
    assert query0["show_overlay"] == False
    assert query0["overlay_day"] == -7
    assert query0["sync_axes"] == False
    assert query0["query_title"] == "title"
    assert len(query0["dimension"]) == 1
    assert query0["dimension"][0] == "Traffic"
    assert query0["cidr"] == 32
    assert query0["cidr6"] == 128
    assert query0["metric"] == ["bytes"]
    assert query0["topx"] == 8
    assert query0["depth"] == 75
    assert query0["fastData"] == "Auto"
    assert query0["outsort"] == "avg_bits_per_sec"
    assert query0["lookback_seconds"] == 0
    assert query0["starting_time"] == "2020-10-20 10:15:00"
    assert query0["ending_time"] == "2020-10-21 10:15:00"
    assert query0["hostname_lookup"] == False
    assert query0["device_name"] == ["dev1", "dev2"]
    assert query0["all_selected"] == False
    assert len(query0["filters"]["filterGroups"]) == 1
    assert query0["filters"]["filterGroups"][0]["connector"] == "All"
    assert query0["filters"]["filterGroups"][0]["not"] == False
    assert len(query0["filters"]["filterGroups"][0]["filters"]) == 1
    assert query0["filters"]["filterGroups"][0]["filters"][0]["filterField"] == "dst_as"
    assert query0["filters"]["filterGroups"][0]["filters"][0]["operator"] == "="
    assert query0["filters"]["filterGroups"][0]["filters"][0]["filterValue"] == ""
    assert query0["saved_filters"] == []
    assert query0["matrixBy"] == ["src_geo_city", "dst_geo_city"]
    assert query0["pps_threshold"] == 1
    assert query0["time_format"] == "Local"
    assert query0["descriptor"] == "descriptor"
    assert len(query0["aggregates"]) == 3
    assert query0["aggregates"][0]["name"] == "avg_bits_per_sec"
    assert query0["aggregates"][0]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][0]["fn"] == "average"
    assert query0["aggregates"][0]["raw"] == True
    assert query0["aggregates"][1]["name"] == "p95th_bits_per_sec"
    assert query0["aggregates"][1]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][1]["fn"] == "percentile"
    assert query0["aggregates"][1]["rank"] == 95
    assert query0["aggregates"][2]["name"] == "max_bits_per_sec"
    assert query0["aggregates"][2]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][2]["fn"] == "max"

    # and response properly parsed
    assert result.image_type == ImageType.png
    assert result.image_data == b'"f\xa0x6\xadhI\xdc\xa1\xd7\x9d\x05\xab\x1e\xeb'


def test_query_url_success() -> None:
    # given
    unquoted_response = "https://portal.kentik.com/portal/#Charts/shortUrl/e0d24b3cc8dfe41f9093668e531cbe96"
    query_response_payload = f'"{unquoted_response}"'  # actual response is url in quotation marks
    connector = StubAPIConnector(query_response_payload, HTTPStatus.OK)
    query_api = QueryAPI(connector)

    # when
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
    result = query_api.url(query_object)

    # then request properly formed
    assert connector.last_url_path == "/query/url"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert len(connector.last_payload["queries"]) == 1
    assert connector.last_payload["queries"][0]["bucket"] == "Left +Y Axis"
    query0 = connector.last_payload["queries"][0]["query"]
    assert query0["viz_type"] == "stackedArea"
    assert len(query0["dimension"]) == 1
    assert query0["dimension"][0] == "Traffic"
    assert query0["cidr"] == 32
    assert query0["cidr6"] == 128
    assert query0["metric"] == ["bytes"]
    assert query0["topx"] == 8
    assert query0["depth"] == 75
    assert query0["fastData"] == "Auto"
    assert query0["outsort"] == "avg_bits_per_sec"
    assert query0["lookback_seconds"] == 3600
    assert query0["hostname_lookup"] == True
    assert query0["device_name"] == []
    assert query0["all_selected"] == True
    assert "filters_obj" not in query0
    assert query0["descriptor"] == ""

    # and response properly parsed
    assert result.url == unquoted_response
