from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class HostResources(_message.Message):
    __slots__ = (
        "cpu_num_cores",
        "cpu_used_cores",
        "mem_total_bytes",
        "mem_used_bytes",
        "disk_total_bytes",
        "disk_used_bytes",
    )
    CPU_NUM_CORES_FIELD_NUMBER: _ClassVar[int]
    CPU_USED_CORES_FIELD_NUMBER: _ClassVar[int]
    MEM_TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    MEM_USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISK_TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISK_USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    cpu_num_cores: int
    cpu_used_cores: float
    mem_total_bytes: int
    mem_used_bytes: int
    disk_total_bytes: int
    disk_used_bytes: int
    def __init__(
        self,
        cpu_num_cores: _Optional[int] = ...,
        cpu_used_cores: _Optional[float] = ...,
        mem_total_bytes: _Optional[int] = ...,
        mem_used_bytes: _Optional[int] = ...,
        disk_total_bytes: _Optional[int] = ...,
        disk_used_bytes: _Optional[int] = ...,
    ) -> None: ...

class ProcessResources(_message.Message):
    __slots__ = ("cpu_used_cores", "mem_used_bytes", "disk_used_bytes")
    CPU_USED_CORES_FIELD_NUMBER: _ClassVar[int]
    MEM_USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISK_USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    cpu_used_cores: float
    mem_used_bytes: int
    disk_used_bytes: int
    def __init__(
        self,
        cpu_used_cores: _Optional[float] = ...,
        mem_used_bytes: _Optional[int] = ...,
        disk_used_bytes: _Optional[int] = ...,
    ) -> None: ...
