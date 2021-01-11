# pylint: disable=redefined-outer-name
"""
Examples of using the typed devices API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import (
    KentikAPI,
    Device,
    SNMPv3Conf,
    AuthenticationProtocol,
    PrivacyProtocol,
    DeviceSubtype,
    CDNAttribute,
)


logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud_router() -> None:
    """
    Expected response is like:

    ### CREATE
    {'plan_id': None, 'site_id': None, 'device_description': 'testapi router with full config', 'device_sample_rate': '1', 'sending_ips': ['128.0.0.10'], 'device_snmp_ip': '127.0.0.1', 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.device: 'device'>, 'device_bgp_neighbor_ip': '127.0.0.42', 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': '77', 'device_bgp_flowspec': True, 'device_bgp_password': '******************ord', 'use_bgp_device_id': None, 'device_snmp_v3_conf': SNMPv3Conf(user_name='John', authentication_protocol=<AuthenticationProtocol.md5: 'MD5'>, authentication_passphrase='Auth_Pass', privacy_protocol=<PrivacyProtocol.des: 'DES'>, privacy_passphrase='******ass'), 'cdn_attr': None, '_id': 78619, '_device_name': 'testapi_router_router_full_postman', '_device_type': <DeviceType.router: 'router'>, '_device_subtype': <DeviceSubtype.router: 'router'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2021-01-08T14:15:48.378Z', '_updated_date': '2021-01-08T14:15:48.378Z', '_bgp_peer_ip4': '208.76.14.223', '_bgp_peer_ip6': '2620:129:1:2::1', '_plan': Plan(id=11466, company_id=None, name=None, description=None, active=None, max_devices=None, max_fps=None, bgp_enabled=None, fast_retention=None, full_retention=None, cdate=None, edate=None, max_bigdata_fps=None, deviceTypes=[], devices=[], metadata=None), '_site': <kentik_api.public.site.Site object at 0x7f7a878fea30>, '_labels': [], '_all_interfaces': []}

    ### UPDATE
    {'plan_id': None, 'site_id': None, 'device_description': 'updated description', 'device_sample_rate': '10', 'sending_ips': ['128.0.0.15', '128.0.0.16'], 'device_snmp_ip': '127.0.0.1', 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.device: 'device'>, 'device_bgp_neighbor_ip': '127.0.0.42', 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': '88', 'device_bgp_flowspec': True, 'device_bgp_password': '******************ord', 'use_bgp_device_id': None, 'device_snmp_v3_conf': SNMPv3Conf(user_name='John', authentication_protocol=<AuthenticationProtocol.md5: 'MD5'>, authentication_passphrase='Auth_Pass', privacy_protocol=<PrivacyProtocol.des: 'DES'>, privacy_passphrase='******ass'), 'cdn_attr': None, '_id': 78619, '_device_name': 'testapi_router_router_full_postman', '_device_type': <DeviceType.router: 'router'>, '_device_subtype': <DeviceSubtype.router: 'router'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2021-01-08T14:15:48.378Z', '_updated_date': '2021-01-08T14:15:49.250Z', '_bgp_peer_ip4': '208.76.14.223', '_bgp_peer_ip6': '2620:129:1:2::1', '_plan': Plan(id=11466, company_id=None, name=None, description=None, active=None, max_devices=None, max_fps=None, bgp_enabled=None, fast_retention=None, full_retention=None, cdate=None, edate=None, max_bigdata_fps=None, deviceTypes=[], devices=[], metadata=None), '_site': <kentik_api.public.site.Site object at 0x7f7a878fe7c0>, '_labels': [], '_all_interfaces': []}

    ### GET
    {'plan_id': None, 'site_id': None, 'device_description': 'updated description', 'device_sample_rate': '10', 'sending_ips': ['128.0.0.15', '128.0.0.16'], 'device_snmp_ip': '127.0.0.1', 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.device: 'device'>, 'device_bgp_neighbor_ip': '127.0.0.42', 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': '88', 'device_bgp_flowspec': True, 'device_bgp_password': '******************ord', 'use_bgp_device_id': None, 'device_snmp_v3_conf': SNMPv3Conf(user_name='John', authentication_protocol=<AuthenticationProtocol.md5: 'MD5'>, authentication_passphrase='Auth_Pass', privacy_protocol=<PrivacyProtocol.des: 'DES'>, privacy_passphrase='******ass'), 'cdn_attr': None, '_id': 78619, '_device_name': 'testapi_router_router_full_postman', '_device_type': <DeviceType.router: 'router'>, '_device_subtype': <DeviceSubtype.router: 'router'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2021-01-08T14:15:48.378Z', '_updated_date': '2021-01-08T14:15:49.250Z', '_bgp_peer_ip4': '208.76.14.223', '_bgp_peer_ip6': '2620:129:1:2::1', '_plan': Plan(id=11466, company_id=74333, name='Free Trial Plan', description='Your Free Trial includes 6 devices at a maximum of 1000 fps each. Please contact sales@kentik.com for trials of higher flow rates or additional devices.', active=True, max_devices=6, max_fps=1000, bgp_enabled=True, fast_retention=30, full_retention=30, cdate='2020-09-03T08:41:57.489Z', edate='2020-09-03T08:41:57.489Z', max_bigdata_fps=30, deviceTypes=[], devices=[], metadata={}), '_site': <kentik_api.public.site.Site object at 0x7f7a878fe610>, '_labels': [], '_all_interfaces': []}

    ### DELETE
    True
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE")
    snmp_v3_conf = (
        SNMPv3Conf.new(user_name="John")
        .with_authentication(protocol=AuthenticationProtocol.md5, passphrase="Auth_Pass")
        .with_privacy(protocol=PrivacyProtocol.des, passphrase="Priv_Pass")
    )
    device = Device.new_router(
        device_name="testapi_router-router_full_postman",
        device_subtype=DeviceSubtype.router,
        sending_ips=["128.0.0.10"],
        device_sample_rate=1,
        device_description="testapi router with full config",
        device_snmp_ip="127.0.0.1",
        plan_id=11466,
        site_id=8483,
        minimize_snmp=False,
        device_snmp_v3_conf=snmp_v3_conf,
        device_bgp_flowspec=True,
    ).with_bgp_type_device(
        device_bgp_neighbor_ip="127.0.0.42",
        device_bgp_neighbor_asn="77",
        device_bgp_password="bgp-optional-password",
    )
    created = client.devices.create(device)
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.device_description = "updated description"
    created.sending_ips = ["128.0.0.15", "128.0.0.16"]
    created.device_sample_rate = 10
    created.device_bgp_neighbor_asn = "88"
    updated = client.devices.update(created)
    print(updated.__dict__)
    print()

    # first make sure the label ids exist!
    # print("### APPLY LABELS")
    # label_ids = [3011, 3012]
    # labels = client.devices.apply_labels(updated.id, label_ids)
    # print(labels.__dict__)
    # print()

    print("### GET")
    got = client.devices.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.devices.delete(updated.id)  # archive
    deleted = client.devices.delete(updated.id)  # delete
    print(deleted)


