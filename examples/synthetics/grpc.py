# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""List synthetic tests and agents (gRPC transport)."""

from kentik_api.client import KentikAPI
from kentik_api.errors import KentikError


def main() -> None:
    """List synthetic tests and agents over gRPC."""
    client = KentikAPI(protocol="grpc")
    try:
        tests_resp = client.synthetics.list_tests()
        tests = [test for test in (tests_resp.tests or []) if test is not None]
        print(f"Found {len(tests)} synthetic test(s).")
        for test in tests[:5]:
            print(f"  {test.id}: {test.name} (status={test.status})")

        agents_resp = client.synthetics.list_agents()
        agents = [
            agent for agent in (agents_resp.agents or []) if agent is not None
        ]
        print(f"\nFound {len(agents)} synthetic agent(s).")
        for agent in agents[:5]:
            print(
                f"  {agent.id}: {agent.alias} ({agent.city}, {agent.country})"
            )
    except KentikError as exc:
        print(f"API error over gRPC: {exc}")


if __name__ == "__main__":
    main()
