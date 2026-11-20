# Contract: lint command and CI lint job

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)

## `make lint`

Runs, in this order, and stops at the first failure:

```sh
uv run ruff check --fix .
uv run ruff format .
uv run rumdl check --fix .
```

- It fixes what it can and fails on what it cannot.
- It needs only `uv sync`. No Node.

## CI `lint` job (`.github/workflows/tests.yml`)

Each step fails the job on any finding, and prints GitHub annotations:

```sh
uv run ruff check --output-format github .
uv run ruff format --check --output-format github .
uv run rumdl check --output-format github .
```

## CI `audit` job (new)

```sh
uv audit --preview-features audit-command
```

The job has `continue-on-error: true`. A finding shows on the pull request
and does not block the merge (FR-014).

## Scope

| Check | Checks | Skips |
| --- | --- | --- |
| `ruff check` | All Python files that Git does not ignore | `.specify/`, `.claude/skills/`, `.github/skills/` |
| `ruff format` | Python files, and Python code blocks in Markdown files | Same as above |
| `rumdl check` | Markdown files | `ignores` in `.markdownlint-cli2.jsonc` |

## Configuration

- `[tool.ruff]` has no `include` key.
- `[tool.ruff.lint]` has no `select` key, so the Ruff 0.17 default set
  applies, and `extend-select = ["E4", "E7", "E9", "F"]` keeps today's
  rules. `per-file-ignores` lists every added default family except `E`,
  `F`, and `I` for `gen/**`, and except `E` and `F` for `client_mixin.py`,
  with a comment that gives the reason.
- Every entry in `[tool.ruff.lint] ignore` has a comment with its reason.
- `.markdownlint-cli2.jsonc` disables MD036, with the reason: the bold
  `**Out of scope**` line is a marker that `scripts/check_spec_refs.py`
  reads. Its header comment names rumdl as the reader.

## Failure examples

| Input | Result |
| --- | --- |
| A Python block in `docs/sphinx/guides/rest.md` with `x=1` | `ruff format --check` fails and annotates the line. |
| A list with no blank line before it in a new spec file | `rumdl check` fails with `MD032`, file, and line. |
| A relative link to a missing file | `rumdl check` fails with `MD057`. |
| A `try`/`except Exception: pass` in `scripts/` | `ruff check` fails with `BLE001` or `S110`. |
| The same code in `src/kentik_api/gen/` | No finding, as today. |
