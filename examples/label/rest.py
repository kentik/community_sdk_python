# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List all device labels in the account."""

from kentik_api.client import KentikAPI


def main() -> None:
    """List device labels over REST."""
    client = KentikAPI(protocol="rest")
    response = client.label.list()
    labels = [label for label in (response.labels or []) if label is not None]
    print(f"Found {len(labels)} label(s).")
    for label in labels:
        print(f"  {label.id}: {label.name} (color: {label.color})")


if __name__ == "__main__":
    main()
