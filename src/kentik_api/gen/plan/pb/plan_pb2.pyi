from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from . import plan_message_pb2 as _plan_message_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class ListPlansRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListPlansResponse(_message.Message):
    __slots__ = ("plans",)
    PLANS_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[_plan_message_pb2.Plan]
    def __init__(
        self,
        plans: _Optional[_Iterable[_Union[_plan_message_pb2.Plan, _Mapping]]] = ...,
    ) -> None: ...
