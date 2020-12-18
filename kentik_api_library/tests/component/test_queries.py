from http import HTTPStatus

from kentik_api.api_resources.query_api import QueryAPI
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.query_object import QueryObject, ImageType
from tests.component.stub_api_connector import StubAPIConnector


def test_get_query_data_success() -> None:
    # given
    get_response_payload = """
    {
        "results": [
            {
            "bucket": "Left +Y Axis",
            "data": [
                {
                "Geography_src": "US",
                "avg_bits_per_sec": 130548781.51111111,
                "key": "US",
                "max_bits_per_sec": 153616657.06666666,
                "p95th_bits_per_sec": 150816290.13333333,
                "timeSeries": {
                    "both_bits_per_sec": {
                    "flow": [
                        [
                        1482186900000,
                        128568524.8,
                        60
                        ],
                        [
                        1482186960000,
                        133069482.66666667,
                        60
                        ],
                        [
                        1482187020000,
                        115999675.73333333,
                        60
                        ],
                        [
                        1482187080000,
                        153616657.06666666,
                        60
                        ],
                        [
                        1482187140000,
                        104022425.6,
                        60
                        ],
                        [
                        1482187258438,
                        148015923.2,
                        60
                        ]
                    ]
                    }
                }
                },
                {
                "Geography_src": "AU",
                "avg_bits_per_sec": 732114.4888888889,
                "key": "AU",
                "max_bits_per_sec": 1145924.2666666666,
                "p95th_bits_per_sec": 1003315.2
                }
            ]
            }
        ]
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    queries_api = QueryAPI(connector)

    # when
    query_object = QueryObject(queries=[], imageType=ImageType.png)
    result = queries_api.data(query_object)

    # then request properly formed
    assert connector.last_url == "/query/topXdata"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["imageType"] == "png"

    # and response properly parsed
    assert len(result.results) == 1
    assert result.results[0]["bucket"] == "Left +Y Axis"
    assert result.results[0]["data"] is not None
