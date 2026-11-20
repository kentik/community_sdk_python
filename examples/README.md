<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../pyproject.toml). Edit directly. -->

# Quick-start examples for the Kentik Community Python SDK

These examples use the Kentik Community Python SDK to call the live Kentik API.
The V5 batch example previews changes by default. With `--send`, it writes to your account.

> [!NOTE]
> The [`examples/`](README.md) directory is hand-written. [`uv run poe generate`](../pyproject.toml) and
> [`uv run poe clean`](../pyproject.toml) do not generate or remove it. Edit these files directly
> when you add new examples or update existing ones.

## Setup

Use your secret manager to supply `KENTIK_EMAIL` and `KENTIK_API_TOKEN` to the example process.

From the repository root, run an example as a module.
This prevents Python from importing the example named `grpc.py` instead of the `grpc` package.

```bash
uv run python -m examples.device.rest
uv run python -m examples.device.grpc
```

## Layout

Each service has a `rest.py` and a `grpc.py` that perform the same
operation over each transport. The API surface is identical. Only the
`protocol=` argument differs. [`common/error_handling.py`](common/error_handling.py) is a standalone
example, not a helper module. To run it over gRPC, pass `grpc` as its first argument.

[`tests/smoke/test_examples_import.py`](../tests/smoke/test_examples_import.py)
imports every example. It also makes sure that each `client.<service>.<method>(...)` call
resolves against the real client. So an example that stops matching the SDK fails
`uv run poe test`.

| Directory | Service | REST | gRPC |
| --- | --- | --- | --- |
| [`device/`](device/) | Device management | [`rest.py`](device/rest.py) | [`grpc.py`](device/grpc.py) |
| [`user/`](user/) | User management | [`rest.py`](user/rest.py) | [`grpc.py`](user/grpc.py) |
| [`label/`](label/) | Device labels | [`rest.py`](label/rest.py) | [`grpc.py`](label/grpc.py) |
| [`site/`](site/) | Sites and markets | [`rest.py`](site/rest.py) | [`grpc.py`](site/grpc.py) |
| [`alerting/`](alerting/) | Alerting | [`rest.py`](alerting/rest.py) | [`grpc.py`](alerting/grpc.py) |
| [`synthetics/`](synthetics/) | Synthetic tests | [`rest.py`](synthetics/rest.py) | [`grpc.py`](synthetics/grpc.py) |
| [`common/`](common/) | Error handling on either transport | [`error_handling.py`](common/error_handling.py) | same file, `grpc` argument |

### V5 query and batch examples

[`v5/`](v5/) holds ports of the 1.x query, batch, and analytics examples.
`client.v5` always uses REST, so these scripts have no gRPC variant. See the
[V5 guide](../docs/sphinx/guides/v5.md).

| Script | What it does |
| --- | --- |
| [`v5/query.py`](v5/query.py) | Top-X data, Data Explorer URL, and chart queries. Read-only |
| [`v5/batch.py`](v5/batch.py) | Flow tag batch. A dry run by default. If you pass `--send`, it writes to your account |
| [`v5/analytics_topx.py`](v5/analytics_topx.py) | Flat-traffic analysis with pandas. Needs `kentik-api[analytics]`. Read-only |

[`tests/smoke/test_examples_v5.py`](../tests/smoke/test_examples_v5.py) runs
each one against a mocked API.

## Transport selection

Both transports return the same Pydantic models. Switch with one argument:

```python
client = KentikAPI(protocol="rest")  # REST transport (default)
client = KentikAPI(protocol="grpc")  # gRPC transport
```

See the [gRPC guide](../docs/sphinx/guides/grpc.md) for transport internals and
sequence diagrams.

## Further reading

- [docs/sphinx/guides/quickstart.md](../docs/sphinx/guides/quickstart.md)
- [docs/sphinx/guides/rest.md](../docs/sphinx/guides/rest.md)
- [docs/sphinx/guides/grpc.md](../docs/sphinx/guides/grpc.md)
- [docs/sphinx/guides/error_handling.md](../docs/sphinx/guides/error_handling.md)
