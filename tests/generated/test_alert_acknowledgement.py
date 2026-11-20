# HAND-WRITTEN: not modified by `uv run poe generate`.
"""An alert that carries an acknowledgement must parse (audit finding B2)."""

from __future__ import annotations

from kentik_api.gen.alerting.models import (
    Alert,
    AlertAcknowledgement,
    v202505AlertAcknowledgement,
)


def test_alert_acknowledgement_is_the_object_not_the_state_enum():
    state = next(iter(v202505AlertAcknowledgement))

    alert = Alert.model_validate(
        {
            "acknowledgement": {
                "state": state.value,
                "ackedByUser": "ops@example.com",
                "autoAckId": "7",
                "ackedAt": "2026-10-13T00:00:00Z",
            }
        }
    )

    assert isinstance(alert.acknowledgement, AlertAcknowledgement)
    assert alert.acknowledgement.state == state
    assert alert.acknowledgement.ackedByUser == "ops@example.com"
