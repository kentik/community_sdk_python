# Feature Specification: Cross-Platform Task Runner with Poe the Poet

**Feature Branch**: `chore/poe-task-runner`

**Created**: 2026-10-17

**Status**: Draft

**Input**: User description: "Move from Make to a Python task runner, so the
whole project works on any OS without custom or manual installs. Use
poethepoet instead of Invoke, and use the agent skill that it ships."

## Background

The project runs its tasks through a `Makefile` with 25 targets. Make is
not installed on Windows by default. The recipes also use POSIX shell
commands: `rm -rf`, `find -exec`, `grep` and `awk` in `help`, and a `[ ]`
test in the `local` marker target. CI calls `make` in 5 places and runs
only on Ubuntu, so nothing tests the project on Windows or macOS.

Poe the Poet (`poethepoet`, MIT license, version 0.49.0 of 2026-10-15) is a
task runner that reads its tasks from `pyproject.toml`. The facts that
matter here, from its documentation and its bundled skill:

- A `cmd` task runs its command as a subprocess without a shell. Globs
  expand through Python `pathlib`, so they work the same way on every OS.
- A `script` task calls a Python function. A `sequence` task runs tasks in
  order, and a `switch` task picks a task by platform or argument.
- Tasks take named options with defaults, types, and help text. Running
  `poe` with no task lists every task with its help text.
- Its only extra dependency is PyYAML, which the lock already holds. Adding
  poethepoet adds one package to the lock.
- The package bundles an agent skill: a `SKILL.md` file and 5 reference
  files that target poe 0.49.0. The command
  `poe _install_skill [<skills-dir>] [--upgrade]` copies it to
  `<skills-dir>/poethepoet/`. The skill tells the agent to warn the user
  when the installed poe is newer than the skill.

Claude Code reads project skills from `.claude/skills/`. GitHub Copilot
reads project skills from `.github/skills/`, `.claude/skills/`, or
`.agents/skills/`, as its documentation "About agent skills" states. One
copy in `.claude/skills/` therefore serves both agents.

Invoke 3.0.3 was the other candidate. It reads tasks from a Python file and
runs each command string through a shell: bash on Linux and macOS, cmd.exe
on Windows. It published no release between July 2023 and October 2025.
Poe the Poet runs plain commands without a shell and keeps the tasks in
`pyproject.toml` with the rest of the tool configuration.

The move touches many files:

- The generator writes the header "Rebuilt on every `make generate`" into
  1,431 generated files.
- 194 hand-written files mention `make` commands 582 times. Most are docs,
  `CLAUDE.md`, the agent file, messages that scripts print, and specs
  001 to 006.

Two parts of the repository can fail on Windows:

- `AGENTS.md` is a Git symbolic link to `CLAUDE.md`. Without symbolic link
  support, Git checks it out as a text file that contains only `CLAUDE.md`.
- The repository has no `.gitattributes` file. A Windows Git configured to
  convert line endings checks out files with CRLF line endings, and the
  generated-output drift check compares bytes.

This spec builds on spec 006, which adds rumdl to the lint task.

## Clarifications

### Session 2026-10-17

- Q: What happens to the `Makefile`? A: Delete it. The project has one way
  to run tasks.
- Q: Which agent folders receive the poe skill? A: Both Claude Code and
  GitHub Copilot get it from one copy in `.claude/skills/poethepoet/`,
  because both agents read that folder. There is no second copy and no
  symbolic link. A symbolic link fails on Windows checkouts in the same
  way as `AGENTS.md`.
- Q: Which tasks must CI run on Windows and macOS? A: `test`, `lint`,
  `typecheck`, and `generate` with the drift check, on both. macOS is the
  main development platform, so it gets the full set.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Any OS runs every task (Priority: P1)

A contributor on Windows, macOS, or Linux installs uv and Git, clones the
repository, and runs `uv sync`. Every project task then runs with
`uv run poe <task>`, with no other install.

**Why this priority**: This is the reason for the change. Today a Windows
contributor must install Make and a POSIX shell first.

**Independent Test**: On a clean Windows host with only uv and Git, clone
the repository and run `test`, `lint`, `typecheck`, and `generate`.

