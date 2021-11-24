from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.plans_api import PlansAPI
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_get_all_plans_success() -> None:
    # given
    get_response_payload = """
    {
        "plans":[
            {
                "active":true,
                "bgp_enabled":true,
                "cdate":"2020-09-03T08:41:57.489Z",
                "company_id":74333,
                "description":"Your Free Trial includes 6 devices at a maximum of 1000 fps each. Please contact...",
                "deviceTypes":[
                    {
                        "device_type":"router"
                    },
                    {
                        "device_type":"host-nprobe-dns-www"
                    }
                ],
                "devices":[
                    {
                        "id":"77714",
                        "device_name":"testapi_router_minimal_1",
                        "device_type":"router"
                    },
                    {
                        "id":"77720",
                        "device_name":"testapi_dns_minimal_1",
                        "device_type":"host-nprobe-dns-www"
                    },
                    {
                        "id":"77724",
                        "device_name":"testapi_router_minimal_postman",
                        "device_type":"router"
                    },
                    {
                        "id":"77715",
                        "device_name":"testapi_router_full_1",
                        "device_type":"router"
                    }
                ],
                "edate":"2020-09-03T08:41:57.489Z",
                "fast_retention":30,
                "full_retention":30,
                "id":11466,
                "max_bigdata_fps":30,
                "max_devices":6,
                "max_fps":1000,
                "name":"Free Trial Plan",
                "metadata":{
                }
            }]
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    plans_api = PlansAPI(connector)

    # when
    plans = plans_api.get_all()

    # then request properly formed
    assert connector.last_url_path == f"/plans"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then response properly parsed
    assert len(plans) == 1
    assert plans[0].active is True
    assert plans[0].company_id == ID(74333)
    assert plans[0].device_types is not None
    assert len(plans[0].device_types) == 2
    assert plans[0].device_types[0].device_type == "router"
    assert plans[0].devices is not None
    assert len(plans[0].devices) == 4
    assert plans[0].devices[0].id == ID(77714)
