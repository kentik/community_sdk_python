# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Live reads that fail because of an upstream bug, and the bug each one hits.

Both read suites mark these as strict xfails. Any other 5xx still fails the
suite. When upstream fixes a bug, its reads pass, strict xfail reports XPASS,
and the entry here must go.
"""

from __future__ import annotations

UNKNOWN_ID = "Upstream: an ID that does not exist answers 500, not 404"
MALFORMED_ID = "Upstream: a malformed ID answers 500, not 400"
NOT_IMPLEMENTED = (
    "Upstream: the schema publishes this operation, but the server answers 501"
)

_BOTH = ("rest", "grpc")

SERVER_ERRORS: dict[str, tuple[str, tuple[str, ...]]] = {
    "AlertingServiceWrapper.auto_ack_get": (UNKNOWN_ID, _BOTH),
    "AlertingServiceWrapper.list_comments": (UNKNOWN_ID, _BOTH),
    "AlertingServiceWrapper.silence_notifications_get": (UNKNOWN_ID, _BOTH),
    "AlertingServiceWrapper.suppression_get": (UNKNOWN_ID, _BOTH),
    "AuditServiceWrapper.get_event": (UNKNOWN_ID, _BOTH),
    "AuditServiceWrapper.get_event_by_ctime": (UNKNOWN_ID, _BOTH),
    "VaultServiceWrapper.get_secret": (UNKNOWN_ID, _BOTH),
    "VaultServiceWrapper.list_secret": (UNKNOWN_ID, _BOTH),
    "AlertingServiceWrapper.mitigations_get": (MALFORMED_ID, _BOTH),
    # REST rejects the sample policyType first; gRPC sends a valid one.
    "AlertingServiceWrapper.policy_get": (MALFORMED_ID, ("grpc",)),
    "CustomApplicationServiceWrapper.get": (MALFORMED_ID, _BOTH),
    "KmiServiceWrapper.get_asn_insights": (MALFORMED_ID, _BOTH),
    "KagentServiceWrapper.get_capability": (NOT_IMPLEMENTED, _BOTH),
    "KagentServiceWrapper.list_capabilities": (NOT_IMPLEMENTED, _BOTH),
    "KmetaServiceWrapper.get_service_now_config": (NOT_IMPLEMENTED, _BOTH),
    "KmetaServiceWrapper.list_service_now_configs": (NOT_IMPLEMENTED, _BOTH),
    "SyntheticsServiceWrapper.get_bulk_update_tests_status": (NOT_IMPLEMENTED, _BOTH),
}


def server_error(operation: str, transport: str) -> str | None:
    """The upstream bug that `operation` hits on `transport`, if any."""
    reason, transports = SERVER_ERRORS.get(operation, (None, ()))
    return reason if transport in transports else None
