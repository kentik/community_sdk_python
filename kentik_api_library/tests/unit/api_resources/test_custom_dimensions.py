from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.custom_dimensions_api import CustomDimensionsAPI
from kentik_api.public.custom_dimension import CustomDimension, Populator
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_custom_dimension_success() -> None:
    # given
    create_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name",
            "type": "string",
            "company_id": "74333",
            "populators": []
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension = CustomDimension(
        name="c_testapi_dimension_1",
        display_name="dimension_display_name",
        type="string",
    )
    created = custom_dimensions_api.create(dimension)

    # then request properly formed
    assert connector.last_url_path == "/customdimension"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload == {
        "name": "c_testapi_dimension_1",
        "display_name": "dimension_display_name",
        "type": "string",
    }

    # and response properly parsed
    assert created.id == ID(42)
    assert created.name == "c_testapi_dimension_1"
    assert created.display_name == "dimension_display_name"
    assert created.type == "string"
    assert created.company_id == ID(74333)
    assert created.populators is not None
    assert len(created.populators) == 0


def test_get_custom_dimension_success() -> None:
    # given
    get_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name",
            "type": "string",
            "company_id": "74333",
            "populators": [
                {
                    "id": 1510871096,
                    "dimension_id": 24001,
                    "value": "testapi-dimension-value-1",
                    "direction": "DST",
                    "device_name": "128.0.0.100,device1",
                    "interface_name": "interface1,interface2",
                    "addr": "128.0.0.1/32,128.0.0.2/32",
                    "addr_count": 2,
                    "port": "1001,1002",
                    "tcp_flags": "160",
                    "protocol": "6,17",
                    "asn": "101,102",
                    "nexthop_asn": "201,202",
                    "nexthop": "128.0.200.1/32,128.0.200.2/32",
                    "bgp_aspath": "3001,3002",
                    "bgp_community": "401:499,501:599",
                    "user": "144319",
                    "created_date": "2020-12-15T08:32:19.503788Z",
                    "updated_date": "2020-12-15T08:32:19.503788Z",
                    "company_id": "74333",
                    "device_type": "device-type1",
                    "site": "site1,site2,site3",
                    "lasthop_as_name": "asn101,asn102",
                    "nexthop_as_name": "asn201,asn202",
                    "mac": "FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF",
                    "mac_count": 2,
                    "country": "NL,SE",
                    "vlans": "2001,2002"
                },
                {
                    "id": 1510862280,
                    "dimension_id": 24001,
                    "value": "testapi-dimension-value-3",
                    "direction": "SRC",
                    "addr_count": 0,
                    "user": "144319",
                    "created_date": "2020-12-15T07:55:23.911095Z",
                    "updated_date": "2020-12-15T11:11:30.300681Z",
                    "company_id": "74333",
                    "site": "site3",
                    "mac_count": 0
                }
            ]
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = ID(42)
    dimension = custom_dimensions_api.get(dimension_id)

    # then request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert dimension.id == ID(42)
    assert dimension.name == "c_testapi_dimension_1"
    assert dimension.display_name == "dimension_display_name"
    assert dimension.type == "string"
    assert dimension.company_id == ID(74333)
    assert dimension.populators is not None
    assert len(dimension.populators) == 2
    assert dimension.populators[1].id == ID(1510862280)
    assert dimension.populators[1].dimension_id == ID(24001)
    assert dimension.populators[1].value == "testapi-dimension-value-3"
    assert dimension.populators[1].direction == Populator.Direction.SRC
    assert dimension.populators[1].addr_count == 0
    assert dimension.populators[1].user == "144319"
    assert dimension.populators[1].created_date == "2020-12-15T07:55:23.911095Z"
    assert dimension.populators[1].updated_date == "2020-12-15T11:11:30.300681Z"
    assert dimension.populators[1].company_id == ID(74333)
    assert dimension.populators[1].site == "site3"
    assert dimension.populators[1].mac_count == 0


def test_update_custom_dimension_success() -> None:
    # given
    update_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name2",
            "type": "string",
            "company_id": "74333",
            "populators": []
        }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = ID(42)
    dimension = CustomDimension(id=dimension_id, display_name="dimension_display_name2")
    updated = custom_dimensions_api.update(dimension)

    # then request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "display_name": "dimension_display_name2",
    }

    # and response properly parsed
    assert updated.id == ID(42)
    assert updated.name == "c_testapi_dimension_1"
    assert updated.display_name == "dimension_display_name2"
    assert updated.type == "string"
    assert updated.company_id == ID(74333)
    assert updated.populators is not None
    assert len(updated.populators) == 0


