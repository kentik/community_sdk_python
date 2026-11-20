# Feature Specification: Dependency Feature Adoption and Reduction

**Feature Branch**: `chore/dependency-feature-adoption`

**Created**: 2026-10-17

**Status**: Draft

**Input**: User description: "Review the recent Python dependency upgrades for
new features. Audit where they can improve this codebase, and where a dependency
can retire another one. For example, Ruff 0.17 also formats Markdown, and this
project uses markdownlint. Spec out the adoption of the new features for every
dependency, and find where the number of dependencies can go down."

## Background

Commit `6fc5590` moved the lock to the latest releases. It changed Ruff from
0.14.11 to 0.17.1, ty from 0.0.82 to 0.0.89, Pydantic from 2.13.5 to 2.14.1,
and python-dotenv from 1.2.3 to 1.2.4. It kept the Ruff 0.14 rule set and
Python-only formatting on purpose, and left their adoption to a later change.
This specification is that change, widened to every declared dependency.

The audit on 2026-10-17 read the GitHub release notes of each dependency and
ran read-only probes against this repository. The main results are:

- Ruff does not lint Markdown. Since 0.16.0, `ruff format` formats only the
  fenced Python code blocks in Markdown files. A probe file with mixed list
  markers and a heading without a space came back unchanged, and
  `ruff check` found no files to check. Ruff cannot retire markdownlint.
- markdownlint is not a Python dependency of this project. Only the
  configuration file `.markdownlint-cli2.jsonc` exists. No Makefile target
  and no CI job runs it, and it is not installed on the maintainer host.
  Markdown rules are not enforced today.
- If Ruff formats the Python blocks in Markdown, 7 files change: 3
  generated service pages, 3 spec documents, and `src/kentik_api/README.md`.
- The Ruff 0.17 default rule set (413 rules, up from 59) reports 117
  findings in hand-written code, 61 of them with a safe automatic fix. With
  the generated code included, it reports 11,011 findings.
- The dependency floor `ty>=0.0.73` permits versions before 0.0.84. ty
  0.0.84 fixed the advisory GHSA-vxvm-j4xq-q7m4, a use-after-free fault
  that can cause arbitrary code execution during incremental type checking.
- python-dotenv 1.2.3 removes a leading UTF-8 byte order mark, which made
  the first variable in a `.env` file disappear. Version 1.2.4 reads
  `KEY= # comment` as an empty value, not as the comment text. The SDK reads
  credentials with python-dotenv, and its floor is `>=1.2.1`.
- MyST-Parser 5.1.0 added the `alert` syntax extension. Three GitHub alerts
  (`> [!WARNING]`, `> [!NOTE]`) in `docs/sphinx/guides/` render in Sphinx
  as plain block quotes with the literal marker text today.
- The docs floors `myst-parser>=2.0.0` and `sphinxcontrib-mermaid>=1.0.0`
  are lower than what `sphinx>=9.1.0` needs. MyST-Parser 5.0.0 is the first
  release that supports Sphinx 9.
- `openapi-python-generator` always installs Black, isort, and orjson. The
  generator calls it with `--formatter none` and formats with Ruff, so the
  project never uses those three packages.
- `tests/generator/test_openapi_templates.py` imports `jinja2`, but no
  dependency group declares it. It installs only as a dependency of other
  packages.
- `uv audit`, an experimental uv command, found no known vulnerabilities in
  the 76 locked packages.

### Dependency inventory

