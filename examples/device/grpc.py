# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List all devices in the account (gRPC transport)."""

from kentik_api.client import KentikAPI
from kentik_api.errors import KentikError


def main() -> None:
    """List devices over gRPC and print up to five entries."""
    display_limit = 5
    client = KentikAPI(protocol="grpc")
    try:
        response = client.device.list()
        devices = [
            device for device in (response.devices or []) if device is not None
        ]
        print(f"Found {len(devices)} device(s).")
        for device in devices[:display_limit]:
            print(f"  {device.id}: {device.deviceName}")
        if len(devices) > display_limit:
            print(f"  ... and {len(devices) - display_limit} more.")
    except KentikError as exc:
        print(f"API error over gRPC: {exc}")


if __name__ == "__main__":
    main()
