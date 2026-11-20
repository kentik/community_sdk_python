---
description: "Task list for feature 006: dependency feature adoption and reduction"
---

# Tasks: Dependency Feature Adoption and Reduction

**Input**: Design documents from `/specs/006-dependency-feature-adoption/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md),
[research.md](research.md), [data-model.md](data-model.md),
[contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: Required where a requirement asks for a check: the generator's
Markdown pass (FR-005), the import and inventory check (FR-011, FR-012), and
the `.env` parsing at the new floor (FR-002). Write each test before the
change it covers, and see it fail first.

**Organization**: Tasks are grouped by user story so each story can be built
and checked on its own.

## Format: `[ID] [P?] [Story] Description`

- [P] marks tasks that can run in parallel (different files, no open
  dependency).
- [Story] maps a task to a user story (US1 to US5).
- Every task names a file path. Requirement IDs are in parentheses.
- Never hand-edit `src/kentik_api/gen/`, `src/kentik_api/client_mixin.py`,
  or `docs/sphinx/services/`. Change the generator, then run
  `make generate`.
- Keep every line of this file at 200 characters or less. rumdl checks it
  once US3 lands.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add the two new packages once, so later stories never fight
over `uv.lock`.

- [X] T001 Add `rumdl==0.3.0` to the `dev` group and `jinja2>=3.1.6` to the
  `test` group in pyproject.toml, run `uv lock` and `uv sync`, and confirm
  with `git diff uv.lock` that the lock adds only rumdl and changes no
  locked version (SC-004, FR-008, FR-011)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Record a green baseline, so each story can prove it broke
nothing.

**Critical**: No user story work starts before this phase is complete.

- [X] T002 Run `make test`, `make typecheck`, `make check-specs`,
  `uv run ruff check .`, `uv run ruff format --check .`, and
  `uv run sphinx-build -W --keep-going -b html docs/sphinx docs/build/html`,
  confirm all pass, and copy api_surface.json to
  `$TMPDIR/api_surface.before.json` for the FR-016 comparison in T020

**Checkpoint**: Baseline green. User stories can start.

---

## Phase 3: User Story 1 - Floors exclude known-bad versions (Priority: P1) 🎯 MVP

**Goal**: No permitted version of a declared dependency has a known advisory
or a known credentials parsing fault, and CI reports new advisories.

**Independent Test**: Resolve at the lowest permitted versions (quickstart
step 6) and confirm each floor. Run `make check-changelog SINCE=HEAD`.

### Tests for User Story 1

- [X] T003 [P] [US1] Add two tests to tests/smoke/test_client_mounts_and_calls.py
  next to `test_explicit_env_file_path_is_used`: an `env_file` that starts
  with a UTF-8 byte order mark still gives `KENTIK_EMAIL`, and
  `KENTIK_API_TOKEN= # set me` reads as empty, so `KentikAPI` raises
  `ConfigurationError` naming `KENTIK_API_TOKEN` (FR-002)

### Implementation for User Story 1

- [X] T004 [US1] Raise the floors in pyproject.toml exactly as in
  contracts/dependency-records.md: `python-dotenv>=1.2.4` and
  `pydantic>=2.14.0` in `[project.dependencies]`, `ty>=0.0.84` in `dev`,
  `myst-parser>=5.1.0` in `docs`; keep `sphinxcontrib-mermaid>=1.0.0`; run
  `uv lock` and confirm no locked version changes (FR-001, FR-002, FR-003,
  FR-015, SC-004)
- [X] T005 [US1] Run `make generate` and confirm that the only change in
  api_surface.json is `requirements` for python-dotenv and pydantic (FR-017)
- [X] T006 [US1] Add both raised runtime floors to the Unreleased section of
  CHANGELOG.md as breaking changes, named the way the `API SURFACE CHANGED`
  alert from T005 names them, then run `make check-changelog SINCE=HEAD`
  (FR-017)
- [X] T007 [P] [US1] Add an `audit` job to .github/workflows/tests.yml with
  the same pinned checkout and setup-uv actions as the other jobs, running
  `uv audit --preview-features audit-command` with
  `continue-on-error: true` and a one-line comment that the command is
  experimental (FR-014, research R11)
