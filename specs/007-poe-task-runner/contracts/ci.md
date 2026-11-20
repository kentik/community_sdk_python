# Contract: CI jobs

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)

Every step that runs a project command calls `uv run poe <task>` after
`uv sync --locked`. No step calls `make` (FR-007).

## `.github/workflows/tests.yml`

| Job | OS | Python | Steps |
| --- | --- | --- | --- |
| `test` | ubuntu | 3.12, 3.13, 3.14 | `poe test` |
| `test` | windows, macos | 3.12 | `poe test` |
| `lint` | ubuntu, windows, macos | 3.12 | `poe lint-check` |
| `typecheck` | ubuntu, windows, macos | 3.12 | `poe typecheck` |
| `generated-output-matches-schema-pin` | ubuntu, windows, macos | 3.12 | `poe generate`, then `poe check-drift` |
| `spec-references` | ubuntu | 3.12 | `poe check-specs` |
| `changelog` | ubuntu | 3.12 | `poe check-changelog --since "$(git merge-base HEAD origin/<base>)"` |
| `audit` | ubuntu | 3.12 | `poe audit`, non-blocking |
| `docs` | ubuntu | 3.12 | `poe docs-build` |

The `changelog` step keeps `$(...)` and runs in bash on Ubuntu only.

Each matrix job sets `fail-fast: false`, so a Windows failure does not
cancel the Linux result.

## Other workflows

| Workflow | Change |
| --- | --- |
| `schema-sync.yml` | `make sync-schema` becomes `uv run poe sync-schema`, and its pull request text names the poe command |
| `build.yml`, `release.yml` | No `make` today. No change |

## Failure examples

| Change | Failing job |
| --- | --- |
| A task that uses `rm -rf` | `generated-output-matches-schema-pin` or `test` on windows |
| A generated path that differs from another only by case | `generated-output-matches-schema-pin` on windows and macos |
| A file checked out with CRLF that the generator rewrites with LF | none, `.gitattributes` keeps both sides LF |
| `poethepoet` bumped without `_install_skill --upgrade` | `test` on every OS |
