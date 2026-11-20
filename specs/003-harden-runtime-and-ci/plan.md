# Implementation Plan: Harden the Shared Runtime, Retire Dead Code, Enforce CI

**Branch**: `FA-2-Update-the-python-SDK-from-V5-to-V6` | **Date**: 2026-09-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-harden-runtime-and-ci/spec.md`

## Summary

Close the gaps a 2026-09-21 stability review found, plus one the review's
follow-up investigation surfaced: REST and gRPC raise **different exception
types for the same failure**, so a caller's `except` clauses do not survive the
protocol switch the client advertises.

The technical approach is deliberately narrow. Every runtime change lands in
`src/kentik_api/core/`, `errors/`, `transports/`, and `auth/`, which
Constitution Principle II already designates as the single place cross-cutting
behavior belongs. Eleven of twelve user stories therefore produce a **zero-line
generated diff**. Only User Story 10 (per-call configuration override) changes
generated output, and it does so through `wrapper_generation.py`, never by hand.

Two properties that hold today but are unguarded, generation determinism and
formatting, become CI gates in the same feature that relies on them.

## Technical Context

**Language/Version**: Python >=3.12 (CI matrix 3.12, 3.13, 3.14; local 3.14.2)

**Primary Dependencies**: httpx >=0.28.1, grpcio >=1.84.0, pydantic >=2.12.5,
protobuf >=7.35.1,<8, python-dotenv. Dev: pytest >=9, respx, ty, ruff, sphinx.

**Storage**: N/A (stateless client library)

**Testing**: pytest with 5 layers (`tests/generated/`, `tests/runtime/`,
`tests/smoke/`, `tests/generator/` mocked and default; `tests/e2e/` opt-in via
`-m e2e` / `-m e2e_grpc`). HTTP mocked with `respx`. Type-checked with `ty`.

**Target Platform**: Published library (`kentik-api` on PyPI), any OS

**Project Type**: Single library, generated end-to-end from an OpenAPI v3 schema
by `scripts/generate_sdk.py` plus the phase modules in `scripts/generation/`

**Performance Goals**: N sequential REST calls on one client open 1 connection,
not N. Every gRPC call terminates within a bounded deadline.

**Constraints**:

- Zero-line `make generate local` diff for every story except User Story 10
- No per-endpoint connection, auth, retry, or timeout code (Principle II)
- `make test` stays mocked-only, no network, no credentials
- Kentik enforces 60 requests / 60s **per endpoint**, shared by both transports

**Scale/Scope**: 35 mounted services, 233 wrapper operations, 1198 generated
files, 198 operations with a gRPC translation

## Constitution Check

*GATE: evaluated before Phase 0 and re-evaluated after Phase 1 design.*

| Principle | Assessment | Gate |
| --- | --- | --- |
| **I. Generated code is never hand-edited** | US10 is the only story that changes `gen/`, and it does so by editing `wrapper_generation.py` then regenerating. No hand edits anywhere. | PASS |
| **II. One shared runtime for every endpoint** | Every timeout, deadline, connection, auth-header, error-mapping, and rate-limit change lands in `core/`, `errors/`, or `transports/`. This feature strengthens the principle rather than straining it. | PASS |
| **III. Generator phase modules stay independently testable** | US10 touches only `wrapper_generation.py`; US11 raises coverage of three phase modules. Intra-package imports stay relative. | PASS |
| **IV. Test coverage exhaustive, not representative** | US2 changes which exception a 401 produces, so `tests/generated/test_endpoint_schema_coverage.py` must be updated to assert the new expectation for **every** discovered endpoint, not spot-checked. Promoted from a note to FR-041 and FR-042, which also require proving the suite still fails when the fix is reverted. | PASS with gate |
| **V. E2E tests opt-in and safe-by-default** | FR-050 forbids any e2e job in CI. The rate-limit investigation and the learning exercise both used read-only calls only. | PASS |
| **VI. Credentials never enter code, logs, or prompts** | The exercise directory is gitignored before any file was created, uses `.env` the same way `KentikAPI()` does, and prints server response headers only, never request headers. | PASS |
| **VII. Compatibility and scope discipline** | `ConfigurationError` replacing `ValueError`, REST raising `AuthenticationError`, and gRPC timeouts becoming `TransportError` are all caller-visible. FR-058 requires each to be named in release notes. V6 is a clean break from V5 (tags v1.0.0 to v1.0.7, 2022 to 2023), recorded in the spec. | PASS with callout |

**Gate IV detail, now a hard requirement rather than a note.**
`test_endpoint_schema_coverage.py` drives every status in each service's
generated `response_error_map`. Routing 401 to `AuthenticationError` in the
shared runtime means generated per-operation error classes never see a 401, so
this suite's expectation changes for **every discovered endpoint at once**.

That is precisely the situation in which a suite gets quietly weakened to make a
change pass. Three requirements close that door:

- **FR-041** forbids narrowing, skipping, or making the suite status-agnostic.
- **FR-042** requires proving the suite still bites: deliberately revert the
  shared-runtime 401 path and confirm the suite **fails**. A suite that stays
  green either way has been narrowed.
- **FR-042** further requires that this check be performed and its result
  recorded, not assumed.

Implementation note: FR-042's check is a one-off manual verification during
Phase A, not a permanent test. Record the outcome in the pull request that lands
User Story 2.

**No complexity violations.** The Complexity Tracking table below is empty.

## Project Structure

### Documentation (this feature)

```text
specs/003-harden-runtime-and-ci/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: design decisions and their rationale
├── data-model.md        # Phase 1: the entities this feature adds or changes
├── quickstart.md        # Phase 1: how to verify each story locally
├── contracts/
│   └── runtime-api.md   # Phase 1: the public surface that changes
└── tasks.md             # Phase 2 output (/speckit-tasks, NOT created here)
```

### Source code (repository root)

Only these paths change. Everything else, including all 1198 files under
`src/kentik_api/gen/`, is untouched except by User Story 10's regeneration.

```text
src/kentik_api/
├── core/
│   ├── api_config.py          # + timeout, + shared httpx.Client, + validation
│   ├── rest_runtime.py        # persistent client, 401 -> AuthenticationError,
│   │                          #   rate-limit capture
│   ├── grpc_runtime.py        # deadline, status classification, rate-limit
│   │                          #   capture from initial metadata
│   └── rate_limit.py          # NEW: the RateLimit value object and parser
├── errors/__init__.py         # ConfigurationError raise sites, rate_limit field
├── transports/
│   ├── rest_client.py         # close() releases the shared client
│   └── grpc_client.py         # unchanged behavior, now covered by tests
├── auth/credentials.py        # get_rest_headers() becomes the single source
└── client.py                  # ConfigurationError instead of ValueError

