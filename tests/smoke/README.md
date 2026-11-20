<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# Smoke Tests

This layer is mocked and uses no network. See the layered strategy in
[../README.md](../README.md) for how this layer fits with the other
four.

## Purpose

[`test_client_mounts_and_calls.py`](test_client_mounts_and_calls.py) holds lightweight checks for
overall wiring:

- Multi-region endpoint configuration: `_REGION_ENDPOINTS` for `us`/`eu`, and the
  `ConfigurationError` raised for an unrecognized region.
- `KentikAPI` mounts the expected service attributes.
- A call through one mounted wrapper reaches the generated REST module.

The other files in this layer:

| File | Covers |
| --- | --- |
| [`test_declared_dependencies.py`](test_declared_dependencies.py) | [`pyproject.toml`](../../pyproject.toml) declares every third-party import in [`src/`](../../src/), [`scripts/`](../../scripts/README.md), and [`tests/`](../README.md), and [`docs/sphinx/dependencies.md`](../../docs/sphinx/dependencies.md) lists exactly the declared packages. |
| [`test_docs_contract.py`](test_docs_contract.py) | Documentation and tooling facts that the audit found wrong (findings D7 to D10). |
| [`test_examples_import.py`](test_examples_import.py) | Each example imports, and its `client.<service>.<method>(...)` calls resolve against a real client. Nothing is sent. |
| [`test_packaging_contract.py`](test_packaging_contract.py) | Packaging metadata that the published artifacts depend on (audit findings K4 to K9, K11). |

## Run

```bash
uv run poe test-smoke
# or
uv run pytest tests/smoke/
```

## Add a test here

Add only small, high-value checks. Keep this suite minimal and fast.
Put detailed per-operation or per-status-code coverage in
[`tests/generated/`](../generated/README.md) instead.
