# Research: Cross-Platform Task Runner with Poe the Poet

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-10-17

Each section records one decision, why it was made, and what else was
considered. Probes ran with poethepoet 0.49.0 from `uvx` in scratch
folders under `$TMPDIR`, on macOS, on 2026-10-17. Windows facts that no
local probe can show are marked "expected"; the Windows CI job confirms
them.

## R1. Poe version and how tasks run

- **Decision**: Pin `poethepoet==0.49.0` in the dev group. Contributors and
  CI run `uv run poe <task>`.
- **Rationale**:
  - `poe --version` prints "Poe the Poet (version 0.49.0)". Bare `poe` lists
    each task with its help text, and `poe -h <task>` lists the task's
    options (FR-005).
  - A `cmd` task runs without a shell. In a probe,
    `pkg/*/__pycache__` expanded to the matching folder through Python, and
    `sys.argv` showed plain arguments.
  - A `switch` task on `sys.platform` picked the `posix` branch on macOS.
- **Alternatives considered**: Invoke 3.0.3: rejected in the spec. It runs
  every command through a shell (bash or cmd.exe).

## R2. Task forms and option passing

- **Decision**:
  - A one-command task is a `cmd` task.
  - A task with options writes each option into the command with
    conditional expansion: `${since:+--since "${since}"}`. A boolean option
    uses the same form: `${local:+--local-repo ../api-schema-public/}`.
  - A task that runs several commands is a `sequence` task: `lint` and
    `all`. `docs` is a sequence of `generate` and the Sphinx build, as the
    Make target is today.
  - A task that deletes files or inspects Git is a `script` task that calls
    a function in a new module, `scripts/tasks.py`: `clean`, `deep-clean`,
    and `check-drift`.
- **Rationale**:
  - Poe does not append named options to a `cmd` task. A probe with
    `args = [{ name = "local", type = "boolean" }]` and no `${local}` in
    the command passed `[]` for `--local`.
  - Without quotes, a value is split on spaces: `--local-repo "/p a/b"`
    reached the program as `/p` and `a/b`. With `"${local_repo}"` it
    reached it as `/p a/b`. An option that is not given expands to nothing.
  - `rm -rf` and `find -exec` have no portable form, and `shutil.rmtree`
    and `pathlib` do (FR-004).
- **Alternatives considered**: A `script` task for every task: rejected.
  It hides plain commands in Python that contributors then have to read.

## R3. No task loads `.env`

- **Decision**: No `envfile` key in `[tool.poe]` or in any task. A test reads
  the `[tool.poe]` table and fails on an `envfile` key at any level (FR-006).
- **Rationale**: In a probe, a `.env` with `SECRETX=leak` next to
  `pyproject.toml` did not reach a task: the task printed `None`. Poe loads a
  file only when a task names it. The test keeps it that way.

## R4. Console encoding on Windows

- **Decision**: `[tool.poe.env]` sets `PYTHONUTF8 = "1"` for every task.
- **Rationale**: Five generator modules print emoji (`✅`, `❌`, `⚠️`). When a
  Windows console output is redirected, as in CI, Python writes with the
  ANSI code page, which has no emoji, and `print` raises
  `UnicodeEncodeError` (expected; Python UTF-8 Mode, PEP 540). UTF-8 Mode
  removes that dependency on the code page. The variable is not a secret.
- **Alternatives considered**: Remove the emoji: rejected, it changes
  generator output text for an OS problem. Set the variable only in CI:
  rejected, a Windows contributor would hit the same error.

## R5. Line endings

- **Decision**: Add `.gitattributes` with `* text=auto eol=lf`, and set
  `line-ending = "lf"` in `[tool.ruff.format]`.
- **Rationale**:
  - With `eol=lf`, Git checks out text files with LF on every OS, whatever
    `core.autocrlf` says, and Git still detects binary files (FR-013).
  - On Windows, `Path.write_text` writes CRLF (expected; Python text mode).
    `git status` reports a CRLF file as modified even under `eol=lf`, though
    `git diff` shows nothing. The first Windows drift job failed this way.
    So every generator write goes through `write_text_lf()` in `_shared.py`,
    which writes the UTF-8 bytes as is, and a test rejects any other
    `write_text` call in the generator.
  - `Path.write_text(newline=...)` exists only from Python 3.13, and the
    project supports 3.12.
- **Alternatives considered**: Rely on Ruff `line-ending = "lf"` and Git
  normalization alone: rejected after the Windows drift job failed, because
  the generator rewrites files after Ruff runs (the generated headers, the
  JSON records, `schema.lock`).

## R6. `AGENTS.md` without a symbolic link

- **Decision**: `AGENTS.md` becomes a regular file with today's `CLAUDE.md`
  content. `CLAUDE.md` becomes one line, `@AGENTS.md`. A test checks that
  `AGENTS.md` is not a link and that `CLAUDE.md` is exactly the import.
- **Rationale**:
  - The Claude Code memory docs say: "if you or anyone who clones the
    repository works on Windows, use the `@AGENTS.md` import instead",
    because Git checks a committed link out as a one-line text file unless
    `core.symlinks` is on. They also say the import never loads `AGENTS.md`
    twice.
  - GitHub Copilot reads `AGENTS.md` directly. It does not expand `@`
    imports, so the content must live in `AGENTS.md`, not `CLAUDE.md`.
  - The `agents-md` skill writes its shared-rules block into `AGENTS.md`,
    so it keeps working. The block's note "AGENTS.md is a symlink to this
    file" changes.
  - Every reference to `CLAUDE.md` still resolves, because the file stays.
