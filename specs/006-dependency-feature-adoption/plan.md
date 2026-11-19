# Implementation Plan: Dependency Feature Adoption and Reduction

**Branch**: `chore/dependency-feature-adoption` | **Date**: 2026-10-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-dependency-feature-adoption/spec.md`

## Summary

Put the features of the upgraded dependencies to use, and make sure that
every declared dependency has a reason. Raise four floors: python-dotenv,
Pydantic, ty, and MyST-Parser, and declare jinja2. Add rumdl as the
Markdown linter. It reads the existing markdownlint configuration and needs
no Node. Turn on Ruff's Markdown code-block formatting and its 0.17 default
rule set for hand-written code. Generated code keeps today's rules. The
generator formats its own Markdown, so the drift check stays green. Move
pytest to its native TOML table with strict mode, and render GitHub alerts
in Sphinx. Add an inventory page with a test that holds it and the imports
to the declared set. Add a non-blocking `uv audit` CI job, and draft the
upstream report for `openapi-python-generator`.

## Technical Context

**Language/Version**: Python 3.12 to 3.14

**Primary Dependencies**: Ruff 0.17.1, rumdl 0.3.0 (new), pytest 9.1.1,
MyST-Parser 5.1.0, Sphinx 9.1.0, ty 0.0.89, uv 0.13.0.

**Storage**: N/A

**Testing**: pytest (mocked layers), ty, Ruff, rumdl, Sphinx with `-W`, the
CI drift check.

**Target Platform**: Any platform with CPython 3.12 or later. CI runs on
Ubuntu.

**Project Type**: Library (generated SDK) with a code generator.

**Performance Goals**: N/A. rumdl checks 125 files in under 50 ms.

**Constraints**:

- No behavior change in the shared runtime (Principle II, FR-016). Lint
  fixes there are annotation syntax and line suppressions only (R5).
- No hand edit in generated files (Principle I). The 3 service pages
  change through the generator (R4).
- The lock grows by one package at most (SC-004).
- No new check needs an edit in `.specify/`, `.claude/skills/`, or
  `.github/skills/`.

**Scale/Scope**: 117 Ruff findings and 133 rumdl findings to clear. About 30
hand-written files change by lint fixes, 4 Markdown files by format, 3
generated pages by regeneration. One generator line, one new test, one new
docs page, one new CI job.

No item is NEEDS CLARIFICATION. [research.md](research.md) resolves each
design point. R7 corrects one spec statement: the sphinxcontrib-mermaid floor
already works with Sphinx 9.1.0, so it stays.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | How the design meets it |
| --- | --- | --- |
| I. Generated code is never hand-edited | Pass | The 3 service pages change through a generator fix: the final `ruff format` pass covers its Markdown output (R4). |
| II. One shared runtime | Pass | No control flow changes in `core/`, `errors/`, `transports/`, or `auth/`. Only annotation syntax and `# noqa` lines with reasons (R5). |
| III. Phase modules stay testable | Pass | The change is in the orchestration in `generate_sdk.py`, with a test in `tests/generator/test_generate_sdk.py`. No phase module import changes. |
| IV. Exhaustive coverage | Pass | Strict mode adds checks and removes none. A duplicate parametrize ID gets a unique ID, never a removed case (R8). |
| V. E2E opt-in and safe | Pass | Markers and the default `-m` deselection move unchanged to `[tool.pytest]`. |
| VI. Credentials | Pass | The python-dotenv floor rises. `dotenv_values` stays. No probe reads `.env`. |
| VII. Compatibility and scope | Pass | The two raised runtime floors are breaking for some installs. `CHANGELOG.md` names them, and `make check-changelog` enforces it (FR-017). |

The Development Workflow section says `make lint` is "`ruff check --fix` +
`ruff format`". It becomes stale when rumdl joins, so a task amends it
(PATCH 1.4.3). `CLAUDE.md` gets the same fix.

Re-check after Phase 1: all principles pass.

## Project Structure

### Documentation (this feature)

