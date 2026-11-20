# Implementation Plan: Validate Schema Checkout Before Generating

**Branch**: `001-validate-schema-checkout` | **Date**: 2026-08-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-validate-schema-checkout/spec.md`

## Summary

Add a structural pre-flight check that runs immediately after the generator
selects the latest swagger file per service family (in
`parity.select_latest_swagger_files_by_service()`), and before any code
generation begins. It confirms every selected swagger file parses as JSON
and has the required top-level OpenAPI keys (`paths`, `info`,
`swagger`/`openapi`). If any file fails, `generate_modular_sdk()` raises
immediately, printing every offending file and reason together, before
`SDK_OUTPUT_DIR` is touched. This directly closes the gap found on
2026-08-26, where a locally truncated `device.swagger.json` (1625 lines cut
to 1) was silently accepted and caused the `kagent`/`monitoring` services to
disappear from the generated SDK undetected.

## Technical Context

**Language/Version**: Python 3.14 (matches the rest of `scripts/generation/`)

**Primary Dependencies**: Standard library only (`json`), no new dependency;
consistent with how `generate_sdk.py` already parses swagger files (see
`patched_swagger()`)

**Storage**: N/A (reads local files only, writes nothing on the validation
path itself)

**Testing**: pytest, following the existing `tests/generator/test_parity.py`
pattern (`tmp_path` fixtures, no real schema checkout needed)

**Target Platform**: Same as the rest of the generator: developer machines
and CI running `make generate` / `make generate local`

**Project Type**: Single project, internal build tooling
(`scripts/generation/`), not a user-facing library surface

**Performance Goals**: Negligible overhead versus the rest of a generation
run (which already runs `protoc` and `uvx openapi-python-generator` per
service); a JSON parse of ~40 small-to-medium swagger files adds a
sub-second cost

**Constraints**: MUST NOT change generated output for a valid schema
checkout (spec SC-002); MUST run unconditionally (no new CLI flag) so it
can't be silently skipped; MUST reuse the already-selected file list rather
than re-scanning the filesystem

**Scale/Scope**: ~40 swagger files across ~38-40 services today; a small,
single-purpose addition, not a validation framework

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checked against `.specify/memory/constitution.md` v1.1.0:

| Principle / Section | Assessment |
| --- | --- |
| I. Generated Code Is Never Hand-Edited | PASS: only hand-written files change (`scripts/generation/parity.py`, `scripts/generate_sdk.py`); nothing under `gen/` is touched. |
| II. One Shared Runtime for Every Endpoint | N/A: this feature is generator tooling, not request/runtime code. |
| III. Generator Phase Modules Stay Independently Testable | PASS: validation logic is added to `parity.py` (an existing phase module) as plain functions, unit-tested in `tests/generator/test_parity.py` with no real schema checkout required. |
| IV. Test Coverage Must Be Exhaustive, Not Representative | N/A to this feature directly (that principle governs SDK endpoint coverage), but the same exhaustive spirit is applied to this feature's own tests (see Phase 1 quickstart / tasks). |
| V. End-to-End Tests Are Opt-In and Safe-by-Default | N/A: no e2e surface added. |
| VI. Credentials Never Enter Code, Logs, or Prompts | PASS: no credentials involved; error output is limited to file paths and structural reasons. |
| VII. Compatibility and Scope Discipline | PASS: additive only, no breaking change; change stays scoped to the one new gate (no unrelated refactors bundled in). |
| Dev Workflow guardrail (v1.1.0, schema-checkout integrity) | This feature is the code-level enforcement of that guardrail. It turns a documented manual check into an automatic one. |

No violations. Complexity Tracking table is not needed.

## Project Structure

### Documentation (this feature)

```text
specs/001-validate-schema-checkout/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

No `contracts/` directory: this feature has no external interface (API,
CLI flag, or public library surface). It's an internal safety gate inside
the existing generation pipeline, matching the plan template's own
guidance to skip contracts for purely internal build tooling.

### Source Code (repository root)

```text
scripts/
├── generate_sdk.py              # generate_modular_sdk(): call the new
│                                 # validation right after
│                                 # parity.select_latest_swagger_files_by_service()
└── generation/
    └── parity.py                 # add validate_schema_files() and
                                   # validate_schema_files_or_raise()

tests/
└── generator/
    └── test_parity.py            # add regression tests, including a fixture
                                   # shaped like the 2026-08-26 incident
```

**Structure Decision**: Single project (this repo has no
frontend/backend/mobile split). The new logic lives in the existing
`parity.py` phase module rather than a new module, because it operates on
the exact same "which swagger files will we trust for this run" concern
`parity.py` already owns (`select_latest_swagger_files_by_service`). No new
abstraction or module is introduced for what is fundamentally one small,
related check.

## Complexity Tracking

*No violations. Table intentionally omitted.*
