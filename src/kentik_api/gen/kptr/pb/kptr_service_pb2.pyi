from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from . import ptr_result_pb2 as _ptr_result_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateAddressNamesRequest(_message.Message):
    __slots__ = ("address_names",)
    ADDRESS_NAMES_FIELD_NUMBER: _ClassVar[int]
    address_names: _containers.RepeatedCompositeFieldContainer[
        _ptr_result_pb2.PtrResult
    ]
    def __init__(
        self,
        address_names: _Optional[
            _Iterable[_Union[_ptr_result_pb2.PtrResult, _Mapping]]
        ] = ...,
    ) -> None: ...

class UpdateAddressNamesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNetworkRangeAssignmentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNetworkRangeAssignmentsResponse(_message.Message):
    __slots__ = ("network_ranges",)
    NETWORK_RANGES_FIELD_NUMBER: _ClassVar[int]
    network_ranges: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, network_ranges: _Optional[_Iterable[str]] = ...) -> None: ...

class ResolveAddressesRequest(_message.Message):
    __slots__ = ("ip_addresses",)
    IP_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    ip_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ip_addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class ResolveAddressesResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[_ptr_result_pb2.PtrResult]
    def __init__(
        self,
        results: _Optional[
            _Iterable[_Union[_ptr_result_pb2.PtrResult, _Mapping]]
        ] = ...,
    ) -> None: ...

class ListResolvedAddressesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListResolvedAddressesResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[_ptr_result_pb2.PtrResult]
    def __init__(
        self,
        results: _Optional[
            _Iterable[_Union[_ptr_result_pb2.PtrResult, _Mapping]]
        ] = ...,
    ) -> None: ...
