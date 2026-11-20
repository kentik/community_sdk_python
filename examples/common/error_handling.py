# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Handle the same SDK exceptions on REST and gRPC."""

from kentik_api.client import KentikAPI
from kentik_api.errors import AuthenticationError, HTTPException, TransportError


def main(protocol: str = "rest") -> None:
    """Print the device count or report why the request failed.

    Args:
        protocol: Transport name, either `rest` or `grpc`.
    """
    client = KentikAPI(protocol=protocol)

    try:
        devices = client.device.list()
        print(f"Retrieved {len(devices.devices or [])} device(s).")
    except AuthenticationError as exc:
        print(f"Authentication failed: {exc}")
    except HTTPException as exc:
        request = f"{exc.method} {exc.path}"
        print(f"HTTP {exc.status_code} on {request}: {exc.message}")
    except TransportError as exc:
        print(f"Network error: {exc}")


if __name__ == "__main__":
    import sys

    main(protocol=sys.argv[1] if len(sys.argv) > 1 else "rest")