- [X] T008 [US1] Run quickstart.md step 6 and confirm ty 0.0.84,
  pydantic 2.14.0, python-dotenv 1.2.4, MyST-Parser 5.1.0, and a docs build
  that exits 0; if any result differs, update research.md R7 and the floor
  (FR-003, SC-001)

**Checkpoint**: `make test` passes, and the floors hold at their lowest
versions.

---

## Phase 4: User Story 2 - Ruff features in use (Priority: P2)

**Goal**: Ruff formats Python blocks in Markdown, applies its 0.17 default
rules to hand-written code, and annotates CI findings.

**Independent Test**: Quickstart steps 2 to 4. A badly formatted Python
block fails `ruff format --check` with an annotation.

### Tests for User Story 2

- [X] T009 [US2] In tests/generator/test_generate_sdk.py, add a test that
  the final formatting pass of `generate_modular_sdk()` formats
  `docs/sphinx/services`, `docs/sphinx/sdk_runtime_architecture.md`,
  `docs/sphinx/README.md`, and the four guides with marker blocks
  (contracts/generator.md; FR-005)

### Implementation for User Story 2

- [X] T010 [US2] In scripts/generate_sdk.py, make the final formatting pass
  run `uv run ruff format` on the paths from T009, after
  `endpoint_docs_collector.render()` and before `api_surface.generate()`;
  T009 must pass (research R4; FR-005)
- [X] T011 [US2] In pyproject.toml `[tool.ruff]`, delete the `include` key
  and its comment, and add `.claude/skills` and `.github/skills` to
  `extend-exclude` with a one-line reason (research R3; FR-004)
- [X] T012 [US2] Run `make generate` twice and confirm that the first run
  changes only `docs/sphinx/services/bgp_monitoring.md`,
  `cloud_export.md`, and `kagent.md`, one import line per example, and
  the second run changes nothing (FR-005, SC-002)
- [X] T013 [US2] Run `uv run ruff format .` and confirm it changes only
  src/kentik_api/README.md, specs/003-harden-runtime-and-ci/contracts/runtime-api.md,
  specs/003-harden-runtime-and-ci/research.md, and
  specs/005-v5-query-batch/contracts/helpers.md (FR-004, SC-002)
- [X] T014 [US2] In pyproject.toml `[tool.ruff.lint]`, delete `select` and
  its comment; in `per-file-ignores`, add `src/kentik_api/gen/**` and
  `src/kentik_api/client_mixin.py` with every default family except `E`
  and `F` (list in research.md R5) and a one-line reason; confirm
  `uv run ruff check src/kentik_api/gen src/kentik_api/client_mixin.py`
  reports nothing (FR-006)
- [X] T015 [US2] Run `uv run ruff check --fix .` for the safe fixes only,
  then confirm with `git diff src/kentik_api/core src/kentik_api/errors`
  that the runtime changes are annotation syntax and `__all__` order only
  (FR-016, research R5)
- [X] T016 [P] [US2] Fix the remaining findings in scripts/ and reports/;
  where the code does it on purpose, add `# noqa: <code>` with a reason
  after it (data-model.md "Line suppression"; FR-006)
- [X] T017 [P] [US2] Fix the remaining findings in tests/, with the same
  suppression rule; never delete or narrow a test case (FR-006)
- [X] T018 [P] [US2] Fix the remaining findings in src/kentik_api/ and
  examples/ and docs/sphinx/conf.py; in `core/`, `errors/`, `transports/`,
  and `auth/`, use only annotation syntax or a `# noqa: BLE001` or
  `# noqa: S112` with a reason, never a narrower `except` (FR-006, FR-016)
- [X] T019 [US2] Confirm `uv run ruff check .` reports zero findings and
  `RUF100` finds no unused suppression; run `make test` and
  `make typecheck` (SC-003)
- [X] T020 [US2] Run `make generate`, then compare api_surface.json with
  `$TMPDIR/api_surface.before.json` from T002: only `requirements` may
  differ; revert or suppress any fix that changes another key (FR-016)