- **Alternatives considered**: A copy in both files with an equality test:
  rejected, every edit must happen twice.

## R7. The poe agent skill

- **Decision**: Run `uv run poe _install_skill .claude/skills` once and
  commit `.claude/skills/poethepoet/`. Add `.claude/skills/poethepoet/**` to
  the `ignores` in `.markdownlint-cli2.jsonc`. A test compares
  `.claude/skills/poethepoet/version.txt` with
  `importlib.metadata.version("poethepoet")` (FR-012).
- **Rationale**:
  - A probe install wrote `SKILL.md`, five files under `references/`, and
    `version.txt`. `SKILL.md` says "Targets poe 0.49.0".
  - Ruff already excludes `.claude/skills` (spec 006).
  - The test runs in the mocked suite, so a Dependabot bump of poe fails CI
    until someone runs `uv run poe _install_skill .claude/skills --upgrade`.
- **Alternatives considered**: Ignore the skill in Git and install it per
  clone: rejected, agents would not have it until someone runs a command.

## R8. The regeneration header and the hand-written marker

- **Decision**:
  - One constant in `scripts/generation/_shared.py`,
    `REGENERATE_COMMAND = "uv run poe generate"`, feeds every generated
    header and every message that names the command. The one Jinja2
    template that hard-codes the header, `service.jinja2`, gets a test that
    its text matches the constant.
  - The hand-written marker line
    "HAND-WRITTEN: not modified by `make generate`" becomes
    "HAND-WRITTEN: not modified by `uv run poe generate`". A Markdown marker
    that links to `Makefile` links to `pyproject.toml` instead.
- **Rationale**:
  - The header text appears in 10 places in `scripts/` today: 8 string
    literals in 3 phase modules (`endpoint_docs`, `docs_rendering`,
    `wrapper_generation`), `_inject_generated_headers()`, and the template.
    One constant makes the next change a one-place edit.
  - 1,385 files under `gen/` and 45 service pages carry the header. The
    regeneration changes only that line (FR-010).
  - rumdl's `MD057` fails on any link left pointing at the deleted
    `Makefile`.

## R9. CI on three operating systems

- **Decision**: `test`, `lint`, `typecheck`, and the drift check run on
  `ubuntu-latest`, `windows-latest`, and `macos-latest`. Linux keeps Python
  3.12, 3.13, and 3.14 for `test`; Windows and macOS run 3.12. Every step
  calls `uv run poe <task>`. The drift check becomes a task, `check-drift`,
  so it needs no shell syntax.
- **Rationale**:
  - The current drift step uses a bash `if`. The Windows runner's default
    shell is PowerShell. A Python task runs the same on all three.
  - `schema-sync.yml` calls `make sync-schema` and becomes
    `uv run poe sync-schema`.
  - Docs, changelog, spec references, the audit, and the wheel check stay on
    Linux only (spec Assumptions).
- **Risk**: Generation on Windows runs `protoc` through `grpc_tools` with
  Windows paths, and has never run there. The Windows drift job is the
  first proof.

## R10. `deep-clean` on Windows

- **Decision**: `deep-clean` runs `clean`, then removes `.pytest_cache`,
  `.ruff_cache`, and `.venv`. When the running interpreter lives in
  `.venv` on Windows, it leaves `.venv` in place and prints the one command
  that removes it after poe exits.
- **Rationale**: Windows does not let a process delete its own running
  executable (spec Edge Cases). On macOS and Linux, `shutil.rmtree` removes
  `.venv` while poe runs, as `rm -rf` does today.

## R11. No `make` command left behind

- **Decision**: A test scans every tracked text file for a `make <target>`
  command or a `Makefile` reference, and fails with file and line. It skips
  `specs/001-*` to `specs/007-*`, `reports/`, `.specify/`, and vendored
  skills (SC-002).
- **Rationale**: More than 1,500 tracked files mention a `make` command or
  `Makefile` today. A one-time rewrite misses some, and a later edit can
  bring one back.
- **Spec deviation**: SC-002 names specs 001 to 006 as the only exception.
  Spec 007 itself must name the Make targets it replaces, so the test also
  skips `specs/007-*` (plan.md Complexity Tracking).
- Two existing tests read the `Makefile`: `test_make_help_lists_targets_with_digits`
  in `tests/smoke/test_docs_contract.py`, and the sandbox copy in
  `tests/generator/conftest.py`. The first becomes a test that every poe
  task has a help text (FR-005). The second stops copying `Makefile`.

## R12. Task names

- **Decision**: Keep each Make target name (FR-002). Drop `help`,
  `install`, `local`, `services`, and `tests`. Add four tasks so that every
  CI job calls a poe task (FR-007): `check-drift` (R9), `lint-check` (the
  check-only form of `lint`), `docs-build` (the Sphinx build without
  regeneration, which `docs` runs after `generate`), and `audit`. The full
  map is in [contracts/tasks.md](contracts/tasks.md).
