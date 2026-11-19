# Research: Dependency Feature Adoption and Reduction

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-10-17

Each section records one decision, why it was made, and what else was
considered. All probes ran read-only on the `chore/dependency-feature-adoption`
tree on 2026-10-17, with the locked versions: Ruff 0.17.1, pytest 9.1.1,
MyST-Parser 5.1.0, Sphinx 9.1.0, uv 0.13.0.

## R1. Markdown linter: rumdl 0.3.0

- **Decision**: Pin `rumdl==0.3.0` in the dev group. `make lint` runs
  `rumdl check --fix .`. The CI lint job runs
  `rumdl check --output-format github .`.
- **Rationale**:
  - rumdl reads `.markdownlint-cli2.jsonc` without changes. `rumdl config`
    shows `MD013.line-length = 200`, `MD024.siblings-only`, and
    `MD033.allowed-elements` "from .markdownlint-cli2.jsonc".
  - It honors the `ignores` list. Of 232 tracked Markdown files, 107 match
    an ignore pattern, and rumdl checks the other 125. A direct run on
    `docs/sphinx/services/kagent.md` and a vendored skill reports "2 files
    found were filtered out".
  - It installs from PyPI through uv, so no contributor and no CI job needs
    Node (FR-008).
  - It has a `github` output format, so CI findings show as annotations.
- **Alternatives considered**:
  - markdownlint-cli2: rejected, it needs Node.
  - Ruff: rejected, it formats only the Python blocks in Markdown and has no
    Markdown lint rules (spec Background).

## R2. The existing Markdown findings

- **Decision**: Fix every finding before CI enforces the rules, with one
  recorded rule change: disable MD036 in `.markdownlint-cli2.jsonc`.

- **Rationale**: rumdl reports 133 findings on the committed tree (134 with
  the plan template, which this plan replaces):

  | Rule | Count | Files | Fix |
  | --- | --- | --- | --- |
  | MD013 line length | 103 | `specs/003-*/tasks.md` (57), `specs/005-*/tasks.md` (41), `.github/agents/kentik-sdk-autogen.agent.md` (2), 3 spec files (1 each) | Wrap the line. A task line keeps its `- [ ] T###` start, so `check_spec_refs.py` still finds it. |
  | MD036 emphasis as heading | 10 | `specs/003-*/spec.md` | Rule change, see below. |
  | MD032 list spacing | 10 | `specs/004-*/research.md` | `rumdl check --fix` |
  | MD040 fence language | 5 | `specs/003-*`, `docs/sphinx/index.md` | `rumdl check --fix`, then check the tag. |
  | MD057 broken link | 3 | `specs/004-*/spec.md` | Point the links at `../../reports/...`. |
  | MD050, MD076 | 2 | `specs/005-*/tasks.md`, `docs/sphinx/guides/v5.md` | `rumdl check --fix` |

  - `scripts/check_spec_refs.py` reads a bold `**Out of scope**` line as a
    marker (`OUT_OF_SCOPE`, line 34). MD036 flags exactly that convention.
    A heading would break the check, so the rule goes, with the reason in
    the configuration comment.
  - Wrapping lines changes no words. Spec 007 keeps specs 001 to 006 "as
    written" for their `make` commands, which wrapping does not touch.

- **Found during implementation**: two `rumdl check --fix` fixes were
  wrong and were reverted. `MD040` turned the MyST fence ```` ```{toctree} ````
  into ```` ```text {toctree} ````, which Sphinx no longer reads as a directive;
  `docs/sphinx/index.md` now uses MyST's colon fence, `:::{toctree}`. `MD050`
  turned a bare `__init__.py` into `**init**.py`; the path is now a code span.
  Review the diff after each `rumdl check --fix`.

- **Alternatives considered**:
  - Exclude `specs/` from the check: rejected, new specs would never be
    checked.
  - Turn MD013 off for `tasks.md`: rejected, markdownlint-cli2 has no
    per-file rule settings, and the editor extension would then disagree
    with CI.

## R3. Ruff formats Markdown code blocks

- **Decision**: Delete the `include` override in `[tool.ruff]`. Add
  `.claude/skills` and `.github/skills` to `extend-exclude`.
