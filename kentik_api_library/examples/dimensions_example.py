# pylint: disable=redefined-outer-name
"""
Examples of using the typed custom dimensions API
"""

import os
import sys
import logging
import random
import string
from typing import Tuple
from kentik_api import KentikAPI, CustomDimension, Populator

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def rand_uid() -> str:
    num_characters = 5
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=num_characters))


def run_crud() -> None:
    """
    Expected response is like:
    ### CREATE DIMENSION
    {'name': 'c_testapi_dim_zmisn', 'display_name': 'test_dimension', 'type': 'string', 'populators': [], '_id': 24115, '_company_id': '74333'}

    ### UPDATE DIMENSION
    {'name': 'c_testapi_dim_zmisn', 'display_name': 'test_dimension_updated', 'type': 'string', 'populators': [], '_id': 24115, '_company_id': '74333'}

    ### CREATE POPULATOR
    {'value': 'testapi-dimension-value-1', 'direction': <Direction.DST: 'DST'>, 'device_name': '128.0.0.100,device1', 'interface_name': 'interface1,interface2', 'addr': '128.0.0.1/32,128.0.0.2/32', 'port': '1001,1002', 'tcp_flags': '160', 'protocol': '6,17', 'asn': '101,102', 'nexthop_asn': '201,202', 'nexthop': '128.0.200.1/32,128.0.200.2/32', 'bgp_aspath': '3001,3002', 'bgp_community': '401:499,501:599', 'device_type': 'device-type1', 'site': 'site1,site2,site3', 'lasthop_as_name': 'asn101,asn102', 'nexthop_as_name': 'asn201,asn202', 'mac': 'FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF', 'country': 'NL,SE', 'vlans': '2001,2002', '_id': 1510982658, '_company_id': '74333', '_dimension_id': 24115, '_user': '144319', '_mac_count': 2, '_addr_count': 2, '_created_date': '2020-12-15T13:18:01.813469Z', '_updated_date': '2020-12-15T13:18:01.813469Z'}

    ### UPDATE POPULATOR
    {'value': 'testapi-dimension-value-updated', 'direction': <Direction.EITHER: 'EITHER'>, 'device_name': '128.0.0.100,device1', 'interface_name': 'interface1,interface2', 'addr': '128.0.0.1/32,128.0.0.2/32', 'port': '1001,1002', 'tcp_flags': '160', 'protocol': '6,17', 'asn': '101,102', 'nexthop_asn': '201,202', 'nexthop': '128.0.200.1/32,128.0.200.2/32', 'bgp_aspath': '3001,3002', 'bgp_community': '401:499,501:599', 'device_type': 'device-type1', 'site': 'site1,site2,site3', 'lasthop_as_name': 'asn101,asn102', 'nexthop_as_name': 'asn201,asn202', 'mac': 'FF:FF:FF:FF:FF:FA,FF:FF:FF:FF:FF:FF', 'country': 'NL,SE', 'vlans': '2001,2002', '_id': 1510982658, '_company_id': '74333', '_dimension_id': 24115, '_user': '144319', '_mac_count': 2, '_addr_count': 2, '_created_date': '2020-12-15T13:18:01.813469Z', '_updated_date': '2020-12-15T13:18:02.298902Z'}

    ### GET DIMENSION
    {'name': 'c_testapi_dim_zmisn', 'display_name': 'test_dimension_updated', 'type': 'string', 'populators': [<kentik_api.public.custom_dimension.Populator object at 0x7f879166aa30>], '_id': 24115, '_company_id': '74333'}

    ### DELETE POPULATOR
    True

    ### DELETE DIMENSION
    True
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE DIMENSION")
    dimension = CustomDimension(
        name="c_testapi_dim_" + rand_uid(),  # random uid as even deleted names are held for 1 year and must be unique
        display_name="test_dimension",
        type="string",
    )
    created = client.custom_dimensions.create(dimension)
    print(created.__dict__)
    print()

    print("### UPDATE DIMENSION")
    created.display_name = "test_dimension_updated"
    updated = client.custom_dimensions.update(created)
    print(updated.__dict__)
    print()

    print("### CREATE POPULATOR")
    populator = Populator(
        dimension_id=updated.id,
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
    created_populator = client.custom_dimensions.populators.create(populator)
    print(created_populator.__dict__)
    print()

    print("### UPDATE POPULATOR")
    created_populator.value = "testapi-dimension-value-updated"
    created_populator.direction = Populator.Direction.EITHER
    updated_populator = client.custom_dimensions.populators.update(created_populator)
    print(updated_populator.__dict__)
    print()

    print("### GET DIMENSION")
    got = client.custom_dimensions.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE POPULATOR")
    deleted_populator = client.custom_dimensions.populators.delete(updated_populator.dimension_id, updated_populator.id)
    print(deleted_populator)
    print()

    print("### DELETE DIMENSION")
    deleted = client.custom_dimensions.delete(updated.id)
    print(deleted)


def run_list() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)
    dimensions = client.custom_dimensions.get_all()
    for d in dimensions:
        print(d.__dict__)


if __name__ == "__main__":
    run_crud()
    # run_list()