- [X] T021 [US2] In the `lint` job of .github/workflows/tests.yml, add
  `--output-format github` to `ruff check` and `ruff format --check`
  (contracts/lint.md; FR-007)

**Checkpoint**: `ruff check .` and `ruff format --check .` are clean, and
regeneration is stable.

---

## Phase 5: User Story 3 - Markdown rules are enforced (Priority: P2)

**Goal**: rumdl checks every hand-written Markdown file with the existing
rules, in `make lint` and in CI, with no Node.

**Independent Test**: Quickstart step 3. A list with no blank line before
it fails with `MD032`.

Run this phase after US2: both phases edit the same spec files.

### Implementation for User Story 3

- [X] T022 [US3] In .markdownlint-cli2.jsonc, disable `MD036` with the
  reason that `scripts/check_spec_refs.py` reads the bold
  `**Out of scope**` line, and change the header comment to name rumdl as
  the reader (research R2; FR-008)
- [X] T023 [US3] Run `uv run rumdl check --fix .` and check each `MD040`
  fence language it added in specs/003-harden-runtime-and-ci/ and
  docs/sphinx/index.md (FR-008)
- [X] T024 [US3] Wrap every line over 200 characters, with no word change,
  in specs/003-harden-runtime-and-ci/tasks.md,
  specs/005-v5-query-batch/tasks.md, specs/005-v5-query-batch/spec.md,
  specs/004-pre-pr-audit-remediation/plan.md,
  specs/006-dependency-feature-adoption/spec.md, and
  .github/agents/kentik-sdk-autogen.agent.md; keep each `- [ ] T###` at
  the start of its line, then run `make check-specs` (FR-008)
- [X] T025 [P] [US3] Point the three relative links in
  specs/004-pre-pr-audit-remediation/spec.md at
  `../../reports/pre-pr-audit-2026-10-10/` (FR-008)
- [X] T026 [US3] Confirm `uv run rumdl check .` reports zero findings
  (FR-008)
- [X] T027 [US3] Add `uv run rumdl check --fix .` as the last command of
  the `lint` target in Makefile, and name Ruff and rumdl in its help text
  (contracts/lint.md; FR-008)
- [X] T028 [US3] Add a `uv run rumdl check --output-format github .` step
  to the `lint` job in .github/workflows/tests.yml (FR-007, FR-008)
- [X] T029 [P] [US3] Amend the Development Workflow section of
  .specify/memory/constitution.md (PATCH 1.4.3): `make lint` runs
  `ruff check --fix`, `ruff format`, and `rumdl check --fix`; record it in
  the Sync Impact Report, and fix the `make lint` line in CLAUDE.md the
  same way (plan.md Constitution Check)

**Checkpoint**: `make lint` changes nothing, and quickstart step 3 fails on
both probes.

---

## Phase 6: User Story 4 - Test and docs tooling features in use (Priority: P3)

**Goal**: pytest runs in strict mode from its native table, and GitHub
alerts render as admonitions.

**Independent Test**: An unknown marker stops pytest. The generation guide
shows its warning as an admonition.

### Implementation for User Story 4

- [X] T030 [US4] In pyproject.toml, replace `[tool.pytest.ini_options]`
  with `[tool.pytest]` as in contracts/dependency-records.md:
  `pythonpath = ["."]`, `strict = true`, the three markers unchanged, and
  `addopts` as a list (research R8; FR-009)
- [X] T031 [US4] Run `make test`; fix each strict-mode failure by a unique
  parametrize ID or a registered marker, never by removing a case, and
  record any fix in research.md R8 (FR-009)
- [X] T032 [US4] Add `@pytest.mark.typo` to a mocked test, confirm
  `make test` stops with an unknown-marker error, and revert (FR-009)
- [X] T033 [P] [US4] Add `"alert"` to `myst_enable_extensions` in
  docs/sphinx/conf.py, build the docs with `-W`, and confirm the two alerts
  in docs/sphinx/guides/generation.md and the one in
  docs/sphinx/guides/quickstart.md render as admonitions with no `[!` text
  (research R9; FR-010, SC-005)

**Checkpoint**: `make test` and the docs build pass.