**Acceptance Scenarios**:

1. **Given** a fresh clone and `uv sync`, **When** the contributor runs
   `uv run poe`, **Then** poe lists every task with a one-line help text.
2. **Given** a Windows host, **When** the contributor runs
   `uv run poe test`, **Then** the mocked suite passes.
3. **Given** any OS, **When** the contributor runs `uv run poe clean`,
   **Then** the same paths are removed as on Linux.

---

### User Story 2 - CI uses the same tasks on three OSs (Priority: P1)

CI calls the same poe tasks that contributors run, and it runs them on
Windows, macOS, and Linux.

**Why this priority**: Without a Windows and a macOS job, nothing proves
User Story 1, and it breaks again unnoticed.

**Independent Test**: Open a pull request and make sure that every job
calls a poe task and that the Windows and macOS jobs pass.

**Acceptance Scenarios**:

1. **Given** a pull request, **When** CI runs, **Then** no job calls
   `make`.
2. **Given** a change that breaks a task on Windows only, **When** CI
   runs, **Then** the Windows job fails.
3. **Given** a regeneration on Windows or macOS at the pinned schema
   commit, **When** the drift check runs, **Then** the tree matches the
   committed tree byte for byte.

---

### User Story 3 - Same task names and options (Priority: P2)

A maintainer who knows the `Makefile` finds each target under the same
name, with options in place of Make variables.

**Why this priority**: Familiar names make the move cheap for people and
for agents.

**Independent Test**: For each `Makefile` target, run the poe task with
the same name and the same inputs, and compare the result.

**Acceptance Scenarios**:

1. **Given** `make generate local`, **When** the maintainer runs
   `uv run poe generate --local`, **Then** the generator reads
   `../api-schema-public/`.
2. **Given** `make generate LOCAL_REPO=<path>` or `SCHEMA_REF=<ref>`,
   **When** the maintainer runs `uv run poe generate --local-repo <path>`
   or `--schema-ref <ref>`, **Then** the generator gets the same argument.
3. **Given** `make check-changelog SINCE=<ref>`, **When** the maintainer
   runs `uv run poe check-changelog --since <ref>`, **Then** the result is
   the same.

---

### User Story 4 - Docs and agents point to poe (Priority: P2)

A reader of the docs, an agent that reads `CLAUDE.md`, or a reader of a
generated file finds poe commands, not `make` commands. An agent also has
the poe skill.

**Why this priority**: Stale instructions send people and agents to a tool
that is gone or that does not run on their OS.

**Independent Test**: Search the hand-written instructions and the
generated headers for `make` commands, and check the skill version.

**Acceptance Scenarios**:

1. **Given** a regeneration, **When** a reader opens a generated file,
   **Then** its header names the poe command.
2. **Given** an agent with the poe skill, **When** it compares the skill
   version with the locked poe version, **Then** they match.
3. **Given** a Windows checkout, **When** an agent reads `AGENTS.md`,
   **Then** it finds the same instructions as in `CLAUDE.md`.

### Edge Cases

- `KentikAPI` reads `.env` into a dictionary and never into the process
  environment, because the environment leaks to every subprocess. A poe
  task with `envfile = ".env"` would load the credentials into every
  command that the task runs. No task can do this.
- `deep-clean` deletes `.venv`, which holds the running poe executable.
  Windows does not let a process delete its own running executable, so the
  task must handle that case on Windows.
- `test-e2e` and `test-e2e-grpc` use real credentials. They stay out of
  `all` and out of CI, as they are today.
- Dependabot can move poe ahead of the committed skill. The version check
  then fails until a maintainer runs `poe _install_skill <dir> --upgrade`.
- The committed skill is third-party content. The Markdown check and the
  Spec Kit tooling must leave it alone, like the vendored Spec Kit skills.
- The default file systems on Windows and macOS ignore letter case. Today
  no two tracked paths differ only by case. A generated path that does
  would collide there, and the Windows and macOS jobs catch it.
- Specs 001 to 006 record past decisions. Their `make` commands stay as
  written.
