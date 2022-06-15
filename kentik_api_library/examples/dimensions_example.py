# pylint: disable=redefined-outer-name
"""
Examples of using the typed custom dimensions API
"""

import logging
import random
import string

from examples.utils import pretty_print
from kentik_api import CustomDimension, KentikAPI, Populator
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def rand_uid() -> str:
    num_characters = 5
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=num_characters))


def run_crud() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE DIMENSION")
    dimension = CustomDimension(
        name="c_testapi_dim_" + rand_uid(),  # random uid as even deleted names are held for 1 year and must be unique
        display_name="test_dimension",
        type="string",
    )
    created = client.custom_dimensions.create(dimension)
    pretty_print(created)
    print()

    print("### UPDATE DIMENSION")
    created.display_name = "test_dimension_updated"
    updated = client.custom_dimensions.update(created)
    pretty_print(updated)
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
    pretty_print(created_populator)
    print()

    print("### UPDATE POPULATOR")
    created_populator.value = "testapi-dimension-value-updated"
    created_populator.direction = Populator.Direction.EITHER
    updated_populator = client.custom_dimensions.populators.update(created_populator)
    pretty_print(updated_populator)
    print()

    print("### GET DIMENSION")
    got = client.custom_dimensions.get(updated.id)
    pretty_print(got)
    print()

    print("### DELETE POPULATOR")
    deleted_populator = client.custom_dimensions.populators.delete(updated_populator.dimension_id, updated_populator.id)
    print(deleted_populator)
    print()

    print("### DELETE DIMENSION")
    deleted = client.custom_dimensions.delete(updated.id)
    print(deleted)
    print()


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET ALL")
    dimensions = client.custom_dimensions.get_all()
    pretty_print(dimensions)
    print()


if __name__ == "__main__":
    run_crud()
    run_list()