| Dependency | Group | Locked | Finding | Proposed decision |
| --- | --- | --- | --- | --- |
| python-dotenv | runtime | 1.2.4 | Parser fixes for credentials files | Keep, raise floor |
| googleapis-common-protos | runtime | 1.75.5 | Needed by gRPC stubs | Keep |
| grpcio | runtime | 1.84.0 | gRPC transport | Keep |
| protobuf | runtime | 7.36.2 | Ships no type information | Keep |
| httpx | runtime | 0.28.1 | No release since 2024-12-06 | Keep the `<1` cap |
| pydantic | runtime | 2.14.1 | Thread-safe model rebuild, constant-time secret comparison | Keep, raise floor |
| pandas | analytics | 3.0.6 | Used by the analytics package | Keep |
| pyarrow | analytics | 26.0.0 | Reads and writes the Parquet cache | Keep |
| pyyaml | analytics | 6.0.3 | Reads query definition files | Keep |
| grpcio-tools | dev | 1.84.0 | Compiles the protos | Keep |
| types-protobuf | dev | 7.35.1 | protobuf ships no `py.typed` | Keep |
| ty | dev | 0.0.89 | Security fix in 0.0.84 | Keep, raise floor |
| ruff | dev | 0.17.1 | Markdown code blocks, wider default rules, CI annotations | Keep, adopt features |
| openapi-python-generator | dev | 2.1.2 | Installs unused Black, isort, orjson | Keep, report upstream |
| packaging | dev | 26.3 | Imported by the release scripts | Keep |
| pytest | test | 9.1.1 | Native TOML table, strict mode, subtests | Keep, adopt features |
| respx | test | 0.23.1 | Replacing it needs a transport seam in the protected runtime | Keep |
| autodoc-pydantic | docs | 2.2.0 | Last release 2024-04-27, but the repository is active | Keep, record the risk |
| myst-parser | docs | 5.1.0 | GitHub alert extension, floor too low | Keep, adopt, raise floor |
| sphinx | docs | 9.1.0 | No change | Keep |
| sphinx-book-theme | docs | 1.4.0 | No change | Keep |
| sphinxcontrib-mermaid | docs | 2.1.1 | Floor too low | Keep, raise floor |
| hatchling, hatch-vcs | build | n/a | `uv_build` has no documented VCS version source | Keep |
| rumdl | dev | new | Markdown linter installed through uv, reads the markdownlint configuration | Add |

The audit found no declared dependency that a newer release of another
dependency makes redundant. The dependency count can go down only through
an upstream change in `openapi-python-generator`.

## Clarifications

### Session 2026-10-17

- Q: How must the project enforce Markdown rules? A: Add rumdl to the dev
  group and run it in the lint command and in CI. It installs through uv
  like Ruff and ty, so neither CI nor a contributor needs Node. It reads
  `.markdownlint-cli2.jsonc` without changes. On 2026-10-17 it found 133
  issues, and markdownlint-cli2 0.23.3 found 138. Both agree on the large
  groups. Only markdownlint flagged 8 table-style issues (MD060). Only
  rumdl flagged 3 broken relative links (MD057).
- Q: Which Ruff lint rule set must the project use? A: The full Ruff 0.17
  default set for hand-written code.
- Q: Must the runtime floor for Pydantic rise to 2.14? A: Yes. Every user
  gets thread-safe model rebuilds and constant-time secret comparison.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Floors exclude known-bad versions (Priority: P1)

A maintainer or an SDK user installs the project without the lock file. The
resolver must not pick a version with a known security advisory or a known
credentials parsing fault.

**Why this priority**: The lock protects only this repository. Users of the
published package and anyone who runs `uv sync --upgrade` resolve from the
floors.

**Independent Test**: Resolve the project at the lowest permitted versions
and make sure that each floor named in FR-001 to FR-003 holds.

**Acceptance Scenarios**:

1. **Given** a fresh environment, **When** the dev group resolves at its
   lowest versions, **Then** ty is 0.0.84 or later.
2. **Given** a user installs the SDK at its lowest versions, **When** the
   SDK reads a `.env` file with a byte order mark or a `KEY= # comment`
   line, **Then** it reads the same values that the locked version reads.
3. **Given** a user installs the SDK at its lowest versions, **When** the
   resolver picks Pydantic, **Then** it is 2.14.0 or later.
4. **Given** the docs group resolves at its lowest versions, **When** the
   Sphinx build runs, **Then** it passes with warnings as errors.
5. **Given** the raised runtime floors, **When** `make check-changelog`
   runs, **Then** it passes because `CHANGELOG.md` names each one.

---

### User Story 2 - Ruff features in use (Priority: P2)

A maintainer runs `make lint` and the CI lint job. Ruff formats the Python
examples in hand-written Markdown, applies the agreed rule set, and shows
each CI finding as an annotation on the pull request.

**Why this priority**: The upgrade is in the lock but its features are off.
Python examples in the docs can drift from the code style today.

**Independent Test**: Run `make lint` and the CI lint job on a branch with
one badly formatted Markdown code block and one rule violation.

