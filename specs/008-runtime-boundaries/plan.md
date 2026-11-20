# Implementation Plan: Runtime Boundary Fixes

**Branch**: `fix/008-runtime-boundaries`

**Date**: 2026-10-19

**Spec**: [Runtime Boundary Fixes](spec.md)

## Summary

Fix timeout ownership, batch wait limits, and empty cache refreshes.
Copy timeout values into and out of active configuration state.
Carry one absolute batch deadline through a private configuration copy
and the existing REST runtime. Return `None` for a current cache.

The deadline model remains cooperative, not hard cancellation.
A timeout observed at or after the batch deadline becomes
`BatchWaitTimeout`. Earlier observed timeouts and all non-timeout errors
remain unchanged. The spec records these delegated defaults.

## Technical Context

| Area | Decision |
| --- | --- |
| Language | Python 3.12 minimum, with existing 3.13 and 3.14 support |
| Dependencies | Existing HTTPX, Pydantic, pandas, pyarrow, and pytest |
| Storage | Existing Parquet cache files, with no format migration |
| Testing | Existing pytest suites, controlled clocks, mocked HTTP |
| Platforms | Linux, macOS, and Windows |
| Project type | Python library with generated API operations |
| Performance | No extra HTTP client, request, or repeated no-op scan |
| Constraints | Stable signatures, no dependencies or generated changes |
| Scope | Four hand-written modules and existing tests and guides |

No technical unknown remains under the delegated defaults.
New regressions need no real sleeps, credentials, external API, or
cancellation thread. Existing unrelated tests retain their behavior.

## Constitution Check

The initial gate passes against constitution 1.4.4:

| Principle | Initial Assessment |
| --- | --- |
| I: Generated code | No generated source or schema changes |
| II: Shared runtime | All REST requests still use `request_json()` |
| III: Generator phases | No generator or shared-parser changes |
| IV: Exhaustive tests | No narrowed contracts or skipped response cases |
| V: Live tests | No live test or real-account access is needed |
| VI: Credentials | Dummy fixtures only, no credential-file access |
| VII: Compatibility | Stable signatures, explicit behavior corrections |

Preserve the timeout getter's `httpx.Timeout` type, not object identity.
Reject invalid polling values with `ValueError`. Document the corrections
in release notes. No constitution exception is required.

## Project Structure

### Feature Documents

```text
specs/008-runtime-boundaries/
  spec.md
  plan.md
  research.md
  data-model.md
  quickstart.md
  contracts/runtime-behavior.md
  checklists/requirements.md
```

The implementation task list belongs to the next command.
This planning phase does not create it.

### Source Code

```text
src/kentik_api/
  core/api_config.py
  core/rest_runtime.py
  v5_tools.py
  analytics/cache.py
tests/
  runtime/test_api_config.py
  runtime/test_rest_runtime.py
  runtime/test_rest_deadline.py
  runtime/test_connection_reuse.py
  runtime/test_v5_batch_wait.py
  analytics/test_cache.py
  smoke/test_client_mounts_and_calls.py
  smoke/test_helpers_no_direct_http.py
```

Keep these ownership boundaries. Add no new runtime module or class.
Extend existing tests rather than creating parallel test infrastructure.

## Phase 0: Research

Resolve timeout value ownership, absolute deadlines, dispatch-time limits,
timeout classification, and the no-op cache result. Record decisions,
rationales, source evidence, and rejected alternatives in the research
artifact. Two read-only research agents examined configuration ownership
and batch deadline propagation. Their findings are incorporated.

## Phase 1: Design

### Configuration Ownership

In [api_config.py](../../src/kentik_api/core/api_config.py), copy and
validate timeout input into private state. Return detached snapshots.
Keep scalar and per-phase meanings, validation, and read-only errors.

Add one private derivation method for an absolute REST wait deadline.
Its timeout-only copy keeps the same pool owner and quota map.
Keep this absolute deadline separate from the scalar relative limit.
Further copies retain the earlier absolute deadline. Explicit timeout
resets retain their current meaning without extending the wait deadline.

Add a private method that calculates effective phase limits and the
total deadline. Keep HTTPX timeout recognition in a private core helper.
No new public arguments, methods, or classes are needed.

### Shared REST Dispatch

In [rest_runtime.py](../../src/kentik_api/core/rest_runtime.py), prepare
the request and capture its start at the existing deadline point before
lazy client setup. Resolve the pooled client before calculating final
limits. Inside the request-error wrapping block, obtain fresh elapsed
time. Expired budgets fail before dispatch.

Choose the earlier absolute deadline from the wait and scalar client
limits. Derive the scalar instant from the original request start.
Cap every phase without relaxing a tighter limit. Pass the same absolute
deadline in the existing request extension. Do not restart it.
Calls without a wait override keep their existing behavior and start point.

### Batch Wait

In [v5_tools.py](../../src/kentik_api/v5_tools.py), validate finite,
positive timeout and interval values before any operation. Own one
absolute deadline and `last_status=None`. Use a deadline copy of
`client.v5_api_config` with the generated status operation.

Require positive budget before each poll and sleep. Save received status
before the post-call deadline test. Accept completion only before expiry.
Cap sleeps and start no poll after an exhausted sleep.

Catch only `TransportError` for possible timeout translation. Use core's
private timeout predicate and the observation-time policy. Preserve
the cause chain and non-timeout errors. Add no helper-level retries.

### Cache Refresh

In [cache.py](../../src/kentik_api/analytics/cache.py), compare the newest
cached time with the existing rounded current time. If no positive range
exists, return `None` before calling `fetch()`. Keep validation, initial
range, file format, contents, stepping, and deduplication unchanged.

### Public Documentation

Update hand-written timeout, V5, and analytics guidance when the fixes
ship. Record intentional behavior corrections in
[CHANGELOG.md](../../CHANGELOG.md). Leave generated marker blocks alone.
The contract artifact defines public behavior, not a new HTTP interface.

## Validation Strategy

Write each regression before its fix and record its failure on the
original implementation. Confirm that each test detects its own defect.
Do not weaken generated contracts or skip existing cases.

Use offline generated status operations with the real REST runtime.
Capture all four phase limits and absolute deadline extensions. Cover
preparation that consumes the budget, equality, tighter client limits,
late completion, and error classification. Helper-only mocks are not
sufficient for this request-path proof.

For timeout isolation, parameterize all phases and external mutation
values. Replace identity assertions with equal values and distinct
snapshots. Retain pool, quota, close, and credential-isolation assertions.
Cover V5 and V6 configurations built from one supplied object.

For cache refreshes, use a fixed clock and temporary Parquet files.
Assert query counts, return values, file bytes, and later readability.
Cover equal, future, and next-minute cache times.

After focused suites, run the full mocked suite, type check, lint check,
specification-reference check, and docs build. Run no live API test or
generation because neither endpoint definitions nor generated output
changes. A documentation-only planning run does not prove these fixes.

## Post-Design Constitution Check

All seven gates still pass. HTTPX-dependent policy stays in core.
Every request stays on the shared runtime. Public signatures and
dependencies remain unchanged. Generated contracts run without narrowing.
No credential redirection or new security boundary is introduced.
Timing limitations and timeout classification are explicit.

## Complexity Tracking

No exception or new abstraction is required. Private configuration state
carries the additional deadline. Existing exceptions, functions, and
test helpers cover the remaining behavior.