- A contributor who types `make` out of habit after the move gets an error
  from Make, because no `Makefile` exists. The `README.md` names the poe
  command.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The dev group MUST pin poethepoet to an exact version.
- **FR-002**: Each `Makefile` target MUST have a poe task with the same
  name, except `help` (bare `poe` lists the tasks), `install` (poe needs
  `uv sync` first), and `local` (it becomes the `--local` option).
- **FR-003**: Make variables MUST become named task options:
  `--local`, `--local-repo`, and `--schema-ref` on `generate`, `--since`
  and `--out` on `release-notes` and `impact-report`, `--since` on
  `check-changelog`, and `--no-checks` on `impact-report`.
- **FR-004**: No task MUST need a POSIX shell. A task MUST be a plain
  command, a Python function, or a combination of tasks.
- **FR-005**: Every task MUST have a one-line help text.
- **FR-006**: No task MUST load `.env` into the environment.
- **FR-007**: CI MUST call poe tasks and MUST NOT call `make`.
- **FR-008**: CI MUST run `test`, `lint`, `typecheck`, and `generate` with
  the drift check on Windows and macOS, in addition to the current Linux
  jobs.
- **FR-009**: The `Makefile` MUST be deleted.
- **FR-010**: The generator MUST write a header that names the poe
  regeneration command. The regenerated tree MUST change only in that
  header.
- **FR-011**: Hand-written docs, `CLAUDE.md`, the agent file, the
  `README.md` files, and messages that scripts print MUST name poe tasks.
  Specs 001 to 006 MUST stay as written.
- **FR-012**: The poe skill MUST exist as one committed copy in
  `.claude/skills/poethepoet/`, with no other copy and no symbolic link. A
  check MUST fail when its version differs from the locked poe version.
- **FR-013**: Text files MUST check out with LF line endings on every OS.
- **FR-014**: An agent on a Windows checkout MUST find the same
  instructions in `AGENTS.md` as in `CLAUDE.md`.
- **FR-015**: The work MUST NOT change the SDK runtime, the public API
  surface, or generated code other than the header in FR-010.

### Key Entities

- **Task**: A named, documented project command in `[tool.poe.tasks]`,
  with optional named options. It replaces a `Makefile` target.
- **Agent skill**: The `SKILL.md` and reference files that poethepoet
  bundles, with the poe version that they target.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On Windows, macOS, and Linux, a fresh clone with only uv and
  Git runs `test`, `lint`, `typecheck`, and `generate`, and the drift
  check passes.
- **SC-002**: Zero `make` commands remain in CI, in hand-written
  instructions, or in generated headers. Specs 001 to 006 are the only
  exception.
- **SC-003**: The lock file grows by one package, poethepoet.
- **SC-004**: All 25 `Makefile` targets have a poe task or the documented
  replacement from FR-002.
- **SC-005**: The committed skill version equals the locked poe version.
- **SC-006**: The mocked test suite, the type check, the lint check, the
  docs build, and the generated-output drift check pass on Linux, as they
  do today.

## Assumptions

- Contributors install uv and Git with the official installers. Both exist
  for Windows, macOS, and Linux.
- Contributors run tasks as `uv run poe <task>`. A global poe install is
  optional.
- The aliases `services` and `tests` go away, and the docs name `generate`
  and `test`. `all` stays.
- The Vercel skills page that started this idea lists Vercel-published
  skills and describes the `skills` command-line tool, which needs Node.
  It does not list poethepoet. The poe skill comes from the poethepoet
  package itself, so installing it needs no Node.
- Python and the generator scripts already avoid POSIX-only calls. They
  call subprocesses with argument lists and use `shutil` and `pathlib`.
  The Windows job is the proof.
- The Windows and macOS jobs run one Python version, 3.12, like the other
  single-version jobs. The docs build, the changelog check, and the spec
  reference check stay on Linux only.
- The repository is public, so GitHub-hosted Windows and macOS runners
  add no cost.
- The 10 Spec Kit skills in `.github/skills/` repeat names that also exist
  in `.claude/skills/`. They date from the Copilot integration that
  commit `f1ba4c0` replaced. Removing them is out of scope here.