scripts/
├── generate_sdk.py                     # formatting fix (US4)
└── generation/wrapper_generation.py    # stop stripping api_config_override (US10)

tests/
├── runtime/
│   ├── test_rest_runtime.py            # connection reuse, timeouts, 401
│   ├── test_grpc_runtime.py            # deadline, all 16 codes, rate limit
│   ├── test_transport_symmetry.py      # NEW: same failure, both transports
│   └── test_rate_limit.py              # NEW: header and metadata parsing
├── generated/test_endpoint_schema_coverage.py   # updated 401 expectation
├── generator/                          # raised coverage (US11)
└── smoke/test_examples_import.py       # NEW: every example imports (US12)

.github/workflows/                      # lint, determinism, docs gates (US4)
docs/sphinx/guides/rest-vs-grpc.md      # NEW: the published guide (US9)
learn/                                  # gitignored exercise, never committed
```

**Structure Decision**: single-library layout, unchanged. This feature adds
exactly one new runtime module (`core/rate_limit.py`) and three new test
modules. Everything else edits files that already exist. No new package, no new
layer, and no new abstraction: the shared runtime already is the seam this work
belongs behind.

## Implementation Phases

Sequenced so each phase leaves the tree green and independently reviewable.

| Phase | Stories | Why here |
| --- | --- | --- |
| **A. Correctness** | US2 error symmetry, then US1 deadline, then US3 tests | US2 first: adding a deadline before fixing the mapping would make the *expected* timeout path report a fabricated HTTP 500. US3 last, so the new tests lock in both fixes. |
| **B. Enforcement** | US4 CI gates | Runs early so every later phase is protected by determinism, lint, and docs gates. |
| **C. Runtime** | US5 `ConfigurationError`, US6 auth headers, US7 connection reuse, US8 rate limits | US7 before US8: both touch response handling in `request_json`, and US8's capture point sits inside the client US7 introduces. |
| **D. Documentation** | US9 exercise and guide | Needs Phase A complete, because the guide documents the corrected error behavior. |
| **E. Deferred** | US10 per-call override, US11 generator coverage, US12 examples | US10 last: the only generated-output change, committed on its own with a regenerated `api_surface.json`. |

### Baseline (captured 2026-09-22, before any source change)

The success criteria are measured against these figures (T001 to T003).

| Check | Result |
| --- | --- |
| `make test` | 2016 passed, 43 skipped, 466 deselected |
| `make typecheck` | clean |
| `ruff check .` | clean |
| `ruff format --check .` | 7 files would be reformatted: `scripts/generate_sdk.py` (T034) and 6 files under `.specify/` added by the Spec Kit upgrade |
| `make generate local && git diff --exit-code` | no generated file changed |

Runtime line coverage (SC-004 raises the first three to 100%):

| Module | Coverage |
| --- | --- |
| `core/grpc_runtime.py` | 65% |
| `auth/credentials.py` | 44% |
| `transports/grpc_client.py` | 50% |
| `core/rest_runtime.py` | 79% |
| `core/api_config.py` | 100% |
| `transports/base.py` | 80% |
| `transports/rest_client.py` | 100% |

Generator line coverage from `tests/generator/` alone:

| Module | Coverage | FR-043 floor |
| --- | --- | --- |
| `docs_rendering.py` | 18% | 85% |
| `endpoint_docs.py` | 26% | 85% |
| `wrapper_generation.py` | 54% | 85% |
| `parity.py` | 91% | 91% (no regression) |
| `error_package.py` | 94% | 94% (no regression) |
| `_shared.py` | 95% | 95% (no regression) |
| `fixup.py` | 95% | 95% (no regression) |
| `api_surface.py` | 97% | 97% (no regression) |

The per-module threshold is 85% (FR-043). A module already above it keeps its
current figure as its floor, so the bar is never met by letting it fall.

## Complexity Tracking

> No Constitution Check violations. Table intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| None | N/A | N/A |
