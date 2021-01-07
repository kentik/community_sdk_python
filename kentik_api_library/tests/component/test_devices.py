from http import HTTPStatus

from kentik_api.api_resources.devices_api import DevicesAPI
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.device import (
    Device,
    DeviceType,
    DeviceSubtype,
    DeviceBGPType,
    AuthenticationProtocol,
    PrivacyProtocol,
    CDNAttribute,
)
from tests.component.stub_api_connector import StubAPIConnector


def test_create_device_router_success() -> None:
    pass


def test_create_device_dns_success() -> None:
    pass


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
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    devices_api = DevicesAPI(connector)

    # when
    device_id = 42
    device = devices_api.get(device_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert device.id == 42
    assert device.company_id == "74333"
    assert device.device_name == "testapi_router_full_1"
    assert device.device_type == DeviceType.router
    assert device.device_status == "V"
    assert device.device_description == "testapi router with full config"
    assert device.site is not None
    assert device.site.id == 8483
    assert device.site.site_name == "marina gdańsk"
    assert device.site.latitude == 54.348972
    assert device.site.longitude == 18.659791
    assert device.site.company_id == 74333
    assert device.plan.active == True
    assert device.plan.bgp_enabled == True
    assert device.plan.cdate == "2020-09-03T08:41:57.489Z"
    assert device.plan.company_id == 74333
    assert device.plan.description == "Your Free Trial includes 6 devices (...)"
    assert device.plan.deviceTypes == []
    assert device.plan.devices == []
    assert device.plan.edate == "2020-09-03T08:41:57.489Z"
    assert device.plan.fast_retention == 30
    assert device.plan.full_retention == 30
    assert device.plan.id == 11466
    assert device.plan.max_bigdata_fps == 30
    assert device.plan.max_devices == 6
    assert device.plan.max_fps == 1000
    assert device.plan.name == "Free Trial Plan"
    assert device.plan.metadata == {}
    assert len(device.labels) == 2
    assert device.labels[0].id == 2590
    assert device.labels[0].name == "AWS: terraform-demo-aws"
    assert device.labels[0].updated_date == "2020-10-05T15:28:00.276Z"
    assert device.labels[0].created_date == "2020-10-05T15:28:00.276Z"
    assert device.labels[0].user_id == "133210"
    assert device.labels[0].company_id == "74333"
    assert device.labels[0].color == "#5340A5"
    assert device.labels[1].id == 2751
    assert device.labels[1].name == "GCP: traffic-generator-gcp"
    assert device.labels[1].updated_date == "2020-11-20T12:54:49.575Z"
    assert device.labels[1].created_date == "2020-11-20T12:54:49.575Z"
    assert device.labels[1].user_id == "136885"
    assert device.labels[1].company_id == "74333"
    assert device.labels[1].color == "#5289D9"
    assert len(device.all_interfaces) == 0
    assert device.device_flow_type == "auto"
    assert device.device_sample_rate == "1001"
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
    device_id = 43
    device = devices_api.get(device_id)

    # then request properly formed
    assert connector.last_url_path == f"/device/{device_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert device.id == 43
    assert device.company_id == "74333"
    assert device.device_name == "testapi_dns_minimal_1"
    assert device.device_type == DeviceType.host_nprobe_dns_www
    assert device.device_status == "V"
    assert device.device_description == "testapi dns with minimal config"
    assert device.site is None
    assert device.plan.active == True
    assert device.plan.bgp_enabled == True
    assert device.plan.cdate == "2020-09-03T08:41:57.489Z"
    assert device.plan.company_id == 74333
    assert device.plan.description == "Your Free Trial includes 6 devices (...)"
    assert device.plan.deviceTypes == []
    assert device.plan.devices == []
    assert device.plan.edate == "2020-09-03T08:41:57.489Z"
    assert device.plan.fast_retention == 30
    assert device.plan.full_retention == 30
    assert device.plan.id == 11466
    assert device.plan.max_bigdata_fps == 30
    assert device.plan.max_devices == 6
    assert device.plan.max_fps == 1000
    assert device.plan.name == "Free Trial Plan"
    assert device.plan.metadata == {}
    assert len(device.labels) == 0
    assert len(device.all_interfaces) == 0
    assert device.device_flow_type == "auto"
    assert device.device_sample_rate == "1"
    assert len(device.sending_ips) == 0
    assert device.device_snmp_ip is None
    assert device.device_snmp_community == ""
    assert device.minimize_snmp == False
    assert device.device_bgp_type == DeviceBGPType.none
    assert device.device_bgp_neighbor_ip is None
    assert device.device_bgp_neighbor_ip6 is None
    assert device.device_bgp_neighbor_asn is None
    assert device.device_bgp_flowspec == False
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
    pass


def test_update_device_dns_success() -> None:
    pass


def test_delete_device_success() -> None:
    pass


def test_get_all_devices_success() -> None:
    pass
