# pylint: disable=redefined-outer-name
"""
Examples of using the typed devices API
"""

import logging

from examples.utils import pretty_print
from kentik_api import (
    AuthenticationProtocol,
    CDNAttribute,
    Device,
    DeviceSubtype,
    Interface,
    KentikAPI,
    PrivacyProtocol,
    SNMPv3Conf,
)
from kentik_api.public.types import ID
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud_router() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE DEVICE")
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
        plan_id=ID("11466"),
        site_id=ID("8483"),
        minimize_snmp=False,
        device_snmp_v3_conf=snmp_v3_conf,
        device_bgp_flowspec=True,
    ).with_bgp_type_device(
        device_bgp_neighbor_ip="127.0.0.42",
        device_bgp_neighbor_asn="77",
        device_bgp_password="bgp-optional-password",
    )
    created_device = client.devices.create(device)
    pretty_print(created_device)
    print()

    print("### UPDATE DEVICE")
    created_device.device_description = "updated description"
    created_device.sending_ips = ["128.0.0.15", "128.0.0.16"]
    created_device.device_sample_rate = 10
    created_device.device_bgp_neighbor_asn = "88"
    updated_device = client.devices.update(created_device)
    pretty_print(updated_device)
    print()

    print("### CREATE INTERFACE")
    interface = Interface(
        device_id=created_device.id,
        snmp_id=ID("2"),
        snmp_speed=15,
        interface_description="testapi-interface",
    )
    created_interface = client.devices.interfaces.create(interface)
    pretty_print(created_interface)
    print()

    print("### UPDATE INTERFACE")
    created_interface.snmp_speed = 24
    updated_interface = client.devices.interfaces.update(created_interface)
    pretty_print(updated_interface)
    print()

    print("### GET DEVICE")
    got = client.devices.get(updated_device.id)
    pretty_print(got)
    print()

    print("### DELETE INTERFACE")
    deleted = client.devices.interfaces.delete(created_interface.device_id, created_interface.id)
    print(deleted)
    print()

    print("### DELETE DEVICE")
    deleted = client.devices.delete(updated_device.id)  # archive
    deleted = client.devices.delete(updated_device.id)  # delete
    print(deleted)
    print()


def run_crud_dns() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE")
    device = Device.new_dns(
        device_name="testapi_dns-aws_subnet_bgp_other_device",
        device_subtype=DeviceSubtype.aws_subnet,
        cdn_attr=CDNAttribute.yes,
        device_sample_rate=1,
        plan_id=ID("11466"),
        site_id=ID("8483"),
        device_bgp_flowspec=True,
    )

    created = client.devices.create(device)
    pretty_print(created)
    print()

    print("### UPDATE")
    created.device_description = "updated description"
    created.cdn_attr = CDNAttribute.no
    created.device_sample_rate = 10
    created.device_bgp_flowspec = False
    updated = client.devices.update(created)
    pretty_print(updated)
    print()

    # first make sure the label ids exist!
    # print("### APPLY LABELS")
    # label_ids = [3011, 3012]
    # labels = client.devices.apply_labels(updated.id, label_ids)
    # pretty_print(labels)
    # print()

    print("### GET")
    got = client.devices.get(updated.id)
    pretty_print(got)
    print()

    print("### DELETE")
    deleted = client.devices.delete(updated.id)  # archive
    deleted = client.devices.delete(updated.id)  # delete
    print(deleted)
    print()


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET ALL")
    devices = client.devices.get_all()
    pretty_print(devices)
    print()


if __name__ == "__main__":
    run_crud_router()
    run_crud_dns()
    run_list()
