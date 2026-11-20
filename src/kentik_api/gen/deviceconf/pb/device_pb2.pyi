import datetime
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class DevicePlatform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEVICE_PLATFORM_UNSPECIFIED: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_ARISTA_EOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_ARUBA_WLC: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_CISCO_IOSXE: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_CISCO_IOSXR: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_CISCO_NXOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_CISCO_IOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_CUMULUS_LINUX: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_CUMULUS_VTYSH: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_HP_COMWARE: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_HUAWEI_VRP: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_IPINFUSION_OCNOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_JUNIPER_JUNOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_NOKIA_SRL: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_NOKIA_SROS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_NOKIA_SROS_CLASSIC: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_PALOALTO_PANOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_RUIJIE_RGOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_VYATTA_VYOS: _ClassVar[DevicePlatform]
    DEVICE_PLATFORM_UBIQUITI_EDGEOS: _ClassVar[DevicePlatform]

DEVICE_PLATFORM_UNSPECIFIED: DevicePlatform
DEVICE_PLATFORM_ARISTA_EOS: DevicePlatform
DEVICE_PLATFORM_ARUBA_WLC: DevicePlatform
DEVICE_PLATFORM_CISCO_IOSXE: DevicePlatform
DEVICE_PLATFORM_CISCO_IOSXR: DevicePlatform
DEVICE_PLATFORM_CISCO_NXOS: DevicePlatform
DEVICE_PLATFORM_CISCO_IOS: DevicePlatform
DEVICE_PLATFORM_CUMULUS_LINUX: DevicePlatform
DEVICE_PLATFORM_CUMULUS_VTYSH: DevicePlatform
DEVICE_PLATFORM_HP_COMWARE: DevicePlatform
DEVICE_PLATFORM_HUAWEI_VRP: DevicePlatform
DEVICE_PLATFORM_IPINFUSION_OCNOS: DevicePlatform
DEVICE_PLATFORM_JUNIPER_JUNOS: DevicePlatform
DEVICE_PLATFORM_NOKIA_SRL: DevicePlatform
DEVICE_PLATFORM_NOKIA_SROS: DevicePlatform
DEVICE_PLATFORM_NOKIA_SROS_CLASSIC: DevicePlatform
DEVICE_PLATFORM_PALOALTO_PANOS: DevicePlatform
DEVICE_PLATFORM_RUIJIE_RGOS: DevicePlatform
DEVICE_PLATFORM_VYATTA_VYOS: DevicePlatform
DEVICE_PLATFORM_UBIQUITI_EDGEOS: DevicePlatform

class DeviceSSHCreds(_message.Message):
    __slots__ = ("username", "private_key", "passphrase")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    username: str
    private_key: str
    passphrase: str
    def __init__(
        self,
        username: _Optional[str] = ...,
        private_key: _Optional[str] = ...,
        passphrase: _Optional[str] = ...,
    ) -> None: ...

class FetchParameters(_message.Message):
    __slots__ = ("fetch_interval", "fetch_timeout")
    FETCH_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    FETCH_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    fetch_interval: _duration_pb2.Duration
    fetch_timeout: _duration_pb2.Duration
    def __init__(
        self,
        fetch_interval: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
        fetch_timeout: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
    ) -> None: ...

class Device(_message.Message):
    __slots__ = ("id", "name", "hostname", "platform", "ssh_creds", "fetch_params")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    SSH_CREDS_FIELD_NUMBER: _ClassVar[int]
    FETCH_PARAMS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    hostname: str
    platform: DevicePlatform
    ssh_creds: DeviceSSHCreds
    fetch_params: FetchParameters
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        hostname: _Optional[str] = ...,
        platform: _Optional[_Union[DevicePlatform, str]] = ...,
        ssh_creds: _Optional[_Union[DeviceSSHCreds, _Mapping]] = ...,
        fetch_params: _Optional[_Union[FetchParameters, _Mapping]] = ...,
    ) -> None: ...
