# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""DeviceLookup finds devices, links, and link speeds, and saves JSON (FR-021)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
import respx

from kentik_api import KentikAPI
from kentik_api.devices import DeviceLookup
from kentik_api.gen.device.models import DeviceDetailed
from kentik_api.gen.interface.models import Interface

DEVICES = [
    DeviceDetailed.model_validate(
        {"id": "1", "deviceName": "router1", "labels": [{"name": "edge"}]}
    ),
    DeviceDetailed.model_validate({"id": "2", "deviceName": "router2", "labels": []}),
]
INTERFACES = [
    Interface.model_validate(
        {"deviceId": "1", "interfaceDescription": "eth0:uplink", "snmpSpeed": 1000}
    ),
    Interface.model_validate(
        {"deviceId": "1", "interfaceDescription": "eth1", "initialSnmpSpeed": 10}
    ),
    Interface.model_validate({"deviceId": "2", "interfaceDescription": "eth0"}),
]


def _lookup(**kwargs) -> DeviceLookup:
    return DeviceLookup(DEVICES, INTERFACES, **kwargs)


def test_devices_by_id_or_name():
    lookup = _lookup()

    assert lookup["router1"] is DEVICES[0]
    assert lookup[2] is DEVICES[1]
    assert lookup["2"] is DEVICES[1]
    assert lookup.get_by_id(1) is DEVICES[0]
    assert lookup["nope"] is None
    assert lookup.count == 2


def test_link_names_and_speeds_in_bits_per_second():
    lookup = _lookup()

    assert lookup.make_link(DEVICES[0], INTERFACES[0]) == "router1:eth0:uplink"
    speeds = lookup.get_link_speeds(
        ["router1:eth0:uplink", "router1:eth1", "router2:eth0"]
    )
    assert speeds["router1:eth0:uplink"] == 1e9
    assert speeds["router1:eth1"] == 1e7
    assert math.isnan(speeds["router2:eth0"])
    assert math.isnan(lookup.get_link_speeds(["nope:eth0"])["nope:eth0"])
    assert set(lookup.get_link_speeds()) == {
        "router1:eth0:uplink",
        "router1:eth1",
        "router2:eth0",
    }


def test_labels_select_devices():
    lookup = _lookup(labels=["edge"])

    assert [d.deviceName for d in lookup.all] == ["router1"]


def test_a_link_without_a_colon_is_refused():
    with pytest.raises(ValueError, match="not '<device name>:<interface"):
        _lookup().parse_link("router1")


def test_count_matches_iteration_with_a_duplicate_name():
    twin = DeviceDetailed.model_validate({"id": "3", "deviceName": "router1"})
    lookup = DeviceLookup([*DEVICES, twin])

    assert lookup.count == len(list(lookup)) == 3
    assert lookup.duplicate_names == 1


def test_save_and_load_round_trip_as_json(tmp_path: Path):
    path = tmp_path / "devices.json"
    _lookup(labels=["edge"]).save(path)

    json.loads(path.read_text())  # plain JSON, nothing that runs code
    loaded = DeviceLookup.load(path)

    assert loaded.labels == ["edge"]
    assert loaded["router1"] == DEVICES[0]
    assert loaded.get_link_speeds(["router1:eth0:uplink"]) == {
        "router1:eth0:uplink": 1e9
    }


@respx.mock
def test_from_api_loads_devices_and_interfaces_and_skips_deleted_ones():
    respx.get(url__regex=r".*/device/.*").respond(
        200,
        json={
            "devices": [
                {"id": "1", "deviceName": "router1", "deviceStatus": "V"},
                {"id": "3", "deviceName": "gone", "deviceStatus": "D"},
            ]
        },
    )
    respx.get(url__regex=r".*/interface/.*").respond(
        200, json={"interfaces": [{"deviceId": "1", "interfaceDescription": "eth0"}]}
    )
    client = KentikAPI("dev@example.com", "token", env_file=None)
    try:
        lookup = DeviceLookup.from_api(client)
    finally:
        client.close()

    assert [d.deviceName for d in lookup.all] == ["router1"]
    router1 = lookup["router1"]
    assert router1 is not None
    assert [i.interfaceDescription for i in lookup.interfaces(router1)] == ["eth0"]