**Acceptance Scenarios**:

1. **Given** a badly formatted Python block in a hand-written Markdown file,
   **When** the CI lint job runs, **Then** it fails and annotates the line.
2. **Given** a regeneration, **When** the generator writes service pages,
   **Then** their Python examples already pass the Ruff Markdown formatter.
3. **Given** the Ruff 0.17 default rule set on hand-written code, **When**
   `ruff check .` runs, **Then** it reports zero findings.
4. **Given** a regeneration, **When** `ruff check .` runs on generated
   code, **Then** it applies the same rules as today.

---

### User Story 3 - Markdown rules are enforced (Priority: P2)

A contributor opens a pull request that adds a Markdown file. rumdl checks
it with the rules in `.markdownlint-cli2.jsonc`, in the lint command and in
CI.

**Why this priority**: The project writes a configuration that nothing
enforces. The configuration and the files drift apart.

**Independent Test**: Add a Markdown file that breaks rule MD032 and run
the lint command.

**Acceptance Scenarios**:

1. **Given** a Markdown file that breaks a configured rule, **When** the
   CI lint job runs, **Then** it fails and names the file, the line, and
   the rule.
2. **Given** a relative link to a file that does not exist, **When** the
   lint command runs, **Then** it reports the link.
3. **Given** a fresh clone with only uv and Git installed, **When** the
   contributor runs the lint command, **Then** the Markdown check runs
   without Node.

---

### User Story 4 - Test and docs tooling features in use (Priority: P3)

A maintainer runs the tests and builds the docs. pytest fails on unknown
markers, configuration typos, and unexpected passes. GitHub alerts render as
admonitions in Sphinx.

**Why this priority**: These are improvements, not faults. Each one is small.

**Independent Test**: Add a test with an unknown marker, and build the docs
page that contains a `> [!WARNING]` alert.

**Acceptance Scenarios**:

1. **Given** a test with a misspelled marker, **When** `make test` runs,
   **Then** pytest stops with an error.
2. **Given** `docs/sphinx/guides/generation.md`, **When** Sphinx builds it,
   **Then** the warning renders as an admonition without the `[!WARNING]`
   text.

---

### User Story 5 - Every dependency has a recorded reason (Priority: P3)

A maintainer who reviews a Dependabot pull request finds why each declared
dependency exists and what the last audit decided.

**Why this priority**: The inventory makes the next audit faster and keeps
undeclared imports from returning.

**Independent Test**: Compare the inventory with the declared dependencies
and with the third-party imports in `src/`, `scripts/`, and `tests/`.

**Acceptance Scenarios**:

1. **Given** a third-party import in project code, **When** a check runs,
   **Then** a dependency group declares that package.

### Edge Cases

- The generated pages under `docs/sphinx/services/` and `gen/*/README.md`
  must stay byte-identical to generator output. If Ruff formats them, the
  generator must emit the formatted text first, or the CI drift check fails.
- Ruff Markdown formatting changes Python blocks that show intentionally
  invalid code or a long one-line example. Those blocks need a language tag
  that Ruff skips, or a suppression.
- `uv audit` is experimental. A CI job that uses it must not block a merge
  on a change in its output format.
- Spec Kit rewrites `.specify/`, `.github/skills/`, and `.claude/skills/` on
  upgrade. No new check can require edits in those paths.
- pytest strict mode enables new strictness options in later pytest
  releases. This is safe only because the lock pins pytest.
- The default rule set reports 11,011 findings when it includes generated
  code. Generated code is out of scope for the wider set. The generator
  output must still pass the rules it passes today.
- A finding that a rule reports on purpose-built code, for example `exec`
  in a test helper, needs a suppression on that line with a reason. A
  rule that is wrong for the whole project needs an entry in the ignore
  list with a reason.
- The 133 existing Markdown findings, 103 of them long lines, must be
  fixed or covered by a recorded rule change before CI enforces the rules.
- A contributor whose editor runs the markdownlint extension can see a
  result that differs from CI, for example on table style. The CI result
  decides.
- Vendored agent skills under `.claude/skills/` and `.github/skills/` stay
  outside the Markdown check, as they are in the markdownlint ignores
  today.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The dev group floor for ty MUST be 0.0.84 or later.
