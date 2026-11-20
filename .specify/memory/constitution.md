<!--
Sync Impact Report
Version change: 1.4.3 → 1.4.4
Rationale: feature 007 replaces the Makefile with Poe the Poet tasks, so
every `make <target>` here becomes `uv run poe <task>`. `AGENTS.md` now holds
the instructions, and `CLAUDE.md` imports it with `@AGENTS.md`, because a
symlink checks out on Windows as a one-line text file. No principle changed,
so this is PATCH.
Modified principles: none (IV, V, Architecture, Development Workflow, and
Governance wording only)
Added sections: none
Removed sections: n/a
Deferred TODOs: none
Prior report (1.4.2 → 1.4.3, retained for history):
Version change: 1.4.2 → 1.4.3
Rationale: feature 006 adds rumdl, a Markdown linter, to `make lint`. The
Development Workflow section named only the two Ruff commands. No principle
changed, so this is PATCH.
Modified principles: none (Development Workflow wording only)
Added sections: none
Removed sections: n/a
Deferred TODOs: none
Prior report (1.4.1 → 1.4.2, retained for history):
Version change: 1.4.1 → 1.4.2
Rationale: the Architecture section said the SDK comes only from
`kentik/api-schema-public`. Feature 005 adds the local schema base,
`schema/openapi/`: hand-maintained descriptions of endpoints that upstream
does not publish (the V5 query and batch endpoints). The generator reads it
next to the upstream schema, and every service from it is REST-only. No
principle changed, so this is PATCH.
Modified principles: none (Architecture section wording only)
Added sections: none
Removed sections: n/a
Deferred TODOs: none
Prior report (1.4.0 → 1.4.1, retained for history):
Version change: 1.4.0 → 1.4.1
Rationale: factual drift fixes. No principle changed, so this is PATCH.
`make generate` fetches the schema at the commit in `schema.lock`, not at
HEAD. `make sync-schema` fetches HEAD and moves that pin. `public_names`
joins the phase modules. `make typecheck` checks the SDK (generated code
included), scripts, and tests, not only hand-written code.
Modified principles: none (III wording only)
Added sections: none
Removed sections: n/a
Deferred TODOs: none
Prior report (1.3.0 → 1.4.0, retained for history):
Version change: 1.3.0 → 1.4.0
Rationale: Principle VI prescribed `load_dotenv`, which writes `.env` into
os.environ, so every subprocess inherits the secrets. A Spec Kit run that
followed the principle would bring that leak back. The SDK reads the file
into a dict with `dotenv_values`, after explicit arguments and environment
variables. Principle VI now states that order and forbids `load_dotenv`.
This adds a MUST NOT, so it is MINOR.
Also in this revision (factual drift fixes, no principle changed): gRPC
routing matches a REST operation to the RPC with the same HTTP rule, not
the same name; `make generate` clones the schema and only `make generate
local` reads the sibling checkout, with no fallback; `make all` runs
`services tests`, and docs are opt-in; `fixup._fix_path_parameters()` and
the template sentinel join the guarded coupling; `api_surface` joins the
phase modules.
Modified principles: VI
Added sections: none
Removed sections: n/a
Deferred TODOs: none
Prior report (1.2.1 → 1.3.0, retained for history): Principle IV was
expanded to state that coverage means asserting the SDK's actual
observable behavior for every declared status, whichever layer produces
it (a 401 raises AuthenticationError in `request_json()`), with an
explicit anti-narrowing rule.
-->

# Kentik Community Python SDK Constitution

## Core Principles

### I. Generated Code Is Never Hand-Edited

`src/kentik_api/gen/`, `client_mixin.py`, and the generated docs pages under
`docs/sphinx/services/` and `docs/sphinx/sdk_runtime_architecture.md` are wiped
and rebuilt by `uv run poe generate` on every run. MUST NOT hand-edit any generated
file. If generated output is wrong, fix `scripts/generate_sdk.py`, the
responsible phase module in `scripts/generation/`, or the Jinja2 templates in
`scripts/openapi_templates/`, then regenerate. A parity check
(`parity.validate_generated_service_parity()`) fails the whole generation run
when generated service directories don't match the schema's service
directories; partial or manual patches do not survive it.

### II. One Shared Runtime for Every Endpoint

Every REST call MUST go through `request_json()` in
`src/kentik_api/core/rest_runtime.py`; every gRPC call MUST go through
`call_grpc()` in `src/kentik_api/core/grpc_runtime.py`. These centralize auth
headers, request execution, transport-failure wrapping, status checking, and
error-class dispatch for every service. MUST NOT generate, hand-write, or
suggest per-endpoint connection, auth, or retry code, and MUST NOT inline
request logic into individual service wrappers. Extend `request_json`,
`call_grpc`, or `APIConfig` instead.