---

## Phase 7: User Story 5 - Every dependency has a recorded reason (Priority: P3)

**Goal**: An inventory page names every declared dependency with its
purpose and decision, and a test holds it and the imports to the declared
set.

**Independent Test**: Quickstart step 7. An undeclared import fails the
test.

### Tests for User Story 5

- [X] T034 [US5] Create tests/smoke/test_declared_dependencies.py: every
  third-party top-level import in src/, scripts/, and tests/ maps through
  `importlib.metadata.packages_distributions()` to a dependency declared
  in pyproject.toml, and the table in docs/sphinx/dependencies.md names
  exactly the declared dependencies; failures name the file and module, or
  the missing and extra rows (research R10; contracts/dependency-records.md;
  FR-011, FR-012); see the table half fail before T035
- [X] T035 [US5] Create docs/sphinx/dependencies.md with one row per
  declared dependency: "Dependency", "Group", "Purpose", "Decision (audit
  2026-10-17)", from the spec's inventory table; the openapi-python-generator
  row records the upstream state and the fork conditions from research.md
  R12; add a note that CI decides when rumdl and the editor disagree; add
  the page to the toctree in docs/sphinx/index.md (FR-012)
- [X] T036 [P] [US5] Write the issue draft in
  reports/upstream/upstream-openapi-python-generator-optional-formatters.md: the
  `--formatter none` call, Black, isort, and orjson in the lock, no import
  of them in project code, and the ask to make them optional extras; the
  maintainer files it (research R12; FR-013)
- [X] T037 [US5] Add `test_declared_dependencies.py` to the table in
  tests/smoke/README.md, run T034, and run quickstart.md step 7 (SC-006)

**Checkpoint**: The new test passes, and an undeclared import fails it.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T038 Run every step in quickstart.md, including the mocked suite on
  Python 3.12, 3.13, and 3.14 (SC-007, FR-016)
- [X] T039 Run `make check-specs`, `make check-changelog SINCE=HEAD`, and
  `uv run rumdl check .`, then mark each finished task `[X]` in this file

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: none.
- **Foundational (Phase 2)**: after Setup. Blocks all stories.
- **US1 (Phase 3)**: after Foundational.
- **US2 (Phase 4)**: after Foundational. T020 reads the baseline from T002.
- **US3 (Phase 5)**: after US2, because both edit spec files and the CI
  lint job.
- **US4 (Phase 6)**: after Foundational. Independent of US1 to US3.
- **US5 (Phase 7)**: after Setup (jinja2 is declared). Its inventory uses
  the floors from US1, so finish US1 first or update the rows after.
- **Polish (Phase 8)**: after all stories.

### Within Each Story

- A test task comes before the change it covers, and fails first.
- Every pyproject.toml change is sequential: T004, T011, T014, and T030
  edit the same file.
- `make generate` runs after any generator or floor change (T005, T012,
  T020).

### Parallel Opportunities

- T003 and T007 in US1.
- T016, T017, and T018 in US2: different directories.
- T025 and T029 in US3.
- T033 in US4 with T030 to T032.
- T036 in US5 with T034 and T035.
- US4 can run beside US1 or US2 on another worktree, except for the
  pyproject.toml edit in T030.

## Parallel Example: User Story 2

```text
Task: "T016 [P] [US2] Fix the remaining findings in scripts/ and reports/"
Task: "T017 [P] [US2] Fix the remaining findings in tests/"
Task: "T018 [P] [US2] Fix the remaining findings in src/kentik_api/, examples/, and docs/sphinx/conf.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 and Phase 2.
2. Phase 3: the floors, the changelog entries, and the audit job.
3. Stop and validate with quickstart.md step 6 and `make check-changelog`.
   This alone closes the security advisory and the parsing faults.

### Incremental Delivery

1. US1: floors and audit.
2. US2: Ruff Markdown formatting and rules.
3. US3: Markdown rules in CI.
4. US4: pytest strict mode and alerts.
5. US5: inventory and the import check.

Each story ends with green `make test`, `make lint`, and `make typecheck`,
and can be a separate commit on `chore/dependency-feature-adoption`.
