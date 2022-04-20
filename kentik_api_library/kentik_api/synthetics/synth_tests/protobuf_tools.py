from datetime import datetime, timezone
from typing import Any, Dict, Iterable

from google.protobuf.timestamp_pb2 import Timestamp


def pb_to_datetime_utc(t: Timestamp) -> datetime:
    return datetime.fromtimestamp(t.seconds, timezone.utc)


def pb_from_datetime(dt: datetime) -> Timestamp:
    seconds = int(dt.timestamp())
    return Timestamp(seconds=seconds, nanos=0)


def pb_assign_collection(src: Iterable[Any], dst) -> None:
    """Assignment prosthesis for protobuf lists that lack assignment functionality"""

    while len(dst):
        dst.pop()
    dst.extend(src)


def pb_assign_map(src: Dict[Any, Any], dst) -> None:
    """Assignment prosthesis for protobuf maps that lack assignment functionality"""

    while len(dst):
        dst.pop()
    dst.update(src)
