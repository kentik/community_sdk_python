# Read-only: the list calls that 500 in the e2e suite, called with no optional arguments.
from functools import partial

from kentik_api.client import KentikAPI

for protocol in ("rest", "grpc"):
    client = KentikAPI(protocol=protocol)
    calls = {
        "alerting.mitigation_methods_list": client.alerting.mitigation_methods_list,
        "alerting.mitigation_platforms_list": client.alerting.mitigation_platforms_list,
        "cost.list_provider_summaries": client.cost.list_provider_summaries,
        "interface.list": client.interface.list,
        "synthetics.list_agent_alerts": client.synthetics.list_agent_alerts,
        "vault.list_secret": partial(
            client.vault.list_secret, names=["sdk-e2e-test-missing-secret"]
        ),
    }
    for name, call in calls.items():
        try:
            call()
            print(f"{protocol:4} {name}: OK")
        except Exception as exc:  # noqa: BLE001
            print(f"{protocol:4} {name}: {type(exc).__name__}: {str(exc)[:110]}")
    client.close()
