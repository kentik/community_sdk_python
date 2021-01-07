# pylint: disable=redefined-outer-name
"""
Examples of using the typed devices API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, Device


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

    ### UPDATE

    ### GET
    {'plan_id': None, 'site_id': None, 'device_name': 'testapi_dns_minimal_1', 'device_description': 'testapi dns with minimal config', 'device_sample_rate': '1', 'sending_ips': [], 'device_snmp_ip': None, 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.none: 'none'>, 'device_bgp_neighbor_ip': None, 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': None, 'device_bgp_flowspec': False, 'device_bgp_password': None, 'use_bgp_device_id': None, 'device_snmp_v3_conf': None, 'cdn_attr': <CDNAttribute.yes: 'Y'>, '_id': 77720, '_device_type': <DeviceType.host_nprobe_dns_www: 'host-nprobe-dns-www'>, '_device_subtype': <DeviceSubtype.aws_subnet: 'aws_subnet'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2020-12-17T12:53:01.025Z', '_updated_date': '2020-12-23T18:33:55.125Z', '_bgp_peer_ip4': None, '_bgp_peer_ip6': None, '_plan': Plan(id=11466, company_id=74333, name='Free Trial Plan', description='Your Free Trial includes 6 devices at a maximum of 1000 fps each. Please contact sales@kentik.com for trials of higher flow rates or additional devices.', active=True, max_devices=6, max_fps=1000, bgp_enabled=True, fast_retention=30, full_retention=30, cdate='2020-09-03T08:41:57.489Z', edate='2020-09-03T08:41:57.489Z', max_bigdata_fps=30, deviceTypes=[], devices=[], metadata={}), '_site': <kentik_api.public.site.Site object at 0x7f03c43fac10>, '_labels': [], '_all_interfaces': []}

    ### DELETE
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    # print("### CREATE")
    # device = Device(...)
    # created = client.devices.create(device)
    # print(created.__dict__)
    # print()

    # print("### UPDATE")
    # created.device_description = "updated description"
    # updated = client.devices.update(created)
    # print(updated.__dict__)
    # print()

    print("### GET")
    # router 77865
    # dns 77720
    got = client.devices.get(77720)
    print(got.__dict__)
    print()

    # print("### DELETE")
    # deleted = client.devices.delete(updated.id)
    # print(deleted)


# def run_list() -> None:
#     email, token = get_auth_email_token()
#     client = KentikAPI(email, token)
#     labels = client.devices.get_all()
#     for d in devices:
#         print(d.__dict__)


if __name__ == "__main__":
    run_crud()
    # run_list()
