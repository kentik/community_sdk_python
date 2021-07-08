import logging
from datetime import datetime, timedelta
from typing import Generator

log = logging.getLogger("time_sequence")


def time_seq(start: datetime, end: datetime, step: timedelta) -> Generator[datetime, None, None]:
    """
    Generate datetime objects
    :param start: start timestamp
    :param end: end timestamp (not included in the range)
    :param step: interval in which timestamps are generated
    :return: yields datetime objects
    """
    cur = start
    while cur < end:
        yield cur
        cur += step
