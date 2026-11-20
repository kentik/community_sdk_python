# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Find devices and interfaces by ID or name, and get link speeds.

The 2.x replacement of 1.x `kentik_api.utils.DeviceCache`. It loads devices
and interfaces once through the V6 `device` and `interface` services, and saves
and loads them as JSON, never pickle, so a lookup file cannot run code.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, TextIO

from kentik_api.gen.device.models import DeviceDetailed
from kentik_api.gen.interface.models import Interface

if TYPE_CHECKING:
    from kentik_api.client import KentikAPI

log = logging.getLogger(__name__)


class DeviceLookup:
    @classmethod
    def from_api(
        cls,
        client: KentikAPI,
        labels: Iterable[str] | None = None,
        include_deleted: bool = False,
    ) -> DeviceLookup:
        """Loads every device and interface. Deleted devices only on request."""
        devices = [
            d
            for d in client.device.list().devices or []
            if d is not None and (include_deleted or d.deviceStatus != "D")
        ]
        interfaces = [
            i for i in client.interface.list().interfaces or [] if i is not None
        ]
        return cls(devices, interfaces, labels)

    @classmethod
    def load(cls, path: str | os.PathLike[str]) -> DeviceLookup:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            [DeviceDetailed.model_validate(d) for d in data["devices"]],
            [Interface.model_validate(i) for i in data["interfaces"]],
            data.get("labels"),
        )

    def __init__(
        self,
        devices: Iterable[DeviceDetailed],
        interfaces: Iterable[Interface] = (),
        labels: Iterable[str] | None = None,
    ) -> None:
        self.labels = list(labels) if labels else None
        wanted = frozenset(self.labels or ())
        self._by_name: dict[str, DeviceDetailed] = {}
        self._by_id: dict[str, DeviceDetailed] = {}
        self.duplicate_names = 0
        for device in devices:
            names = {label.name for label in device.labels or [] if label is not None}
            if wanted and not wanted <= names:
                continue
            if device.deviceName in self._by_name:
                log.warning("Duplicate device name: %s", device.deviceName)
                self.duplicate_names += 1
            elif device.deviceName:
                self._by_name[device.deviceName] = device
            if device.id is not None:
                self._by_id.setdefault(device.id, device)
        self._interfaces: dict[str, dict[str, Interface]] = {}
        for interface in interfaces:
            if interface.deviceId in self._by_id and interface.interfaceDescription:
                self._interfaces.setdefault(interface.deviceId, {})[
                    interface.interfaceDescription
                ] = interface

    def __repr__(self) -> str:
        return f"DeviceLookup: {self.count} devices"

    def __iter__(self) -> Iterator[DeviceDetailed]:
        return iter(sorted(self._by_id.values(), key=lambda d: int(d.id or 0)))

    def __getitem__(self, id_or_name: str | int) -> DeviceDetailed | None:
        """A device by numeric ID (int or digit string) or by name."""
        key = str(id_or_name)
        return self._by_id.get(key) if key.isdigit() else self._by_name.get(key)

    @property
    def count(self) -> int:
        return len(self._by_id)

    @property
    def all(self) -> Iterator[DeviceDetailed]:
        yield from self._by_name.values()

    def get_by_id(self, device_id: str | int) -> DeviceDetailed | None:
        return self._by_id.get(str(device_id))

    def interfaces(self, device: DeviceDetailed) -> list[Interface]:
        return list(self._interfaces.get(device.id or "", {}).values())

    def info(self, out: TextIO | None = None) -> None:
        print(f"{self.count:5} devices", file=out)
        if self.labels is not None:
            print(f"matching labels: {','.join(self.labels)}", file=out)
        print(f"{self.duplicate_names:5} duplicate names", file=out)

    @staticmethod
    def make_link(device: DeviceDetailed, interface: Interface) -> str:
        """A link name: `<device name>:<interface description>`."""
        return f"{device.deviceName}:{interface.interfaceDescription}"

    def parse_link(self, link: str) -> tuple[DeviceDetailed | None, Interface | None]:
        # Interface descriptions may contain colons; device names cannot.
        name, sep, description = link.partition(":")
        if not sep:
            raise ValueError(
                f"Link {link!r} is not '<device name>:<interface description>'"
            )
        device = self._by_name.get(name)
        if device is None:
            log.warning("Device %s not in the lookup", name)
            return None, None
        interface = self._interfaces.get(device.id or "", {}).get(description)
        if interface is None:
            log.warning("Device %s has no interface named %s", name, description)
        return device, interface

    def get_link_speeds(self, links: Iterable[str] | None = None) -> dict[str, float]:
        """Link speed in bits/s for each link, NaN when it is unknown."""
        if links is None:
            return {
                self.make_link(device, interface): _speed(interface)
                for device in self.all
                for interface in self.interfaces(device)
            }
        speeds: dict[str, float] = {}
        for link in links:
            _, interface = self.parse_link(link)
            speeds[link] = float("nan") if interface is None else _speed(interface)
        return speeds

    def save(self, path: str | os.PathLike[str]) -> None:
        data = {
            "labels": self.labels,
            "devices": [
                d.model_dump(mode="json", by_alias=True) for d in self._by_id.values()
            ],
            "interfaces": [
                i.model_dump(mode="json", by_alias=True)
                for by_name in self._interfaces.values()
                for i in by_name.values()
            ],
        }
        Path(path).write_text(json.dumps(data), encoding="utf-8")


def _speed(interface: Interface) -> float:
    # SNMP speed is in Mbit/s.
    speed = (
        interface.snmpSpeed
        if interface.snmpSpeed is not None
        else interface.initialSnmpSpeed
    )
    return float("nan") if speed is None else float(speed) * 1e6