def test_delete_custom_dimension_success() -> None:
    # given
    delete_response_payload = ""  # deleting custom dimension responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = ID(42)
    delete_successful = custom_dimensions_api.delete(dimension_id)

    # then request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful


def test_get_all_custom_dimensions_success() -> None:
    # given
    get_response_payload = """
    {
        "customDimensions": [
            {
                "id": 42,
                "name": "c_testapi_dimension_1",
                "display_name": "dimension_display_name1",
                "type": "string",
                "populators": [],
                "company_id": "74333"
            },
            {
                "id": 43,
                "name": "c_testapi_dimension_2",
                "display_name": "dimension_display_name2",
                "type": "uint32",
                "company_id": "74334",
                "populators": [
                    {
                        "id": 1510862280,
                        "dimension_id": 24001,
                        "value": "testapi-dimension-value-3",
                        "device_type": "device-type3",
                        "direction": "SRC",
                        "interface_name": "interface3",
                        "addr_count": 0,
                        "user": "144319",
                        "created_date": "2020-12-15T07:55:23.911095Z",
                        "updated_date": "2020-12-15T10:50:22.35787Z",
                        "company_id": "74333",
                        "site": "site3",
                        "mac_count": 0
                    }
                ]
            }
        ]
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimensions = custom_dimensions_api.get_all()

    # then request properly formed
    assert connector.last_url_path == "/customdimensions"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert len(dimensions) == 2
    assert dimensions[1].id == ID(43)
    assert dimensions[1].name == "c_testapi_dimension_2"
    assert dimensions[1].display_name == "dimension_display_name2"
    assert dimensions[1].type == "uint32"
    assert dimensions[1].company_id == ID(74334)
    assert dimensions[1].populators is not None
    assert len(dimensions[1].populators) == 1
    assert dimensions[1].populators[0].id == ID(1510862280)
    assert dimensions[1].populators[0].dimension_id == ID(24001)
    assert dimensions[1].populators[0].value == "testapi-dimension-value-3"
    assert dimensions[1].populators[0].direction == Populator.Direction.SRC
    assert dimensions[1].populators[0].interface_name == "interface3"
    assert dimensions[1].populators[0].addr_count == 0
    assert dimensions[1].populators[0].user == "144319"
    assert dimensions[1].populators[0].created_date == "2020-12-15T07:55:23.911095Z"
    assert dimensions[1].populators[0].updated_date == "2020-12-15T10:50:22.35787Z"
    assert dimensions[1].populators[0].company_id == ID(74333)
    assert dimensions[1].populators[0].device_type == "device-type3"
    assert dimensions[1].populators[0].site == "site3"
    assert dimensions[1].populators[0].mac_count == 0


def test_create_populator_success() -> None:
    # given
    create_response_payload = """
    {
        "populator": {
            "dimension_id": 24001,
            "value": "testapi-dimension-value-1",
            "direction": "DST",
            "device_name": "128.0.0.100,device1",
            "interface_name": "interface1,interface2",
            "addr": "128.0.0.1/32,128.0.0.2/32",
            "port": "1001,1002",
            "tcp_flags": "160",
            "protocol": "6,17",
            "asn": "101,102",
            "nexthop_asn": "201,202",
            "nexthop": "128.0.200.1/32,128.0.200.2/32",
            "bgp_aspath": "3001,3002",
            "bgp_community": "401:499,501:599",
            "device_type": "device-type1",
            "site": "site1,site2,site3",
            "lasthop_as_name": "asn101,asn102",
            "nexthop_as_name": "asn201,asn202",
            "mac": "FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF",
            "country": "NL,SE",
            "vlans": "2001,2002",
            "id": 1510862280,
            "company_id": "74333",
            "user": "144319",
            "mac_count": 2,
            "addr_count": 2,
            "created_date": "2020-12-15T07:55:23.911095Z",
            "updated_date": "2020-12-15T07:55:23.911095Z"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = ID(24001)
    populator = Populator(
        dimension_id=dimension_id,
        value="testapi-dimension-value-1",
        direction=Populator.Direction.DST,
        device_name="device1,128.0.0.100",
        interface_name="interface1,interface2",
        addr="128.0.0.1/32,128.0.0.2/32",
        port="1001,1002",
        tcp_flags="160",
        protocol="6,17",
        asn="101,102",
        nexthop_asn="201,202",
        nexthop="128.0.200.1/32,128.0.200.2/32",
        bgp_aspath="3001,3002",
        bgp_community="401:499,501:599",
        device_type="device-type1",
        site="site1,site2,site3",
        lasthop_as_name="asn101,asn102",
        nexthop_as_name="asn201,asn202",
        mac="FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF",
        country="NL,SE",
        vlans="2001,2002",
    )
    created = custom_dimensions_api.populators.create(populator)

    # then request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}/populator"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload == {
        "populator": {
            "value": "testapi-dimension-value-1",
            "direction": "DST",
            "device_name": "device1,128.0.0.100",
            "device_type": "device-type1",
            "site": "site1,site2,site3",
            "interface_name": "interface1,interface2",
            "addr": "128.0.0.1/32,128.0.0.2/32",
            "port": "1001,1002",
            "tcp_flags": "160",
            "protocol": "6,17",
            "asn": "101,102",
            "lasthop_as_name": "asn101,asn102",
            "nexthop_asn": "201,202",
            "nexthop_as_name": "asn201,asn202",
            "nexthop": "128.0.200.1/32,128.0.200.2/32",
            "bgp_aspath": "3001,3002",
            "bgp_community": "401:499,501:599",
            "mac": "FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF",
            "country": "NL,SE",
            "vlans": "2001,2002",
        }
    }

    # and response properly parsed
    assert created.dimension_id == ID(24001)
    assert created.value == "testapi-dimension-value-1"
    assert created.direction == Populator.Direction.DST
    assert created.device_name == "128.0.0.100,device1"
    assert created.interface_name == "interface1,interface2"
    assert created.addr == "128.0.0.1/32,128.0.0.2/32"
    assert created.port == "1001,1002"
    assert created.tcp_flags == "160"
    assert created.protocol == "6,17"
    assert created.asn == "101,102"
    assert created.nexthop_asn == "201,202"
    assert created.nexthop == "128.0.200.1/32,128.0.200.2/32"
    assert created.bgp_aspath == "3001,3002"
    assert created.bgp_community == "401:499,501:599"
    assert created.device_type == "device-type1"
    assert created.site == "site1,site2,site3"
    assert created.lasthop_as_name == "asn101,asn102"
    assert created.nexthop_as_name == "asn201,asn202"
    assert created.mac == "FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF"
    assert created.country == "NL,SE"
    assert created.vlans == "2001,2002"
    assert created.id == ID(1510862280)
    assert created.company_id == ID(74333)
    assert created.user == "144319"
    assert created.mac_count == 2
    assert created.addr_count == 2
    assert created.created_date == "2020-12-15T07:55:23.911095Z"
    assert created.updated_date == "2020-12-15T07:55:23.911095Z"


def test_update_populator_success() -> None:
    # given
    update_response_payload = """
    {
        "populator": {
            "id": 1510862280,
            "dimension_id": 24001,
            "value": "testapi-dimension-value-3",
            "direction": "SRC",
            "interface_name": "interface3",
            "addr_count": 0,
            "tcp_flags": "12",
            "protocol": "17",
            "user": "144319",
            "created_date": "2020-12-15T07:55:23.911095Z",
            "updated_date": "2020-12-15T10:50:22.35787Z",
            "company_id": "74333",
            "device_type": "device-type3",
            "site": "site3",
            "mac_count": 0
        }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    populator_id = ID(1510862280)
    dimension_id = ID(24001)
    populator = Populator(
        id=populator_id,
        dimension_id=dimension_id,
        value="testapi-dimension-value-3",
        direction=Populator.Direction.SRC,
        interface_name="interface3",
        tcp_flags="12",
        protocol="17",
        device_type="device-type3",
        site="site3",
    )
    updated = custom_dimensions_api.populators.update(populator)

    # then request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}/populator/{populator_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "populator": {
            "value": "testapi-dimension-value-3",
            "direction": "SRC",
            "device_type": "device-type3",
            "site": "site3",
            "interface_name": "interface3",
            "tcp_flags": "12",
            "protocol": "17",
        },
    }

    # and response properly parsed
    assert updated.id == ID(1510862280)
    assert updated.dimension_id == ID(24001)
    assert updated.value == "testapi-dimension-value-3"
    assert updated.direction == Populator.Direction.SRC
    assert updated.interface_name == "interface3"
    assert updated.addr_count == 0
    assert updated.tcp_flags == "12"
    assert updated.protocol == "17"
    assert updated.user == "144319"
    assert updated.created_date == "2020-12-15T07:55:23.911095Z"
    assert updated.updated_date == "2020-12-15T10:50:22.35787Z"
    assert updated.company_id == ID(74333)
    assert updated.device_type == "device-type3"
    assert updated.site == "site3"
    assert updated.mac_count == 0


def test_delete_populator_success() -> None:
    # given
    delete_response_payload = ""  # deleting populator responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    populator_id = ID(42)
    dimension_id = ID(4002)
    delete_successful = custom_dimensions_api.populators.delete(dimension_id, populator_id)

    # then request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}/populator/{populator_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful


def test_get_and_update_custom_dimension_with_unknown_enum_fields() -> None:
    # given
    dimension_id = ID(42)
    populator_id = ID(1510862280)

    get_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name",
            "type": "string",
            "company_id": "74333",
            "populators": [
                {
                    "id": 1510862280,
                    "dimension_id": 42,
                    "value": "testapi-dimension-value-3",
                    "direction": "d_teapot",
                    "addr_count": 0,
                    "user": "144319",
                    "created_date": "2020-12-15T07:55:23.911095Z",
                    "updated_date": "2020-12-15T11:11:30.300681Z",
                    "company_id": "74333",
                    "mac_count": 0
                }
            ]
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when custom dimension got
    dimension = custom_dimensions_api.get(dimension_id)

    # then get request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then get response properly parsed
    check_dimension_one(
        dimension,
        expected_value="testapi-dimension-value-3",
        expected_direction="D_TEAPOT",
    )

    # given
    update_response_payload = """
    {
        "populator": {
            "id": 1510862280,
            "dimension_id": 42,
            "value": "updated_value",
            "direction": "D_TEAPOT",
            "addr_count": 0,
            "user": "144319",
            "created_date": "2020-12-15T07:55:23.911095Z",
            "updated_date": "2020-12-15T11:11:30.300681Z",
            "company_id": "74333",
            "mac_count": 0
        }
    }"""
    connector.response_text = update_response_payload

    assert dimension.populators is not None
    assert len(dimension.populators) == 1
    populator = dimension.populators[0]

    # when populator updated
    populator.value = "updated_value"
    populator = custom_dimensions_api.populators.update(populator)

    # then update request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}/populator/{populator_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "populator": {
            "value": "updated_value",
            "direction": "D_TEAPOT",
        },
    }

    # then update response properly parsed
    check_populator_one(populator, expected_value="updated_value", expected_direction="D_TEAPOT")


def test_get_and_update_custom_dimension_with_empty_enum_fields() -> None:
    # given
    dimension_id = ID(42)
    populator_id = ID(1510862280)

    get_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name",
            "type": "string",
            "company_id": "74333",
            "populators": [
                {
                    "id": 1510862280,
                    "dimension_id": 42,
                    "value": "testapi-dimension-value-3",
                    "direction": "",
                    "addr_count": 0,
                    "user": "144319",
                    "created_date": "2020-12-15T07:55:23.911095Z",
                    "updated_date": "2020-12-15T11:11:30.300681Z",
                    "company_id": "74333",
                    "mac_count": 0
                }
            ]
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when custom dimension get
    dimension = custom_dimensions_api.get(dimension_id)

    # then get request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then get response properly parsed
    check_dimension_one(dimension, expected_value="testapi-dimension-value-3", expected_direction="")

    # given
    update_response_payload = """
    {
        "populator": {
            "id": 1510862280,
            "dimension_id": 42,
            "value": "updated_value",
            "direction": "",
            "addr_count": 0,
            "user": "144319",
            "created_date": "2020-12-15T07:55:23.911095Z",
            "updated_date": "2020-12-15T11:11:30.300681Z",
            "company_id": "74333",
            "mac_count": 0
        }
    }"""
    connector.response_text = update_response_payload

    assert dimension.populators is not None
    assert len(dimension.populators) == 1
    populator = dimension.populators[0]

    # when populator updated
    populator.value = "updated_value"
    populator = custom_dimensions_api.populators.update(populator)

    # then update request properly formed
    assert connector.last_url_path == f"/customdimension/{dimension_id}/populator/{populator_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "populator": {
            "value": "updated_value",
            "direction": "",
        },
    }

    # then update response properly parsed
    check_populator_one(populator, expected_value="updated_value", expected_direction="")


def check_dimension_one(dimension, expected_value, expected_direction) -> None:
    assert dimension.id == ID(42)
    assert dimension.name == "c_testapi_dimension_1"
    assert dimension.display_name == "dimension_display_name"
    assert dimension.type == "string"
    assert dimension.company_id == ID(74333)

    assert dimension.populators is not None
    assert len(dimension.populators) == 1
    check_populator_one(
        dimension.populators[0],
        expected_value=expected_value,
        expected_direction=expected_direction,
    )


def check_populator_one(populator, expected_value, expected_direction) -> None:
    assert populator.id == ID(1510862280)
    assert populator.dimension_id == ID(42)
    assert populator.value == expected_value
    assert populator.direction == expected_direction
    assert populator.addr_count == 0
    assert populator.user == "144319"
    assert populator.created_date == "2020-12-15T07:55:23.911095Z"
    assert populator.updated_date == "2020-12-15T11:11:30.300681Z"
    assert populator.company_id == ID(74333)
    assert populator.mac_count == 0
