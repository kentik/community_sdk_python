# Contract: repository files

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)

## New files

| File | Content |
| --- | --- |
| `.gitattributes` | `* text=auto eol=lf` (FR-013) |
| `scripts/tasks.py` | `clean()`, `deep_clean()`, `check_drift()` (see [tasks.md](tasks.md)) |
| `.claude/skills/poethepoet/` | Output of `uv run poe _install_skill .claude/skills`: `SKILL.md`, `references/*.md` (5 files), `version.txt` |

## Changed files

| File | Change |
| --- | --- |
| `pyproject.toml` | `poethepoet==0.49.0` in `dev`; `[tool.poe.env]` and `[tool.poe.tasks]`; `line-ending = "lf"` in `[tool.ruff.format]`; marker help texts name poe commands |
| `AGENTS.md` | A regular file holding today's `CLAUDE.md` text, with poe commands |
| `CLAUDE.md` | Exactly one line: `@AGENTS.md` |
| `.markdownlint-cli2.jsonc` | `ignores` gains `.claude/skills/poethepoet/**` |
| `scripts/generation/_shared.py` | `REGENERATE_COMMAND = "uv run poe generate"` |
| `scripts/generate_sdk.py`, `scripts/generation/{endpoint_docs,docs_rendering,wrapper_generation,api_surface}.py`, `scripts/openapi_templates/service.jinja2` | Headers and messages use the constant (or, in the template, the same text) |
| `.github/workflows/{tests,schema-sync}.yml` | See [ci.md](ci.md) |
| `.specify/memory/constitution.md` | PATCH 1.4.4: every `make <target>` becomes `uv run poe <task>`, and the governance line says `AGENTS.md` holds the instructions and `CLAUDE.md` imports it |
| Hand-written docs and READMEs, `CHANGELOG.md`, `CONTEXT.md`, `.github/agents/*.md`, script messages | `make <target>` becomes `uv run poe <task>`; the `HAND-WRITTEN` marker names `uv run poe generate` and links to `pyproject.toml` |

## Deleted files

| File | Replaced by |
| --- | --- |
| `Makefile` | `[tool.poe.tasks]` (FR-009) |

## Unchanged on purpose

- `specs/001-*` to `specs/006-*`: past decisions keep their `make`
  commands (FR-011).
- `.specify/`, `.github/skills/`, `.claude/skills/speckit-*`: Spec Kit
  rewrites them.
- `src/kentik_api/` runtime code and the public API surface (FR-015).

## Generated header

Before and after, in every file under `src/kentik_api/gen/`,
`src/kentik_api/client_mixin.py`, and the generated docs pages:

```text
# Rebuilt on every `make generate`. Do not edit by hand.
# Rebuilt on every `uv run poe generate`. Do not edit by hand.
```

Markdown pages use the same text inside `<!-- ... -->`. No other line of
generated output changes (FR-010).

## Checks

| Test | Fails when |
| --- | --- |
| `tests/smoke/test_task_runner.py::test_every_task_has_help` | A task in `[tool.poe.tasks]` has no `help` (FR-005) |
| `tests/smoke/test_task_runner.py::test_no_task_loads_an_env_file` | `envfile` appears anywhere under `[tool.poe]` (FR-006) |
| `tests/smoke/test_task_runner.py::test_agent_skill_matches_locked_poe` | `version.txt` differs from the installed poethepoet version (FR-012) |
| `tests/smoke/test_task_runner.py::test_agents_md_is_a_regular_file_and_claude_md_imports_it` | `AGENTS.md` is a link, or `CLAUDE.md` is not exactly `@AGENTS.md` (FR-014) |
| `tests/smoke/test_task_runner.py::test_no_make_commands_outside_past_specs` | A tracked text file outside the skipped paths names a `make` target or `Makefile` (SC-002) |
| `tests/generator/test_openapi_templates.py::test_service_template_header_names_the_regenerate_command` | The `service.jinja2` header differs from `REGENERATE_COMMAND` (FR-010) |