- **Rationale**:
  - Ruff 0.17 formats `*.md` by default. A scratch file `a.md` with
    `x=1` in a Python block reports "1 file would be reformatted" with
    `--isolated`. The override exists only to turn that off.
  - With Markdown on, 7 files change: 3 generated service pages (R4), 3
    spec documents, and `src/kentik_api/README.md` (hand-written, its header
    says so). `ruff format .` fixes the 4 hand-written ones.
  - Spec Kit rewrites the vendored skills on upgrade, so no check may need
    edits there (spec Edge Cases). `.specify` is already excluded.
  - `docs/build/` is in `.gitignore`, and Ruff respects it.
- **Alternatives considered**: `extend-include = ["*.md"]`: rejected, the
  default already has it.

## R4. Generated pages pass the Markdown formatter

- **Decision**: The generator's final formatting pass in
  `generate_modular_sdk()` also runs `ruff format` on the Markdown files the
  generator writes: `docs/sphinx/services/`, the runtime architecture page,
  and the guide files with marker blocks. `src/kentik_api/gen/` is already
  in that pass, so its `README.md` files follow once R3 lands.
- **Rationale**:
  - The 3 failing service pages differ only in one import line that is
    longer than 88 characters, for example
    `from kentik_api.gen.kagent.models import ProvisioningTokenServiceRevokeProvisioningTokenBody`.
    `endpoint_docs._render_example_snippet()` writes it on one line.
  - `docs_rendering._update_guide_snippets()` can write the same kind of
    line in the `request-body-example` marker.
  - Ruff is the formatter already, for the generated Python. One formatter,
    pinned to one version, decides the style of both. The CI drift check
    then compares against Ruff's output.
  - The hand-written parts of the guide files already pass the CI check, so
    the pass changes nothing there.
- **Alternatives considered**: Wrap long imports in the snippet code:
  rejected, it copies Ruff's rules into the generator and drifts on the
  next Ruff upgrade.

## R5. Ruff 0.17 default rule set on hand-written code

- **Decision**: Delete `select` in `[tool.ruff.lint]`, so the default set
  applies, and add `extend-select = ["E4", "E7", "E9", "F"]`. In
  `per-file-ignores`, ignore every added default family except `E`, `F`, and
  `I` for `src/kentik_api/gen/**`, and except `E` and `F` for
  `src/kentik_api/client_mixin.py`. Fix the findings; suppress a finding on
  its line, with a reason, only where the code does it on purpose.
- **Found during implementation**:
  - The 0.17 default set enables only `E722` and `E902` of the `E` rules.
    Without `extend-select`, the `E4`, `E7`, and `E9` rules that every file
    passes today would turn off.
  - The generator sorts imports with `ruff check --select F,I --fix` on
    `gen/`. A per-file ignore of `I` applies after `--select`, so it stopped
    that sort and broke the wrapper byte-for-byte test. `gen/` keeps `I`.
  - The broad `except` blocks in `scripts/` guarded `ast.parse()` of a file.
    They now catch `OSError`, `SyntaxError`, and `ValueError` only, so an
    unexpected fault is no longer hidden.
- **Rationale**:
  - The default set has 413 rules in these families: ASYNC, B, BLE, C, D,
    DTZ, E, EXE, F, FA, FLY, FURB, G, I, INT, ISC, LOG, N, PERF, PGH, PIE,
    PLC, PLE, PLR, PLW, PT, PTH, PYI, RET, RUF, S, SIM, T, TC, TRY, UP, W,
    YTT.
  - Ruff has no per-path `select`. Ignoring the added families on generated
    paths keeps generated code on today's rules (FR-006). Ruff is pinned to
    an exact version, so a new default family arrives only with a deliberate
    upgrade, and it then shows as findings in generated code, not silently.
  - Findings by area: `scripts/` 38, `src/kentik_api/core/` 16, `reports/` 9,
    `src/kentik_api/errors/` 5, `tests/` 45, and 1 each in `v5_tools.py`,
    `analytics/`, `examples/`, and `docs/`. 61 have a safe fix.
  - The 21 findings in the protected runtime (`core/`, `errors/`) are of two
    kinds. 15 are annotation syntax (`UP045`, `UP006`, `UP035`, `RUF022`).
    6 are `BLE001` and `S112` on deliberate broad `except` blocks, for
    example the transport-failure wrap in `rest_runtime.py` line 76. The
    first kind changes no behavior. The second kind gets a line suppression
    with a reason, because a narrower `except` changes behavior.
