import logging
import pickle
import sys
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Type, TypeVar

from kentik_api import KentikAPI
from kentik_api.public import Device, DeviceInterface
from kentik_api.public.types import ID

log = logging.getLogger("device_cache")


class DeviceCacheIterator:
    def __init__(self, devices) -> None:
        self.devices = devices
        self.id_list = sorted([d.id for d in devices.all])

    def __next__(self):
        try:
            return self.devices[self.id_list.pop(0)]
        except IndexError:
            raise StopIteration


T = TypeVar("T", bound="DeviceCache")


class DeviceCache:
    @classmethod
    def from_api(cls: Type[T], api: KentikAPI, labels: Optional[List[str]] = None) -> T:
        log.debug("Fetching all devices")
        devices = api.devices.get_all()
        return cls(devices, labels)

    @classmethod
    def from_pickle(cls: Type[T], filename: str) -> T:
        file = Path(filename)
        log.debug(f"Reading device data from {file.resolve()}")
        with file.open("rb") as f:
            return pickle.load(f)

    def __init__(self, devices: List[Device], labels: Optional[List[str]] = None) -> None:
        self._devices_by_name: Dict[str, Device] = dict()
        self._devices_by_id: Dict[ID, Device] = dict()
        self.duplicate_names = 0
        self.labels = labels

        if labels:
            label_set = frozenset(labels)
        else:
            label_set = frozenset()
        for device in devices:
            if label_set and not label_set.issubset(set([label.name for label in device.labels])):
                log.debug("Ignoring device: %s (id: %d)", device.device_name, device.id)
                continue
            if device.device_name in self._devices_by_name:
                log.critical("Duplicate device name: %s", device.device_name)
                self.duplicate_names += 1
            else:
                self._devices_by_name[device.device_name] = device
            if device.id in self._devices_by_id:
                log.critical("Duplicate device id: %d", device.id)
            else:
                self._devices_by_id[device.id] = device
        log.debug(
            "Got %d devices (%d duplicate names)",
            len(self._devices_by_name),
            self.duplicate_names,
        )

    def __repr__(self) -> str:
        return f"DeviceCache: {self.count} devices"

    def __iter__(self):
        return DeviceCacheIterator(self)

    def __getitem__(self, item):
        if type(item) == int:
            return self._devices_by_id.get(item)
        else:
            return self._devices_by_name.get(item)

    def info(self, out=sys.stdout) -> None:
        print("{:5} devices".format(len(self._devices_by_name)), file=out)
        if self.labels is not None:
            print("matching labels: {}".format(",".join(self.labels)), file=out)
        print("{:5} duplicate names".format(self.duplicate_names), file=out)

    @property
    def count(self) -> int:
        return len(self._devices_by_name)

    @property
    def all(self) -> Generator[Device, None, None]:
        for d in self._devices_by_name.values():
            yield d

    def get_by_id(self, device_id: ID) -> Optional[Device]:
        return self._devices_by_id.get(device_id)

    @staticmethod
    def make_link(device: Device, ifc: DeviceInterface) -> str:
        return f"{device.device_name}:{ifc.name}"

    def parse_link(self, link: str) -> Tuple[Optional[Device], Optional[DeviceInterface]]:
        d, i = link.split(":", maxsplit=1)
        device = self._devices_by_name.get(d)
        if device is None:
            log.critical("Device %s not in cache", d)
            ifc = None
        else:
            ifc = device.get_interface(i)
            if ifc is None:
                log.critical("Device %s has no interface named %s", device.device_name, i)
        return device, ifc

    def get_link_speeds(self, links: Optional[str] = None) -> Dict[str, float]:
        """
        Return dictionary of link speeds. Link = '<device_name>:<interface_name>'
        :param links: List of links to consider. If None is provided, all interfaces of all devices in the cache are
                      considered
        :return: dictionary keyed by link and value corresponding speed (in bits/s). If device is not in the cache
                 or does not have specified interface, or speed information is not available, the link has undefined
                 speed represented as floating point 'NaN'
        """
        speeds: Dict[str, float] = dict()
        if links is None:
            speeds = {self.make_link(d, i): i.speed for d in self.all for i in d.interfaces}
        else:
            for link in links:
                # interface names may contain colons, device names cannot
                device, ifc = self.parse_link(link)
                if device is None or ifc is None:
                    speeds[link] = float("NaN")
                else:
                    speeds[link] = ifc.speed
        return speeds

    def to_pickle(self, filename: str) -> None:
        """
        Pickle device cache to file
        :param filename: Output file name
        """
        with Path(filename).open("wb") as f:
            pickle.dump(self, f)