- **FR-002**: The runtime floor for python-dotenv MUST be 1.2.4 or later.
- **FR-003**: The docs group floors MUST match the lowest versions that
  support the declared Sphinx floor, for myst-parser and
  sphinxcontrib-mermaid at a minimum.
- **FR-004**: `ruff format` MUST format the Python code blocks in
  hand-written Markdown files, and the CI lint job MUST check them.
- **FR-005**: The generator MUST write service pages and service READMEs
  whose Python code blocks already pass the Ruff Markdown formatter.
- **FR-006**: Hand-written code MUST pass the Ruff 0.17 default rule set
  with zero findings. Each ignored rule MUST have a recorded reason.
  Generated code MUST keep its current rule groups.
- **FR-007**: The CI lint job MUST report Ruff findings as GitHub
  annotations.
- **FR-008**: rumdl, pinned to an exact version in the dev group, MUST
  check every hand-written Markdown file with the rules in
  `.markdownlint-cli2.jsonc`. The lint command and CI MUST run it, and
  neither MUST need Node.
- **FR-009**: pytest configuration MUST use the native `[tool.pytest]`
  table with strict mode on, and the full mocked suite MUST pass.
- **FR-010**: Sphinx MUST render GitHub alerts as admonitions, and the
  docs build MUST pass with warnings as errors.
- **FR-011**: Every third-party package that project code imports MUST be
  declared in a dependency group. This includes `jinja2` for the generator
  tests.
- **FR-012**: The project MUST record each declared dependency with its
  purpose and the decision of the last audit.
- **FR-013**: The project MUST report to `openapi-python-generator` that
  Black, isort, and orjson are mandatory dependencies when
  `--formatter none` and the default JSON library make them unused.
- **FR-014**: CI MUST run a dependency vulnerability audit that does not
  block a merge while the audit command is experimental.
- **FR-015**: The runtime floor for Pydantic MUST be 2.14.0 or later.
- **FR-016**: The work MUST NOT change the public API surface, the shared
  REST runtime, or generated code outside formatting. The runtime floors
  in FR-002 and FR-015 are the only exception.
- **FR-017**: `CHANGELOG.md` MUST name each raised runtime floor in its
  Unreleased section, and `api_surface.json` MUST record the new floors.
  `make check-changelog` treats a raised floor as a breaking change.

### Key Entities

- **Declared dependency**: A package in `[project.dependencies]`, an
  optional extra, a dependency group, or `[build-system]`. It has a floor,
  a locked version, a purpose, and an audit decision.
- **Audit decision**: Keep, retire, raise floor, adopt features, or report
  upstream, with the evidence that supports it.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: No permitted version of a declared dependency has a published
  security advisory that a later release fixes.
- **SC-002**: Zero hand-written Markdown files fail the Ruff Markdown
  formatter check, and a regeneration leaves the tree unchanged.
- **SC-003**: `ruff check .` reports zero findings, with the Ruff 0.17
  default rule set on all hand-written code.
- **SC-004**: The lock file grows by one package at most, rumdl.
  Declaring a package that is already locked, such as jinja2, does not
  add one.
- **SC-005**: All 3 GitHub alerts in `docs/sphinx/guides/` render as
  admonitions.
- **SC-006**: 100% of third-party imports in `src/`, `scripts/`, and
  `tests/` map to a declared dependency.
- **SC-007**: The mocked test suite, the type check, the docs build, and
  the generated-output drift check pass on Python 3.12, 3.13, and 3.14.

## Assumptions

- The lock keeps its current versions. This work adopts features and
  changes floors, but does not upgrade packages.
- The audit used GitHub release notes as the primary source. Ruff 0.17.1,
  ty 0.0.89, Pydantic 2.14.1, pytest 9.1.1, and MyST-Parser 5.1.0 are the
  baselines.
- `pyrightconfig.json` stays, because Pylance in the editor reads it.
- Retiring respx needs a transport injection point in `APIConfig`. The
  project protects that runtime, so respx stays.
- Retiring python-dotenv needs a hand-written `.env` parser for
  credentials. The risk is higher than the benefit of one fewer package.
- `uv_build` documents no VCS version source, so hatchling and hatch-vcs
  stay.
