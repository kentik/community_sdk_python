# Tasks: Fix Generator Correctness Defects

**Input**: Design documents from `/specs/002-fix-generator-correctness/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included. Constitution Principle IV and the existing
`tests/generator/` convention treat every phase-module change as needing direct
unit tests. Two of the four stories are specifically about test correctness, so
tests are the deliverable rather than an accessory.

**Organization**: One phase per user story, in spec priority order. All four
stories are independent and can land in any order or separately; the sequence
below is chosen so the cheapest, highest-certainty change lands first.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1–US4 for feature work; unlabeled for setup/polish

## Phase 1: Setup

- [x] T001 Confirm the local schema checkout is clean before any regeneration,
      per the constitution's schema-checkout guardrail: run
      `git -C ../api-schema-public status --short` and expect no output. If it
      is dirty, use plain `make generate` (fresh clone) for every later
      regeneration task instead of `make generate local`.
- [x] T002 Capture the "before" baseline so the fixes are provable, recording
      each value: pages naming a missing function
      (`grep -l '_render_sphinx_stubs' docs/sphinx/services/*.md | wc -l`,
      expect 42); real Services vs pages (expect 40 and 40); presence of
      `docs/sphinx/services/pb_companions.md` (expect present) and
      `docs/sphinx/services/core.md` (expect absent); and current `make test`
      pass/skip counts.

## Phase 2: Foundational

Not applicable. No shared prerequisite blocks the stories: each touches a
different defect, and the one piece of new shared code (the Service rule) is
itself the deliverable of US2 rather than a precondition for the others.

## Phase 3: User Story 1 - Test suite fails when production breaks (Priority: P1) 🎯 MVP

**Goal**: Remove the dead in-place schema mutator and move its three assertions
onto the code path `make generate` actually runs.

**Independent Test**: `uv run pytest tests/generator/test_generate_sdk.py -v`
passes, and every schema-patching assertion now exercises `patched_swagger`.
Verified further by breaking `patched_swagger` deliberately and confirming a
test fails.

### Tests for User Story 1

- [x] T003 [US1] In `tests/generator/test_generate_sdk.py`, rewrite the three
      tests at the `patch_schema_for_clean_names` call sites (currently lines
      113, 149, 173) to drive `patched_swagger` instead, asserting the same
      requestBody `$ref` inlining behaviour by reading the yielded temp file.
- [x] T004 [US1] In `tests/generator/test_generate_sdk.py`, confirm the existing
      `test_patched_swagger_does_not_modify_original` still asserts the
      no-mutation property, and extend it if the rewritten tests do not already
      cover the original file staying byte-identical.
- [x] T005 [US1] Run `uv run pytest tests/generator/test_generate_sdk.py -v` and
      confirm the rewritten tests pass **before** deleting the function, proving
      they stand on their own rather than passing incidentally.

### Implementation for User Story 1

- [x] T006 [US1] Delete `patch_schema_for_clean_names` from
      `scripts/generate_sdk.py` (line 198) and remove its now-unused import from
      `tests/generator/test_generate_sdk.py` (line 30). Depends on T003–T005.
- [x] T007 [US1] Verify no reference survives:
      `grep -rn 'patch_schema_for_clean_names' --include='*.py' scripts/ tests/`
      must return nothing. Depends on T006.
- [x] T008 [US1] Red-test the new coverage: temporarily break
      `patched_swagger`'s inlining, confirm at least one test fails, then
      restore. This proves the retargeted tests would catch a real regression.

**Checkpoint**: The generator no longer contains a code path that rewrites the
schema checkout in place, and the tests guard the live path (FR-001, FR-002,
SC-004, SC-005).

## Phase 4: User Story 2 - Only real services appear in documentation (Priority: P1)

**Goal**: One shared rule for what counts as a Service, replacing nine divergent
inline exclusion sets, so `core` gains a page and `pb_companions` stops being
documented as a Service.

**Independent Test**: `uv run pytest tests/generator/test_parity.py -v` passes
with new cases asserting the rule includes `core` and excludes `pb_companions`;
after regeneration, documented Services equal real Services as a **set**, not
just a count.

### Tests for User Story 2

- [x] T009 [US2] In `tests/generator/test_parity.py`, add a test that
      `iter_service_dirs()` excludes every name in `INTERNAL_GEN_DIRS` and
      includes an operationless Service directory, using `tmp_path` fixtures
      that mimic the real tree shape (a dir with `models/` but no wrapper).
- [x] T010 [US2] In `tests/generator/test_parity.py`, add a regression test
      naming this defect: a fixture tree containing `pb_companions` must not
      yield it as a Service, and a fixture `core`-like directory must be
      yielded. Depends on T009.

### Implementation for User Story 2

- [x] T011 [US2] In `scripts/generation/_shared.py`, add `INTERNAL_GEN_DIRS`
      (`frozenset({"__pycache__", "pb_companions"})`) and
      `iter_service_dirs(root=SDK_OUTPUT_DIR)` per data-model.md, yielding
      Service directories sorted by name. Depends on T009–T010.
- [x] T012 [US2] In `scripts/generation/parity.py`, replace the inline exclusion
      in `validate_generated_service_parity()` (line 83) with
      `iter_service_dirs()`. This site's rule is already correct, so its
      validation behaviour must not change. It is the reference the other eight
      sites are being brought into line with. Depends on T011.
- [x] T013 [P] [US2] In `scripts/generation/docs_rendering.py`, replace the three
      divergent filters in `_generate_service_readmes()`, `_discover_example_ops()`,
      and `_update_guide_snippets()` with `iter_service_dirs()`. Depends on T011.
- [x] T014 [P] [US2] In `scripts/generation/endpoint_docs.py`, replace the filter
      in `render_endpoint_docs()` with `iter_service_dirs()`, removing the
      hardcoded `"core"` and `"docs"` literals that suppress a real Service.
      Depends on T011.
- [x] T015 [P] [US2] In `scripts/generation/wrapper_generation.py`, replace the
      filters in `_generate_service_wrappers()` (line 115) and
      `_generate_client_mixin()` (line 429) with `iter_service_dirs()`. Both
      currently exclude `{__pycache__, docs, core, pb}`; the shared rule excludes
      only `{__pycache__, pb_companions}`, so `core` becomes visible to both
      functions for the first time. `core/services/` exists but contains only
      `__init__.py`, so it must fall through the existing no-wrapper check and
      produce no wrapper and no mount. Keep that no-wrapper check as a separate
      explicit condition rather than folding it into the Service rule.
      **Verify directly**: after this task, `git diff -- src/kentik_api/client_mixin.py`
      must be empty. Depends on T011.
- [x] T016 [P] [US2] In `scripts/generate_sdk.py`, replace the three loop filters
      with `iter_service_dirs()`. Depends on T011.
- [x] T017 [P] [US2] In `tests/_discovery.py`, adopt `iter_service_dirs()` in
      `discover_cases()`, which currently excludes nothing. Separately, delete
      the duplicate local `service_to_pascal_case` at line 53 in favour of the
      `_shared` import the file already has (FR-014); the two definitions are
      byte-identical today and nothing would catch them drifting apart.
      Depends on T011.
- [x] T018 [US2] Run `make test` and confirm no regression, then run
      `make generate local` (or `make generate` per T001) and confirm the
      documentation diff is exactly: `core.md` added, `pb_companions.md`
      removed, `index.md` toctree updated, and `pb_companions/README.md` no
      longer titled as a Service. Depends on T012–T017.
- [x] T019 [US2] Assert the FR-011 guarantee across **both** generated code
      locations, not just one:
      `git diff --stat -- 'src/kentik_api/gen/**/*.py' src/kentik_api/client_mixin.py`
      must be empty after regeneration. `client_mixin.py` is generated but lives
      outside `gen/`, so a check scoped to `gen/` alone would miss the single
      most likely FR-011 violation, which T015 is the task most able to cause.
      Depends on T018.