### III. Generator Phase Modules Stay Independently Testable

`scripts/generation/` is split into single-concern phase modules (`parity`,
`error_package`, `fixup`, `wrapper_generation`, `docs_rendering`,
`endpoint_docs`, `api_surface`, `public_names`), each independently unit-tested under `tests/generator/`.
Intra-subpackage imports MUST stay relative (`from ._shared import ...`); MUST
NOT switch to absolute `scripts.generation.*` imports, since
`generate_sdk.py`'s own direct-execution import path depends on the relative
form. A helper used by only one phase module stays local to that module rather
than moving into `_shared.py` "for consistency."

### IV. Test Coverage Must Be Exhaustive, Not Representative

Generated and contract tests MUST exercise every endpoint and every option
discoverable from the OpenAPI schemas: every operationId (path × method),
every declared request parameter and body field, and every declared response
status code, including error responses. This is a standing rule, re-verified
every time the schema grows or `gen/` is regenerated, not a one-time task.
Incomplete endpoint or option coverage is a bug in the test suite or the
generator, not an acceptable gap.

Coverage of a status code means asserting the **SDK's actual observable
behavior** for that status, not asserting that a particular layer produced it.
A status MAY be handled in the shared runtime before per-operation dispatch,
in which case the generated per-operation error class never sees it and the
suite MUST assert the runtime's behavior instead. Handling a cross-cutting
status once in the runtime is the Principle II answer and MUST NOT be read as
a coverage gap. What is forbidden is the status going unasserted.

A suite MUST NOT be narrowed, skipped, parameterized away, or made
status-agnostic in order to make a change pass. When a runtime change shifts
the expected behavior for many endpoints at once, the suite is updated to the
new expectation for **every** affected endpoint. Whoever makes such a change
MUST demonstrate the suite still detects regressions, by reverting the change
and confirming the suite fails, and MUST record that result in the pull
request. A suite that stays green with the change reverted has been narrowed
and does not satisfy this principle.

### V. End-to-End Tests Are Opt-In and Safe-by-Default

`tests/e2e/` runs against the real Kentik API and MUST NOT run as part of
`uv run poe test`, `uv run poe all`, or default CI. It MUST stay gated behind an explicit
opt-in (`uv run poe test-e2e`, a `-m e2e` marker, or both). Coverage MUST default to
non-mutating List/Get operations; Create/Update/Delete coverage against a real
account is only acceptable against a disposable, sandboxed resource with
guaranteed cleanup (e.g. create-then-delete in a `finally`/fixture teardown),
and adding such coverage MUST be called out explicitly rather than added as a
side effect of other work.

### VI. Credentials Never Enter Code, Logs, or Prompts

`KentikAPI` takes each credential from the first source that has it: the
`email`/`api_token` arguments, then the `KENTIK_EMAIL`/`KENTIK_API_TOKEN`
environment variables, then the `env_file` (`.env` by default, found with
`find_dotenv`). The file MUST be read into a dict with `dotenv_values`, and
MUST NOT be loaded with `load_dotenv`: writing it into `os.environ` leaks the
secrets into every subprocess. MUST NOT hardcode credentials
in tests or examples, and MUST NOT read or print `.env` contents in code,
tests, or agent output.

### VII. Compatibility and Scope Discipline

MUST NOT introduce breaking API surface changes without calling them out
explicitly. Changes MUST stay focused; unrelated refactors belong in a
separate change. Known generator warnings are non-blocking but MUST be
tracked and reduced over time, not silently ignored.

## Architecture & Generation Pipeline

- The SDK is generated end-to-end from Kentik's public OpenAPI v3 schema
  (`kentik/api-schema-public`). `uv run poe generate` fetches it at the commit in
  `schema.lock`. `uv run poe sync-schema` fetches HEAD and moves that pin.
  `uv run poe generate --local` reads the sibling checkout `../api-schema-public/`
  and fails if it is absent. Neither falls back to the other.
- The generator also reads the local schema base, `schema/openapi/` in this
  repository. It MUST hold only hand-maintained descriptions of endpoints
  that upstream does not publish, and a service MUST NOT appear in both
  (the run fails). Every service from it is REST-only: the client mounts it
  on a REST transport to its own host, whatever the protocol.
- When multiple versioned swagger files exist for the same `(service,
  namespace, filename)` family, the generator MUST use only the newest
  version per family.
