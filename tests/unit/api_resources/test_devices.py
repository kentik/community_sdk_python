from datetime import datetime, timezone
from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.devices_api import DevicesAPI
from kentik_api.public.device import (
    AuthenticationProtocol,
    CDNAttribute,
    Device,
    DeviceBGPType,
    DeviceSubtype,
    DeviceType,
    Interface,
    PrivacyProtocol,
    SecondaryIP,
    SNMPv3Conf,
    VRFAttributes,
)
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_device_router_success() -> None:
    # given
    create_response_payload = """
    {
        "device": {
            "id": "42",
            "company_id": "74333",
            "device_name": "testapi_router_router_full",
            "device_type": "router",
            "device_status": "V",
            "device_description": "testapi router with full config",
            "site": {
                "id": 8483,
                "site_name": null,
                "lat": null,
                "lon": null,
                "company_id": null
            },
            "plan": {
                "active": null,
                "bgp_enabled": null,
                "cdate": null,
                "company_id": null,
                "description": null,
                "deviceTypes": [],
                "devices": [],
                "edate": null,
                "fast_retention": null,
                "full_retention": null,
                "id": 11466,
                "max_bigdata_fps": null,
                "max_devices": null,
                "max_fps": null,
                "name": null,
                "metadata": null
            },
            "labels": [],
            "all_interfaces": [],
            "device_flow_type": "auto",
            "device_sample_rate": "1",
            "sending_ips": [
                "128.0.0.10"
            ],
            "device_snmp_ip": "127.0.0.1",
            "device_snmp_community": "",
            "minimize_snmp": false,
            "device_bgp_type": "device",
            "device_bgp_neighbor_ip": "127.0.0.2",
            "device_bgp_neighbor_ip6": null,
            "device_bgp_neighbor_asn": "77",
            "device_bgp_flowspec": true,
            "device_bgp_password": "******************ord",
            "use_bgp_device_id": null,
            "custom_columns": "",
            "custom_column_data": [],
            "device_chf_client_port": null,
            "device_chf_client_protocol": null,
            "device_chf_interface": null,
            "device_agent_type": null,
            "max_flow_rate": null,
            "max_big_flow_rate": null,
            "device_proxy_bgp": "",
            "device_proxy_bgp6": "",
            "created_date": "2021-01-08T08:17:07.338Z",
            "updated_date": "2021-01-08T08:17:07.338Z",
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationProtocol": "MD5",
                "AuthenticationPassphrase": "Auth_Pass",
                "PrivacyProtocol": "DES",
                "PrivacyPassphrase": "******ass"
            },
            "bgpPeerIP4": "208.76.14.223",
            "bgpPeerIP6": "2620:129:1:2::1",
            "snmp_last_updated": null,
            "device_subtype": "router"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    devices_api = DevicesAPI(connector)

    # when
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
        plan_id=ID(11466),
        site_id=ID(8483),
        minimize_snmp=False,
        device_snmp_v3_conf=snmp_v3_conf,
        device_bgp_flowspec=True,
    ).with_bgp_type_device(
        device_bgp_neighbor_ip="127.0.0.2",
        device_bgp_neighbor_asn="77",
        device_bgp_password="bgp-optional-password",
    )
    created = devices_api.create(device)

    # then request properly formed
    assert connector.last_url_path == "/device"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload == {
        "device": {
            "device_name": "testapi_router-router_full_postman",
            "device_type": "router",
            "device_subtype": "router",
            "sending_ips": ["128.0.0.10"],
            "device_sample_rate": "1",
            "device_description": "testapi router with full config",
            "device_snmp_ip": "127.0.0.1",
            "plan_id": 11466,
            "site_id": 8483,
            "minimize_snmp": False,
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationProtocol": "MD5",
                "AuthenticationPassphrase": "Auth_Pass",
                "PrivacyProtocol": "DES",
                "PrivacyPassphrase": "Priv_Pass",
            },
            "device_bgp_type": "device",
            "device_bgp_neighbor_asn": "77",
            "device_bgp_neighbor_ip": "127.0.0.2",
            "device_bgp_password": "bgp-optional-password",
            "device_bgp_flowspec": True,
        }
    }

    # and response properly parsed
    assert created.id == ID(42)
    assert created.company_id == ID(74333)
    assert created.device_name == "testapi_router_router_full"
    assert created.device_type == DeviceType.router
    assert created.device_status == "V"
    assert created.device_description == "testapi router with full config"
    assert created.site is not None
    assert created.site.id == ID(8483)
    assert created.site.site_name is None
    assert created.site.latitude is None
    assert created.site.longitude is None
    assert created.site.company_id is None
    assert created.plan.active is None
    assert created.plan.bgp_enabled is None
    assert created.plan.created_date is None
    assert created.plan.company_id is None
    assert created.plan.description is None
    assert created.plan.device_types == []
    assert created.plan.devices == []
    assert created.plan.updated_date is None
    assert created.plan.fast_retention is None
    assert created.plan.full_retention is None
    assert created.plan.id == ID(11466)
    assert created.plan.max_bigdata_fps is None
    assert created.plan.max_devices is None
    assert created.plan.max_fps is None
    assert created.plan.name is None
    assert created.plan.metadata is None
    assert len(created.labels) == 0
    assert len(created.interfaces) == 0
    assert created.device_flow_type == "auto"
    assert created.device_sample_rate == 1
    assert created.sending_ips is not None
    assert len(created.sending_ips) == 1
    assert created.sending_ips[0] == "128.0.0.10"
    assert created.device_snmp_ip == "127.0.0.1"
    assert created.device_snmp_community == ""
    assert created.minimize_snmp == False
    assert created.device_bgp_type == DeviceBGPType.device
    assert created.device_bgp_neighbor_ip == "127.0.0.2"
    assert created.device_bgp_neighbor_ip6 is None
    assert created.device_bgp_neighbor_asn == "77"
    assert created.device_bgp_flowspec == True
    assert created.device_bgp_password == "******************ord"
    assert created.use_bgp_device_id is None
    assert created.created_date == "2021-01-08T08:17:07.338Z"
    assert created.updated_date == "2021-01-08T08:17:07.338Z"
    assert created.device_snmp_v3_conf is not None
    assert created.device_snmp_v3_conf.user_name == "John"
    assert created.device_snmp_v3_conf.authentication_protocol == AuthenticationProtocol.md5
    assert created.device_snmp_v3_conf.authentication_passphrase == "Auth_Pass"
    assert created.device_snmp_v3_conf.privacy_protocol == PrivacyProtocol.des
    assert created.device_snmp_v3_conf.privacy_passphrase == "******ass"
    assert created.bgp_peer_ip4 == "208.76.14.223"
    assert created.bgp_peer_ip6 == "2620:129:1:2::1"
    assert created.snmp_last_updated is None
    assert created.device_subtype == DeviceSubtype.router


def test_create_device_dns_success() -> None:
    # given
    create_response_payload = """
    {
        "device": {
            "id": "43",
            "company_id": "74333",
            "device_name": "testapi_dns_aws_subnet_bgp_other_device",
            "device_type": "host-nprobe-dns-www",
            "device_status": "V",
            "device_description": "testapi dns with minimal config",
            "site": {
                "id": 8483,
                "site_name": null,
                "lat": null,
                "lon": null,
                "company_id": null
            },
            "plan": {
                "active": null,
                "bgp_enabled": null,
                "cdate": null,
                "company_id": null,
                "description": null,
                "deviceTypes": [],
                "devices": [],
                "edate": null,
                "fast_retention": null,
                "full_retention": null,
                "id": 11466,
                "max_bigdata_fps": null,
                "max_devices": null,
                "max_fps": null,
                "name": null,
                "metadata": null
            },
            "labels": [],
            "all_interfaces": [],
            "device_flow_type": "auto",
            "device_sample_rate": "1",
            "sending_ips": [],
            "device_snmp_ip": null,
            "device_snmp_community": "",
            "minimize_snmp": false,
            "device_bgp_type": "other_device",
            "use_bgp_device_id": 42,
            "device_bgp_flowspec": true,
            "custom_columns": "",
            "custom_column_data": [],
            "device_chf_client_port": null,
            "device_chf_client_protocol": null,
            "device_chf_interface": null,
            "device_agent_type": null,
            "max_flow_rate": null,
            "max_big_flow_rate": null,
            "device_proxy_bgp": "",
            "device_proxy_bgp6": "",
            "created_date": "2021-01-08T11:10:33.465Z",
            "updated_date": "2021-01-08T11:10:33.465Z",
            "device_snmp_v3_conf": null,
            "cdn_attr": "Y",
            "bgpPeerIP4": "208.76.14.223",
            "bgpPeerIP6": "2620:129:1:2::1",
            "snmp_last_updated": null,
            "device_subtype": "aws_subnet"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    devices_api = DevicesAPI(connector)

    # when
    device = Device.new_dns(
        device_name="testapi_dns-aws_subnet_bgp_other_device",
        device_subtype=DeviceSubtype.aws_subnet,
        cdn_attr=CDNAttribute.yes,
        device_sample_rate=1,
        device_description="testapi dns with minimal config",
        plan_id=ID(11466),
        site_id=ID(8483),
        device_bgp_flowspec=True,
    ).with_bgp_type_other_device(use_bgp_device_id=ID(42))
    created = devices_api.create(device)

    # then request properly formed
    assert connector.last_url_path == "/device"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload == {
        "device": {
            "device_name": "testapi_dns-aws_subnet_bgp_other_device",
            "device_type": "host-nprobe-dns-www",
            "device_subtype": "aws_subnet",
            "cdn_attr": "Y",
            "device_sample_rate": "1",
            "device_description": "testapi dns with minimal config",
            "plan_id": 11466,
            "site_id": 8483,
            "device_bgp_type": "other_device",
            "use_bgp_device_id": 42,
            "device_bgp_flowspec": True,
        }
    }

    # and response properly parsed
    assert created.id == ID(43)
    assert created.company_id == ID(74333)
    assert created.device_name == "testapi_dns_aws_subnet_bgp_other_device"
    assert created.device_type == DeviceType.host_nprobe_dns_www
    assert created.device_status == "V"
    assert created.device_description == "testapi dns with minimal config"
    assert created.site is not None
    assert created.site.id == ID(8483)
    assert created.site.site_name is None
    assert created.site.latitude is None
    assert created.site.longitude is None
    assert created.site.company_id is None
    assert created.plan.active is None
    assert created.plan.bgp_enabled is None
    assert created.plan.created_date is None
    assert created.plan.company_id is None
    assert created.plan.description is None
    assert created.plan.device_types == []
    assert created.plan.devices == []
    assert created.plan.updated_date is None
    assert created.plan.fast_retention is None
    assert created.plan.full_retention is None
    assert created.plan.id == ID(11466)
    assert created.plan.max_bigdata_fps is None
    assert created.plan.max_devices is None
    assert created.plan.max_fps is None
    assert created.plan.name is None
    assert created.plan.metadata is None
    assert len(created.labels) == 0
    assert len(created.interfaces) == 0
    assert created.device_flow_type == "auto"
    assert created.device_sample_rate == 1
    assert created.sending_ips == []
    assert created.device_snmp_ip is None
    assert created.device_snmp_community == ""
    assert created.minimize_snmp == False
    assert created.device_bgp_type == DeviceBGPType.other_device
    assert created.device_bgp_flowspec == True
    assert created.use_bgp_device_id == ID(42)
    assert created.created_date == "2021-01-08T11:10:33.465Z"
    assert created.updated_date == "2021-01-08T11:10:33.465Z"
    assert created.device_snmp_v3_conf is None
    assert created.bgp_peer_ip4 == "208.76.14.223"
    assert created.bgp_peer_ip6 == "2620:129:1:2::1"
    assert created.snmp_last_updated is None
    assert created.device_subtype == DeviceSubtype.aws_subnet


def test_get_device_router_success() -> None:
    # given
    get_response_payload = """
    {
        "device": {
            "id": "42",
            "company_id": "74333",
            "device_name": "testapi_router_full_1",
            "device_type": "router",
            "device_status": "V",
            "device_description": "testapi router with full config",
            "site": {
                "id": 8483,
                "site_name": "marina gdańsk",
                "lat": 54.348972,
                "lon": 18.659791,
                "company_id": 74333
            },
            "plan": {
                "active": true,
                "bgp_enabled": true,
                "cdate": "2020-09-03T08:41:57.489Z",
                "company_id": 74333,
                "description": "Your Free Trial includes 6 devices (...)",
                "deviceTypes": [],
                "devices": [],
                "edate": "2020-09-03T08:41:57.489Z",
                "fast_retention": 30,
                "full_retention": 30,
                "id": 11466,
                "max_bigdata_fps": 30,
                "max_devices": 6,
                "max_fps": 1000,
                "name": "Free Trial Plan",
                "metadata": {}
            },
            "labels": [
                        {
                            "id": 2590,
                            "name": "AWS: terraform-demo-aws",
                            "description": null,
                            "edate": "2020-10-05T15:28:00.276Z",
                            "cdate": "2020-10-05T15:28:00.276Z",
                            "user_id": "133210",
                            "company_id": "74333",
                            "color": "#5340A5",
                            "order": null,
                            "_pivot_device_id": "77715",
                            "_pivot_label_id": "2590"
                        },
                        {
                            "id": 2751,
                            "name": "GCP: traffic-generator-gcp",
                            "description": null,
                            "edate": "2020-11-20T12:54:49.575Z",
                            "cdate": "2020-11-20T12:54:49.575Z",
                            "user_id": "136885",
                            "company_id": "74333",
                            "color": "#5289D9",
                            "order": null,
                            "_pivot_device_id": "77373",
                            "_pivot_label_id": "2751"
                        }
                    ],
            "all_interfaces": [
                {
                    "interface_description": "testapi-interface-1",
                    "initial_snmp_speed": null,
                    "device_id": "42",
                    "snmp_speed": "75"
                },
                {
                    "interface_description": "testapi-interface-2",
                    "initial_snmp_speed": "7",
                    "device_id": "42",
                    "snmp_speed": "7"
                }
            ],
            "device_flow_type": "auto",
            "device_sample_rate": "1001",
            "sending_ips": [
                "128.0.0.11",
                "128.0.0.12"
            ],
            "device_snmp_ip": "129.0.0.1",
            "device_snmp_community": "",
            "minimize_snmp": false,
            "device_bgp_type": "device",
            "device_bgp_neighbor_ip": "127.0.0.1",
            "device_bgp_neighbor_ip6": null,
            "device_bgp_neighbor_asn": "11",
            "device_bgp_flowspec": true,
            "device_bgp_password": "*********ass",
            "use_bgp_device_id": null,
            "custom_columns": "",
            "custom_column_data": [],
            "device_chf_client_port": null,
            "device_chf_client_protocol": null,
            "device_chf_interface": null,
            "device_agent_type": null,
            "max_flow_rate": 1000,
            "max_big_flow_rate": 30,
            "device_proxy_bgp": "",
            "device_proxy_bgp6": "",
            "created_date": "2020-12-17T08:24:45.074Z",
            "updated_date": "2020-12-17T08:24:45.074Z",
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationProtocol": "MD5",
                "AuthenticationPassphrase": "john_md5_pass",
                "PrivacyProtocol": "DES",
                "PrivacyPassphrase": "**********ass"
            },
            "bgpPeerIP4": "208.76.14.223",
            "bgpPeerIP6": "2620:129:1:2::1",
            "snmp_last_updated": null,
            "device_subtype": "router"
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    device = devices_api.get(device_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert device.id == ID(42)
    assert device.company_id == ID(74333)
    assert device.device_name == "testapi_router_full_1"
    assert device.device_type == DeviceType.router
    assert device.device_status == "V"
    assert device.device_description == "testapi router with full config"
    assert device.site is not None
    assert device.site.id == ID(8483)
    assert device.site.site_name == "marina gdańsk"
    assert device.site.latitude == 54.348972
    assert device.site.longitude == 18.659791
    assert device.site.company_id == ID(74333)
    assert device.plan.active == True
    assert device.plan.bgp_enabled == True
    assert device.plan.created_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.company_id == ID(74333)
    assert device.plan.description == "Your Free Trial includes 6 devices (...)"
    assert device.plan.device_types == []
    assert device.plan.devices == []
    assert device.plan.updated_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.fast_retention == 30
    assert device.plan.full_retention == 30
    assert device.plan.id == ID(11466)
    assert device.plan.max_bigdata_fps == 30
    assert device.plan.max_devices == 6
    assert device.plan.max_fps == 1000
    assert device.plan.name == "Free Trial Plan"
    assert device.plan.metadata == {}
    assert len(device.labels) == 2
    assert device.labels[0].id == ID(2590)
    assert device.labels[0].name == "AWS: terraform-demo-aws"
    assert device.labels[0].updated_date == datetime(2020, 10, 5, 15, 28, 0, 276000, tzinfo=timezone.utc)
    assert device.labels[0].created_date == datetime(2020, 10, 5, 15, 28, 0, 276000, tzinfo=timezone.utc)
    assert device.labels[0].user_id == ID(133210)
    assert device.labels[0].company_id == ID(74333)
    assert device.labels[0].color == "#5340A5"
    assert device.labels[1].id == ID(2751)
    assert device.labels[1].name == "GCP: traffic-generator-gcp"
    assert device.labels[1].updated_date == datetime(2020, 11, 20, 12, 54, 49, 575000, tzinfo=timezone.utc)
    assert device.labels[1].created_date == datetime(2020, 11, 20, 12, 54, 49, 575000, tzinfo=timezone.utc)
    assert device.labels[1].user_id == ID(136885)
    assert device.labels[1].company_id == ID(74333)
    assert device.labels[1].color == "#5289D9"
    assert len(device.interfaces) == 2
    assert device.interfaces[0].interface_description == "testapi-interface-1"
    assert device.interfaces[0].initial_snmp_speed is None
    assert device.interfaces[0].device_id == ID(42)
    assert device.interfaces[0].snmp_speed == 75
    assert device.interfaces[1].interface_description == "testapi-interface-2"
    assert device.interfaces[1].initial_snmp_speed == 7
    assert device.interfaces[1].device_id == ID(42)
    assert device.interfaces[1].snmp_speed == 7
    assert device.device_flow_type == "auto"
    assert device.device_sample_rate == 1001
    assert device.sending_ips is not None
    assert len(device.sending_ips) == 2
    assert device.sending_ips[0] == "128.0.0.11"
    assert device.sending_ips[1] == "128.0.0.12"
    assert device.device_snmp_ip == "129.0.0.1"
    assert device.device_snmp_community == ""
    assert device.minimize_snmp == False
    assert device.device_bgp_type == DeviceBGPType.device
    assert device.device_bgp_neighbor_ip == "127.0.0.1"
    assert device.device_bgp_neighbor_ip6 is None
    assert device.device_bgp_neighbor_asn == "11"
    assert device.device_bgp_flowspec == True
    assert device.device_bgp_password == "*********ass"
    assert device.use_bgp_device_id is None
    assert device.created_date == "2020-12-17T08:24:45.074Z"
    assert device.updated_date == "2020-12-17T08:24:45.074Z"
    assert device.device_snmp_v3_conf is not None
    assert device.device_snmp_v3_conf.user_name == "John"
    assert device.device_snmp_v3_conf.authentication_protocol == AuthenticationProtocol.md5
    assert device.device_snmp_v3_conf.authentication_passphrase == "john_md5_pass"
    assert device.device_snmp_v3_conf.privacy_protocol == PrivacyProtocol.des
    assert device.device_snmp_v3_conf.privacy_passphrase == "**********ass"
    assert device.bgp_peer_ip4 == "208.76.14.223"
    assert device.bgp_peer_ip6 == "2620:129:1:2::1"
    assert device.snmp_last_updated is None
    assert device.device_subtype == DeviceSubtype.router


def test_get_device_dns_success() -> None:
    # given
    get_response_payload = """
    {
        "device": {
                "id": "43",
                "company_id": "74333",
                "device_name": "testapi_dns_minimal_1",
                "device_type": "host-nprobe-dns-www",
                "device_status": "V",
                "device_description": "testapi dns with minimal config",
                "site": {},
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "labels": [],
                "all_interfaces": [],
                "device_flow_type": "auto",
                "device_sample_rate": "1",
                "sending_ips": [],
                "device_snmp_ip": null,
                "device_snmp_community": "",
                "minimize_snmp": false,
                "device_bgp_type": "none",
                "device_bgp_neighbor_ip": null,
                "device_bgp_neighbor_ip6": null,
                "device_bgp_neighbor_asn": null,
                "device_bgp_flowspec": false,
                "device_bgp_password": null,
                "use_bgp_device_id": null,
                "custom_columns": "",
                "custom_column_data": [],
                "device_chf_client_port": null,
                "device_chf_client_protocol": null,
                "device_chf_interface": null,
                "device_agent_type": null,
                "max_flow_rate": 1000,
                "max_big_flow_rate": 30,
                "device_proxy_bgp": "",
                "device_proxy_bgp6": "",
                "created_date": "2020-12-17T12:53:01.025Z",
                "updated_date": "2020-12-17T12:53:01.025Z",
                "device_snmp_v3_conf": null,
                "cdn_attr": "Y",
                "snmp_last_updated": null,
                "device_subtype": "aws_subnet"
            }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(43)
    device = devices_api.get(device_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert device.id == ID(43)
    assert device.company_id == ID(74333)
    assert device.device_name == "testapi_dns_minimal_1"
    assert device.device_type == DeviceType.host_nprobe_dns_www
    assert device.device_status == "V"
    assert device.device_description == "testapi dns with minimal config"
    assert device.site is None
    assert device.plan.active == True
    assert device.plan.bgp_enabled == True
    assert device.plan.created_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.company_id == ID(74333)
    assert device.plan.description == "Your Free Trial includes 6 devices (...)"
    assert device.plan.device_types == []
    assert device.plan.devices == []
    assert device.plan.updated_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.fast_retention == 30
    assert device.plan.full_retention == 30
    assert device.plan.id == ID(11466)
    assert device.plan.max_bigdata_fps == 30
    assert device.plan.max_devices == 6
    assert device.plan.max_fps == 1000
    assert device.plan.name == "Free Trial Plan"
    assert device.plan.metadata == {}
    assert len(device.labels) == 0
    assert len(device.interfaces) == 0
    assert device.device_flow_type == "auto"
    assert device.device_sample_rate == 1
    assert device.sending_ips is not None
    assert len(device.sending_ips) == 0
    assert device.device_snmp_ip is None
    assert device.device_snmp_community == ""
    assert not device.minimize_snmp
    assert device.device_bgp_type == DeviceBGPType.none
    assert device.device_bgp_neighbor_ip is None
    assert device.device_bgp_neighbor_ip6 is None
    assert device.device_bgp_neighbor_asn is None
    assert not device.device_bgp_flowspec
    assert device.device_bgp_password is None
    assert device.use_bgp_device_id is None
    assert device.created_date == "2020-12-17T12:53:01.025Z"
    assert device.updated_date == "2020-12-17T12:53:01.025Z"
    assert device.device_snmp_v3_conf is None
    assert device.cdn_attr == CDNAttribute.yes
    assert device.bgp_peer_ip4 is None
    assert device.bgp_peer_ip6 is None
    assert device.snmp_last_updated is None
    assert device.device_subtype == DeviceSubtype.aws_subnet


def test_update_device_router_success() -> None:
    # given
    update_response_payload = """
    {
        "device": {
            "id": "42",
            "company_id": "74333",
            "device_name": "testapi_router_paloalto_minimal",
            "device_type": "router",
            "device_status": "V",
            "device_description": "updated description",
            "site": {
                "id": 8483,
                "site_name": null,
                "lat": null,
                "lon": null,
                "company_id": null
            },
            "plan": {
                "active": null,
                "bgp_enabled": null,
                "cdate": null,
                "company_id": null,
                "description": null,
                "deviceTypes": [],
                "devices": [],
                "edate": null,
                "fast_retention": null,
                "full_retention": null,
                "id": 11466,
                "max_bigdata_fps": null,
                "max_devices": null,
                "max_fps": null,
                "name": null,
                "metadata": null
            },
            "labels": [],
            "all_interfaces": [],
            "device_flow_type": "auto",
            "device_sample_rate": "10",
            "sending_ips": [
                "128.0.0.10",
                "128.0.0.11"
            ],
            "device_snmp_ip": "127.0.0.10",
            "device_snmp_community": "",
            "minimize_snmp": true,
            "device_bgp_type": "device",
            "device_bgp_neighbor_ip": null,
            "device_bgp_neighbor_ip6": "2001:db8:85a3:8d3:1319:8a2e:370:7348",
            "device_bgp_neighbor_asn": "77",
            "device_bgp_flowspec": true,
            "device_bgp_password": "******************ord",
            "use_bgp_device_id": null,
            "custom_columns": "",
            "custom_column_data": [],
            "device_chf_client_port": null,
            "device_chf_client_protocol": null,
            "device_chf_interface": null,
            "device_agent_type": null,
            "max_flow_rate": null,
            "max_big_flow_rate": null,
            "device_proxy_bgp": "",
            "device_proxy_bgp6": "",
            "created_date": "2021-01-08T13:02:45.733Z",
            "updated_date": "2021-01-08T13:11:57.795Z",
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationProtocol": "SHA",
                "AuthenticationPassphrase": "Auth_Pass",
                "PrivacyProtocol": "AES",
                "PrivacyPassphrase": "******ass"
            },
            "bgpPeerIP4": "208.76.14.223",
            "bgpPeerIP6": "2620:129:1:2::1",
            "snmp_last_updated": null,
            "device_subtype": "paloalto"
        }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    snmp_v3_conf = (
        SNMPv3Conf.new(user_name="John")
        .with_authentication(protocol=AuthenticationProtocol.sha, passphrase="Auth_Pass")
        .with_privacy(protocol=PrivacyProtocol.aes, passphrase="Priv_Pass")
    )
    device_id = ID(42)
    device = Device(
        id=device_id,
        sending_ips=["128.0.0.10", "128.0.0.11"],
        device_sample_rate=10,
        device_description="updated description",
        device_snmp_ip="127.0.0.10",
        plan_id=ID(11466),
        site_id=ID(8483),
        minimize_snmp=True,
        device_snmp_v3_conf=snmp_v3_conf,
        device_bgp_type=DeviceBGPType.device,
        device_bgp_neighbor_asn="77",
        device_bgp_neighbor_ip6="2001:db8:85a3:8d3:1319:8a2e:370:7348",
        device_bgp_password="bgp-optional-password",
        device_bgp_flowspec=True,
    )
    updated = devices_api.update(device)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "device": {
            "sending_ips": ["128.0.0.10", "128.0.0.11"],
            "device_sample_rate": "10",
            "device_description": "updated description",
            "device_name": "<id: 42>",
            "device_snmp_ip": "127.0.0.10",
            "plan_id": 11466,
            "site_id": 8483,
            "minimize_snmp": True,
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationProtocol": "SHA",
                "AuthenticationPassphrase": "Auth_Pass",
                "PrivacyProtocol": "AES",
                "PrivacyPassphrase": "Priv_Pass",
            },
            "device_bgp_type": "device",
            "device_bgp_neighbor_asn": "77",
            "device_bgp_neighbor_ip6": "2001:db8:85a3:8d3:1319:8a2e:370:7348",
            "device_bgp_password": "bgp-optional-password",
            "device_bgp_flowspec": True,
        }
    }

    # and response properly parsed
    assert updated.id == ID(42)
    assert updated.company_id == ID(74333)
    assert updated.device_name == "testapi_router_paloalto_minimal"
    assert updated.device_type == DeviceType.router
    assert updated.device_status == "V"
    assert updated.device_description == "updated description"
    assert updated.site is not None
    assert updated.site.id == ID(8483)
    assert updated.site.site_name is None
    assert updated.site.latitude is None
    assert updated.site.longitude is None
    assert updated.site.company_id is None
    assert updated.plan.active is None
    assert updated.plan.bgp_enabled is None
    assert updated.plan.created_date is None
    assert updated.plan.company_id is None
    assert updated.plan.description is None
    assert updated.plan.device_types == []
    assert updated.plan.devices == []
    assert updated.plan.updated_date is None
    assert updated.plan.fast_retention is None
    assert updated.plan.full_retention is None
    assert updated.plan.id == ID(11466)
    assert updated.plan.max_bigdata_fps is None
    assert updated.plan.max_devices is None
    assert updated.plan.max_fps is None
    assert updated.plan.name is None
    assert updated.plan.metadata is None
    assert len(updated.labels) == 0
    assert len(updated.interfaces) == 0
    assert updated.device_flow_type == "auto"
    assert updated.device_sample_rate == 10
    assert updated.sending_ips is not None
    assert len(updated.sending_ips) == 2
    assert updated.sending_ips[0] == "128.0.0.10"
    assert updated.sending_ips[1] == "128.0.0.11"
    assert updated.device_snmp_ip == "127.0.0.10"
    assert updated.device_snmp_community == ""
    assert updated.minimize_snmp == True
    assert updated.device_bgp_type == DeviceBGPType.device
    assert updated.device_bgp_neighbor_ip6 == "2001:db8:85a3:8d3:1319:8a2e:370:7348"
    assert updated.device_bgp_neighbor_asn == "77"
    assert updated.device_bgp_flowspec == True
    assert updated.device_bgp_password == "******************ord"
    assert updated.use_bgp_device_id is None
    assert updated.created_date == "2021-01-08T13:02:45.733Z"
    assert updated.updated_date == "2021-01-08T13:11:57.795Z"
    assert updated.device_snmp_v3_conf is not None
    assert updated.device_snmp_v3_conf.user_name == "John"
    assert updated.device_snmp_v3_conf.authentication_protocol == AuthenticationProtocol.sha
    assert updated.device_snmp_v3_conf.authentication_passphrase == "Auth_Pass"
    assert updated.device_snmp_v3_conf.privacy_protocol == PrivacyProtocol.aes
    assert updated.device_snmp_v3_conf.privacy_passphrase == "******ass"
    assert updated.bgp_peer_ip4 == "208.76.14.223"
    assert updated.bgp_peer_ip6 == "2620:129:1:2::1"
    assert updated.snmp_last_updated is None
    assert updated.device_subtype == DeviceSubtype.paloalto


def test_delete_device_success() -> None:
    # given
    delete_response_payload = ""  # deleting device responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    delete_successful = devices_api.delete(device_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # and response properly parsed
    assert delete_successful


def test_get_all_devices_success() -> None:
    # given
    get_response_payload = """
    {
        "devices": [
            {
                "id": "42",
                "company_id": "74333",
                "device_name": "testapi_router_full_1",
                "device_type": "router",
                "device_status": "V",
                "device_description": "testapi router with full config",
                "site": {
                    "id": 8483,
                    "site_name": "marina gdańsk",
                    "lat": 54.348972,
                    "lon": 18.659791,
                    "company_id": 74333
                },
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "labels": [
                            {
                                "id": 2590,
                                "name": "AWS: terraform-demo-aws",
                                "description": null,
                                "edate": "2020-10-05T15:28:00.276Z",
                                "cdate": "2020-10-05T15:28:00.276Z",
                                "user_id": "133210",
                                "company_id": "74333",
                                "color": "#5340A5",
                                "order": null,
                                "_pivot_device_id": "77715",
                                "_pivot_label_id": "2590"
                            },
                            {
                                "id": 2751,
                                "name": "GCP: traffic-generator-gcp",
                                "description": null,
                                "edate": "2020-11-20T12:54:49.575Z",
                                "cdate": "2020-11-20T12:54:49.575Z",
                                "user_id": null,
                                "company_id": "74333",
                                "color": "#5289D9",
                                "order": null,
                                "_pivot_device_id": "77373",
                                "_pivot_label_id": "2751"
                            }
                        ],
                "all_interfaces": [],
                "device_flow_type": "auto",
                "device_sample_rate": "1001",
                "sending_ips": [
                    "128.0.0.11",
                    "128.0.0.12"
                ],
                "device_snmp_ip": "129.0.0.1",
                "device_snmp_community": "",
                "minimize_snmp": false,
                "device_bgp_type": "device",
                "device_bgp_neighbor_ip": "127.0.0.1",
                "device_bgp_neighbor_ip6": null,
                "device_bgp_neighbor_asn": "11",
                "device_bgp_flowspec": true,
                "device_bgp_password": "*********ass",
                "use_bgp_device_id": null,
                "custom_columns": "",
                "custom_column_data": [],
                "device_chf_client_port": null,
                "device_chf_client_protocol": null,
                "device_chf_interface": null,
                "device_agent_type": null,
                "max_flow_rate": 1000,
                "max_big_flow_rate": 30,
                "device_proxy_bgp": "",
                "device_proxy_bgp6": "",
                "created_date": "2020-12-17T08:24:45.074Z",
                "updated_date": "2020-12-17T08:24:45.074Z",
                "device_snmp_v3_conf": {
                    "UserName": "John",
                    "AuthenticationProtocol": "MD5",
                    "AuthenticationPassphrase": "john_md5_pass",
                    "PrivacyProtocol": "DES",
                    "PrivacyPassphrase": "**********ass"
                },
                "bgpPeerIP4": "208.76.14.223",
                "bgpPeerIP6": "2620:129:1:2::1",
                "snmp_last_updated": null,
                "device_subtype": "router"
            },
            {
                "id": "43",
                "company_id": "74333",
                "device_name": "testapi_dns_minimal_1",
                "device_type": "host-nprobe-dns-www",
                "device_status": "V",
                "device_description": "testapi dns with minimal config",
                "site": {
                    "id": null,
                    "site_name": null,
                    "lat": null,
                    "lon": null,
                    "company_id": null
                },
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "labels": [],
                "all_interfaces": [],
                "device_flow_type": "auto",
                "device_sample_rate": "1",
                "sending_ips": [],
                "device_snmp_ip": null,
                "device_snmp_community": "",
                "minimize_snmp": false,
                "device_bgp_type": "none",
                "device_bgp_neighbor_ip": null,
                "device_bgp_neighbor_ip6": null,
                "device_bgp_neighbor_asn": null,
                "device_bgp_flowspec": false,
                "device_bgp_password": null,
                "use_bgp_device_id": null,
                "custom_columns": "",
                "custom_column_data": [],
                "device_chf_client_port": null,
                "device_chf_client_protocol": null,
                "device_chf_interface": null,
                "device_agent_type": null,
                "max_flow_rate": 1000,
                "max_big_flow_rate": 30,
                "device_proxy_bgp": "",
                "device_proxy_bgp6": "",
                "created_date": "2020-12-17T12:53:01.025Z",
                "updated_date": "2020-12-17T12:53:01.025Z",
                "device_snmp_v3_conf": null,
                "cdn_attr": "Y",
                "snmp_last_updated": null,
                "device_subtype": "aws_subnet"
            }
        ]
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    devices = devices_api.get_all()

    # then request properly formed
    assert connector.last_url_path == "/devices"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert len(devices) == 2
    device = devices[0]
    assert device.id == ID(42)
    assert device.company_id == ID(74333)
    assert device.device_name == "testapi_router_full_1"
    assert device.device_type == DeviceType.router
    assert device.device_status == "V"
    assert device.device_description == "testapi router with full config"
    assert device.site is not None
    assert device.site.id == ID(8483)
    assert device.site.site_name == "marina gdańsk"
    assert device.site.latitude == 54.348972
    assert device.site.longitude == 18.659791
    assert device.site.company_id == ID(74333)
    assert device.plan.active == True
    assert device.plan.bgp_enabled == True
    assert device.plan.created_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.company_id == ID(74333)
    assert device.plan.description == "Your Free Trial includes 6 devices (...)"
    assert device.plan.device_types == []
    assert device.plan.devices == []
    assert device.plan.updated_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.fast_retention == 30
    assert device.plan.full_retention == 30
    assert device.plan.id == ID(11466)
    assert device.plan.max_bigdata_fps == 30
    assert device.plan.max_devices == 6
    assert device.plan.max_fps == 1000
    assert device.plan.name == "Free Trial Plan"
    assert device.plan.metadata == {}
    assert len(device.labels) == 2
    assert device.labels[0].id == ID(2590)
    assert device.labels[0].name == "AWS: terraform-demo-aws"
    assert device.labels[0].updated_date == datetime(2020, 10, 5, 15, 28, 0, 276000, tzinfo=timezone.utc)
    assert device.labels[0].created_date == datetime(2020, 10, 5, 15, 28, 0, 276000, tzinfo=timezone.utc)
    assert device.labels[0].user_id == ID(133210)
    assert device.labels[0].company_id == ID(74333)
    assert device.labels[0].color == "#5340A5"
    assert device.labels[1].id == ID(2751)
    assert device.labels[1].name == "GCP: traffic-generator-gcp"
    assert device.labels[1].updated_date == datetime(2020, 11, 20, 12, 54, 49, 575000, tzinfo=timezone.utc)
    assert device.labels[1].created_date == datetime(2020, 11, 20, 12, 54, 49, 575000, tzinfo=timezone.utc)
    assert device.labels[1].user_id is None
    assert device.labels[1].company_id == ID(74333)
    assert device.labels[1].color == "#5289D9"
    assert len(device.interfaces) == 0
    assert device.device_flow_type == "auto"
    assert device.device_sample_rate == 1001
    assert device.sending_ips is not None
    assert len(device.sending_ips) == 2
    assert device.sending_ips[0] == "128.0.0.11"
    assert device.sending_ips[1] == "128.0.0.12"
    assert device.device_snmp_ip == "129.0.0.1"
    assert device.device_snmp_community == ""
    assert device.minimize_snmp == False
    assert device.device_bgp_type == DeviceBGPType.device
    assert device.device_bgp_neighbor_ip == "127.0.0.1"
    assert device.device_bgp_neighbor_ip6 is None
    assert device.device_bgp_neighbor_asn == "11"
    assert device.device_bgp_flowspec == True
    assert device.device_bgp_password == "*********ass"
    assert device.use_bgp_device_id is None
    assert device.created_date == "2020-12-17T08:24:45.074Z"
    assert device.updated_date == "2020-12-17T08:24:45.074Z"
    assert device.device_snmp_v3_conf is not None
    assert device.device_snmp_v3_conf.user_name == "John"
    assert device.device_snmp_v3_conf.authentication_protocol == AuthenticationProtocol.md5
    assert device.device_snmp_v3_conf.authentication_passphrase == "john_md5_pass"
    assert device.device_snmp_v3_conf.privacy_protocol == PrivacyProtocol.des
    assert device.device_snmp_v3_conf.privacy_passphrase == "**********ass"
    assert device.bgp_peer_ip4 == "208.76.14.223"
    assert device.bgp_peer_ip6 == "2620:129:1:2::1"
    assert device.snmp_last_updated is None
    assert device.device_subtype == DeviceSubtype.router


def test_apply_labels_success() -> None:
    # given
    apply_labels_response_payload = """
    {
        "id": "42",
        "device_name": "test_router",
        "labels": [
            {
                "id": 3011,
                "name": "apitest-label-red",
                "description": null,
                "edate": "2021-01-11T08:38:08.678Z",
                "cdate": "2021-01-11T08:38:08.678Z",
                "user_id": "144319",
                "company_id": "74333",
                "color": "#FF0000",
                "order": null,
                "_pivot_device_id": "79175",
                "_pivot_label_id": "3011"
            },
            {
                "id": 3012,
                "name": "apitest-label-blue",
                "description": null,
                "edate": "2021-01-11T08:38:42.627Z",
                "cdate": "2021-01-11T08:38:42.627Z",
                "user_id": "144319",
                "company_id": "74333",
                "color": "#0000FF",
                "order": null,
                "_pivot_device_id": "79175",
                "_pivot_label_id": "3012"
            }
        ]
    }"""
    connector = StubAPIConnector(apply_labels_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    labels = [ID(3011), ID(3012)]
    apply_result = devices_api.apply_labels(device_id, labels)

    # then request properly formed
    assert connector.last_url_path == f"/devices/{device_id}/labels"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "labels": [
            {"id": 3011},
            {"id": 3012},
        ]
    }

    # and response properly parsed
    assert apply_result.id == ID(42)
    assert apply_result.device_name == "test_router"
    assert len(apply_result.labels) == 2
    assert apply_result.labels[0].id == ID(3011)
    assert apply_result.labels[0].name == "apitest-label-red"
    assert apply_result.labels[0].created_date == datetime(2021, 1, 11, 8, 38, 8, 678000, tzinfo=timezone.utc)
    assert apply_result.labels[0].updated_date == datetime(2021, 1, 11, 8, 38, 8, 678000, tzinfo=timezone.utc)
    assert apply_result.labels[0].user_id == ID(144319)
    assert apply_result.labels[0].company_id == ID(74333)
    assert apply_result.labels[0].color == "#FF0000"
    assert apply_result.labels[1].id == ID(3012)
    assert apply_result.labels[1].name == "apitest-label-blue"
    assert apply_result.labels[1].created_date == datetime(2021, 1, 11, 8, 38, 42, 627000, tzinfo=timezone.utc)
    assert apply_result.labels[1].updated_date == datetime(2021, 1, 11, 8, 38, 42, 627000, tzinfo=timezone.utc)
    assert apply_result.labels[1].user_id == ID(144319)
    assert apply_result.labels[1].company_id == ID(74333)
    assert apply_result.labels[1].color == "#0000FF"


def test_create_interface_minimal_success() -> None:
    # given
    create_response_payload = """
    {
        "snmp_id": "2",
        "snmp_speed": 8,
        "interface_description": "testapi-interface-2",
        "interface_kvs": "",
        "company_id": "74333",
        "device_id": "42",
        "edate": "2021-01-13T08:41:16.191Z",
        "cdate": "2021-01-13T08:41:16.191Z",
        "id": "43"
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interface = Interface(
        device_id=device_id,
        snmp_id=ID(2),
        snmp_speed=15,
        interface_description="testapi-interface-2",
    )
    created = devices_api.interfaces.create(interface)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload == {
        "snmp_id": "2",
        "snmp_speed": 15,
        "interface_description": "testapi-interface-2",
    }

    # and response properly parsed
    assert created.snmp_id == ID(2)
    assert created.snmp_alias is None
    assert created.snmp_speed == 8
    assert created.interface_description == "testapi-interface-2"
    assert created.interface_ip is None
    assert created.interface_ip_netmask is None
    assert created.company_id == ID(74333)
    assert created.device_id == ID(42)
    assert created.updated_date == "2021-01-13T08:41:16.191Z"
    assert created.created_date == "2021-01-13T08:41:16.191Z"
    assert created.id == ID(43)
    assert created.vrf_id is None
    assert created.vrf is None
    assert created.secondary_ips is None


def test_create_interface_full_success() -> None:
    # given
    create_response_payload = """
    {
        "snmp_id": "243205880",
        "snmp_alias": "interace-description-1",
        "snmp_speed": 8,
        "interface_description": "testapi-interface-1",
        "interface_ip": "127.0.0.1",
        "interface_ip_netmask": "255.255.255.0",
        "interface_kvs": "",
        "company_id": "74333",
        "device_id": "42",
        "edate": "2021-01-13T08:31:40.629Z",
        "cdate": "2021-01-13T08:31:40.619Z",
        "id": "43",
        "vrf_id": 39903,
        "secondary_ips": [
            {
                "address": "198.186.193.51",
                "netmask": "255.255.255.240"
            },
            {
                "address": "198.186.193.63",
                "netmask": "255.255.255.225"
            }
        ]
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    devices_api = DevicesAPI(connector)

    # when
    vrf = VRFAttributes(
        name="vrf-name",
        description="vrf-description",
        route_target="101:100",
        route_distinguisher="11.121.111.13:3254",
        ext_route_distinguisher=15,
    )
    secondary_ip1 = SecondaryIP(address="127.0.0.2", netmask="255.255.255.0")
    secondary_ip2 = SecondaryIP(address="127.0.0.3", netmask="255.255.255.0")
    device_id = ID(42)
    interface = Interface(
        device_id=device_id,
        snmp_id=ID(1),
        interface_description="testapi-interface-1",
        snmp_alias="interace-description-1",
        interface_ip="127.0.0.1",
        interface_ip_netmask="255.255.255.0",
        snmp_speed=15,
        vrf=vrf,
        secondary_ips=[secondary_ip1, secondary_ip2],
    )
    created = devices_api.interfaces.create(interface)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload == {
        "snmp_id": "1",
        "snmp_alias": "interace-description-1",
        "snmp_speed": 15,
        "interface_description": "testapi-interface-1",
        "interface_ip": "127.0.0.1",
        "interface_ip_netmask": "255.255.255.0",
        "vrf": {
            "name": "vrf-name",
            "description": "vrf-description",
            "route_target": "101:100",
            "route_distinguisher": "11.121.111.13:3254",
            "ext_route_distinguisher": 15,
        },
        "secondary_ips": [
            {"address": "127.0.0.2", "netmask": "255.255.255.0"},
            {"address": "127.0.0.3", "netmask": "255.255.255.0"},
        ],
    }

    # and response properly parsed
    assert created.snmp_id == ID(243205880)
    assert created.snmp_alias == "interace-description-1"
    assert created.snmp_speed == 8
    assert created.interface_description == "testapi-interface-1"
    assert created.interface_ip == "127.0.0.1"
    assert created.interface_ip_netmask == "255.255.255.0"
    assert created.company_id == ID(74333)
    assert created.device_id == ID(42)
    assert created.updated_date == "2021-01-13T08:31:40.629Z"
    assert created.created_date == "2021-01-13T08:31:40.619Z"
    assert created.id == ID(43)
    assert created.vrf_id == ID(39903)
    assert created.secondary_ips is not None
    assert len(created.secondary_ips) == 2
    assert created.secondary_ips[0].address == "198.186.193.51"
    assert created.secondary_ips[0].netmask == "255.255.255.240"
    assert created.secondary_ips[1].address == "198.186.193.63"
    assert created.secondary_ips[1].netmask == "255.255.255.225"


def test_update_interface_minimal_success() -> None:
    # given
    update_response_payload = """
    {
        "id": "43",
        "company_id": "74333",
        "device_id": "42",
        "snmp_id": "1",
        "snmp_speed": 75,
        "snmp_type": null,
        "snmp_alias": "interace-description-1",
        "interface_ip": "127.0.0.1",
        "interface_description": "testapi-interface-1",
        "interface_kvs": "",
        "interface_tags": "",
        "interface_status": "V",
        "cdate": "2021-01-13T08:50:37.068Z",
        "edate": "2021-01-13T08:58:27.276Z",
        "initial_snmp_id": "",
        "initial_snmp_alias": null,
        "initial_interface_description": null,
        "initial_snmp_speed": null,
        "interface_ip_netmask": "255.255.255.0",
        "secondary_ips": null,
        "connectivity_type": "",
        "network_boundary": "",
        "initial_connectivity_type": "",
        "initial_network_boundary": "",
        "top_nexthop_asns": null,
        "provider": "",
        "initial_provider": "",
        "vrf_id": "39902",
        "initial_interface_ip": null,
        "initial_interface_ip_netmask": null
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interface_id = ID(43)
    interface = Interface(snmp_speed=75, device_id=device_id, id=interface_id)
    updated = devices_api.interfaces.update(interface)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface/{interface_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {"snmp_speed": 75}

    # and response properly parsed
    assert updated.id == ID(43)
    assert updated.company_id == ID(74333)
    assert updated.device_id == ID(42)
    assert updated.snmp_id == ID(1)
    assert updated.snmp_speed == 75
    assert updated.snmp_alias == "interace-description-1"
    assert updated.interface_ip == "127.0.0.1"
    assert updated.interface_description == "testapi-interface-1"
    assert updated.created_date == "2021-01-13T08:50:37.068Z"
    assert updated.updated_date == "2021-01-13T08:58:27.276Z"
    assert updated.initial_snmp_id is None
    assert updated.initial_snmp_alias is None
    assert updated.initial_interface_description is None
    assert updated.initial_snmp_speed is None
    assert updated.interface_ip_netmask == "255.255.255.0"
    assert updated.secondary_ips is None
    assert updated.top_nexthop_asns == []
    assert updated.provider == ""
    assert updated.vrf_id == ID(39902)


def test_update_interface_full_success() -> None:
    # given
    update_response_payload = """
    {
        "id": "43",
        "company_id": "74333",
        "device_id": "42",
        "snmp_id": "4",
        "snmp_speed": 44,
        "snmp_type": null,
        "snmp_alias": "interace-description-44",
        "interface_ip": "127.0.44.55",
        "interface_description": "testapi-interface-44",
        "interface_kvs": "",
        "interface_tags": "",
        "interface_status": "V",
        "cdate": "2021-01-14T14:43:43.104Z",
        "edate": "2021-01-14T14:46:21.200Z",
        "initial_snmp_id": "",
        "initial_snmp_alias": null,
        "initial_interface_description": null,
        "initial_snmp_speed": null,
        "interface_ip_netmask": "255.255.255.0",
        "secondary_ips": [],
        "connectivity_type": "",
        "network_boundary": "",
        "initial_connectivity_type": "",
        "initial_network_boundary": "",
        "top_nexthop_asns": null,
        "provider": "",
        "initial_provider": "",
        "vrf_id": 40055,
        "initial_interface_ip": null,
        "initial_interface_ip_netmask": null
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interface_id = ID(43)
    vrf = VRFAttributes(
        name="vrf-name-44",
        description="vrf-description-44",
        route_target="101:100",
        route_distinguisher="11.121.111.13:444",
        ext_route_distinguisher=44,
    )
    interface = Interface(
        device_id=device_id,
        id=interface_id,
        snmp_id=ID(4),
        snmp_speed=44,
        snmp_alias="interace-description-44",
        interface_ip="127.0.44.55",
        interface_ip_netmask="255.255.255.0",
        interface_description="testapi-interface-44",
        vrf=vrf,
        secondary_ips=[],
    )
    updated = devices_api.interfaces.update(interface)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface/{interface_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "snmp_id": "4",
        "snmp_alias": "interace-description-44",
        "snmp_speed": 44,
        "interface_description": "testapi-interface-44",
        "interface_ip": "127.0.44.55",
        "interface_ip_netmask": "255.255.255.0",
        "vrf": {
            "name": "vrf-name-44",
            "description": "vrf-description-44",
            "route_target": "101:100",
            "route_distinguisher": "11.121.111.13:444",
            "ext_route_distinguisher": 44,
        },
        "secondary_ips": [],
    }

    # and response properly parsed
    assert updated.id == ID(43)
    assert updated.company_id == ID(74333)
    assert updated.device_id == ID(42)
    assert updated.snmp_id == ID(4)
    assert updated.snmp_speed == 44
    assert updated.snmp_alias == "interace-description-44"
    assert updated.interface_ip == "127.0.44.55"
    assert updated.interface_description == "testapi-interface-44"
    assert updated.created_date == "2021-01-14T14:43:43.104Z"
    assert updated.updated_date == "2021-01-14T14:46:21.200Z"
    assert updated.initial_snmp_id is None
    assert updated.initial_snmp_alias is None
    assert updated.initial_interface_description is None
    assert updated.initial_snmp_speed is None
    assert updated.interface_ip_netmask == "255.255.255.0"
    assert updated.secondary_ips == []
    assert updated.top_nexthop_asns == []
    assert updated.provider == ""
    assert updated.vrf_id == ID(40055)


def test_get_interface_minimal_success() -> None:
    # given
    get_response_payload = """
    {
        "interface": {
            "id": "43",
            "company_id": "74333",
            "device_id": "42",
            "snmp_id": "1",
            "snmp_speed": "15",
            "snmp_type": null,
            "snmp_alias": null,
            "interface_ip": null,
            "interface_description": null,
            "cdate": "2021-01-13T08:50:37.068Z",
            "edate": "2021-01-13T08:55:59.403Z",
            "initial_snmp_id": null,
            "initial_snmp_alias": null,
            "initial_interface_description": null,
            "initial_snmp_speed": null,
            "interface_ip_netmask": null,
            "top_nexthop_asns": null,
            "provider": null,
            "vrf_id": null,
            "vrf": null,
            "secondary_ips": null
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interface_id = ID(43)
    interface = devices_api.interfaces.get(device_id, interface_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface/{interface_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert interface.id == ID(43)
    assert interface.company_id == ID(74333)
    assert interface.device_id == ID(42)
    assert interface.snmp_id == ID(1)
    assert interface.snmp_speed == 15
    assert interface.snmp_alias is None
    assert interface.interface_ip is None
    assert interface.interface_description is None
    assert interface.created_date == "2021-01-13T08:50:37.068Z"
    assert interface.updated_date == "2021-01-13T08:55:59.403Z"
    assert interface.initial_snmp_id is None
    assert interface.initial_snmp_alias is None
    assert interface.initial_interface_description is None
    assert interface.initial_snmp_speed is None
    assert interface.interface_ip_netmask is None
    assert len(interface.top_nexthop_asns) == 0
    assert interface.provider is None
    assert interface.vrf_id is None
    assert interface.vrf is None
    assert interface.secondary_ips is None


def test_get_interface_full_success() -> None:
    # given
    get_response_payload = """
    {
        "interface": {
            "id": "43",
            "company_id": "74333",
            "device_id": "42",
            "snmp_id": "1",
            "snmp_speed": "15",
            "snmp_type": null,
            "snmp_alias": "interace-description-1",
            "interface_ip": "127.0.0.1",
            "interface_description": "testapi-interface-1",
            "interface_kvs": "",
            "interface_tags": "",
            "interface_status": "V",
            "extra_info": {},
            "cdate": "2021-01-13T08:50:37.068Z",
            "edate": "2021-01-13T08:55:59.403Z",
            "initial_snmp_id": "150",
            "initial_snmp_alias": "initial-interace-description-1",
            "initial_interface_description": "initial-testapi-interface-1",
            "initial_snmp_speed": "7",
            "interface_ip_netmask": "255.255.255.0",
            "connectivity_type": "",
            "network_boundary": "",
            "initial_connectivity_type": "",
            "initial_network_boundary": "",
            "top_nexthop_asns": [
                {
                    "Asn": 20,
                    "Packets":30100
                },
                {
                    "Asn": 21,
                    "fala": "hala",
                    "Packets":30101
                }
            ],
            "provider": "",
            "initial_provider": "",
            "vrf_id": "39902",
            "vrf": {
                "id": 39902,
                "company_id": "74333",
                "description": "vrf-description",
                "device_id": "79175",
                "name": "vrf-name",
                "route_distinguisher": "11.121.111.13:3254",
                "route_target": "101:100"
            },
            "secondary_ips": [
                {
                "address": "198.186.193.51",
                "netmask": "255.255.255.240"
                },
                {
                "address": "198.186.193.63",
                "netmask": "255.255.255.225"
                }
            ]
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interface_id = ID(43)
    interface = devices_api.interfaces.get(device_id, interface_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface/{interface_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert interface.id == ID(43)
    assert interface.company_id == ID(74333)
    assert interface.device_id == ID(42)
    assert interface.snmp_id == ID(1)
    assert interface.snmp_speed == 15
    assert interface.snmp_alias == "interace-description-1"
    assert interface.interface_ip == "127.0.0.1"
    assert interface.interface_description == "testapi-interface-1"
    assert interface.created_date == "2021-01-13T08:50:37.068Z"
    assert interface.updated_date == "2021-01-13T08:55:59.403Z"
    assert interface.initial_snmp_id == ID(150)
    assert interface.initial_snmp_alias == "initial-interace-description-1"
    assert interface.initial_interface_description == "initial-testapi-interface-1"
    assert interface.initial_snmp_speed == 7
    assert interface.interface_ip_netmask == "255.255.255.0"
    assert len(interface.top_nexthop_asns) == 2
    assert interface.top_nexthop_asns[0].asn == 20
    assert interface.top_nexthop_asns[0].packets == 30100
    assert interface.top_nexthop_asns[1].asn == 21
    assert interface.top_nexthop_asns[1].packets == 30101
    assert interface.provider == ""
    assert interface.vrf_id == ID(39902)
    assert interface.vrf is not None
    assert interface.vrf.company_id == ID(74333)
    assert interface.vrf.description == "vrf-description"
    assert interface.vrf.device_id == ID(79175)
    assert interface.vrf.name == "vrf-name"
    assert interface.vrf.route_distinguisher == "11.121.111.13:3254"
    assert interface.vrf.route_target == "101:100"
    assert interface.secondary_ips is not None
    assert len(interface.secondary_ips) == 2
    assert interface.secondary_ips[0].address == "198.186.193.51"
    assert interface.secondary_ips[0].netmask == "255.255.255.240"
    assert interface.secondary_ips[1].address == "198.186.193.63"
    assert interface.secondary_ips[1].netmask == "255.255.255.225"


def test_delete_interface_success() -> None:
    # given
    delete_response_payload = "{}"  # deleting device responds with empty dictionary
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.OK)  # responds with 200 OK
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interface_id = ID(43)
    delete_successful = devices_api.interfaces.delete(device_id, interface_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interface/{interface_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # and response properly parsed
    assert delete_successful


def test_get_all_interfaces_success() -> None:
    # given
    get_response_payload = """
    [
        {
            "id": "43",
            "company_id": "74333",
            "device_id": "42",
            "snmp_id": "1",
            "snmp_speed": "15",
            "snmp_type": null,
            "snmp_alias": "interace-description-1",
            "interface_ip": "127.0.0.1",
            "interface_description": "testapi-interface-1",
            "interface_kvs": "",
            "interface_tags": "",
            "interface_status": "V",
            "extra_info": {},
            "cdate": "2021-01-13T08:50:37.068Z",
            "edate": "2021-01-13T08:55:59.403Z",
            "initial_snmp_id": "150",
            "initial_snmp_alias": "initial-interace-description-1",
            "initial_interface_description": "initial-testapi-interface-1",
            "initial_snmp_speed": "7",
            "interface_ip_netmask": "255.255.255.0",
            "connectivity_type": "",
            "network_boundary": "",
            "initial_connectivity_type": "",
            "initial_network_boundary": "",
            "top_nexthop_asns": [
                {
                    "Asn": 20,
                    "Packets":30100
                },
                {
                    "Asn": 21,
                    "Packets":30101
                }
            ],
            "provider": "",
            "initial_provider": "",
            "vrf_id": "39902",
            "vrf": {
                "id": 39902,
                "company_id": "74333",
                "description": "vrf-description",
                "device_id": "79175",
                "name": "vrf-name",
                "route_distinguisher": "11.121.111.13:3254",
                "route_target": "101:100"
            },
            "secondary_ips": [
                {
                "address": "198.186.193.51",
                "netmask": "255.255.255.240"
                },
                {
                "address": "198.186.193.63",
                "netmask": "255.255.255.225"
                }
            ]
        },
        {
            "id": "44",
            "company_id": "74333",
            "device_id": "42",
            "snmp_id": "1",
            "snmp_speed": "15",
            "snmp_type": null,
            "snmp_alias": "interace-description-1",
            "interface_ip": "127.0.0.1",
            "interface_description": "testapi-interface-1",
            "interface_kvs": "",
            "interface_tags": "",
            "interface_status": "V",
            "extra_info": {},
            "cdate": "2021-01-13T08:50:37.068Z",
            "edate": "2021-01-13T08:50:37.074Z",
            "initial_snmp_id": "",
            "initial_snmp_alias": null,
            "initial_interface_description": null,
            "initial_snmp_speed": null,
            "interface_ip_netmask": "255.255.255.0",
            "secondary_ips": null,
            "connectivity_type": "",
            "network_boundary": "",
            "initial_connectivity_type": "",
            "initial_network_boundary": "",
            "top_nexthop_asns": null,
            "provider": "",
            "initial_provider": "",
            "vrf_id": "39902",
            "vrf": {
                "id": 39902,
                "company_id": "74333",
                "description": "vrf-description",
                "device_id": "42",
                "name": "vrf-name",
                "route_distinguisher": "11.121.111.13:3254",
                "route_target": "101:100"
            }
        }
    ]"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = ID(42)
    interfaces = devices_api.interfaces.get_all(device_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}/interfaces"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert len(interfaces) == 2
    interface = interfaces[0]
    assert interface.id == ID(43)
    assert interface.company_id == ID(74333)
    assert interface.device_id == ID(42)
    assert interface.snmp_id == ID(1)
    assert interface.snmp_speed == 15
    assert interface.snmp_alias == "interace-description-1"
    assert interface.interface_ip == "127.0.0.1"
    assert interface.interface_description == "testapi-interface-1"
    assert interface.created_date == "2021-01-13T08:50:37.068Z"
    assert interface.updated_date == "2021-01-13T08:55:59.403Z"
    assert interface.initial_snmp_id == ID(150)
    assert interface.initial_snmp_alias == "initial-interace-description-1"
    assert interface.initial_interface_description == "initial-testapi-interface-1"
    assert interface.initial_snmp_speed == 7
    assert interface.interface_ip_netmask == "255.255.255.0"
    assert len(interface.top_nexthop_asns) == 2
    assert interface.top_nexthop_asns[0].asn == 20
    assert interface.top_nexthop_asns[0].packets == 30100
    assert interface.top_nexthop_asns[1].asn == 21
    assert interface.top_nexthop_asns[1].packets == 30101
    assert interface.provider == ""
    assert interface.vrf_id == ID(39902)
    assert interface.vrf is not None
    assert interface.vrf.company_id == ID(74333)
    assert interface.vrf.description == "vrf-description"
    assert interface.vrf.device_id == ID(79175)
    assert interface.vrf.name == "vrf-name"
    assert interface.vrf.route_distinguisher == "11.121.111.13:3254"
    assert interface.vrf.route_target == "101:100"
    assert interface.secondary_ips is not None
    assert len(interface.secondary_ips) == 2
    assert interface.secondary_ips[0].address == "198.186.193.51"
    assert interface.secondary_ips[0].netmask == "255.255.255.240"
    assert interface.secondary_ips[1].address == "198.186.193.63"
    assert interface.secondary_ips[1].netmask == "255.255.255.225"


def test_get_and_update_device_with_unknown_enum_fields() -> None:
    # given
    get_response_payload = """
    {
        "device": {
                "id": "43",
                "company_id": "74333",
                "device_name": "testapi_dns_minimal_1",
                "device_type": "dt_teapot",
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "device_sample_rate": "1",
                "device_bgp_type": "dbt_teapot",
                "created_date": "2020-12-17T12:53:01.025Z",
                "updated_date": "2020-12-17T12:53:01.025Z",
                "device_snmp_v3_conf": {
                    "UserName": "John",
                    "AuthenticationProtocol": "ap_teapot",
                    "AuthenticationPassphrase": "Auth_Pass",
                    "PrivacyProtocol": "pp_teapot",
                    "PrivacyPassphrase": "******ass"
                },
                "cdn_attr": "cdna_teapot",
                "device_subtype": "ds_teapot"
            }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when device got
    device_id = ID(43)
    device = devices_api.get(device_id)

    # then get request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then get response properly parsed
    check_device_dns_minimal(
        device,
        device_sample_rate=1,
        device_type="dt_teapot",
        device_bgp_type="dbt_teapot",
        authentication_protocol="ap_teapot",
        privacy_protocol="pp_teapot",
        cdn_attr="cdna_teapot",
        device_subtype="ds_teapot",
    )

    # given
    update_response_payload = """
    {
        "device": {
                "id": "43",
                "company_id": "74333",
                "device_name": "testapi_dns_minimal_1",
                "device_type": "dt_teapot",
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "device_sample_rate": "10",
                "device_bgp_type": "dbt_teapot",
                "created_date": "2020-12-17T12:53:01.025Z",
                "updated_date": "2020-12-17T12:53:01.025Z",
                "device_snmp_v3_conf": {
                    "UserName": "John",
                    "AuthenticationProtocol": "ap_teapot",
                    "AuthenticationPassphrase": "Auth_Pass",
                    "PrivacyProtocol": "pp_teapot",
                    "PrivacyPassphrase": "******ass"
                },
                "cdn_attr": "cdna_teapot",
                "device_subtype": "ds_teapot"
            }
    }"""
    connector.response_text = update_response_payload

    # when device updated
    device.device_sample_rate = 10
    device = devices_api.update(device)

    # then update request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "device": {
            "device_name": "testapi_dns_minimal_1",
            "device_type": "dt_teapot",
            "device_subtype": "ds_teapot",
            "device_sample_rate": "10",
            "device_bgp_type": "dbt_teapot",
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationProtocol": "ap_teapot",
                "AuthenticationPassphrase": "Auth_Pass",
                "PrivacyProtocol": "pp_teapot",
                "PrivacyPassphrase": "******ass",
            },
            "cdn_attr": "cdna_teapot",
        },
    }

    # then update response properly parsed
    check_device_dns_minimal(
        device,
        device_sample_rate=10,
        device_type="dt_teapot",
        device_bgp_type="dbt_teapot",
        authentication_protocol="ap_teapot",
        privacy_protocol="pp_teapot",
        cdn_attr="cdna_teapot",
        device_subtype="ds_teapot",
    )


def test_get_and_update_device_with_empty_enum_fields() -> None:
    # given
    get_response_payload = """
    {
        "device": {
                "id": "43",
                "company_id": "74333",
                "device_name": "testapi_dns_minimal_1",
                "device_type": "",
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "device_sample_rate": "1",
                "device_bgp_type": "",
                "created_date": "2020-12-17T12:53:01.025Z",
                "updated_date": "2020-12-17T12:53:01.025Z",
                "device_snmp_v3_conf": {
                    "UserName": "John",
                    "AuthenticationProtocol": "",
                    "AuthenticationPassphrase": "Auth_Pass",
                    "PrivacyProtocol": "",
                    "PrivacyPassphrase": "******ass"
                },
                "cdn_attr": "",
                "device_subtype": ""
            }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when device got
    device_id = ID(43)
    device = devices_api.get(device_id)

    # then get request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then get response properly parsed
    check_device_dns_minimal(
        device,
        device_sample_rate=1,
        device_type="",
        device_bgp_type="",
        authentication_protocol=None,
        privacy_protocol=None,
        cdn_attr=None,
        device_subtype="",
    )

    # given
    update_response_payload = """
    {
        "device": {
                "id": "43",
                "company_id": "74333",
                "device_name": "testapi_dns_minimal_1",
                "device_type": "",
                "plan": {
                    "active": true,
                    "bgp_enabled": true,
                    "cdate": "2020-09-03T08:41:57.489Z",
                    "company_id": 74333,
                    "description": "Your Free Trial includes 6 devices (...)",
                    "deviceTypes": [],
                    "devices": [],
                    "edate": "2020-09-03T08:41:57.489Z",
                    "fast_retention": 30,
                    "full_retention": 30,
                    "id": 11466,
                    "max_bigdata_fps": 30,
                    "max_devices": 6,
                    "max_fps": 1000,
                    "name": "Free Trial Plan",
                    "metadata": {}
                },
                "device_sample_rate": "10",
                "device_bgp_type": "",
                "created_date": "2020-12-17T12:53:01.025Z",
                "updated_date": "2020-12-17T12:53:01.025Z",
                "device_snmp_v3_conf": {
                    "UserName": "John",
                    "AuthenticationProtocol": "",
                    "AuthenticationPassphrase": "Auth_Pass",
                    "PrivacyProtocol": "",
                    "PrivacyPassphrase": "******ass"
                },
                "cdn_attr": "",
                "device_subtype": ""
            }
    }"""
    connector.response_text = update_response_payload

    # when device updated
    device.device_sample_rate = 10
    device = devices_api.update(device)

    # then update request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload == {
        "device": {
            "device_name": "testapi_dns_minimal_1",
            "device_sample_rate": "10",
            "device_snmp_v3_conf": {
                "UserName": "John",
                "AuthenticationPassphrase": "Auth_Pass",
                "PrivacyPassphrase": "******ass",
            },
        },
    }

    # then update response properly parsed
    check_device_dns_minimal(
        device,
        device_sample_rate=10,
        device_type="",
        device_bgp_type="",
        authentication_protocol=None,
        privacy_protocol=None,
        cdn_attr=None,
        device_subtype="",
    )


def check_device_dns_minimal(
    device,
    device_sample_rate,
    device_type,
    device_bgp_type,
    authentication_protocol,
    privacy_protocol,
    cdn_attr,
    device_subtype,
) -> None:
    assert device.id == ID(43)
    assert device.company_id == ID(74333)
    assert device.device_name == "testapi_dns_minimal_1"
    assert device.device_type == device_type
    assert device.device_status is None
    assert device.device_description is None
    assert device.site is None
    assert device.plan.active is True
    assert device.plan.bgp_enabled is True
    assert device.plan.created_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.company_id == ID(74333)
    assert device.plan.description == "Your Free Trial includes 6 devices (...)"
    assert device.plan.device_types == []
    assert device.plan.devices == []
    assert device.plan.updated_date == "2020-09-03T08:41:57.489Z"
    assert device.plan.fast_retention == 30
    assert device.plan.full_retention == 30
    assert device.plan.id == ID(11466)
    assert device.plan.max_bigdata_fps == 30
    assert device.plan.max_devices == 6
    assert device.plan.max_fps == 1000
    assert device.plan.name == "Free Trial Plan"
    assert device.plan.metadata == {}
    assert len(device.labels) == 0
    assert len(device.interfaces) == 0
    assert device.device_flow_type is None
    assert device.device_sample_rate == device_sample_rate
    assert device.sending_ips is None
    assert device.device_snmp_ip is None
    assert device.device_snmp_community is None
    assert device.minimize_snmp is None
    assert device.device_bgp_type == device_bgp_type
    assert device.device_bgp_neighbor_ip is None
    assert device.device_bgp_neighbor_ip6 is None
    assert device.device_bgp_neighbor_asn is None
    assert device.device_bgp_flowspec is None
    assert device.device_bgp_password is None
    assert device.use_bgp_device_id is None
    assert device.created_date == "2020-12-17T12:53:01.025Z"
    assert device.updated_date == "2020-12-17T12:53:01.025Z"
    assert device.device_snmp_v3_conf is not None
    assert device.device_snmp_v3_conf.user_name == "John"
    assert device.device_snmp_v3_conf.authentication_protocol == authentication_protocol
    assert device.device_snmp_v3_conf.authentication_passphrase == "Auth_Pass"
    assert device.device_snmp_v3_conf.privacy_protocol == privacy_protocol
    assert device.device_snmp_v3_conf.privacy_passphrase == "******ass"
    assert device.cdn_attr == cdn_attr
    assert device.bgp_peer_ip4 is None
    assert device.bgp_peer_ip6 is None
    assert device.snmp_last_updated is None
    assert device.device_subtype == device_subtype
