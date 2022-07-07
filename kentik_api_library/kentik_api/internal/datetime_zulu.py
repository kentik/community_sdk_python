from datetime import datetime


def from_iso_format_zulu(date_time: str) -> datetime:
    """Support for 'Z' suffix in ISO 8601 datetime parsing"""

    no_zulu = date_time.replace("Z", "+00:00")  # Z stands for Zero (timezone UTC)
    return datetime.fromisoformat(no_zulu)
