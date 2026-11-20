# Data Model: Cross-Platform Task Runner with Poe the Poet

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This feature has no runtime data. Its entities are configuration records.

## Task

One entry in `[tool.poe.tasks]`.

| Field | Rule |
| --- | --- |
| name | A Make target name (FR-002), or one of the four CI tasks: `check-drift`, `lint-check`, `docs-build`, `audit` |
| help | Required, one line (FR-005) |
| type | `cmd`, `sequence`, or `script`. Never `shell` (FR-004) |
| args | Named options only (FR-003). Each value option is quoted in its expansion: `${name:+--flag "${name}"}` |
| env | Inherits `[tool.poe.env]` (`PYTHONUTF8 = "1"`). No `envfile` (FR-006) |

## Agent skill

The folder `.claude/skills/poethepoet/`.

| Field | Source | Rule |
| --- | --- | --- |
| version | `version.txt` | Equals `importlib.metadata.version("poethepoet")` (FR-012) |
| content | `SKILL.md`, `references/*.md` | Written only by `poe _install_skill`. Never hand-edited, never linted |

State: a poe upgrade makes the skill stale until
`uv run poe _install_skill .claude/skills --upgrade` runs. The version test
fails while it is stale.

## Instruction file

| File | Content | Read by |
| --- | --- | --- |
| `AGENTS.md` | All project instructions | GitHub Copilot, other agents, and Claude Code through the import |
| `CLAUDE.md` | `@AGENTS.md` only | Claude Code |

Rule: `AGENTS.md` is a regular file in Git (mode `100644`), never a link
(FR-014).

## Regeneration command

`REGENERATE_COMMAND = "uv run poe generate"` in
`scripts/generation/_shared.py`. Every generated header and every generator
message that names the command uses it (FR-010).