- **FR-016 reading**: Annotation syntax and suppression comments do not
  change the shared REST runtime's behavior, so FR-016 permits them. No
  control flow in `core/`, `errors/`, `transports/`, or `auth/` changes.
  `api_surface.json` must show no change other than `requirements` after the
  fixes.
- **Alternatives considered**:
  - A nested Ruff configuration in `src/kentik_api/gen/`: rejected, it would
    ship in the wheel, and `client_mixin.py` sits outside `gen/`.
  - Two `ruff check` runs with different `--select`: rejected, `make lint`
    and the editor would then disagree.

## R6. CI annotations

- **Decision**: The CI lint job runs `ruff check --output-format github .`,
  `ruff format --check --output-format github .`, and
  `rumdl check --output-format github .`.
- **Rationale**: Ruff 0.17 accepts `--output-format github` on both
  commands; `ruff format` accepts it with `--check`. rumdl lists `github`
  as an output format.

## R7. Dependency floors

- **Decision**:

  | Dependency | Group | Floor now | New floor | Reason |
  | --- | --- | --- | --- | --- |
  | python-dotenv | runtime | `>=1.2.1` | `>=1.2.4` | BOM and `KEY= # comment` fixes (FR-002) |
  | pydantic | runtime | `>=2.12.5` | `>=2.14.0` | Thread-safe rebuild, constant-time secret comparison (FR-015) |
  | ty | dev | `>=0.0.73` | `>=0.0.84` | GHSA-vxvm-j4xq-q7m4 (FR-001) |
  | myst-parser | docs | `>=2.0.0` | `>=5.1.0` | 5.0.0 is the first with Sphinx 9; 5.1.0 adds `alert` (FR-003, FR-010) |
  | sphinxcontrib-mermaid | docs | `>=1.0.0` | `>=1.0.0` | Already the lowest version that works (see below) |
  | jinja2 | test | none | `>=3.1.6` | Imported by `tests/generator/test_openapi_templates.py` (FR-011) |
  | rumdl | dev | none | `==0.3.0` | R1 |

- **Rationale**:
  - A scratch environment resolved the docs group with
    `--resolution lowest-direct` and `myst-parser>=5.0.0`. It installed
    Sphinx 9.1.0, sphinx-book-theme 1.1.0, sphinxcontrib-mermaid 1.0.0,
    autodoc-pydantic 2.2.0, and MyST-Parser 5.0.0. `sphinx-build -W
    --keep-going` on `docs/sphinx` exited 0 with no output.
  - MyST-Parser 5.1.0 declares `sphinx>=8,<10`. `alert` is in its
    `myst_enable_extensions` choices (`config/main.py` line 31) and not in
    5.0.0, so FR-010 needs 5.1.0.
  - **Spec correction**: the spec Background says the
    sphinxcontrib-mermaid floor is too low for Sphinx 9. The probe shows
    that 1.0.0 builds clean, and its metadata puts no bound on Sphinx. The
    floor already meets FR-003, so it stays. The quickstart repeats the
    probe.
  - jinja2 3.1.6 is the locked version, so declaring it adds no package
    (SC-004).
  - `make check-changelog` treats a raised runtime floor as breaking.
    `api_surface.json` records `requirements` from `[project.dependencies]`
    (`api_surface._declared_requirements()`), so a regeneration records the
    new floors (FR-017).

## R8. pytest native configuration and strict mode

- **Decision**: Replace `[tool.pytest.ini_options]` with `[tool.pytest]`
  and add `strict = true`. In the native table, `addopts` is a list of
  arguments, and `markers` and `pythonpath` are lists.
- **Rationale**:
  - pytest 9.1.1 reads a `[tool.pytest]` table in TOML mode
    (`_pytest/config/findpaths.py` line 93).
  - `strict` enables `strict_config`, `strict_markers`, `strict_xfail`, and
    `strict_parametrization_ids` (`_pytest/main.py` lines 114 to 116).
  - The only `xfail` mark in tests sets `strict=False` on purpose
    (`tests/e2e/test_v5_query_e2e.py` line 68), and e2e is opt-in. The
    mocked suite has no `xfail`.
  - The pytest floor `>=9.0.2` already supports both.
- **Risk**: `strict_parametrization_ids` fails on duplicate IDs. The
  auto-discovered suites build IDs from service and method names. The first
  run under strict mode shows any duplicate, and the fix is a unique ID,
  never a removed case (Principle IV).
