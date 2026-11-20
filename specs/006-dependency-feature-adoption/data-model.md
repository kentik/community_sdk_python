# Data Model: Dependency Feature Adoption and Reduction

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This feature has no runtime data. Its entities are configuration records in
`pyproject.toml`, `.markdownlint-cli2.jsonc`, and one docs page.

## Declared dependency

One requirement in `pyproject.toml`.

| Field | Source | Rule |
| --- | --- | --- |
| name | requirement name, PEP 503 normalized | Unique across all groups. |
| group | `[project.dependencies]`, an extra, a `[dependency-groups]` group, or `[build-system]` | One of: runtime, analytics, dev, test, docs, build. |
| specifier | requirement text | A dev tool that formats or lints is pinned with `==` (Ruff, rumdl). Other entries use a `>=` floor. |
| locked version | `uv.lock` | Satisfies the specifier. |

Validation:

- A runtime floor change is a breaking change in `api_surface.json`
  `requirements`, and `CHANGELOG.md` Unreleased names it (FR-017).
- Every third-party import in `src/`, `scripts/`, and `tests/` maps to one
  declared dependency (FR-011).

## Inventory row

One row in the table on `docs/sphinx/dependencies.md`.

| Field | Rule |
| --- | --- |
| Dependency | Equals one declared dependency name. Every declared dependency has exactly one row. |
| Group | Same as the declared group. |
| Purpose | One sentence: what in this project needs it. |
| Decision | Keep, retire, raise floor, adopt features, or report upstream, as decided by the last audit. |

The `[build-system]` pair hatchling and hatch-vcs has one row each.

## Rule scope

Which Ruff rules apply to which paths.

| Path | Ruff lint rules | Ruff format | rumdl |
| --- | --- | --- | --- |
| Hand-written Python | Ruff 0.17 default set, plus `E4`, `E7`, `E9`, `F` | Yes | n/a |
| `src/kentik_api/gen/**` | `E`, `F`, and `I`, as today | Yes | n/a |
| `src/kentik_api/client_mixin.py` | `E` and `F`, as today | Yes | n/a |
| Hand-written Markdown | n/a | Python code blocks | All configured rules |
| Generated Markdown (`docs/sphinx/services/`, `gen/*/README.md`, marker blocks) | n/a | Python code blocks, applied by the generator | `docs/sphinx/services/` ignored, the rest checked |
| `.specify/`, `.claude/skills/`, `.github/skills/` | Excluded | Excluded | Speckit paths ignored, as today |

## Line suppression

A `# noqa: <code>` comment on one line of hand-written code.

- It names one rule code and gives a reason after it, for example
  `# noqa: BLE001 - any transport failure becomes TransportError`.
- `RUF100` (unused `noqa`) stays on, so a stale suppression fails the check.
