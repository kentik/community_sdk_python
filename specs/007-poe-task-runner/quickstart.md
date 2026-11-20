# Quickstart: validate the poe task runner

**Feature**: [spec.md](spec.md) | **Contracts**: [contracts/](contracts/)

Run these steps from the repository root after implementation, on macOS or
Linux. Step 7 needs a Windows host, or reads the Windows CI jobs.

## 1. Install and list tasks

```sh
uv sync --locked
uv run poe
```

Expected: poe lists every task in [contracts/tasks.md](contracts/tasks.md),
each with a one-line help text. `Makefile` does not exist.

## 2. Same tasks, same results

```sh
uv run poe test
uv run poe lint && git status --short
uv run poe typecheck
uv run poe check-specs
uv run poe check-changelog --since HEAD
uv run poe release-notes --since HEAD
uv run poe -h generate
```

Expected: all pass, `lint` changes nothing, and `-h generate` lists
`--local`, `--local-repo`, and `--schema-ref`.

## 3. Options reach the program

```sh
uv run poe -d generate --local
uv run poe -d generate --local-repo "/tmp/a b"
uv run poe -d impact-report --since HEAD --no-checks
```

Expected (`-d` prints without running): `--local-repo ../api-schema-public/`,
then `--local-repo '/tmp/a b'` as one argument, then
`--since HEAD --no-checks`.

## 4. Regeneration changes only the header

```sh
uv run poe generate
uv run poe check-drift
```

Expected after the committed regeneration: `check-drift` exits 0. On the
regeneration commit itself, `git diff --stat` shows only header lines
changed.

## 5. Clean

```sh
uv run poe clean
git status --short | head
uv run poe generate && uv run poe check-drift
```

Expected: `clean` removes `src/kentik_api/gen/`, `docs/build/`,
`docs/sphinx/services/`, and every `__pycache__`; the regeneration brings
the tree back with no drift.

## 6. No `.env` in task environments

```sh
uv run poe test-smoke
```

Expected: `tests/smoke/test_task_runner.py` passes, including the
`envfile`, skill version, `AGENTS.md`, and no-`make` checks.

## 7. Windows and macOS

On a pull request, the `test`, `lint`, `typecheck`, and
`generated-output-matches-schema-pin` jobs pass on `windows-latest` and
`macos-latest`. On a Windows host with only uv and Git:

```powershell
git clone https://github.com/kentik/community_sdk_python
cd community_sdk_python
uv sync
uv run poe test
uv run poe generate
uv run poe check-drift
Get-Content AGENTS.md -TotalCount 3
```

Expected: all pass, and `AGENTS.md` shows the instructions, not the text
`CLAUDE.md`.