def run_crud_dns() -> None:
    """
    Expected response is like:

    ### CREATE
    {'plan_id': None, 'site_id': None, 'device_description': None, 'device_sample_rate': '1', 'sending_ips': [], 'device_snmp_ip': None, 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.none: 'none'>, 'device_bgp_neighbor_ip': None, 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': None, 'device_bgp_flowspec': False, 'device_bgp_password': None, 'use_bgp_device_id': None, 'device_snmp_v3_conf': None, 'cdn_attr': <CDNAttribute.yes: 'Y'>, '_id': 78621, '_device_name': 'testapi_dns_aws_subnet_bgp_other_device', '_device_type': <DeviceType.host_nprobe_dns_www: 'host-nprobe-dns-www'>, '_device_subtype': <DeviceSubtype.aws_subnet: 'aws_subnet'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2021-01-08T14:33:35.193Z', '_updated_date': '2021-01-08T14:33:35.193Z', '_bgp_peer_ip4': None, '_bgp_peer_ip6': None, '_plan': Plan(id=11466, company_id=None, name=None, description=None, active=None, max_devices=None, max_fps=None, bgp_enabled=None, fast_retention=None, full_retention=None, cdate=None, edate=None, max_bigdata_fps=None, deviceTypes=[], devices=[], metadata=None), '_site': <kentik_api.public.site.Site object at 0x7f450e47b580>, '_labels': [], '_all_interfaces': []}

    ### UPDATE
    {'plan_id': None, 'site_id': None, 'device_description': 'updated description', 'device_sample_rate': '10', 'sending_ips': [], 'device_snmp_ip': None, 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.none: 'none'>, 'device_bgp_neighbor_ip': None, 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': None, 'device_bgp_flowspec': False, 'device_bgp_password': None, 'use_bgp_device_id': None, 'device_snmp_v3_conf': None, 'cdn_attr': <CDNAttribute.no: 'N'>, '_id': 78621, '_device_name': 'testapi_dns_aws_subnet_bgp_other_device', '_device_type': <DeviceType.host_nprobe_dns_www: 'host-nprobe-dns-www'>, '_device_subtype': <DeviceSubtype.aws_subnet: 'aws_subnet'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2021-01-08T14:33:35.193Z', '_updated_date': '2021-01-08T14:33:36.037Z', '_bgp_peer_ip4': None, '_bgp_peer_ip6': None, '_plan': Plan(id=11466, company_id=None, name=None, description=None, active=None, max_devices=None, max_fps=None, bgp_enabled=None, fast_retention=None, full_retention=None, cdate=None, edate=None, max_bigdata_fps=None, deviceTypes=[], devices=[], metadata=None), '_site': <kentik_api.public.site.Site object at 0x7f450e47b9d0>, '_labels': [], '_all_interfaces': []}

    ### GET
    {'plan_id': None, 'site_id': None, 'device_description': 'updated description', 'device_sample_rate': '10', 'sending_ips': [], 'device_snmp_ip': None, 'device_snmp_community': '', 'minimize_snmp': False, 'device_bgp_type': <DeviceBGPType.none: 'none'>, 'device_bgp_neighbor_ip': None, 'device_bgp_neighbor_ip6': None, 'device_bgp_neighbor_asn': None, 'device_bgp_flowspec': False, 'device_bgp_password': None, 'use_bgp_device_id': None, 'device_snmp_v3_conf': None, 'cdn_attr': <CDNAttribute.no: 'N'>, '_id': 78621, '_device_name': 'testapi_dns_aws_subnet_bgp_other_device', '_device_type': <DeviceType.host_nprobe_dns_www: 'host-nprobe-dns-www'>, '_device_subtype': <DeviceSubtype.aws_subnet: 'aws_subnet'>, '_device_status': 'V', '_device_flow_type': 'auto', '_company_id': '74333', '_snmp_last_updated': None, '_created_date': '2021-01-08T14:33:35.193Z', '_updated_date': '2021-01-08T14:33:36.037Z', '_bgp_peer_ip4': None, '_bgp_peer_ip6': None, '_plan': Plan(id=11466, company_id=74333, name='Free Trial Plan', description='Your Free Trial includes 6 devices at a maximum of 1000 fps each. Please contact sales@kentik.com for trials of higher flow rates or additional devices.', active=True, max_devices=6, max_fps=1000, bgp_enabled=True, fast_retention=30, full_retention=30, cdate='2020-09-03T08:41:57.489Z', edate='2020-09-03T08:41:57.489Z', max_bigdata_fps=30, deviceTypes=[], devices=[], metadata={}), '_site': <kentik_api.public.site.Site object at 0x7f450e47baf0>, '_labels': [], '_all_interfaces': []}

    ### DELETE
    True
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE")
    device = Device.new_dns(
        device_name="testapi_dns-aws_subnet_bgp_other_device",
        device_subtype=DeviceSubtype.aws_subnet,
        cdn_attr=CDNAttribute.yes,
        device_sample_rate=1,
        plan_id=11466,
        site_id=8483,
        device_bgp_flowspec=True,
    )

    created = client.devices.create(device)
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.device_description = "updated description"
    created.cdn_attr = CDNAttribute.no
    created.device_sample_rate = 10
    created.device_bgp_flowspec = False
    updated = client.devices.update(created)
    print(updated.__dict__)
    print()

    # first make sure the label ids exist!
    # print("### APPLY LABELS")
    # label_ids = [3011, 3012]
    # labels = client.devices.apply_labels(updated.id, label_ids)
    # print(labels.__dict__)
    # print()

    print("### GET")
    got = client.devices.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.devices.delete(updated.id)  # archive
    deleted = client.devices.delete(updated.id)  # delete
    print(deleted)


def run_list() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)
    devices = client.devices.get_all()
    for d in devices:
        print(d.__dict__, "\n")


if __name__ == "__main__":
    run_crud_router()
    # run_crud_dns()
    # run_list()
