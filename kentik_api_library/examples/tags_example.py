# pylint: disable=redefined-outer-name
"""
Examples of using the typed tags API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, Tag

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud() -> None:
    """
    Expected response is like:

    ### CREATE
    {'flow_tag': 'APITEST-TAG-1', 'device_name': '192.168.5.100,device1', 'interface_name': 'interface1,interface2', 'addr': '192.168.0.1/32,192.168.0.2/32', 'port': '9000,9001', 'tcp_flags': '7', 'protocol': '6,17', 'asn': '101,102,103', 'nexthop': '192.168.7.1/32,192.168.7.2/32', 'nexthop_asn': '51,52,53', 'bgp_aspath': '201,202,203', 'bgp_community': '301,302,303', 'device_type': 'router,switch', 'site': 'site1,site2', 'lasthop_as_name': 'as1,as2,as3', 'nexthop_as_name': 'as51,as52,as53', 'mac': 'FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF', 'country': 'ES,IT', 'vlans': '4001,4002,4003', '_id': 1508133144, '_company_id': '74333', '_addr_count': 2, '_user_id': 144319, '_mac_count': 2, '_edited_by': 'john.doe@acme.com', '_created_date': '2020-12-10T15:46:10.149526Z', '_updated_date': '2020-12-10T15:46:10.149526Z'}

    ### UPDATE
    {'flow_tag': 'APITEST-TAG-ONE', 'device_name': '192.168.5.100,device1', 'interface_name': 'interface1,interface2', 'addr': '192.168.0.1/32,192.168.0.2/32', 'port': '9000,9001', 'tcp_flags': '7', 'protocol': '6,17', 'asn': '101,102,103', 'nexthop': '192.168.7.1/32,192.168.7.2/32', 'nexthop_asn': '51,52,53', 'bgp_aspath': '201,202,203', 'bgp_community': '301,302,303', 'device_type': 'nat', 'site': 'site1,site2', 'lasthop_as_name': 'as1,as2,as3', 'nexthop_as_name': 'as51,as52,as53', 'mac': 'FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF', 'country': 'GR', 'vlans': '4001,4002,4003', '_id': 1508133144, '_company_id': '74333', '_addr_count': 2, '_user_id': 144319, '_mac_count': 2, '_edited_by': 'john.doe@acme.com', '_created_date': '2020-12-10T15:46:10.149526Z', '_updated_date': '2020-12-10T15:46:10.922118Z'}

    ### GET
    {'flow_tag': 'APITEST-TAG-ONE', 'device_name': '192.168.5.100,device1', 'interface_name': 'interface1,interface2', 'addr': '192.168.0.1/32,192.168.0.2/32', 'port': '9000,9001', 'tcp_flags': '7', 'protocol': '6,17', 'asn': '101,102,103', 'nexthop': '192.168.7.1/32,192.168.7.2/32', 'nexthop_asn': '51,52,53', 'bgp_aspath': '201,202,203', 'bgp_community': '301,302,303', 'device_type': 'nat', 'site': 'site1,site2', 'lasthop_as_name': 'as1,as2,as3', 'nexthop_as_name': 'as51,as52,as53', 'mac': 'FF:FF:FF:FF:FF:FE,FF:FF:FF:FF:FF:FF', 'country': 'GR', 'vlans': '4001,4002,4003', '_id': 1508133144, '_company_id': '74333', '_addr_count': 2, '_user_id': 144319, '_mac_count': 2, '_edited_by': 'john.doe@acme.com', '_created_date': '2020-12-10T15:46:10.149526Z', '_updated_date': '2020-12-10T15:46:10.922118Z'}

    ### DELETE
    True
    """

    email, token = get_auth_email_token()
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
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.flow_tag = "APITEST-TAG-ONE"
    created.device_type = "nat"
    created.country = "GR"
    updated = client.tags.update(created)
    print(updated.__dict__)
    print()

    print("### GET")
    got = client.tags.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.tags.delete(updated.id)
    print(deleted)


def run_list() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)
    tags = client.tags.get_all()
    for t in tags:
        print(t.__dict__)


if __name__ == "__main__":
    run_crud()
    # run_list()