```text
specs/006-dependency-feature-adoption/
├── spec.md
├── plan.md               # this file
├── research.md           # Phase 0
├── data-model.md         # Phase 1
├── quickstart.md         # Phase 1
├── contracts/            # Phase 1
│   ├── lint.md
│   ├── dependency-records.md
│   └── generator.md
├── checklists/requirements.md
└── tasks.md              # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
pyproject.toml                         # floors, rumdl, jinja2, Ruff rules, [tool.pytest]
uv.lock                                # + rumdl
.markdownlint-cli2.jsonc               # MD036 off, rumdl named as reader
Makefile                               # lint runs rumdl
.github/workflows/tests.yml            # lint annotations, audit job
scripts/generate_sdk.py                # final pass formats generated Markdown
docs/sphinx/conf.py                    # "alert" extension
docs/sphinx/dependencies.md            # new: inventory
docs/sphinx/index.md                   # toctree entry
tests/smoke/test_declared_dependencies.py  # new: imports and inventory
tests/generator/test_generate_sdk.py   # formatting pass covers Markdown
reports/upstream/upstream-openapi-python-generator-optional-formatters.md  # new: issue draft
CHANGELOG.md                           # raised floors
.specify/memory/constitution.md        # PATCH 1.4.3
CLAUDE.md                              # make lint description
specs/00{3,4,5,6}-*/**.md, .github/agents/*.md, docs/sphinx/**.md  # Markdown fixes
scripts/, src/kentik_api/, tests/, reports/, examples/, docs/  # Ruff fixes
docs/sphinx/services/{bgp_monitoring,cloud_export,kagent}.md   # regenerated
api_surface.json                       # regenerated requirements
```

**Structure Decision**: No new module. Configuration stays in
`pyproject.toml` and the existing markdownlint file. The one new test goes in
`tests/smoke/`, next to `test_packaging_contract.py`, because it checks the
package metadata, not generated code.

## Phases after this plan

The order keeps each step's checks green before the next step starts.

1. Floors and packages: the `pyproject.toml` floors, rumdl, jinja2, then
   `uv lock` and `uv sync`.
2. pytest: `[tool.pytest]` with strict mode. Run `make test` and fix any
   strict finding.
3. Ruff Markdown: remove `include`, add the skill excludes, change the
   generator's final pass, add its test, run `make generate`, then
   `ruff format .`.
4. Ruff rules: remove `select`, add the generated-path ignores, apply safe
   fixes, then fix or suppress the rest by hand. Confirm `api_surface.json`
   is unchanged apart from `requirements`.
5. Markdown rules: MD036 off, `rumdl check --fix .`, then the hand fixes
   (wrapping, links). Add rumdl to `make lint`.
6. CI: annotations in the lint job, rumdl step, `audit` job.
7. Docs: the `alert` extension, the inventory page and its test.
8. Records: `CHANGELOG.md`, the constitution PATCH, `CLAUDE.md`, the
   upstream issue draft.
9. Validation: [quickstart.md](quickstart.md), all steps.

## Risks

| Risk | Effect | Response |
| --- | --- | --- |
| Strict parametrization IDs find duplicates in the auto-discovered suites | `make test` fails | Make the IDs unique. Never drop a case (Principle IV). |
| A Ruff fix changes a public annotation that `api_surface.json` records | `check-changelog` flags a false break | Regenerate after step 4 and compare. Revert that fix or add a line suppression. |
| A future Spec Kit run writes a line over 200 characters, for example a long `**Input**` | The CI lint job fails on the new spec | Wrap the line. rumdl names it. |
| rumdl and the editor's markdownlint extension disagree | Contributor confusion | CI decides (spec Edge Cases). The inventory page says so. |
| `uv audit` changes its output or flags | The audit job turns red | It never blocks a merge (`continue-on-error`). |
| The raised Pydantic floor blocks a user who pins Pydantic below 2.14 | Install conflict | Called out in `CHANGELOG.md` as breaking. |

## Complexity Tracking

No constitution violation needs a justification.
