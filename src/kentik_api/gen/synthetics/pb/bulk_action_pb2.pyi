import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import synthetics_pb2 as _synthetics_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class BulkActionItemState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BULK_ACTION_ITEM_STATE_UNSPECIFIED: _ClassVar[BulkActionItemState]
    BULK_ACTION_ITEM_STATE_PENDING: _ClassVar[BulkActionItemState]
    BULK_ACTION_ITEM_STATE_PROCESSING: _ClassVar[BulkActionItemState]
    BULK_ACTION_ITEM_STATE_SUCCEEDED: _ClassVar[BulkActionItemState]
    BULK_ACTION_ITEM_STATE_FAILED: _ClassVar[BulkActionItemState]

class BulkActionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BULK_ACTION_STATE_UNSPECIFIED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_SUBMITTED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_RUNNING: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_PAUSED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_COMPLETED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_FAILED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_CANCELLED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_TERMINATED: _ClassVar[BulkActionState]
    BULK_ACTION_STATE_TIMED_OUT: _ClassVar[BulkActionState]

class BulkFieldOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BULK_FIELD_OP_UNSPECIFIED: _ClassVar[BulkFieldOp]
    BULK_FIELD_OP_REPLACE: _ClassVar[BulkFieldOp]
    BULK_FIELD_OP_ADD: _ClassVar[BulkFieldOp]
    BULK_FIELD_OP_REMOVE: _ClassVar[BulkFieldOp]

BULK_ACTION_ITEM_STATE_UNSPECIFIED: BulkActionItemState
BULK_ACTION_ITEM_STATE_PENDING: BulkActionItemState
BULK_ACTION_ITEM_STATE_PROCESSING: BulkActionItemState
BULK_ACTION_ITEM_STATE_SUCCEEDED: BulkActionItemState
BULK_ACTION_ITEM_STATE_FAILED: BulkActionItemState
BULK_ACTION_STATE_UNSPECIFIED: BulkActionState
BULK_ACTION_STATE_SUBMITTED: BulkActionState
BULK_ACTION_STATE_RUNNING: BulkActionState
BULK_ACTION_STATE_PAUSED: BulkActionState
BULK_ACTION_STATE_COMPLETED: BulkActionState
BULK_ACTION_STATE_FAILED: BulkActionState
BULK_ACTION_STATE_CANCELLED: BulkActionState
BULK_ACTION_STATE_TERMINATED: BulkActionState
BULK_ACTION_STATE_TIMED_OUT: BulkActionState
BULK_FIELD_OP_UNSPECIFIED: BulkFieldOp
BULK_FIELD_OP_REPLACE: BulkFieldOp
BULK_FIELD_OP_ADD: BulkFieldOp
BULK_FIELD_OP_REMOVE: BulkFieldOp

class BulkActionItemStatus(_message.Message):
    __slots__ = ("id", "state", "error", "error_type", "field")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    id: str
    state: BulkActionItemState
    error: str
    error_type: str
    field: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        state: _Optional[_Union[BulkActionItemState, str]] = ...,
        error: _Optional[str] = ...,
        error_type: _Optional[str] = ...,
        field: _Optional[str] = ...,
    ) -> None: ...

class BulkActionStatus(_message.Message):
    __slots__ = (
        "workflow_id",
        "state",
        "start_time",
        "end_time",
        "total_count",
        "succeeded_count",
        "failed_count",
        "pending_count",
        "items",
        "skipped_count",
        "skipped",
    )
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_COUNT_FIELD_NUMBER: _ClassVar[int]
    PENDING_COUNT_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    state: BulkActionState
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    total_count: int
    succeeded_count: int
    failed_count: int
    pending_count: int
    items: _containers.RepeatedCompositeFieldContainer[BulkActionItemStatus]
    skipped_count: int
    skipped: _containers.RepeatedCompositeFieldContainer[BulkActionItemStatus]
    def __init__(
        self,
        workflow_id: _Optional[str] = ...,
        state: _Optional[_Union[BulkActionState, str]] = ...,
        start_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        total_count: _Optional[int] = ...,
        succeeded_count: _Optional[int] = ...,
        failed_count: _Optional[int] = ...,
        pending_count: _Optional[int] = ...,
        items: _Optional[_Iterable[_Union[BulkActionItemStatus, _Mapping]]] = ...,
        skipped_count: _Optional[int] = ...,
        skipped: _Optional[_Iterable[_Union[BulkActionItemStatus, _Mapping]]] = ...,
    ) -> None: ...

class BulkFieldOpRule(_message.Message):
    __slots__ = ("mask", "op")
    MASK_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    mask: _field_mask_pb2.FieldMask
    op: BulkFieldOp
    def __init__(
        self,
        mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
        op: _Optional[_Union[BulkFieldOp, str]] = ...,
    ) -> None: ...

class BulkUpdateTestsRequest(_message.Message):
    __slots__ = ("ids", "test", "mask", "ops", "allow_partial_batch")
    IDS_FIELD_NUMBER: _ClassVar[int]
    TEST_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    OPS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_BATCH_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    test: _synthetics_pb2.Test
    mask: _field_mask_pb2.FieldMask
    ops: _containers.RepeatedCompositeFieldContainer[BulkFieldOpRule]
    allow_partial_batch: bool
    def __init__(
        self,
        ids: _Optional[_Iterable[str]] = ...,
        test: _Optional[_Union[_synthetics_pb2.Test, _Mapping]] = ...,
        mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
        ops: _Optional[_Iterable[_Union[BulkFieldOpRule, _Mapping]]] = ...,
        allow_partial_batch: _Optional[bool] = ...,
    ) -> None: ...

class BulkUpdateTestsResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: BulkActionStatus
    def __init__(
        self, status: _Optional[_Union[BulkActionStatus, _Mapping]] = ...
    ) -> None: ...

class GetBulkUpdateTestsStatusRequest(_message.Message):
    __slots__ = ("workflow_id",)
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    def __init__(self, workflow_id: _Optional[str] = ...) -> None: ...

class GetBulkUpdateTestsStatusResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: BulkActionStatus
    def __init__(
        self, status: _Optional[_Union[BulkActionStatus, _Mapping]] = ...
    ) -> None: ...
