# Implementation Plan: Cross-Platform Task Runner with Poe the Poet

**Branch**: `chore/poe-task-runner` | **Date**: 2026-10-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/007-poe-task-runner/spec.md`

## Summary

Replace the `Makefile` with Poe the Poet tasks in `pyproject.toml`, so every
project task runs with `uv run poe <task>` on Windows, macOS, and Linux
after `uv sync`. Tasks are shell-free: plain commands, sequences, and three
small Python functions for cleaning and the drift check. CI calls the same
tasks and adds Windows and macOS jobs for tests, lint, type check, and
generation with the drift check. The generator's header names the poe
command through one constant. `AGENTS.md` becomes the real instruction file
and `CLAUDE.md` imports it, so Windows checkouts see the instructions. The
poe agent skill is committed once under `.claude/skills/`, and a test keeps
its version equal to the locked poe.

## Technical Context

**Language/Version**: Python 3.12 to 3.14

**Primary Dependencies**: poethepoet 0.49.0 (new, dev group; its one
dependency, PyYAML, is already locked). uv, Ruff, rumdl, ty, pytest, Sphinx
as today.

**Storage**: N/A

**Testing**: pytest (mocked layers, plus a new
`tests/smoke/test_task_runner.py`), ty, Ruff, rumdl, Sphinx with `-W`, the
drift check on three operating systems.

**Target Platform**: Windows, macOS, and Linux, each with only uv and Git
installed.

**Project Type**: Library (generated SDK) with a code generator.

**Performance Goals**: N/A. Poe adds well under one second of startup.

**Constraints**:

- No task may use a shell or load `.env` (FR-004, FR-006).
- Generated output changes only in its header line (FR-010).
- No change to the runtime or the public API surface (FR-015).
- Specs 001 to 006 keep their `make` commands (FR-011).

**Scale/Scope**: 25 Make targets map to 24 tasks (5 dropped, 4 added for CI).
About 1,430 generated files and 45 service pages change one header line.
About 190 hand-written files change `make` commands. 2 workflows, 1 new
Python module, 1 new test file, and 1 new folder of vendored skill files.

No item is NEEDS CLARIFICATION. [research.md](research.md) resolves each
design point from probes of poe 0.49.0 and the Claude Code docs. Windows
behavior that no local probe shows (R4, R5, R9) is confirmed by the new
Windows CI jobs.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | How the design meets it |
| --- | --- | --- |
| I. Generated code is never hand-edited | Pass | The header text changes in the generator, through `REGENERATE_COMMAND`, then a regeneration rewrites every generated file. |
| II. One shared runtime | Pass | No runtime code changes. |
| III. Phase modules stay testable | Pass | The constant goes in `_shared.py` because 4 phase modules use it. Imports stay relative. The template header gets a test in `tests/generator/`. |
| IV. Exhaustive coverage | Pass | No test is removed or narrowed. `test_make_help_lists_targets_with_digits` tests a file that is deleted; its replacement tests that every task has help. The Windows and macOS jobs run the full mocked suite. |
| V. E2E opt-in and safe | Pass | `test-e2e` and `test-e2e-grpc` stay out of `all` and CI. Markers are unchanged. |
| VI. Credentials | Pass | No task has `envfile`; a test enforces it (R3). |
| VII. Compatibility and scope | Pass | No API surface change. The contributor command changes from `make` to `uv run poe`, which `CHANGELOG.md` records. |

The constitution names `make` targets in Principles IV and V, the
Architecture section, and the Development Workflow section, and says
`AGENTS.md` is a symlink. A task amends them (PATCH 1.4.4): the commands
and the instruction-file layout change, no principle changes.

Re-check after Phase 1: all principles pass. One spec deviation is recorded
in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/007-poe-task-runner/
├── spec.md
├── plan.md               # this file
├── research.md           # Phase 0
├── data-model.md         # Phase 1
├── quickstart.md         # Phase 1
├── contracts/            # Phase 1
│   ├── tasks.md
│   ├── ci.md
│   └── repository-files.md
├── checklists/requirements.md
└── tasks.md              # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
pyproject.toml                    # poethepoet, [tool.poe], ruff line-ending
Makefile                          # deleted
.gitattributes                    # new: LF everywhere
AGENTS.md                         # becomes the real instruction file
CLAUDE.md                         # becomes "@AGENTS.md"
.claude/skills/poethepoet/        # new: vendored poe skill
.markdownlint-cli2.jsonc          # ignore the vendored skill
scripts/tasks.py                  # new: clean, deep_clean, check_drift
scripts/generation/_shared.py     # REGENERATE_COMMAND
scripts/generate_sdk.py           # header and messages use the constant
scripts/generation/{endpoint_docs,docs_rendering,wrapper_generation,api_surface}.py
scripts/openapi_templates/service.jinja2
.github/workflows/tests.yml       # poe tasks, Windows and macOS jobs
.github/workflows/schema-sync.yml # poe sync-schema
tests/smoke/test_task_runner.py   # new: help, envfile, skill, AGENTS.md, no make
tests/smoke/test_docs_contract.py # Makefile help test replaced
tests/generator/conftest.py       # stop copying Makefile into the sandbox
tests/generator/test_openapi_templates.py  # template header test
src/kentik_api/gen/**, docs/sphinx/services/**, ...  # regenerated header
docs/, README files, CHANGELOG.md, CONTEXT.md, .github/agents/, .specify/memory/constitution.md
```

