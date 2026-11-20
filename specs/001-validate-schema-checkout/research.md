# Phase 0 Research: Validate Schema Checkout Before Generating

## Decision 1: Where does the validation logic live?

**Decision**: Add two new functions to `scripts/generation/parity.py`:
`validate_schema_files()` (pure, returns a list of failures) and
`validate_schema_files_or_raise()` (raises `RuntimeError` if the list is
non-empty, printing every failure).

**Rationale**: `parity.py` already computes the exact list of swagger files
the generator will trust for this run
(`select_latest_swagger_files_by_service()`, per its own module docstring:
"Swagger file selection and generated/schema service-directory parity
validation"). Structural validation of that same list is the same concern
("which files do we trust"), not a new one. `validate_generated_service_parity()`
in the same file already establishes the pattern this follows: a pure-ish
check function, called from `generate_sdk.py`, that prints every failure
together and raises `RuntimeError`. Reusing means no new error-handling
convention to invent.

**Alternatives considered**:

- A new `scripts/generation/schema_validation.py` module. Rejected: the
  constitution (Principle III) lists `parity.py` as an existing
  single-concern phase module; splitting one small, closely-related check
  into its own module for a ~30-line function would be an unjustified new
  abstraction (`python-simple-architect` bias: don't create a module for a
  one-off concern that already has a natural home).
- Validating inside `generate_sdk.py` directly (no `parity.py` change).
  Rejected: `parity.py` is the hand-written module already tested in
  isolation (`tests/generator/test_parity.py`) without needing a real
  schema checkout; keeping the logic there keeps it consistent with how
  `select_latest_swagger_files_by_service` and
  `validate_generated_service_parity` are both already tested that way.

## Decision 2: What counts as "structurally invalid"?

**Decision**: A file fails validation if: it can't be read; it's empty or
whitespace-only; it doesn't parse as JSON; the parsed JSON isn't an object;
or the object is missing `paths`, `info`, or both `swagger` and `openapi`.

**Rationale**: These are the minimal structural properties every swagger
file already relies on elsewhere in the pipeline (e.g. `patched_swagger()`
in `generate_sdk.py` immediately does `json.loads(...)` and later code reads
`schema["definitions"]`/`schema["components"]` and iterates `paths`).
Checking for exactly these catches the real 2026-08-26 incident (a
1-line-truncated file fails both "parses as JSON" and, even if it happened
to parse, "has `paths`") without requiring full OpenAPI schema-conformance
validation, which the spec's Assumptions section explicitly scopes out as
unnecessary for this incident.

**Alternatives considered**:

- Full JSON Schema / OpenAPI v2 spec validation (e.g. via a schema
  validation library). Rejected as disproportionate: adds a new dependency
  for a problem that structural key-presence checking already solves, and
  the spec's Assumptions section explicitly excludes it.
- A minimum file-size threshold. Rejected per the spec's own edge case: a
  legitimately small service (one operation) must not be rejected just for
  being small; only structural validity matters.

## Decision 3: Where in `generate_modular_sdk()` does the check run?

**Decision**: Immediately after
`selected_swagger_files, selected_count, ignored_count =
parity.select_latest_swagger_files_by_service(openapi_base)`, and (this
matters) **before** `SDK_OUTPUT_DIR` is set up and its old contents are
cleaned (`shutil.rmtree` per existing service directory), not just before
the per-service generation loop.

**Rationale**: An earlier version of this plan placed the check after the
existing "Cleaning old modules" step (reasoning that step was harmless
prerequisite work). Manually reproducing the incident end-to-end
(truncating a real swagger file and running `make generate local` against
it) proved that reasoning wrong: the cleanup step unconditionally
`shutil.rmtree`s every existing service directory under
`src/kentik_api/gen/` *before* any validation ran, so a validation failure
still left the repo with (in the reproduction) 1273 tracked files deleted:
recoverable via `git checkout`, but a direct violation of spec SC-001
("before any file under `src/kentik_api/gen/` is written or modified").
Moving the check to run immediately after schema-file discovery, and
moving `SDK_OUTPUT_DIR` setup/cleanup to run only *after* validation
passes, fixes this: `get_schema_root()` (which produces `schema_root`) has
no dependency on `SDK_OUTPUT_DIR` at all, so reordering is safe. Re-running
the same manual reproduction after the fix confirmed `src/kentik_api/gen/`
is now left with zero changes when validation fails. A dedicated static
test (`test_generate_modular_sdk_validates_schema_before_cleaning_output_dir`
in `tests/generator/test_generate_sdk.py`) asserts this ordering via AST
line numbers, so it can't silently regress again.

**Alternatives considered**:

- Validating inside the per-service loop, right before
  `patched_swagger()`. Rejected: this would only fail after some services
  had already been fully generated (partial output), and would report only
  the first failure encountered rather than every failure in the run (spec
  FR-004 requires reporting all of them together).
- Trusting fixture-based unit tests alone, without a real end-to-end
  reproduction. Rejected after the fact: the fixture tests in
  `test_parity.py` all passed against the original (buggy) ordering too,
  because they only exercise `validate_schema_files()` / `_or_raise()` in
  isolation. They have no way to know *where* the caller invokes them.
  Only running the actual `generate_modular_sdk()` code path surfaced the
  ordering bug.

## Decision 4: Does this run for both `--local-repo` and the cloned fallback?

**Decision**: Yes, unconditionally. `generate_modular_sdk()` doesn't
branch on `repo_source` before this point: `get_schema_root()` already
normalizes local-vs-cloned into one `schema_root` path by the time
`openapi_base` is computed, so the new call needs no source-specific
logic at all.

**Rationale**: Directly satisfies spec FR-005. A fresh clone is less
likely to be corrupted, but a transient truncation during clone/checkout
is possible in principle, and there's no cost to validating it too.
