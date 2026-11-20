# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List alerts from the last 30 days.

Uses the list operation from the AlertService group.
The Kentik backend rejects the call with a 400 unless the filters carry a
startedAt time range, although the schema marks every field optional.
"""

from datetime import UTC, datetime, timedelta

from kentik_api.client import KentikAPI
from kentik_api.gen.alerting.models import (
    AlertFilters,
    AlertServiceListRequest,
    TimeRange,
)


def main() -> None:
    """List alerts over REST using a start-time filter."""
    client = KentikAPI(protocol="rest")

    now = datetime.now(UTC)
    started_at = TimeRange(
        start=(now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        end=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    request = AlertServiceListRequest(
        filters=AlertFilters(startedAt=started_at)
    )
    response = client.alerting.list(data=request)
    alerts = [alert for alert in (response.alerts or []) if alert is not None]
    print(f"Found {len(alerts)} alert(s) in the last 30 days.")
    for alert in alerts[:10]:
        sev = alert.severity if alert.severity else "-"
        print(f"  {alert.id}: severity={sev} state={alert.state}")


if __name__ == "__main__":
    main()
