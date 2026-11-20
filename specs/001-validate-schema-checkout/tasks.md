# Tasks: Validate Schema Checkout Before Generating

**Input**: Design documents from `/specs/001-validate-schema-checkout/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included. This repo's constitution (Principle III) and existing
`tests/generator/` convention treat every phase-module change as needing
direct unit tests; this feature follows that norm.

**Organization**: Single user story (US1, P1). There is only one story in
spec.md, so there is no multi-story sequencing to manage.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 for all feature tasks; unlabeled for setup/polish

## Phase 1: Setup

No new project setup is needed: this feature only touches an existing
hand-written module and its existing test file, using tooling
(pytest/ruff/ty) already configured in the repo.

- [x] T001 Re-read current `scripts/generation/parity.py` and
      `tests/generator/test_parity.py` in full immediately before editing,
      to confirm no unrelated changes have landed since planning (research.md
      Decision 1-3 assume the current shape of both files).

## Phase 2: Foundational

Not applicable: the single user story below *is* the foundational (and
only) unit of work; nothing else depends on shared new infrastructure.

## Phase 3: User Story 1 - Generator refuses to run against an obviously broken schema checkout (Priority: P1) 🎯 MVP

**Goal**: `make generate local` (and `make generate`) fails loudly, before
writing any output, when a discovered swagger file is empty, not valid
JSON, or missing required top-level OpenAPI keys, reporting every
offending file together.

**Independent Test**: Run
`uv run pytest tests/generator/test_parity.py -v`. The new
`test_validate_schema_files_*` cases exercise this story fully without
needing a real schema checkout or running the full generator.

### Tests for User Story 1 ⚠️ write first, confirm they fail before implementing

- [x] T002 [P] [US1] In `tests/generator/test_parity.py`, add
      `test_validate_schema_files_passes_valid_files`: a `tmp_path` fixture
      with 1-2 valid minimal swagger JSON files (`paths`, `info`, `openapi`
      keys present) returns an empty failure list.
- [x] T003 [P] [US1] In `tests/generator/test_parity.py`, add
      `test_validate_schema_files_rejects_empty_file`: a zero-byte fixture
      file is reported as a failure with an "empty" reason.
- [x] T004 [P] [US1] In `tests/generator/test_parity.py`, add
      `test_validate_schema_files_rejects_invalid_json`: a fixture
      containing non-JSON text is reported with an "invalid JSON" reason.
- [x] T005 [P] [US1] In `tests/generator/test_parity.py`, add
      `test_validate_schema_files_rejects_missing_required_keys`: a
      fixture that parses as a valid JSON object but omits `paths` (or
      `info`, or both `swagger`/`openapi`) is reported, naming the missing
      key(s).
- [x] T006 [P] [US1] In `tests/generator/test_parity.py`, add
      `test_validate_schema_files_reports_all_failures_before_raising`: a
      mix of 2+ simultaneously-broken fixture files all appear in one
      `validate_schema_files()` result (FR-004), and
      `validate_schema_files_or_raise()` raises exactly once listing all of
      them, not just the first. (Implemented using `capsys`, not the raised
      message itself. The message is a generic summary, matching the
      existing `validate_generated_service_parity()` print/raise style.)
- [x] T007 [US1] In `tests/generator/test_parity.py`, add
      `test_validate_schema_files_catches_truncated_file_like_2026_08_26_incident`:
      a fixture file containing a single truncated byte (reproducing the
      real `device.swagger.json` incident shape) fails validation with an
      "invalid JSON" reason (SC-003).
- [x] T008 Run `uv run pytest tests/generator/test_parity.py -v` and confirm
      T002-T007 fail (the functions under test don't exist yet).

### Implementation for User Story 1

- [x] T009 [US1] In `scripts/generation/parity.py`, add the
      `SchemaValidationFailure` `TypedDict` (`path: Path`, `reason: str`) per
      data-model.md, next to the existing `SwaggerFileMetadata` `TypedDict`.
- [x] T010 [US1] In `scripts/generation/parity.py`, implement
      `validate_schema_files(swagger_paths: list[Path]) -> list[SchemaValidationFailure]`
      per research.md Decision 2 (unreadable / empty / invalid JSON /
      non-object / missing `paths`, `info`, or `swagger`+`openapi` → one
      failure entry each; valid files contribute nothing). Depends on T009.
- [x] T011 [US1] In `scripts/generation/parity.py`, implement
      `validate_schema_files_or_raise(swagger_paths: list[Path]) -> None`,
      printing every failure from `validate_schema_files()` (mirroring the
      existing `validate_generated_service_parity()` print/raise style) and
      raising `RuntimeError` if the list is non-empty. Depends on T010.
- [x] T012 [US1] In `scripts/generate_sdk.py`'s `generate_modular_sdk()`, call
      `parity.validate_schema_files_or_raise([Path(metadata["path"]) for
      services in selected_swagger_files.values() for metadata in services])`
      immediately after `selected_swagger_files, selected_count,
      ignored_count = parity.select_latest_swagger_files_by_service(...)` and
      before the `for service in sorted(selected_swagger_files):` loop
      (research.md Decision 3). Depends on T011.
- [x] T012a **[discovered during T017]** Move `SDK_OUTPUT_DIR.mkdir(...)` and
      the "Cleaning old modules" `shutil.rmtree(...)` loop to run *after*
      T012's validation call, not before. The initial T012 placement still
      let the existing unconditional cleanup wipe `src/kentik_api/gen/`
      before validation ran, so a corrupted checkout produced a *worse*
      failure mode (silently deleted generated output) than the original
      bug. Added `test_generate_modular_sdk_validates_schema_before_cleaning_output_dir`
      (AST-based, in `tests/generator/test_generate_sdk.py`) so this can't
      silently regress. See research.md Decision 3.
- [x] T013 Run `uv run pytest tests/generator/test_parity.py -v` again and
      confirm T002-T007 now pass. Depends on T009-T012.

**Checkpoint**: User Story 1 is fully implemented and independently
testable: `make generate local` / `make generate` now fail fast and
loudly on a structurally broken schema checkout.

## Final Phase: Polish & Validation

- [x] T014 [P] Run `make lint` (ruff check --fix + ruff format); fix any
      findings in the two touched files.
- [x] T015 [P] Run `make typecheck` (`ty check` includes
      `scripts/generation` and `scripts/generate_sdk.py`); fix any findings.
- [x] T016 Run the full `uv run pytest` / `make test` suite to confirm zero
      regressions elsewhere (SC-002: behavior for a valid checkout must be
      unchanged).
- [x] T017 Manually ran quickstart.md's end-to-end check. First discovery:
      by the time this ran, the sibling `../api-schema-public` checkout had
      already been cleaned up (0 modified files). The original 2026-08-26
      corruption was gone, so `make generate local` completed normally
      (40 services, zero diff vs. committed `gen/`, confirming SC-002 for
      real, not just via fixtures). Re-validated SC-001 by deliberately
      truncating one real file (`network_class.swagger.json`) end-to-end:
      first attempt surfaced the T012a ordering bug (exit code 2, correct
      error, but `git status` showed 1273 deleted files under
      `src/kentik_api/gen/`); restored the file and `gen/`, applied the
      T012a fix, re-ran the same corruption: exit code 2, correct error
      naming the exact file, and zero changes under `src/kentik_api/gen/`.
      Restored the schema file afterward; sibling repo confirmed clean.
- [x] T018 Updated `.specify/memory/constitution.md`'s v1.1.0 guardrail
      bullet (Development Workflow & Quality Gates): it described a manual
      `git status` check; amended to note the structural check is now
      automatic (this feature), while the manual check remains the right
      call for corruption this feature doesn't cover (e.g. a whole service
      directory silently absent, see spec.md Assumptions).

## Dependencies

- T001 (setup) blocks nothing else directly but should happen first.
- T002-T007 (tests) MUST be written and MUST fail (T008) before T009-T012
  (implementation) begin.
- T009 -> T010 -> T011 -> T012 -> T013, strictly sequential (each builds on
  the previous in the same file).
- T014-T018 (polish) run after T013's checkpoint.

## Parallel Execution Example

T002-T007 all add independent test functions to the same file
(`tests/generator/test_parity.py`). They are conceptually parallel (no
shared state between test cases) but land as sequential edits to one file
in practice. T014 and T015 are the only tasks safe to run as literally
concurrent shell commands (lint and typecheck touch disjoint tool caches).

## Implementation Strategy

MVP = all of Phase 3 (there is only one story). Suggested order: T001,
T002-T008 (red), T009-T013 (green), T014-T018 (polish/validate). This
mirrors red-green-refactor even though it wasn't explicitly requested,
because it's the natural shape for a spec whose entire value proposition is
"this check must actually catch the failure modes it claims to."