- Transport is dual-protocol: REST (default, `protocol="rest"`) and gRPC
  (`protocol="grpc"`) both route through the same generated
  `*ServiceWrapper`, bridging via `ParseDict` → `call_grpc()` →
  `MessageToDict` → `model_validate()`, and both MUST return the same
  Pydantic models for every operation gRPC covers. gRPC coverage is
  per-operation, not per-service or all-or-nothing: a wrapper method
  raises `NotImplementedError` for `GrpcTransport` either when that
  service's proto companions failed to import (`gen/pb_companions/`) at
  wrapper `__init__` time, or when the generator found no RPC that shares
  that REST operation's HTTP rule (proto service, verb, and path). Matching
  by RPC name alone is wrong: `alerting` declares `Delete` on several proto
  services. Neither case is a bug by itself.
  `tests/e2e/test_endpoints_e2e_grpc.py` (`uv run poe test-e2e-grpc`) treats
  `NotImplementedError` as an expected, passing outcome for exactly this
  reason. (This bullet previously flagged a drift against CLAUDE.md's
  stale "intentionally a stub" claim; resolved 2026-08-26, and both now
  agree.)
- Two files look hand-written but are fully regenerated every run and MUST
  NOT be hand-edited: `src/kentik_api/client_mixin.py` and
  `docs/sphinx/sdk_runtime_architecture.md` (plus
  `src/kentik_api/gen/README.md`).
- `error_package.inject_service_error_handling()` wires each generated
  service to its error classes by replacing the
  `# __ERROR_IMPORTS_PLACEHOLDER__` sentinel that `service.jinja2` emits,
  falling back to the `from kentik_api.core.rest_runtime import
  request_json` import line. `fixup._fix_path_parameters()` matches that
  same import line. Renaming or relocating `request_json` requires updating
  both in lockstep, or generation fails loudly (`ValueError`) rather than
  silently skipping.

## Development Workflow & Quality Gates

- Every project task is a poe task in `pyproject.toml`, run as
  `uv run poe <task>`, and MUST run the same on Windows, macOS, and Linux:
  no task may need a POSIX shell or load `.env`.
- Standard pipeline: `uv run poe all` runs `generate` then `test` in
  sequence. Docs are opt-in with `uv run poe docs`.
- After any change to generation output: regenerate (`uv run poe generate --local`),
  run the relevant focused test layer, then run the full `uv run poe test` before
  opening a PR.
- `uv run poe lint` (`ruff check --fix`, `ruff format`, and `rumdl check --fix`)
  and `uv run poe typecheck` (`ty check` on the SDK, generated code included, and
  on scripts and tests) MUST stay clean.
- `uv run poe test` MUST stay mocked-only and fast enough to run anywhere; `uv run poe
  test-e2e` MUST stay a separate, explicit, opt-in task (see Principle V).
- `uv run poe generate --local` and `uv run poe generate` both call
  `parity.validate_schema_files_or_raise()` before touching any existing
  generated output: every discovered swagger file MUST parse as JSON and
  declare the expected top-level OpenAPI keys, or the run aborts with a
  non-zero exit and names every offending file
  (specs/001-validate-schema-checkout/). This catches a corrupted or
  truncated schema *file*. It does NOT catch a whole service *directory*
  silently missing from the schema tree (a discovery-time gap, not a
  content one). For that, still verify the local `../api-schema-public/`
  checkout is clean (`git -C ../api-schema-public status`) before trusting
  `uv run poe generate --local`, or regenerate from a clean canonical clone with
  `uv run poe generate` (no `--local`) instead.

## Governance

This constitution governs planning, analysis, and review for all Spec Kit
workflows in this repository; it takes precedence over ad hoc practice when
the two conflict. `AGENTS.md` (which `CLAUDE.md` imports with `@AGENTS.md`)
remains the
detailed, day-to-day reference this constitution distills principles from.
If the two visibly diverge on a factual claim about the architecture, treat
that as a documentation-drift bug to fix, not a reason to silently pick one
(see the gRPC example above).

Amendments: propose the change, update this file, increment the version
below per semantic versioning (MAJOR: incompatible principle
removal/redefinition; MINOR: new principle or materially expanded guidance;
PATCH: wording/typo clarifications), and record the change in a Sync Impact
Report comment at the top of this file. `/speckit-plan`, `/speckit-tasks`,
and `/speckit-analyze` MUST treat this constitution as authoritative context;
complexity or deviation from it MUST be justified explicitly in the relevant
plan, not silently introduced.

**Version**: 1.4.4 | **Ratified**: 2026-08-25 | **Last Amended**: 2026-10-17
