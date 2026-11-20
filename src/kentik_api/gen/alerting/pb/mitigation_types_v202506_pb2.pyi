from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

from kentik_api.gen.ktbgp.pb import route_service_pb2 as _route_service_pb2

from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class MitigationTarget(_message.Message):
    __slots__ = ("ip_cidr", "flowspec", "adaptive_flowspec")
    IP_CIDR_FIELD_NUMBER: _ClassVar[int]
    FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    ADAPTIVE_FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    ip_cidr: str
    flowspec: _route_service_pb2.FlowspecMatch
    adaptive_flowspec: _types_pb2.KeyValue
    def __init__(
        self,
        ip_cidr: _Optional[str] = ...,
        flowspec: _Optional[_Union[_route_service_pb2.FlowspecMatch, _Mapping]] = ...,
        adaptive_flowspec: _Optional[_Union[_types_pb2.KeyValue, _Mapping]] = ...,
    ) -> None: ...
