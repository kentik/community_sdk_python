# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List alerts from the last 30 days, gRPC transport.

Uses the list operation from the AlertService group.
The Kentik backend rejects the call unless the filters carry a startedAt time
range, although the schema marks every field optional.
On the test account, alerting gRPC calls fail with a server 500 RangeError.
REST calls work.
"""

from datetime import UTC, datetime, timedelta

from kentik_api.client import KentikAPI
from kentik_api.errors import KentikError
from kentik_api.gen.alerting.models import (
    AlertFilters,
    AlertServiceListRequest,
    TimeRange,
)


def main() -> None:
    """List alerts over gRPC using a start-time filter."""
    client = KentikAPI(protocol="grpc")
    now = datetime.now(UTC)
    started_at = TimeRange(
        start=(now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        end=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    request = AlertServiceListRequest(
        filters=AlertFilters(startedAt=started_at)
    )
    try:
        response = client.alerting.list(data=request)
        alerts = [
            alert for alert in (response.alerts or []) if alert is not None
        ]
        print(f"Found {len(alerts)} alert(s) in the last 30 days.")
        for alert in alerts[:10]:
            sev = alert.severity if alert.severity else "-"
            print(f"  {alert.id}: severity={sev} state={alert.state}")
    except KentikError as exc:
        print(f"API error over gRPC: {exc}")


if __name__ == "__main__":
    main()
