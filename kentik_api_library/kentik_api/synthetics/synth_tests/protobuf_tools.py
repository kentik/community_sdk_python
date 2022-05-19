from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp


def pb_to_datetime_utc(t: Timestamp) -> datetime:
    return datetime.fromtimestamp(t.seconds, timezone.utc)


def pb_from_datetime(dt: datetime) -> Timestamp:
    seconds = int(dt.timestamp())
    return Timestamp(seconds=seconds, nanos=0)
