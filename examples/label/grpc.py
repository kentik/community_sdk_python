# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List all device labels in the account (gRPC transport)."""

from kentik_api.client import KentikAPI
from kentik_api.errors import KentikError


def main() -> None:
    """List device labels over gRPC."""
    client = KentikAPI(protocol="grpc")
    try:
        response = client.label.list()
        labels = [
            label for label in (response.labels or []) if label is not None
        ]
        print(f"Found {len(labels)} label(s).")
        for label in labels:
            print(f"  {label.id}: {label.name} (color: {label.color})")
    except KentikError as exc:
        print(f"API error over gRPC: {exc}")


if __name__ == "__main__":
    main()
