# Phase 1 Data Model: Fix Generator Correctness Defects

This feature introduces one small shared value and one derived string. Nothing
is persisted; both exist only during a generation run.

## GeneratedTree classification

The single rule for deciding whether a directory under `src/kentik_api/gen/` is
a Service. Lives in `scripts/generation/_shared.py`.

| Name | Type | Notes |
| --- | --- | --- |
| `INTERNAL_GEN_DIRS` | `frozenset[str]` | Directories that exist under `gen/` but are not Services. Value: `{"__pycache__", "pb_companions"}`. |
| `iter_service_dirs(root)` | `Iterator[Path]` | Yields each Service directory under `root`, sorted by name, excluding `INTERNAL_GEN_DIRS` and any non-directory entry. `root` defaults to `SDK_OUTPUT_DIR`. |

### Validation rules

- A Service directory is any direct child directory of `gen/` whose name is not
  in `INTERNAL_GEN_DIRS`.
- Absence of a wrapper does **not** disqualify a directory. Six Services are
  operationless and have no wrapper (see research Decision 1).
- Absence of `models/` does **not** define the rule. It happens to correlate
  today, but relying on it would misclassify a future internal directory.
- The iteration order is sorted by directory name, so callers that build
  documents or indexes produce stable, diff-friendly output.

### Replaces

Nine call sites that each inline their own exclusion set today:

| Site | Current exclusion set |
| --- | --- |
| `parity.validate_generated_service_parity` | `__pycache__`, `pb_companions`: correct |
| `docs_rendering._generate_service_readmes` | `__pycache__` |
| `docs_rendering._discover_example_ops` | `_`-prefixed |
| `docs_rendering._update_guide_snippets` | `_`-prefixed, `pb_companions` |
| `endpoint_docs.render_endpoint_docs` | `__pycache__`, `docs`, `core` |
| `wrapper_generation._generate_service_wrappers` | `__pycache__`, `docs`, `core`, `pb` |
| `wrapper_generation._generate_client_mixin` | same as above |
| `generate_sdk` (three loops) | `__pycache__` |
| `tests/_discovery.discover_cases` | none |

Only the first is correct. The rest are replaced.

## Provenance header

A derived string, not a stored entity. Written into each generated
documentation page so a reader can find the code that produced it.

| Field | Source | Notes |
| --- | --- | --- |
| module path | the writing module's `__file__`, made repo-relative | e.g. `scripts/generation/endpoint_docs.py` |
| function name | the writing function's `__name__` | must resolve to a real function |

### Validation rules

- The named function must exist in the named module. This is the property that
  fails today: 42 pages name `_render_sphinx_stubs()`, which does not exist.
- The value must be derived at write time, never transcribed, so a rename cannot
  leave it stale (FR-008).

## State transitions

None. Both items are computed fresh on each generation run and hold no state
between runs.