**Structure Decision**: Tasks live in `pyproject.toml` next to the other tool
configuration. The three Python task functions go in `scripts/tasks.py`,
next to the other hand-written scripts, and run as `script` tasks. The new
checks go in `tests/smoke/`, next to `test_docs_contract.py` and
`test_packaging_contract.py`, because they check repository and tooling
facts, not generated code.

## Phases after this plan

1. Tooling: add poethepoet, write `[tool.poe]` and `scripts/tasks.py`, with
   `tests/smoke/test_task_runner.py` first. Delete the `Makefile`, and fix
   the two tests that read it.
2. Line endings and encoding: `.gitattributes`, Ruff `line-ending`,
   `PYTHONUTF8`. Renormalize the index once.
3. Header: `REGENERATE_COMMAND`, the template test, then
   `uv run poe generate`. Confirm only header lines changed.
4. Instructions: `AGENTS.md` and `CLAUDE.md`, the vendored skill, the
   constitution PATCH.
5. Text: rewrite `make` commands in hand-written files and script messages,
   until the no-`make` test passes.
6. CI: `tests.yml` matrix and `schema-sync.yml`.
7. Validation: [quickstart.md](quickstart.md), then a pull request run on
   all three operating systems.

## Risks

| Risk | Effect | Response |
| --- | --- | --- |
| Generation has never run on Windows (`protoc` paths, Git clone, subprocess) | The Windows drift job fails | Fix the generator where it assumes POSIX; the job is the proof (R9). |
| A Windows file writes CRLF that `.gitattributes` does not cover | The drift job fails | Done: every generator write uses `write_text_lf()` in `_shared.py` (R5). |
| Python on Windows CI cannot print emoji | The generator crashes in CI | `PYTHONUTF8 = "1"` in `[tool.poe.env]` (R4). |
| A test assumes POSIX paths or tools | The Windows `test` job fails | Fix the test so it holds on every OS. A skip needs a reason that the feature does not exist on that OS, never "to pass". |
| Contributors type `make` from habit | Make prints "No targets" | `README.md` and `AGENTS.md` name the poe commands. |
| A poe upgrade makes the vendored skill stale | The skill version test fails | Run `uv run poe _install_skill .claude/skills --upgrade`, as the failure message says. |

## Complexity Tracking

| Deviation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| SC-002 allows `make` commands only in specs 001 to 006. The no-`make` test also skips `specs/007-*`. | Spec 007 must name the Make targets it replaces, in its spec, research, and contracts. | Rewording spec 007 without the old target names would make the migration map unreadable. |
| FR-002 names only the Make targets as tasks. The plan adds `check-drift`, `lint-check`, `docs-build`, and `audit`. | FR-007 requires every CI job to call a poe task, and those four CI steps had no Make target. | Calling tools directly in those jobs breaks FR-007; a shell drift check fails on Windows' default shell. |
