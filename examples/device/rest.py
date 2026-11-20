# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List all devices in the account."""

from kentik_api.client import KentikAPI


def main() -> None:
    """List devices over REST and print up to five entries."""
    display_limit = 5
    client = KentikAPI(
        protocol="rest"
    )  # loads KENTIK_EMAIL / KENTIK_API_TOKEN from .env
    response = client.device.list()
    devices = [
        device for device in (response.devices or []) if device is not None
    ]
    print(f"Found {len(devices)} device(s).")
    for device in devices[:display_limit]:
        print(f"  {device.id}: {device.deviceName}")
    if len(devices) > display_limit:
        print(f"  ... and {len(devices) - display_limit} more.")


if __name__ == "__main__":
    main()
