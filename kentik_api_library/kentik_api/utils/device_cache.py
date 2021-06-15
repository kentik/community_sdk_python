import logging
import pickle
import sys
from pathlib import Path
from kentik_api import KentikAPI
from kentik_api.public import Device
from typing import Dict, List, Generator, Optional, TypeVar


class DeviceCacheIterator:
    def __init__(self, devices) -> None:
        self.devices = devices
        self.id_list = sorted([d.id for d in devices.all])

    def __next__(self):
        try:
            return self.devices[self.id_list.pop(0)]
        except IndexError:
            raise StopIteration


T = TypeVar('T')


class DeviceCache:
    @classmethod
    def from_api(cls, api: KentikAPI, labels: Optional[List[str]] = None) -> T:
        logging.debug('Fetching all devices')
        devices = api.devices.get_all()
        return cls(devices, labels)

    @classmethod
    def from_pickle(cls, filename: str) -> T:
        file = Path(filename)
        logging.debug(f'Reading device data from {file.resolve()}')
        return pickle.load(file.open('rb'))

    def __init__(self, devices: List[Device], labels: Optional[List[str]] = None) -> None:
        self._devices_by_name = dict()
        self._devices_by_id = dict()
        self.duplicate_names = 0
        self.labels = labels

        if labels:
            label_set = frozenset(labels)
        else:
            label_set = frozenset()
        for device in devices:
            if label_set and not label_set.issubset(set([label.name for label in device.labels])):
                logging.debug('Ignoring device: %s (id: %d)', device.device_name, device.id)
                continue
            if device.device_name in self._devices_by_name:
                logging.critical('Duplicate device name: %s', device.device_name)
                self.duplicate_names += 1
            else:
                self._devices_by_name[device.device_name] = device
            if device.id in self._devices_by_id:
                logging.critical('Duplicate device id: %%d', device.id)
            else:
                self._devices_by_id[device.id] = device
        logging.debug('Got %d devices (%d duplicate names)', len(self._devices_by_name), self.duplicate_names)

    def __repr__(self) -> str:
        return f'DeviceCache: {self.count} devices'

    def __iter__(self):
        return DeviceCacheIterator(self)

    def __getitem__(self, item):
        logging.debug('__getitem__: item: %s', item)
        if type(item) == int:
            return self._devices_by_id.get(item)
        else:
            return self._devices_by_name.get(item)

    def info(self, out=sys.stdout) -> None:
        print('{:5} devices'.format(len(self._devices_by_name)), file=out)
        if self.labels is not None:
            print('matching labels: {}'.format(','.join(self.labels)), file=out)
        print('{:5} duplicate names'.format(self.duplicate_names), file=out)

    @property
    def count(self) -> int:
        return len(self._devices_by_name)

    @property
    def all(self) -> Generator[Device, None, None]:
        for d in self._devices_by_name.values():
            yield d

    def get_by_id(self, device_id: int) -> Optional[Device]:
        return self._devices_by_id.get(device_id)

    def get_link_speeds(self, links: Optional[str] = None) -> Dict:
        """
        Return dictionary of link speeds. Link = '<device_name>:<interface_name>'
        :param links: List of links to consider. If None is provided, all interfaces of all devices in the cache are
                      considered
        :return: dictionary keyed by link and value corresponding speed (in bits/s). If device is not in the cache
                 or does not have specified interface, or speed information is not available, the link has undefined
                 speed represented as floating point 'NaN'
        """
        speeds = dict()
        if links is None:
            for device in self._devices_by_name.values():
                for ifc in device.interfaces:
                    speeds[':'.join((device.device_name, ifc.name))] = ifc.speed
        else:
            for link in links:
                # interface names may contain colons, device names cannot
                d, i = link.split(':', maxsplit=1)
                device = self._devices_by_name.get(d)
                if device is None:
                    logging.critical('Device %s not in cache', d)
                    speeds[link] = float('NaN')
                else:
                    ifc = device.get_interface(i)
                    if ifc is None:
                        logging.critical('Device %s had no interface named %s', device.device_name, i)
                    speeds[link] = ifc.speed
        return speeds

    def to_pickle(self, filename: str) -> None:
        """
        Pickle device cache to file
        :param filename: Output file name
        """
        with Path(filename).open('wb') as f:
            pickle.dump(self, f)
