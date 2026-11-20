---
description: "Task list for feature 007: cross-platform task runner with Poe the Poet"
---

# Tasks: Cross-Platform Task Runner with Poe the Poet

**Input**: Design documents from `/specs/007-poe-task-runner/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md),
[research.md](research.md), [data-model.md](data-model.md),
[contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: Required where a requirement asks for a check: task help texts
(FR-005), no `envfile` (FR-006), the skill version (FR-012), the
`AGENTS.md` layout (FR-014), no `make` commands left (SC-002), and the
template header (FR-010). Write each test before the change it covers, and
see it fail first.

**Organization**: Tasks are grouped by user story so each story can be built
and checked on its own.

## Format: `[ID] [P?] [Story] Description`

- [P] marks tasks that can run in parallel (different files, no open
  dependency).
- [Story] maps a task to a user story (US1 to US4).
- Every task names a file path. Requirement IDs are in parentheses.
- Never hand-edit `src/kentik_api/gen/`, `src/kentik_api/client_mixin.py`,
  or `docs/sphinx/services/`. Change the generator, then regenerate.
- Keep every line of this file at 200 characters or less.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add poethepoet once, so later stories never fight over
`uv.lock`.

- [X] T001 Add `poethepoet==0.49.0` to the `dev` group in pyproject.toml, run
  `uv lock` and `uv sync`, and confirm with `git diff uv.lock` that the lock
  adds only poethepoet and changes no locked version (FR-001, SC-003)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Record a green baseline, and add the one constant that the
header and the script messages share.

**Critical**: No user story work starts before this phase is complete.

- [X] T002 Run `make test`, `make typecheck`, `make lint` with
  `git status --short` clean, `make check-specs`, and
  `uv run sphinx-build -W --keep-going -b html docs/sphinx docs/build/html`,
  confirm all pass, and copy api_surface.json to
  `$TMPDIR/api_surface.before.json` for the FR-015 comparison in T036 (SC-006)
- [X] T003 Add `REGENERATE_COMMAND = "uv run poe generate"` to
  scripts/generation/_shared.py, and list it in the `_shared.py` section of
  scripts/generation/README.md (FR-010)

**Checkpoint**: Baseline green, constant in place. User stories can start.

---

## Phase 3: User Story 1 - Any OS runs every task (Priority: P1) MVP

**Goal**: After `uv sync`, every project task runs as `uv run poe <task>`
with no shell, on any OS, and the `Makefile` is gone.

**Independent Test**: `uv run poe` lists every task with help;
`uv run poe test`, `lint`, `typecheck`, `generate`, and `clean` behave as the
Make targets did, with no POSIX tool.

### Tests for User Story 1

- [X] T004 [US1] Create tests/smoke/test_task_runner.py with
  `test_every_task_has_help` (every entry in `[tool.poe.tasks]` has a
  one-line `help`), `test_no_task_loads_an_env_file` (no `envfile` key at
  any level under `[tool.poe]`), and `test_no_task_uses_a_shell` (no task of
  type `shell`), reading pyproject.toml with `tomllib`; run them and see
  them fail (FR-004, FR-005, FR-006)
- [X] T005 [P] [US1] Create tests/smoke/test_tasks_module.py for
  scripts/tasks.py: `clean()` removes `src/kentik_api/gen/`, `docs/build/`,
  `docs/sphinx/services/`, and every `__pycache__` in a `tmp_path` copy and
  keeps `scripts/openapi_templates/`, `src/kentik_api/core/`, and
  `docs/sphinx/local_generation_workflow.md`; `deep_clean()` keeps `.venv/`
  and prints the removal command when `sys.platform == "win32"` and
  `sys.prefix` is inside it; `check_drift()` returns 1 and prints each path
  on a dirty Git tree and 0 on a clean one; see them fail (FR-004)

### Implementation for User Story 1

- [X] T006 [US1] Create scripts/tasks.py with `clean()`, `deep_clean()`, and
  `check_drift()` per contracts/tasks.md, using `shutil.rmtree`, `pathlib`,
  and `subprocess.run(["git", "status", "--porcelain"])` with an argument
  list; each takes a repository root that defaults to the project root, so
  T005 can pass `tmp_path`; T005 passes (FR-004, R10)
- [X] T007 [US1] Add `[tool.poe.env]` with `PYTHONUTF8 = "1"` and every task
  in the contracts/tasks.md map to `[tool.poe.tasks]` in pyproject.toml:
  `cmd` for one command, `sequence` for `all`, `docs`, `lint`, and
  `lint-check`, `script` for `clean`, `deep-clean`, and `check-drift`, each
  with a one-line `help`, and no `envfile`; T004 passes (FR-002, FR-004,
  FR-005, FR-006, SC-004, R4)
- [X] T008 [US1] Add `line-ending = "lf"` to `[tool.ruff.format]` in
  pyproject.toml, and create .gitattributes with `* text=auto eol=lf`;
  run `git add --renormalize .` and confirm with `git status --short` that
  no tracked file changes (FR-013, R5)
- [X] T009 [US1] Replace `test_make_help_lists_targets_with_digits` in
  tests/smoke/test_docs_contract.py with a test that `uv run poe` exits 0
  and its output names every task in `[tool.poe.tasks]` (FR-005)
- [X] T010 [P] [US1] Stop copying `Makefile` into the sandbox in
  tests/generator/conftest.py, and copy pyproject.toml there if any test in
  tests/generator/ still needs the task table (FR-009)
- [X] T011 [US1] Delete Makefile, then run `uv run poe test`,
  `uv run poe typecheck`, `uv run poe lint-check`, and `uv run poe clean`
  followed by `uv run poe generate` and `uv run poe check-drift`; all pass
  (FR-009, SC-006)

**Checkpoint**: Every task runs through poe on macOS and Linux. No Makefile.

Note (T011): `lint-check` fails here only on rumdl MD057, because 37 Markdown files
still link to the deleted `Makefile`. T029 to T035 rewrite those links, and T035 confirms the pass.

---

## Phase 4: User Story 3 - Same task names and options (Priority: P2)

**Goal**: Each Make variable becomes a named option, and a path with spaces
stays one argument.

**Independent Test**: quickstart.md step 3 prints the expected arguments
with `uv run poe -d`.

Phase 4 runs before US2 because US2's CI jobs call these options.

### Tests for User Story 3

- [X] T012 [US3] Add `test_task_options_reach_the_program` to
  tests/smoke/test_task_runner.py: run `uv run poe -d` for
  `generate --local`, `generate --local-repo "/tmp/a b"`,
  `generate --schema-ref REF`, `check-changelog --since REF`,
  `release-notes --since REF --out PATH`, and
  `impact-report --since REF --no-checks --out PATH`, and check the printed
  arguments; see it fail where an option is missing (FR-003)

### Implementation for User Story 3

- [X] T013 [US3] Add `args` to `generate`, `release-notes`,
  `check-changelog`, and `impact-report` in pyproject.toml, each value option
  written as `${name:+--flag "${name}"}` and `--local` as
  `${local:+--local-repo ../api-schema-public/}`, with help on each option;
  T012 passes (FR-003, R2)
- [X] T014 [US3] Run quickstart.md steps 2 and 3 and confirm
  `uv run poe -h generate` lists `--local`, `--local-repo`, and
  `--schema-ref` (FR-003, SC-004)

**Checkpoint**: Every Make target and variable has its poe form.

---

## Phase 5: User Story 2 - CI uses the same tasks on three OSs (Priority: P1)

**Goal**: CI calls only poe tasks and runs `test`, `lint-check`,
`typecheck`, and the drift check on Windows, macOS, and Linux.

**Independent Test**: A pull request run shows no `make` step, and the
Windows and macOS jobs pass.

### Implementation for User Story 2

- [X] T015 [US2] In .github/workflows/tests.yml, turn the `test` job into an
  `os` by `python` matrix with `fail-fast: false`: ubuntu on 3.12, 3.13, and
  3.14, windows and macos on 3.12, each running `uv run poe test`
  (FR-007, FR-008)
- [X] T016 [US2] In .github/workflows/tests.yml, give the `typecheck` job and
  a new `lint` job an `os` matrix of ubuntu, windows, and macos with
  `fail-fast: false`, running `uv run poe typecheck` and
  `uv run poe lint-check`; remove any direct `ruff` or `rumdl` step that
  `lint-check` replaces (FR-007, FR-008)
- [X] T017 [US2] In .github/workflows/tests.yml, give
  `generated-output-matches-schema-pin` the same three-OS matrix, and replace
  `make generate` and the bash drift step with `uv run poe generate` and
  `uv run poe check-drift` (FR-007, FR-008, R9)
- [X] T018 [US2] In .github/workflows/tests.yml, change `spec-references` to
  `uv run poe check-specs`, `changelog` to
  `uv run poe check-changelog --since "$(git merge-base HEAD origin/${{ github.base_ref }})"`
  with `shell: bash`, `audit` to `uv run poe audit`, and `docs` to
  `uv run poe docs-build`, and rewrite the header comment that names
  `make test-e2e` (FR-007)
- [X] T019 [P] [US2] In .github/workflows/schema-sync.yml, replace
  `make sync-schema` with `uv run poe sync-schema` in the step and in the
  pull request text (FR-007)
- [X] T020 [US2] Validate both workflows: parse each with `yaml.safe_load`
  and confirm `grep -n "make " .github/workflows/*.yml` finds nothing
  (FR-007, SC-002)

**Checkpoint**: CI is written; the pull request run in T038 proves it.

Note (T020): release.yml also ran `scripts/release_notes.py` directly. It now runs
`uv run poe release-notes --out surface-notes.md`, so every CI step calls a poe task (FR-007).

---

## Phase 6: User Story 4 - Docs and agents point to poe (Priority: P2)

**Goal**: Generated headers, hand-written docs, instruction files, and
script messages name poe; the poe skill is committed and current;
`AGENTS.md` works on Windows.

**Independent Test**: `test_no_make_commands_outside_past_specs`,
`test_agent_skill_matches_locked_poe`,
`test_agents_md_is_a_regular_file_and_claude_md_imports_it`, and the
template header test pass, and a regeneration changes only header lines.

### Tests for User Story 4

- [X] T021 [P] [US4] Add
  `test_service_template_header_names_the_regenerate_command` to
  tests/generator/test_openapi_templates.py: the header in
  scripts/openapi_templates/service.jinja2 contains `REGENERATE_COMMAND`;
  see it fail (FR-010)
- [X] T022 [US4] Add `test_agent_skill_matches_locked_poe` and
  `test_agents_md_is_a_regular_file_and_claude_md_imports_it` to
  tests/smoke/test_task_runner.py: `.claude/skills/poethepoet/version.txt`
  equals `importlib.metadata.version("poethepoet")` and the failure message
  names `uv run poe _install_skill .claude/skills --upgrade`; `AGENTS.md` is
  not a link in the index (`git ls-files -s` mode `100644`) and CLAUDE.md is
  exactly `@AGENTS.md`; see both fail (FR-012, FR-014)
- [X] T023 [US4] Add `test_no_make_commands_outside_past_specs` to
  tests/smoke/test_task_runner.py: scan every file from `git ls-files` that
  decodes as UTF-8 for a `make <target>` command (any task or former target
  name) or `Makefile`, skipping `specs/001-*` to `specs/007-*`, `reports/`,
  `.specify/`, `.github/skills/`, and `.claude/skills/`; report file and
  line; see it fail (SC-002, FR-011, R11)

### Implementation for User Story 4

- [X] T024 [US4] Replace the 8 hard-coded header literals in
  scripts/generation/endpoint_docs.py, scripts/generation/docs_rendering.py,
  and scripts/generation/wrapper_generation.py, and the header in
  `_inject_generated_headers()` and the printed messages in
  scripts/generate_sdk.py, with `REGENERATE_COMMAND` through the relative
  `._shared` import (FR-010, R8)
- [X] T025 [US4] Change the header text in
  scripts/openapi_templates/service.jinja2 to `uv run poe generate`, and any
  message in scripts/generation/api_surface.py that names `make generate`;
  T021 passes (FR-010)
- [X] T026 [US4] Run `uv run poe generate`, then confirm with
  `git diff --stat` and `git diff -U0 | grep '^[+-][^+-]'` that only header
  lines changed under src/kentik_api/gen/, src/kentik_api/client_mixin.py,
  docs/sphinx/services/, and the other generated pages, and that
  api_surface.json does not change (FR-010, FR-015)
- [X] T027 [US4] Run `git mv` to swap the files: AGENTS.md becomes a regular
  file with today's CLAUDE.md text, and CLAUDE.md becomes the one line
  `@AGENTS.md`; update the shared-rules note that says AGENTS.md is a
  symlink (FR-014, R6)
- [X] T028 [US4] Run `uv run poe _install_skill .claude/skills`, commit
  `.claude/skills/poethepoet/` as written, and add
  `.claude/skills/poethepoet/**` to `ignores` in .markdownlint-cli2.jsonc
  and to rumdl's exclude in pyproject.toml if it lints that path; T022
  passes (FR-012, SC-005, R7)
- [X] T029 [US4] Rewrite `make` commands to poe tasks in AGENTS.md:
  key commands, testing strategy, generation pipeline, and the
  `HAND-WRITTEN` marker, which names `uv run poe generate` (FR-011)
- [X] T030 [P] [US4] Rewrite `make` commands to poe tasks in README.md,
  README.pypi.md, CONTEXT.md, docs/README.md, scripts/README.md,
  tests/README.md, tests/generator/README.md, scripts/generation/README.md,
  examples/README.md, and learn/README.md; a Markdown link to `Makefile`
  points at `pyproject.toml` instead (FR-011)
- [X] T031 [P] [US4] Rewrite `make` commands to poe tasks in the
  hand-written prose of docs/sphinx/ (guides, authentication.md,
  dependencies.md, local_generation_workflow.md, index.md, README.md),
  outside the `kentik-gen` marker blocks that the generator writes
  (FR-011)
- [X] T032 [P] [US4] Rewrite `make` commands in messages that scripts print
  (scripts/release_notes.py, scripts/impact_report.py,
  scripts/check_spec_refs.py, scripts/sample_consume_sdk.py), in
  pyproject.toml marker help texts, in tests/e2e/ skip messages, and in
  .github/agents/kentik-sdk-autogen.agent.md (FR-011)
- [X] T033 [P] [US4] Amend .specify/memory/constitution.md to PATCH 1.4.4:
  each `make <target>` becomes `uv run poe <task>`, and the governance line
  says AGENTS.md holds the instructions and CLAUDE.md imports it; add the
  Sync Impact Report entry (FR-011, FR-014)
- [X] T034 [US4] Add an Unreleased entry to CHANGELOG.md: contributors run
  `uv run poe <task>` instead of `make <target>`, the `Makefile`,
  `services`, and `tests` aliases are gone, and AGENTS.md is now the
  instruction file (FR-009, FR-011)
- [X] T035 [US4] Run `uv run poe test-smoke` and fix each file that
  `test_no_make_commands_outside_past_specs` reports, until it passes
  (SC-002, FR-011)

**Checkpoint**: No `make` command outside past specs; skill and instruction
files in place.

Note (T029 to T035): `CLAUDE.md` now holds only `@AGENTS.md`, and GitHub Copilot
does not expand imports. References that sent a reader or an agent to `CLAUDE.md`
for content (the Copilot agent file, three README links, and test docstrings and
skip messages) now name `AGENTS.md`. `src/kentik_api/gen/__init__.py` kept the old
header after an incremental run, because the generator only creates it when it is
missing; a clean regeneration (`uv run poe clean`, then `generate`) rewrote it.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Prove nothing outside the task runner changed, and run the
quickstart.

- [X] T036 Run `uv run poe test` on Python 3.12, 3.13, and 3.14,
  `uv run poe typecheck`, `uv run poe lint-check`, `uv run poe check-specs`,
  `uv run poe check-changelog --since feat/v6-sdk`, `uv run poe docs-build`,
  and `uv run poe generate` with `uv run poe check-drift`; compare
  api_surface.json with `$TMPDIR/api_surface.before.json`; confirm no file
  under src/kentik_api/ outside gen/ and client_mixin.py changed
  (SC-006, FR-015)
- [X] T037 Run quickstart.md steps 1 to 6 on macOS and record any difference
  from the expected output in this file (SC-001, SC-004, SC-005)
- [X] T038 On the pull request run (after the user asks for the pull
  request), confirm the `test`, `lint`, `typecheck`, and
  `generated-output-matches-schema-pin` jobs pass on windows-latest and
  macos-latest, and fix any POSIX assumption they show without a skip
  "to pass" (SC-001, FR-008, FR-013)

Results (T036, T037, 2026-10-17, macOS): `uv run poe test` passes 3536 tests on Python 3.12,
3.13, and 3.14. `typecheck`, `lint-check`, `check-specs`, `check-changelog --since feat/v6-sdk`,
and `docs-build` pass. `clean`, then `generate`, then `check-drift` exits 0. api_surface.json
equals the T002 baseline, and the runtime diff outside gen/ is marker and link lines only.
Quickstart steps 1 to 6 match the expected output. One finding: rumdl's MD041 flagged the
one-line CLAUDE.md, so .markdownlint-cli2.jsonc now ignores it.

Results (T038, 2026-10-17, fork CI run 39084416624): all 19 jobs pass on ubuntu, windows,
and macos. The first Windows runs found three POSIX assumptions, each fixed without a skip:
protoc needs `/` in proto file paths, `DFCache` file names held `:`, and `Path.write_text`
wrote CRLF, which `git status` reports as a change (now `write_text_lf()`, R5).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup. Blocks every story.
- **US1 (Phase 3)**: Depends on Phase 2.
- **US3 (Phase 4)**: Depends on US1 (the tasks exist before their options).
- **US2 (Phase 5)**: Depends on US1 and US3 (CI calls the tasks and
  options).
- **US4 (Phase 6)**: T021 to T028 depend only on Phase 2 and T001. The text
  rewrite T029 to T035 depends on US1 and US3, so it names final task and
  option names.
- **Polish (Phase 7)**: Depends on all stories. T038 waits for the user to
  ask for the pull request.

### Within Each Story

- Tests first, and see them fail.
- T006 before T007 (the script tasks call scripts/tasks.py).
- T011 (delete Makefile) after T009 and T010 (the tests that read it).
- T024 and T025 before T026 (regenerate after the header changes).
- T027 before T029 (rewrite AGENTS.md after the swap).

### Parallel Opportunities

- T004 and T005 (different test files).
- T010 with T009.
- T019 with T015 to T018 (different workflow files).
- T021 with T022 and T023.
- T030, T031, T032, and T033 (different files).

---

## Parallel Example: User Story 4

```text
Task: "T030 Rewrite make commands in README files"
Task: "T031 Rewrite make commands in docs/sphinx/ prose"
Task: "T032 Rewrite make commands in script messages and the agent file"
Task: "T033 Amend the constitution to PATCH 1.4.4"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Phase 1 and Phase 2.
2. Phase 3 (US1): poe runs every task, the Makefile is gone.
3. Stop and check: `uv run poe test`, `lint-check`, `typecheck`,
   `generate`, `check-drift`.

### Incremental Delivery

1. US1: tasks run through poe.
2. US3: options match the Make variables.
3. US2: CI calls the tasks on three operating systems.
4. US4: headers, docs, instruction files, and the skill.
5. Polish: full checks, quickstart, then the pull request run.

Commit after each task or logical group.
