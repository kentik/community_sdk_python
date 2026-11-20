# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Live check of alerting.list, a read-only POST the auto-discovered suite skips.

The Kentik backend returns a 400 unless the filters carry a startedAt range,
although the schema marks every field optional. Every alert returned must also
parse, so `Alert.acknowledgement` stays an object model (the B2 regression).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from kentik_api.gen.alerting.models import (
    AlertAcknowledgement,
    AlertFilters,
    AlertServiceListRequest,
    TimeRange,
)


def _last_30_days_request() -> AlertServiceListRequest:
    now = datetime.now(UTC)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    started_at = TimeRange(
        start=(now - timedelta(days=30)).strftime(fmt), end=now.strftime(fmt)
    )
    return AlertServiceListRequest(filters=AlertFilters(startedAt=started_at))


def _assert_alerts_parse(response) -> None:
    for alert in response.alerts or []:
        if alert is not None and alert.acknowledgement is not None:
            assert isinstance(alert.acknowledgement, AlertAcknowledgement)


@pytest.mark.e2e
def test_alert_list_with_started_at_over_rest(real_client):
    response = real_client.alerting.list(data=_last_30_days_request())
    _assert_alerts_parse(response)


@pytest.mark.e2e_grpc
def test_alert_list_with_started_at_over_grpc(grpc_real_client):
    response = grpc_real_client.alerting.list(data=_last_30_days_request())
    _assert_alerts_parse(response)