- [x] T019a [US2] Confirm the corrected membership as a **set**, per SC-002 and
      US2's third acceptance scenario, rather than by comparing totals: the
      documented service names and the real service names must match exactly.
      Totals already agree today, so a count comparison would pass without
      proving anything. Depends on T018.

**Checkpoint**: Documented Services match real Services as a set (FR-003–FR-006,
FR-014, SC-002, SC-003).

## Phase 5: User Story 3 - Provenance traces to real code (Priority: P2)

**Goal**: Generated pages name the function that actually wrote them, derived
rather than transcribed.

**Independent Test**: After regeneration, zero pages name a function that does
not exist.

### Tests for User Story 3

- [x] T020 [US3] In `tests/generator/test_endpoint_docs.py`, add a test
      asserting the provenance header names a function that resolves in the
      module it names, rather than asserting a hardcoded string. The test must
      fail if the writer is renamed without the header following.

### Implementation for User Story 3

- [x] T021 [US3] In `scripts/generation/endpoint_docs.py`, replace the two
      hardcoded `_render_sphinx_stubs()` strings (lines 715 and 792) with a
      header derived from the writing function's `__name__` and its module path,
      per data-model.md. Depends on T020.
- [x] T022 [US3] Regenerate and confirm
      `grep -l '_render_sphinx_stubs' docs/sphinx/services/*.md | wc -l` returns
      0, down from the 42 captured in T002. Depends on T021.

**Checkpoint**: Every provenance note resolves to real code (FR-007, FR-008,
SC-001).

## Phase 6: User Story 4 - Extraction failures are surfaced (Priority: P2)

