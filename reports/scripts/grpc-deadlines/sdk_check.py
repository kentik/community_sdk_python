# Read-only: one List per affected service through the SDK's gRPC client, plus label.
from kentik_api.client import KentikAPI

client = KentikAPI(protocol="grpc")
calls = {
    "alerting": lambda: client.alerting.mitigation_methods_list(),
    "audit": lambda: client.audit.list_events(),
    "custom_application": lambda: client.custom_application.list(),
    "custom_dimension": lambda: client.custom_dimension.list(),
    "plan": lambda: client.plan.list(),
    "saved_filter": lambda: client.saved_filter.list(),
    "label": lambda: client.label.list(),
}
for name, call in calls.items():
    try:
        call()
        print(f"{name}: OK")
    except Exception as exc:  # noqa: BLE001
        print(f"{name}: {type(exc).__name__}: {str(exc)[:100]}")
client.close()