- **Found during implementation**: two suites had duplicate IDs, which
  pytest had made unique without warning. `test_model_wire_names.py` named
  each case by model and field, and several services declare the same model
  (`protobufAny.type`); the ID now starts with the service. One case in
  `test_api_config.py` covered both a scalar and a `connect` timeout under
  one name; each now has its own. The suite still runs 3515 cases.

## R9. GitHub alerts in Sphinx

- **Decision**: Add `"alert"` to `myst_enable_extensions` in
  `docs/sphinx/conf.py`.
- **Rationale**: The 3 alerts are `generation.md` lines 63 and 172 and
  `quickstart.md` line 105. GitHub already renders them, so the source
  stays as is.

## R10. Dependency inventory and the import check

- **Decision**:
  - The inventory is a hand-written docs page, `docs/sphinx/dependencies.md`,
    in the `index.md` toctree. It has one table row per declared dependency:
    name, group, purpose, and the last audit decision.
  - A new test, `tests/smoke/test_declared_dependencies.py`, checks two
    things. First, every third-party top-level import in `src/`, `scripts/`,
    and `tests/` maps to a declared distribution. Second, the inventory
    table names exactly the declared dependencies.
- **Rationale**:
  - The test parses imports with `ast`, drops `sys.stdlib_module_names` and
    first-party names, and maps each module to its distributions with
    `importlib.metadata.packages_distributions()`. It reads the declared set
    from `pyproject.toml` with `tomllib`, across `[project.dependencies]`,
    `[project.optional-dependencies]`, `[dependency-groups]`, and
    `[build-system]`.
  - It needs no new package, so SC-004 holds.
  - The table check keeps the inventory true on the next Dependabot change.
- **Alternatives considered**: deptry: rejected, it adds a dependency for
  one check.
- **Found during implementation**: the check found two more undeclared
  imports, `markdown_it` in `scripts/impact_report.py` and `httpcore` in
  `tests/runtime/test_connection_reuse.py`. Both are now declared at their
  locked versions (`markdown-it-py` in `dev`, `httpcore` in `test`), so the
  lock gains no package. The project's own `kentik-api[analytics]` entry and
  the `{include-group = ...}` tables are not counted as declared packages.

## R11. Vulnerability audit in CI

- **Decision**: A new `audit` job in `.github/workflows/tests.yml` runs
  `uv audit --preview-features audit-command` with
  `continue-on-error: true`.
- **Rationale**: uv 0.13.0 prints "`uv audit` is experimental and may
  change without warning". Today it reports "no known vulnerabilities" in 76
  packages. `continue-on-error` shows a failure on the pull request but does
  not block the merge (FR-014). The flag only silences the warning.

## R12. Upstream report for openapi-python-generator

- **Decision**: Draft the issue text in
  `reports/upstream/upstream-openapi-python-generator-optional-formatters.md`. The
  maintainer files it, and the inventory row links the issue. The draft stays
  untracked, as `reports/.gitignore` keeps every report but the audit record.

- **Rationale**: Filing an issue in a third-party repository is a public
  action, so a person does it. The draft gives the evidence:
  `--formatter none`, Black, isort, and orjson in the lock, and no import
  of them in project code.

- **Upstream state on 2026-10-17**: one owner. The last release (2.1.2,
  2025-09-29) and the last merge (#121, 2025-09-28) are more than 12 months
  old, the longest gap in the project's history. Six pull requests are
  open, some since October 2025 with passing checks. Issues filed in 2026
  have no maintainer reply.

- **Decision on a pull request or a fork**: neither, for this finding. The
  three packages are in the dev group only, so no SDK user installs them.
  Making Black optional is a breaking change upstream, and an inactive
  project is unlikely to merge it. Keep the exact pin.

- **Fork when one of these is true** (the inventory row records them):
  - A needed generator fix is not possible in `scripts/openapi_templates/`
    or `fixup.py`, and upstream does not answer a pull request.
  - A security advisory affects the generator or a mandatory dependency,
    and upstream publishes no fix.
  - Fixing problems at the source would retire a large part of `fixup.py`.

  A fork can be tried without a code change through
  `OPENAPI_GENERATOR_FROM` (`docs/sphinx/local_generation_workflow.md`). A
  git URL in a dependency group is safe to publish, because dependency
  groups are not in the package metadata.

- **Alternatives considered**: An upstream pull request that moves Black and
  isort to an extra: rejected for now, see above. A fork now: rejected, it
  moves the generator's upkeep to this project for a dev-only saving.