**Goal**: A documentation-extraction failure aborts the run instead of printing
a warning while reporting success.

**Independent Test**: Force an extraction failure for one service and confirm
the run exits non-zero rather than emitting an empty page.

### Tests for User Story 4

- [x] T023 [US4] In `tests/generator/test_endpoint_docs.py`, add a test that a
      failing extraction propagates rather than being swallowed, using a fixture
      swagger file that cannot be parsed.

### Implementation for User Story 4

- [x] T024 [US4] In `scripts/generation/endpoint_docs.py`, remove the blanket
      `except Exception` in `EndpointDocsCollector.extract()` (lines 867–873) so
      failures propagate, per research Decision 3. Depends on T023.
- [x] T025 [US4] Resolve the contradictory docstrings in the same file: the
      module docstring claims the ordering constraint "is visible in the
      interface" while the class docstring says it "remains the caller's
      responsibility". Make both state what the code actually guarantees
      (FR-010). Do not add enforcement machinery: that is deferred to the
      follow-up feature. Depends on T024.

**Checkpoint**: Silent documentation failures are impossible (FR-009, FR-010,
SC-007).

## Phase 7: Polish, Documentation & Validation

- [x] T026 [P] In `CONTEXT.md`, sharpen the `Service` entry so it states that a
      Service maps to a directory under `src/kentik_api/gen/` **except** the
      generator-internal directories, naming `pb_companions` as the current
      example (FR-013). This closes the glossary ambiguity that allowed the
      defect.
- [x] T027 [P] In `CLAUDE.md`, fix the `_shared.py` description, which says "the
      two helpers" and names two while the module exports eight. Update it to
      match `scripts/generation/README.md` and include the new Service rule
      (FR-012). Note this is a pre-existing contradiction between the two
      documents, not one introduced here.
- [x] T028 [P] In `scripts/generation/README.md`, add the new Service rule to the
      `_shared.py` public-interface row.
- [x] T029 [P] In `tests/generator/README.md`, add or update Files-table rows for
      the test modules this feature changes.
- [x] T030 Run `npx --yes markdownlint-cli2 "**/*.md"` and confirm zero issues
      across every edited document. Depends on T026–T029.
- [x] T030a Verify SC-009 directly, which T030 cannot: markdownlint checks
      formatting and cannot detect a contradiction. Confirm `CLAUDE.md` and
      `scripts/generation/README.md` now agree on the `_shared.py` public
      interface, and that `CONTEXT.md`'s `Service` entry agrees with
      `INTERNAL_GEN_DIRS` in the code. Depends on T026–T028.
- [x] T031 Run `make lint` and `make typecheck`; both must be clean.
- [x] T032 Run `make test` and confirm no regression against the T002 baseline
      other than tests added or retargeted by this feature.
- [x] T033 Run `make docs` and confirm Sphinx builds with no missing-page or
      orphaned-page warnings, proving `core.md` is in the toctree and
      `pb_companions.md` is gone from it.
- [x] T034 Run the opt-in live suites `make test-e2e` and `make test-e2e-grpc`;
      both must pass unchanged (SC-008).
- [x] T035 Walk `quickstart.md` end to end and confirm every stated expectation
      holds, including that the Service count is still 40 with the corrected
      membership. Depends on T018–T034.

## Dependencies

- T001–T002 (setup) come first; T002's baseline is referenced by T022 and T032.
- **US1 (T003–T008)**, **US2 (T009–T019)**, **US3 (T020–T022)** and
  **US4 (T023–T025)** are mutually independent and may land in any order or as
  separate commits.
- Within US1: T003–T005 (tests green on the live path) strictly precede T006
  (deletion), so coverage never lapses.
- Within US2: T009–T010 precede T011 (the rule), which precedes T012–T017 (the
  call sites), which precede T018 and then T019/T019a (the regeneration checks).
- Within US3 and US4: the test precedes the implementation.
- Phase 7 runs last. T030 depends on T026–T029; T030a depends on T026–T028;
  T035 depends on everything.

## Parallel Execution Example

T013–T017 are the clearest parallel opportunity: five different files, each
swapping one filter for the shared rule, all depending only on T011. T026–T029
are likewise four independent documents. Everything else is sequential because
it either shares a file or gates on a regeneration.

## Implementation Strategy

**MVP = US1.** It is the smallest change, needs no regeneration, and removes a
standing hazard, so it can ship alone.

Suggested order: setup (T001–T002) → US1 → US2 → US3 → US4 → polish. US2 is
sequenced second because it is the only story that changes generated output, so
it benefits from landing while attention is on the regeneration diff. US3 and
US4 both touch `endpoint_docs.py` and are cheap to land together.

Each story ends at a checkpoint that maps to specific functional requirements
and success criteria, so partial delivery still leaves the repo in a coherent,
verifiable state.
