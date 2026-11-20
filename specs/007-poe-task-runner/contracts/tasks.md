# Contract: poe tasks

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)

All tasks live in `[tool.poe.tasks]` in `pyproject.toml`. Each one has a
one-line `help` (FR-005). Run them as `uv run poe <task>`.

## Shared settings

```toml
[tool.poe]
# No `envfile` here or in any task: .env holds real credentials (FR-006).

[tool.poe.env]
PYTHONUTF8 = "1"  # the generator prints emoji; Windows CI output is not UTF-8 otherwise
```

`PYTEST` below stands for `pytest -vv -s -rA`, as in the `Makefile` today.

## Task map

| Make target | Poe task | Type | Runs | Options |
| --- | --- | --- | --- | --- |
| `all` | `all` | sequence | `generate`, `test` | |
| `generate` | `generate` | cmd | `python scripts/generate_sdk.py` | `--local`, `--local-repo PATH`, `--schema-ref REF` |
| `services` | dropped | | use `generate` | |
| `local` | dropped | | becomes `generate --local` | |
| `sync-schema` | `sync-schema` | cmd | `python scripts/generate_sdk.py --schema-ref HEAD` | |
| `docs` | `docs` | sequence | `generate`, `docs-build` | |
| `tests` | dropped | | use `test` | |
| `test` | `test` | cmd | `PYTEST tests/` | |
| `test-generated` | `test-generated` | cmd | `PYTEST tests/generated/` | |
| `test-runtime` | `test-runtime` | cmd | `PYTEST tests/runtime/` | |
| `test-smoke` | `test-smoke` | cmd | `PYTEST tests/smoke/` | |
| `test-generator` | `test-generator` | cmd | `PYTEST tests/generator/` | |
| `test-analytics` | `test-analytics` | cmd | `PYTEST tests/analytics/` | |
| `test-e2e` | `test-e2e` | cmd | `PYTEST -m e2e tests/e2e/` | |
| `test-e2e-grpc` | `test-e2e-grpc` | cmd | `PYTEST -m e2e_grpc tests/e2e/` | |
| `lint` | `lint` | sequence | `ruff check --fix .`, `ruff format .`, `rumdl check --fix .` | |
| `typecheck` | `typecheck` | cmd | `ty check` | |
| `check-specs` | `check-specs` | cmd | `python scripts/check_spec_refs.py` | |
| `release-notes` | `release-notes` | cmd | `python scripts/release_notes.py` | `--since REF`, `--out PATH` (passed as `-o`) |
| `check-changelog` | `check-changelog` | cmd | `python scripts/release_notes.py --check-changelog` | `--since REF` |
| `impact-report` | `impact-report` | cmd | `python scripts/impact_report.py` | `--since REF`, `--no-checks`, `--out PATH` (passed as `-o`) |
| `clean` | `clean` | script | `scripts.tasks:clean` | |
| `deep-clean` | `deep-clean` | script | `scripts.tasks:deep_clean` | |
| `install` | dropped | | `uv sync` (poe needs it first) | |
| `help` | dropped | | bare `uv run poe` | |
| none | `check-drift` | script | `scripts.tasks:check_drift` | |
| none | `lint-check` | sequence | `ruff check --output-format github .`, `ruff format --check --output-format github .`, `rumdl check --output-format github .` | |
| none | `docs-build` | cmd | `sphinx-build -W --keep-going -b html docs/sphinx docs/build/html` (the committed tree, no regeneration) | |
| none | `audit` | cmd | `uv audit --preview-features audit-command` | |

The four new tasks exist so that every CI job calls a poe task (FR-007).
`lint-check` fails where `lint` would fix. The `github` output format prints
plain `file:line` lines outside GitHub Actions too.

`--local` expands to `--local-repo ../api-schema-public/`. Every value
option is quoted inside its expansion, so a path with spaces stays one
argument (research R2).

## Script tasks (`scripts/tasks.py`)

| Function | Does | Exit |
| --- | --- | --- |
| `clean()` | Removes `src/kentik_api/gen/`, `docs/build/`, `docs/sphinx/services/`, and every `__pycache__` folder under the repository | 0 |
| `deep_clean()` | `clean()`, then `.pytest_cache/`, `.ruff_cache/`, and `.venv/`. On Windows, when the running interpreter is inside `.venv/`, it keeps `.venv/` and prints the command that removes it | 0 |
| `check_drift()` | Runs `git status --porcelain`. Prints each differing path and the fix ("Run `uv run poe generate` and commit the result.") | 1 when any path differs |

`clean()` keeps `scripts/openapi_templates/`, `src/kentik_api/core/`, and
`docs/sphinx/local_generation_workflow.md`, as the Make target says today.

## Agent skill

```sh
uv run poe _install_skill .claude/skills            # first install
uv run poe _install_skill .claude/skills --upgrade  # after a poe upgrade
```

`.claude/skills/poethepoet/version.txt` must equal the locked poe version
(FR-012).
