# Implementation Plan: Fix Generator Correctness Defects

**Branch**: `feat/fix-generator-correctness` | **Date**: 2026-08-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-fix-generator-correctness/spec.md`

## Summary

Fix four verified defects in the SDK generator that produce factually wrong
output or false test confidence. Each fix is independent and small.

The governing discovery from Phase 0 research: the correct rule for classifying
a Service **already exists** in `parity.py`; eight other call sites simply
diverge from it. The classification fix is therefore not a design problem but a
sharing problem. Promote the existing correct rule into `_shared.py` and delete
the eight divergent copies.

No SDK runtime behaviour changes. Only documentation output, provenance notes,
failure reporting, and tests.

## Technical Context

**Language/Version**: Python 3.12+ (repo targets 3.12/3.13/3.14)

**Primary Dependencies**: No new dependencies. Uses stdlib `ast`, `json`,
`pathlib`, `contextlib`, already used by the generator.

**Storage**: N/A. The generator reads swagger files and writes source and docs.

**Testing**: pytest. `tests/generator/` is the primary layer here; the mocked
layers `tests/generated/`, `tests/runtime/`, `tests/smoke/` and the opt-in
`tests/e2e/` suites (`-m e2e`, `-m e2e_grpc`) serve as regression verification.

**Target Platform**: Local developer machine and CI, via `make generate`.

**Project Type**: A code generator plus the SDK library it emits. This feature
touches the generator and its documentation output only.

**Performance Goals**: None. Explicitly a non-goal per spec Assumptions. Phase 0
measured the relevant AST parsing at 58 ms for all 124 generated service files,
against a generation run of roughly 35 seconds dominated by about 50 external
tool invocations (`uvx openapi-python-generator` per swagger file, `protoc`, and
two `ruff` passes). No change here is expected to move that number.

**Constraints**:

- Generated SDK code must be byte-identical after this feature. Only the
  intended documentation changes may differ (FR-011). Verified with `git diff`
  on `src/kentik_api/gen/`.
- Fixes belong in the generator, never in generated output (Constitution I).
- The full mocked suite and both opt-in e2e suites must stay green.

**Scale/Scope**: 41 generated directories, of which 40 are Services. Four
generator modules touched, plus `tests/_discovery.py` and three test modules.
Expected diff: one shared helper, eight call-site replacements, two string
fixes, one exception-handling change, three retargeted tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checked against `.specify/memory/constitution.md` v1.2.1:

| Principle / Section | Assessment |
| --- | --- |
| I. Generated Code Is Never Hand-Edited | **PASS**: every fix lands in `scripts/generation/` or `scripts/generate_sdk.py`. Corrected documentation is produced by regenerating, never by editing a generated file. The provenance fix replaces a hand-typed string with a value derived from the writing code, which strengthens this principle. |
| II. One Shared Runtime for Every Endpoint | **N/A**: no request or transport code is touched. |
| III. Generator Phase Modules Stay Independently Testable | **PASS, and improved**: the shared Service rule goes in `_shared.py`, whose stated purpose is helpers that two or more phase modules genuinely use. Nine call sites use it, clearing the "resist single-consumer helpers" bar decisively. No phase module gains a dependency on another. |
| IV. Test Coverage Must Be Exhaustive, Not Representative | **PASS, and improved**: three assertions currently exercise a path production never runs; they move onto the live path. New tests cover the shared rule and the provenance derivation. |
| V. End-to-End Tests Are Opt-In and Safe-by-Default | **PASS**: no change to e2e gating. Both suites are run only as verification. |
| VI. Credentials Never Enter Code, Logs, or Prompts | **N/A**: no credential handling touched. |
| VII. Compatibility and Scope Discipline | **PASS**: no SDK surface change (FR-011). Scope is narrowed to four verified defects, with the structural refactors from the same review deferred and recorded in spec Assumptions. |
| Architecture & Generation Pipeline | **PASS**: pipeline ordering constraints and the `request_json` injection anchor are untouched. Removing the in-place schema mutator strengthens the documented guardrail that generation must not modify the schema checkout. |
| Development Workflow & Quality Gates | **PASS**: `make lint`, `make typecheck`, `make test` must stay clean. Regeneration is required to validate, and the local `../api-schema-public` checkout will be confirmed clean first, per the constitution's schema-checkout guardrail. |

**Gate result: PASS.** No violations, so the Complexity Tracking table is
omitted.

## Project Structure

### Documentation (this feature)

```text
specs/002-fix-generator-correctness/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist (from /speckit-specify)
└── tasks.md             # Phase 2 output (/speckit-tasks, not created here)
```

No `contracts/` directory. This feature changes internal generator behaviour and
documentation output only. It exposes no new interface to users or other
systems, and FR-011 requires the SDK's public surface to stay unchanged. The
plan workflow directs that contracts be skipped for purely internal work.

### Source Code (repository root)

```text
scripts/
├── generate_sdk.py                 # remove the dead in-place schema mutator
└── generation/
    ├── _shared.py                  # NEW: the single Service-classification rule
    ├── parity.py                   # adopt shared rule (its rule is today's correct one)
    ├── docs_rendering.py           # adopt shared rule (3 divergent sites)
    ├── endpoint_docs.py            # adopt shared rule; derive provenance;
    │                               # stop swallowing extraction failures
    └── wrapper_generation.py       # adopt shared rule (2 divergent sites)

src/kentik_api/
└── gen/                            # regenerated: +core.md, -pb_companions page

tests/
├── _discovery.py                   # adopt shared rule (excludes nothing today)
└── generator/
    ├── test_generate_sdk.py        # retarget 3 tests onto patched_swagger
    ├── test_parity.py              # cover the shared rule
    └── test_endpoint_docs.py       # cover provenance + failure surfacing

# Hand-written docs asserting facts this feature changes (FR-012, FR-013)
CONTEXT.md                          # sharpen the Service definition
CLAUDE.md                           # _shared.py export list (already stale)
scripts/generation/README.md        # _shared.py public-interface row
tests/generator/README.md           # rows for any test files added
```

**Structure Decision**: No new modules or directories. The shared rule goes in
the existing `scripts/generation/_shared.py`, which the constitution designates
for helpers used by two or more phase modules. This keeps the change to files
that already exist, matching the spec's Assumption that introducing a dedicated
module for the Service concept is deferred to a follow-up feature.

## Documentation Impact

This feature changes facts that hand-written documents currently assert, so
those documents are in scope (FR-012, FR-013). All follow the repo's existing
conventions: markdownlint-clean, cross-directory references hyperlinked,
steady-state phrasing rather than change narration.

| Document | Why it must change |
| --- | --- |
| `CONTEXT.md` | The `Service` entry says each Service "maps to one directory under `src/kentik_api/gen/`", which reads as though every directory is a Service. That ambiguity is what let an internal directory be documented as one. It must state the exception. |
| `CLAUDE.md` | Describes `_shared.py` as holding "the two helpers" and names two. This is **already wrong** (the module exports eight), and it already contradicts `scripts/generation/README.md`, which lists all eight. Adding a ninth makes it worse. |
| `scripts/generation/README.md` | Its `_shared.py` row lists the module's public interface and needs the new rule added. |
| `tests/generator/README.md` | Its Files table documents every test module; rows are needed for whatever this feature adds. |

Two of these are pre-existing defects rather than consequences of this feature.
The `CLAUDE.md` versus `scripts/generation/README.md` disagreement about
`_shared.py` was introduced by an earlier documentation pass that corrected the
README row without correcting the matching claim in `CLAUDE.md`. It is fixed
here because this feature touches the same module and would otherwise widen the
gap.
