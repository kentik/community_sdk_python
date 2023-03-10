# pylint: disable=redefined-outer-name
"""
Examples of using the typed tags API
"""

import logging

from examples.utils import pretty_print
from kentik_api import KentikAPI, Tag
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE")
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
    created = client.tags.create(tag)
    pretty_print(created)
    print()

    print("### UPDATE")
    created.flow_tag = "APITEST-TAG-ONE"
    created.device_type = "nat"
    created.country = "GR"
    updated = client.tags.update(created)
    pretty_print(updated)
    print()

    print("### GET")
    got = client.tags.get(updated.id)
    pretty_print(got)
    print()

    print("### DELETE")
    deleted = client.tags.delete(updated.id)
    print(deleted)
    print()


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET ALL")
    tags = client.tags.get_all()
    pretty_print(tags)


if __name__ == "__main__":
    run_crud()
    run_list()
