from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.tags_api import TagsAPI
from kentik_api.public.tag import Tag
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_tag_success() -> None:
    # given
    create_response_payload = """
    {
        "tag": {
            "id": 42,
            "flow_tag": "APITEST-TAG-1",
            "device_name": "192.168.5.100,device1",
            "interface_name": "interface1,interface2",
            "addr": "192.168.0.1/32,192.168.0.2/32",
            "addr_count": 2,
            "port": "9000,9001",
            "tcp_flags": "7",
            "protocol": "6,17",
            "asn": "101,102,103",
            "nexthop": "192.168.7.1/32,192.168.7.2/32",
            "nexthop_asn": "51,52,53",
            "bgp_aspath": "201,202,203",
            "bgp_community": "301,302,303",
            "user": "144319",
            "created_date": "2020-12-10T11:53:48.752418Z",
            "updated_date": "2020-12-10T11:53:48.752418Z",
            "company_id": "74333",
            "device_type": "router,switch",
            "site": "site1,site2",
            "lasthop_as_name": "as1,as2,as3",
            "nexthop_as_name": "as51,as52,as53",
            "mac": "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF",
            "mac_count": 2,
            "country": "ES,IT",
            "edited_by": "john.doe@acme.com",
            "vlans": "4001,4002,4003"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    tags_api = TagsAPI(connector)

    # when
    tag = Tag(
        flow_tag="APITEST-TAG-1",
        device_name="device1,192.168.5.100",
        device_type="router,switch",
        site="site1,site2",
        interface_name="interface1,interface2",
        addr="192.168.0.1,192.168.0.2",
        port="9000,9001",
        tcp_flags="7",
        protocol="6,17",
        asn="101,102,103",
        lasthop_as_name="as1,as2,as3",
        nexthop_asn="51,52,53",
        nexthop_as_name="as51,as52,as53",
        nexthop="192.168.7.1,192.168.7.2",
        bgp_aspath="201,202,203",
        bgp_community="301,302,303",
        mac="FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF",
        country="ES,IT",
        vlans="4001,4002,4003",
    )
    created = tags_api.create(tag)

    # then request properly formed
    assert connector.last_url_path == "/tag"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert "tag" in connector.last_payload
    assert connector.last_payload["tag"]["flow_tag"] == "APITEST-TAG-1"
    assert connector.last_payload["tag"]["device_name"] == "device1,192.168.5.100"
    assert connector.last_payload["tag"]["device_type"] == "router,switch"
    assert connector.last_payload["tag"]["site"] == "site1,site2"
    assert connector.last_payload["tag"]["interface_name"] == "interface1,interface2"
    assert connector.last_payload["tag"]["addr"] == "192.168.0.1,192.168.0.2"
    assert connector.last_payload["tag"]["port"] == "9000,9001"
    assert connector.last_payload["tag"]["tcp_flags"] == "7"
    assert connector.last_payload["tag"]["protocol"] == "6,17"
    assert connector.last_payload["tag"]["asn"] == "101,102,103"
    assert connector.last_payload["tag"]["lasthop_as_name"] == "as1,as2,as3"
    assert connector.last_payload["tag"]["nexthop_asn"] == "51,52,53"
    assert connector.last_payload["tag"]["nexthop_as_name"] == "as51,as52,as53"
    assert connector.last_payload["tag"]["nexthop"] == "192.168.7.1,192.168.7.2"
    assert connector.last_payload["tag"]["bgp_aspath"] == "201,202,203"
    assert connector.last_payload["tag"]["bgp_community"] == "301,302,303"
    assert connector.last_payload["tag"]["mac"] == "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF"
    assert connector.last_payload["tag"]["country"] == "ES,IT"
    assert connector.last_payload["tag"]["vlans"] == "4001,4002,4003"

    # and response properly parsed
    assert created.flow_tag == "APITEST-TAG-1"
    assert created.device_name == "192.168.5.100,device1"
    assert created.interface_name == "interface1,interface2"
    assert created.addr == "192.168.0.1/32,192.168.0.2/32"
    assert created.port == "9000,9001"
    assert created.tcp_flags == "7"
    assert created.protocol == "6,17"
    assert created.asn == "101,102,103"
    assert created.nexthop == "192.168.7.1/32,192.168.7.2/32"
    assert created.nexthop_asn == "51,52,53"
    assert created.bgp_aspath == "201,202,203"
    assert created.bgp_community == "301,302,303"
    assert created.device_type == "router,switch"
    assert created.site == "site1,site2"
    assert created.lasthop_as_name == "as1,as2,as3"
    assert created.nexthop_as_name == "as51,as52,as53"
    assert created.mac == "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF"
    assert created.country == "ES,IT"
    assert created.vlans == "4001,4002,4003"
    assert created.id == ID(42)
    assert created.company_id == ID(74333)
    assert created.addr_count == 2
    assert created.user_id == ID(144319)
    assert created.mac_count == 2
    assert created.edited_by == "john.doe@acme.com"
    assert created.created_date == "2020-12-10T11:53:48.752418Z"
    assert created.updated_date == "2020-12-10T11:53:48.752418Z"


def test_get_tag_success() -> None:
    # given
    get_response_payload = """
    {
        "tag": {
            "id": 42,
            "flow_tag": "APITEST-TAG-1",
            "device_name": "192.168.5.100,device1",
            "interface_name": "interface1,interface2",
            "addr": "192.168.0.1/32,192.168.0.2/32",
            "addr_count": 2,
            "port": "9000,9001",
            "tcp_flags": "7",
            "protocol": "6,17",
            "asn": "101,102,103",
            "nexthop": "192.168.7.1/32,192.168.7.2/32",
            "nexthop_asn": "51,52,53",
            "bgp_aspath": "201,202,203",
            "bgp_community": "301,302,303",
            "user": "144319",
            "created_date": "2020-12-10T11:53:48.752418Z",
            "updated_date": "2020-12-10T11:53:48.752418Z",
            "company_id": "74333",
            "device_type": "router,switch",
            "site": "site1,site2",
            "lasthop_as_name": "as1,as2,as3",
            "nexthop_as_name": "as51,as52,as53",
            "mac": "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF",
            "mac_count": 2,
            "country": "ES,IT",
            "edited_by": "john.doe@acme.com",
            "vlans": "4001,4002,4003"
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    tags_api = TagsAPI(connector)

    # when
    tag_id = ID(42)
    tag = tags_api.get(tag_id)

    # then request properly formed
    assert connector.last_url_path == f"/tag/{tag_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert tag.flow_tag == "APITEST-TAG-1"
    assert tag.device_name == "192.168.5.100,device1"
    assert tag.interface_name == "interface1,interface2"
    assert tag.addr == "192.168.0.1/32,192.168.0.2/32"
    assert tag.port == "9000,9001"
    assert tag.tcp_flags == "7"
    assert tag.protocol == "6,17"
    assert tag.asn == "101,102,103"
    assert tag.nexthop == "192.168.7.1/32,192.168.7.2/32"
    assert tag.nexthop_asn == "51,52,53"
    assert tag.bgp_aspath == "201,202,203"
    assert tag.bgp_community == "301,302,303"
    assert tag.device_type == "router,switch"
    assert tag.site == "site1,site2"
    assert tag.lasthop_as_name == "as1,as2,as3"
    assert tag.nexthop_as_name == "as51,as52,as53"
    assert tag.mac == "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF"
    assert tag.country == "ES,IT"
    assert tag.vlans == "4001,4002,4003"
    assert tag.id == ID(42)
    assert tag.company_id == ID(74333)
    assert tag.addr_count == 2
    assert tag.user_id == ID(144319)
    assert tag.mac_count == 2
    assert tag.edited_by == "john.doe@acme.com"
    assert tag.created_date == "2020-12-10T11:53:48.752418Z"
    assert tag.updated_date == "2020-12-10T11:53:48.752418Z"


def test_update_tag_success() -> None:
    # given
    update_response_payload = """
    {
        "tag": {
            "id": 42,
            "flow_tag": "APITEST-TAG-2",
            "device_name": "192.168.5.200,device2",
            "interface_name": "interface3,interface4",
            "addr": "192.168.0.1/32,192.168.0.2/32",
            "addr_count": 2,
            "port": "9000,9001",
            "tcp_flags": "8",
            "protocol": "6,17",
            "asn": "111,112,113",
            "nexthop": "192.168.7.1/32,192.168.7.2/32",
            "nexthop_asn": "51,52,53",
            "bgp_aspath": "201,202,203",
            "bgp_community": "301,302,303",
            "user": "144319",
            "created_date": "2020-12-10T11:53:48.752418Z",
            "updated_date": "2020-12-10T11:53:48.752418Z",
            "company_id": "74333",
            "device_type": "router2,switch2",
            "site": "site3,site4",
            "lasthop_as_name": "as1,as2,as3",
            "nexthop_as_name": "as51,as52,as53",
            "mac": "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF",
            "mac_count": 2,
            "country": "ES,IT",
            "edited_by": "john.doe@acme.com",
            "vlans": "4011,4012,4013"
        }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    tags_api = TagsAPI(connector)

    # when
    tag_id = ID(42)
    tag = Tag(
        id=tag_id,
        flow_tag="APITEST-TAG-2",
        device_name="device2,192.168.5.200",
        device_type="router2,switch2",
        site="site3,site4",
        country="ES,IT",
        vlans="4011,4012,4013",
        interface_name="interface3,interface4",
        tcp_flags="8",
        asn="111,112,113",
    )
    updated = tags_api.update(tag)

    # then request properly formed
    assert connector.last_url_path == f"/tag/{tag_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert "tag" in connector.last_payload
    assert connector.last_payload["tag"]["flow_tag"] == "APITEST-TAG-2"
    assert connector.last_payload["tag"]["device_name"] == "device2,192.168.5.200"
    assert connector.last_payload["tag"]["device_type"] == "router2,switch2"
    assert connector.last_payload["tag"]["site"] == "site3,site4"
    assert connector.last_payload["tag"]["country"] == "ES,IT"
    assert connector.last_payload["tag"]["vlans"] == "4011,4012,4013"
    assert connector.last_payload["tag"]["interface_name"] == "interface3,interface4"
    assert connector.last_payload["tag"]["tcp_flags"] == "8"
    assert connector.last_payload["tag"]["asn"] == "111,112,113"
    assert "addr" not in connector.last_payload["tag"]
    assert "port" not in connector.last_payload["tag"]
    assert "protocol" not in connector.last_payload["tag"]
    assert "lasthop_as_name" not in connector.last_payload["tag"]
    assert "nexthop_asn" not in connector.last_payload["tag"]
    assert "nexthop_as_name" not in connector.last_payload["tag"]
    assert "nexthop" not in connector.last_payload["tag"]
    assert "bgp_aspath" not in connector.last_payload["tag"]
    assert "bgp_community" not in connector.last_payload["tag"]
    assert "mac" not in connector.last_payload["tag"]

    # and response properly parsed
    assert updated.flow_tag == "APITEST-TAG-2"
    assert updated.device_name == "192.168.5.200,device2"
    assert updated.interface_name == "interface3,interface4"
    assert updated.addr == "192.168.0.1/32,192.168.0.2/32"
    assert updated.port == "9000,9001"
    assert updated.tcp_flags == "8"
    assert updated.protocol == "6,17"
    assert updated.asn == "111,112,113"
    assert updated.nexthop == "192.168.7.1/32,192.168.7.2/32"
    assert updated.nexthop_asn == "51,52,53"
    assert updated.bgp_aspath == "201,202,203"
    assert updated.bgp_community == "301,302,303"
    assert updated.device_type == "router2,switch2"
    assert updated.site == "site3,site4"
    assert updated.lasthop_as_name == "as1,as2,as3"
    assert updated.nexthop_as_name == "as51,as52,as53"
    assert updated.mac == "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF"
    assert updated.country == "ES,IT"
    assert updated.vlans == "4011,4012,4013"
    assert updated.id == ID(42)
    assert updated.company_id == ID(74333)
    assert updated.addr_count == 2
    assert updated.user_id == ID(144319)
    assert updated.mac_count == 2
    assert updated.edited_by == "john.doe@acme.com"
    assert updated.created_date == "2020-12-10T11:53:48.752418Z"
    assert updated.updated_date == "2020-12-10T11:53:48.752418Z"


def test_delete_tag_success() -> None:
    # given
    delete_response_payload = ""  # deleting tag responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    tags_api = TagsAPI(connector)

    # when
    tag_id = ID(42)
    delete_successful = tags_api.delete(tag_id)

    # then request properly formed
    assert connector.last_url_path == f"/tag/{tag_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful


def test_get_all_tags_success() -> None:
    # given
    get_response_payload = """
    {
        "tags": [
            {
                "id": 42,
                "flow_tag": "APITEST-TAG-1",
                "device_name": "device1",
                "interface_name": "interface1",
                "addr": "192.168.0.1/32,192.168.0.2/32",
                "addr_count": 2,
                "port": "9000",
                "tcp_flags": "7",
                "protocol": "12",
                "asn": "101,102,103",
                "nexthop": "192.168.7.1/32,192.168.7.2/32",
                "nexthop_asn": "51,52,53",
                "bgp_aspath": "201,202,203",
                "bgp_community": "301,302,303",
                "user": "144319",
                "created_date": "2020-12-10T11:39:44.233335Z",
                "updated_date": "2020-12-10T11:39:44.233335Z",
                "company_id": "74333",
                "device_type": "router",
                "site": "site1",
                "lasthop_as_name": "as1,as2,as3",
                "nexthop_as_name": "as51,as52,as53",
                "mac": "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF",
                "mac_count": 2,
                "country": "ES,IT",
                "edited_by": "john.doe@acme.com",
                "vlans": "4001,4002,4003"
            },
            {
                "id": 43,
                "flow_tag": "APITEST-TAG-2",
                "device_name": "device2",
                "interface_name": "interface1",
                "addr": "192.168.2.1/32,192.168.2.2/32",
                "addr_count": 2,
                "port": "9002",
                "tcp_flags": "2",
                "protocol": "2",
                "asn": "101,102,103",
                "nexthop": "192.168.7.1/32,192.168.7.2/32",
                "nexthop_asn": "51,52,53",
                "bgp_aspath": "201,202,203",
                "bgp_community": "301,302,303",
                "user": "144319",
                "created_date": "2020-12-10T11:39:44.233335Z",
                "updated_date": "2020-12-10T11:39:44.233335Z",
                "company_id": "74333",
                "device_type": "router",
                "site": "site1",
                "lasthop_as_name": "as1,as2,as3",
                "nexthop_as_name": "as51,as52,as53",
                "mac": "FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF",
                "mac_count": 2,
                "country": "ES,IT",
                "edited_by": "john.doe@acme.com",
                "vlans": "4001,4002,4003"
            },
            {
                "id": 452718,
                "flow_tag": "DNS_TRAFFIC",
                "addr_count": 0,
                "port": "53",
                "user": "39242",
                "created_date": "2018-10-04T23:39:29.158284Z",
                "updated_date": "2018-10-04T23:39:29.158284Z",
                "company_id": "26393",
                "mac_count": 0,
                "edited_by": "el.celebes@acme.com"
            }
        ]
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    tags_api = TagsAPI(connector)

    # when
    tags = tags_api.get_all()

    # then request properly formed
    assert connector.last_url_path == "/tags"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert len(tags) == 3
