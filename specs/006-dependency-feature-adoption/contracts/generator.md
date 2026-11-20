# Contract: generator Markdown output

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)

## Guarantee

After `make generate`, every Markdown file the generator writes passes
`ruff format --check`. A second `make generate` changes nothing.

## Files in scope

| File | Writer |
| --- | --- |
| `docs/sphinx/services/*.md` | `endpoint_docs.EndpointDocsCollector.render()` |
| `docs/sphinx/sdk_runtime_architecture.md` | `docs_rendering.generate()` |
| `src/kentik_api/gen/README.md`, `src/kentik_api/gen/*/README.md` | `docs_rendering.generate()` |
| Marker blocks in `docs/sphinx/guides/{quickstart,rest,grpc,generation}.md` and `docs/sphinx/README.md` | `docs_rendering._update_guide_snippets()` |

## Mechanism

`generate_modular_sdk()` in `scripts/generate_sdk.py` runs `ruff format` on
these paths in its final formatting pass, after `render()` and before the
API surface record. The snippet renderers do not wrap lines themselves.

## Expected regeneration diff

Only these 3 pages change, each in one import line per affected example:

- `docs/sphinx/services/bgp_monitoring.md`
- `docs/sphinx/services/cloud_export.md`
- `docs/sphinx/services/kagent.md`

For example:

```python
from kentik_api.gen.kagent.models import (
    ProvisioningTokenServiceRevokeProvisioningTokenBody,
)
```

## Test

`tests/generator/test_generate_sdk.py` asserts that the final formatting
pass includes `docs/sphinx/services` and the other paths above.
