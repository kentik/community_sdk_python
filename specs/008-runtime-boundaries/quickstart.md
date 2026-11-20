# Validation Guide: Runtime Boundary Fixes

Use this guide during implementation of [the plan](plan.md).
The [contract](contracts/runtime-behavior.md) defines public outcomes.
The [data model](data-model.md) defines ownership and deadline state.
This guide contains no implementation or complete test suite.

## Prerequisites

Use the `fix/008-runtime-boundaries` branch with uv, Git, and a supported
Python version. Run commands from the repository root.
The project supports Python 3.12, 3.13, and 3.14 on the existing CI matrix.
Install locked development dependencies before running checks:

```console
uv sync --locked
```

The new regressions use dummy fixtures, mocked HTTP, controlled clocks,
and temporary cache directories. They need no real Kentik credentials.
Do not inspect a credential file or run the live test tasks for this work.

## Establish Regression Evidence

Write the tests in existing files before each fix. Run the focused
commands below against the original implementation and record failures
that match all three findings. Then apply the corresponding fix and
rerun the same command. Do not use a destructive Git reset to demonstrate
the original failure.

Until the new tests and fixes exist, these commands establish only the
current baseline. Passing the old suite does not prove the new contract.
The implementation must retain evidence that each new test detects its
own defect.

## Timeout Isolation

Run the existing configuration, runtime, and ownership test files:

```console
uv run poe test-runtime -k "api_config or rest_runtime or connection_reuse"
uv run poe test-smoke -k "client_mounts_and_calls"
```

New cases must demonstrate all of the following:

- Change connect, read, write, and pool independently on supplied objects
  and returned snapshots without changing active request settings.
- Include another positive value, `None`, zero, negative values, NaN,
  and positive and negative infinity as external mutations.
- Keep originals, children, siblings, further copies, and V5 and V6
  configurations independent when built from the same input.
- Retain scalar total deadlines, per-phase semantics, the public timeout
  type, read-only assignment errors, and existing validation.
- Keep one pooled connection owner, shared quotas, and borrower close
  behavior, with no changes to host, credentials, or TLS settings.

Capture actual request extensions before and after lazy client creation.
Replace old object-identity assertions with value equality and explicit
nonidentity. Do not remove the behavior those assertions protected.

## Whole Batch Wait

Run the batch, shared deadline, and helper-boundary tests:

```console
uv run poe test-runtime -k "v5_batch_wait or rest_deadline"
uv run poe test-smoke -k "helpers_no_direct_http"
```

Use one controllable monotonic clock across the helper, configuration,
and runtime in the new regressions. Replace sleeps with clock advancement.
The existing unrelated socket tests can retain their established timing.

The required observations are:

- Complete before the deadline, exactly at it, and after it. Only the
  first case returns success.
- Exhaust the budget during a sleep. Make sure that no further poll starts.
- Use tighter scalar and unequal phase limits. Make sure that dispatch
  receives every tighter limit and the same absolute wait deadline.
- Consume the budget during client setup. Make sure that HTTP dispatch
  does not occur and the deadline is not restarted.
- Time out on the first request and after a successful pending status.
  Make sure that `last_status` is respectively `None` and that status.
- Return a late status. Make sure that it becomes the timeout's latest
  status rather than a successful result.
- Observe native timeout causes before and at or after expiry. Make sure
  that classification follows observation time and retains cause chains.
- Deliver non-timeout HTTP, authentication, parsing, and transport errors
  after expiry. Make sure that each original error propagates unchanged.
- Pass invalid timeout or interval values. Make sure that `ValueError`
  occurs before configuration access, requests, or sleeps.

Include a test through the real generated status operation and shared
REST runtime. A fake `batch_status()` alone cannot prove final limits.
Use controlled response streams to exercise cooperative deadline checks.
Do not claim hard wall-clock cancellation from a fake-clock test.

## Current Cache Refresh

Run the existing cache tests:

```console
uv run poe test-analytics -k "cache"
```

Use a fixed UTC clock and temporary Parquet files. Test these outcomes:

1. The first refresh uses the existing initial range and returns its data.
2. A second same-minute refresh returns `None` with one total query.
3. Existing file names and bytes stay unchanged and `get()` still works.
4. Advancing one minute queries exactly the missing minute.
5. A future cached end time returns `None` without a reversed query.
6. Explicit invalid ranges, stepping, and deduplication keep their behavior.

## Repository Gates

After the focused tests pass, run the required mocked and static checks:

```console
uv run poe test
uv run poe typecheck
uv run poe lint-check
uv run poe check-specs
uv run poe docs-build
git diff --check
```

All commands must exit successfully. The reference checker can report
existing warnings in completed specs 001 and 002. Do not introduce new
warnings or weaken existing tests. Run the established CI platform and
Python matrix before treating cross-platform acceptance as complete.

Make sure that generated output, schemas, dependency declarations, and
public signatures stay unchanged. Update hand-written user guidance and
release notes, not generated guide marker blocks. No regeneration or
live API run is part of this feature's validation.

## Implementation Evidence

### Baseline And US1

Executed on 2026-10-19 with Python 3.14.2 on macOS arm64.
`uv sync --locked` kept all locked dependencies unchanged.
Poe 0.49.0 lists the existing project tasks. All 16 quality checklist
items are checked. The existing ignore file covers Python caches,
the virtual environment, build output, and the credential file.

The baseline command was:

```console
uv run poe test -qqq -r f --tb=short --capture=fd
uv run poe typecheck
uv run poe lint-check
```

Results: 3,555 passed, 149 skipped, and 487 deselected. Type and lint
checks passed before any source edit.

Before the fix, this mutation regression selection failed:

```console
uv run poe test-runtime -k external_timeout_mutation -qqq -r f --tb=line --capture=fd
```

The failures expose changed accepted phase values, including `None`,
NaN, infinity, and a different finite value. Additional tests through
actual REST requests, V5/V6 clients, and pooled copies also failed on
the original code. These failures did not depend on a missing private API.

After the fix, the isolation and compatibility selection passed 205 cases.
The following broader selection passed 324 cases on each of two runs:

```console
uv run poe test -qqq -r f --tb=short --capture=fd -k 'api_config or rest_runtime or connection_reuse or rest_deadline or client_mounts_and_calls'
```

This includes the existing scalar deadline and per-phase behavior tests.
The same pool owner, quota map, close behavior, and security fields remain
in use. Existing signature and type checks pass.

### US2

Before the batch fix, the polling regressions failed on late success,
exhausted sleeps, invalid input, and late native timeout classification.
The generated-path command was:

```console
uv run poe test-runtime -k 'batch_budget_reaches or lazy_client_setup_does_not or batch_deadline_stops or batch_deadline_copies' -qqq -r f --tb=short --capture=fd
```

Result before the fix: seven failed and one passed. Captured requests
used 60-second phase limits instead of the one-second wait budget.
Late lazy setup still sent HTTP, and the controlled response stream
returned late success. The tighter scalar control case already passed.

After the fix, all 54 polling and generated-path cases passed.
The following combined acceptance selection passed 337 cases twice:

```console
uv run poe test-runtime -k 'api_config or rest_runtime or connection_reuse or rest_deadline or v5_batch_wait' -qqq -r f --tb=short --capture=fd
uv run poe test-smoke -k helpers_no_direct_http -qqq -r f --tb=short --capture=fd
uv run poe typecheck
```

All six helper import cases and the type check passed. The new tests
share one opt-in clock fixture in the existing runtime fixture module.
They use no new real sleep or external request. Actual generated status
calls retain the V5 pool and quota map. Further timeout-only copies keep
the same absolute wait deadline, even after a relative timeout reset.

### US3

The new cache regressions ran before the guard:

```console
uv run poe test-analytics -k 'fetch_latest or latest_refresh' -qqq -r f --tb=short --capture=fd
```

Result before the fix: four failed and three passed. Equal and future
cached end times raised `ValueError` from explicit range validation.
The controls for forwarding and explicit invalid ranges already passed.

After the guard, all seven new cases passed. The complete cache selection
passed 21 cases on each of two runs:

```console
uv run poe test-analytics -k cache -qqq -r f --tb=short --capture=fd
```

Assertions retain original file names and bytes, successful cached reads,
one total query for repeated same-minute refreshes, and exactly the new
interval after minute advancement. The explicit range test uses direct
typed calls to `fetch()` and `get()`. The repository type check passed.

### Final Gates And Scope

Final validation ran on Python 3.14.2, macOS arm64:

| Gate | Result |
| --- | --- |
| `uv run poe test` with concise reporting | 3,806 passed, 149 skipped, 487 deselected |
| `uv run poe typecheck` | Passed |
| `uv run poe lint-check` | Passed |
| `uv run poe check-specs` | Passed, existing warnings only |
| `uv run poe docs-build` | Passed with warnings treated as errors |
| `git diff --check` | Passed |

The full suite adds 251 passing regression cases relative to the
3,555-case baseline. Skip and deselection counts remain unchanged.
Each story's original defect failed before its fix and passed afterward.
Focused acceptance selections ran twice with the same result.

An AST comparison against `HEAD` confirms unchanged argument names,
annotations, defaults, and returns for the five affected public callables.
Only the four planned source modules changed. Generated source, schema
files, API records, generator scripts, dependency declarations, and the
lockfile are unchanged. Generated marker blocks in edited guides match
`HEAD` exactly. The final source review found no additional security or
reliability issue. All requests retain the shared runtime, credential
isolation, connection ownership, and quota tracking.

The new regressions use no real sleeps or external Kentik API calls.
No credential file was inspected. No debug instrumentation, throwaway
prototype, new dependency, commit, push, or remote action was added.
The optional implementation commit hook was not run.

Python 3.12 and 3.13, Linux, and Windows were not exercised in this run.
No CI run for this unpushed branch was started or claimed. The existing
CI matrix remains the cross-platform gate. The Sphinx output is confined
to its existing ignored build directory. No regeneration was needed.

### T029: Exact Regression Evidence

Recorded on 2026-10-21. The failure excerpts below come from the captured
2026-10-19 implementation session, before each corresponding fix.
Unrelated failures and stack frames are omitted, and terminal line
wrapping is normalized. Some full terminal buffers expired. Retained
session excerpts still contain the quoted mutation and polling failures.
The generated-request and cache failures also appear in that session's
captured output. No new pre-fix run or reconstructed source is claimed.

The passing output below comes from fresh 2026-10-21 runs on the current
implementation, with Python 3.14.2 and pytest 9.1.1 on macOS arm64.
No application or test file changed during this evidence update.

#### Timeout Isolation

The original mutation selection is recorded in the US1 section above.
Its retained output identifies this exact failing node:

```text
FAILED tests/runtime/test_api_config.py::test_external_timeout_mutation_cannot_change_accepted_settings[child-None-read] - AssertionError: assert Timeout(connect=2.0, read=None, write=5.0, pool=7.0)...
```

The `read=None` value is the external mutation that the accepted
configuration must not inherit. The ellipsis is present in the original
pytest summary, not a replacement for additional evidence.

The fresh command also selects the grandchild case because its parameter
name contains `child-None-read`:

```console
uv run poe test-runtime -k '(external_timeout_mutation and child-None-read) or (request_timeout_classification_uses_observation_time and False-1.2-ReadTimeout)' --tb=short --capture=fd
```

Observed output:

```text
PASSED tests/runtime/test_api_config.py::test_external_timeout_mutation_cannot_change_accepted_settings[child-None-read]
PASSED tests/runtime/test_api_config.py::test_external_timeout_mutation_cannot_change_accepted_settings[grandchild-None-read]
PASSED tests/runtime/test_v5_batch_wait.py::test_request_timeout_classification_uses_observation_time[False-1.2-ReadTimeout]
3 passed, 465 deselected in 0.41s
```

#### Batch Deadlines

The original polling command was:

```console
uv run poe test-runtime -k v5_batch_wait -qqq -r f --tb=line --capture=fd
```

Its retained failure summary includes exact nodes and observed outcomes:

```text
FAILED tests/runtime/test_v5_batch_wait.py::test_late_completed_status_never_returns_success[1.0] - Failed: DID NOT RAISE BatchWaitTimeout
FAILED tests/runtime/test_v5_batch_wait.py::test_late_completed_status_never_returns_success[30.0] - Failed: DID NOT RAISE BatchWaitTimeout
FAILED tests/runtime/test_v5_batch_wait.py::test_an_exhausted_sleep_cannot_start_another_poll - assert 2 == 1
FAILED tests/runtime/test_v5_batch_wait.py::test_request_timeout_classification_uses_observation_time[False-1.2-ReadTimeout] - kentik_api.errors.TransportError: fixture transport timeout
```

The generated-path selection is recorded in the US2 section above.
Its captured failure at this exact node showed four incorrect phase limits:

```text
tests/runtime/test_rest_deadline.py::test_batch_budget_reaches_real_generated_requests[60.0-first0-second0-deadlines0]
E     comparison failed. Mismatched elements: 4 / 4:
E     Max absolute difference: 59.0
```

The obtained limits were 60 seconds instead of the expected one-second
wait budget. The same capture records lazy setup and controlled-stream
cases that did not raise `BatchWaitTimeout`.

The fresh representative runtime command was:

```console
uv run poe test-runtime -k '(external_timeout_mutation and input-11.0-connect) or late_completed_status_never_returns_success or an_exhausted_sleep_cannot_start_another_poll or batch_budget_reaches_real_generated_requests' --tb=short --capture=fd
```

Observed output:

```text
PASSED tests/runtime/test_api_config.py::test_external_timeout_mutation_cannot_change_accepted_settings[input-11.0-connect]
PASSED tests/runtime/test_rest_deadline.py::test_batch_budget_reaches_real_generated_requests[60.0-first0-second0-deadlines0]
PASSED tests/runtime/test_rest_deadline.py::test_batch_budget_reaches_real_generated_requests[0.25-first1-second1-deadlines1]
PASSED tests/runtime/test_rest_deadline.py::test_batch_budget_reaches_real_generated_requests[rest_timeout2-first2-second2-deadlines2]
PASSED tests/runtime/test_v5_batch_wait.py::test_late_completed_status_never_returns_success[0.5]
PASSED tests/runtime/test_v5_batch_wait.py::test_late_completed_status_never_returns_success[1.0]
PASSED tests/runtime/test_v5_batch_wait.py::test_late_completed_status_never_returns_success[30.0]
PASSED tests/runtime/test_v5_batch_wait.py::test_an_exhausted_sleep_cannot_start_another_poll
8 passed, 460 deselected in 0.58s
```

The separate three-case command above confirms that the original late
native timeout node also passes. These results distinguish accepted
completion before the deadline from rejected completion at or after it.

#### Cache Refresh

The original cache command is recorded in the US3 section above.
Its captured output contains these exact nodes and diagnostic lines:

```text
FAILED tests/analytics/test_cache.py::test_fetch_latest_is_a_noop_until_the_next_minute
E   ValueError: Invalid arguments: start 2025-10-17 00:00:00+00:00 >= end 2025-10-17 00:00:00+00:00
FAILED tests/analytics/test_cache.py::test_fetch_latest_never_queries_a_current_or_future_range[1]
E   ValueError: Invalid arguments: start 2025-10-17 00:01:00+00:00 >= end 2025-10-17 00:00:00+00:00
```

The fresh command was:

```console
uv run poe test-analytics -k 'fetch_latest_is_a_noop_until_the_next_minute or fetch_latest_never_queries_a_current_or_future_range' --tb=short --capture=fd
```

Observed output:

```text
PASSED tests/analytics/test_cache.py::test_fetch_latest_is_a_noop_until_the_next_minute
PASSED tests/analytics/test_cache.py::test_fetch_latest_never_queries_a_current_or_future_range[0]
PASSED tests/analytics/test_cache.py::test_fetch_latest_never_queries_a_current_or_future_range[1]
PASSED tests/analytics/test_cache.py::test_fetch_latest_never_queries_a_current_or_future_range[60]
4 passed, 31 deselected in 0.97s
```

The selected runs passed 15 cases in total. These are focused evidence
runs, not a replacement for the full-suite results already recorded.

### Review Remediation: Complete Late Error Responses

Recorded on 2026-10-21. Local commit `c8408075` preserves the reviewed
implementation. The review reproduced complete late responses becoming
`BatchWaitTimeout` before HTTP or JSON error classification.
The new regression calls `wait_for_batch()` through the generated operation
and the real REST runtime. Only the base transport and clock are controlled.
It uses dummy credentials, no network, and no real sleeps.

Before the fix, run:

```console
uv run poe test-runtime -qqq -r f --tb=short --capture=fd -k received_batch_errors_keep_their_type_after_the_deadline
```

Observed result: four failed and eight passed. Each response received at
1.2 seconds against a one-second budget raised this cause chain:

```text
BatchWaitTimeout -> TransportError -> ReadTimeout
```

Exact failed nodes from the captured pytest summary, with terminal wrapping
normalized:

```text
tests/runtime/test_rest_deadline.py::test_received_batch_errors_keep_their_type_after_the_deadline[401-{"error":"fixture"}-AuthenticationError-1.2]
tests/runtime/test_rest_deadline.py::test_received_batch_errors_keep_their_type_after_the_deadline[404-{"error":"fixture"}-BatchStatusNotFoundError-1.2]
tests/runtime/test_rest_deadline.py::test_received_batch_errors_keep_their_type_after_the_deadline[500-{"error":"fixture"}-BatchStatusInternalServerErrorError-1.2]
tests/runtime/test_rest_deadline.py::test_received_batch_errors_keep_their_type_after_the_deadline[200-not-json-HTTPException-1.2]
```

The eight responses delivered at 0.5 or 1.0 seconds retained their expected
error types. After the fix, all twelve cases pass. Fully buffered responses
reach normal error classification first. Successful responses still face a
deadline check, and unfinished streams retain transport deadline checks.

The focused guard command is:

```console
uv run poe test-runtime -qqq -r f --tb=short --capture=fd -k 'received_batch or buffered_success or native_batch_timeouts or batch_deadline_stops_a_controlled_response_stream'
```

Observed result: `21 passed, 467 deselected`. These cases cover error types,
late-success rejection, scalar versus per-phase meaning, native timeout
cause chains, and interruption of an unfinished response stream.

Final checks for this remediation:

| Command | Observed Result |
| --- | --- |
| `uv run poe test -qqq -r f --tb=short --capture=fd` | 3,826 passed, 149 skipped, 487 deselected |
| `uv run poe typecheck` | Passed |
| `uv run poe lint-check` | Passed |
| `uv run poe check-specs` | Passed, existing warnings in specs 001 and 002 only |
| `uv run poe docs-build` | Passed with warnings treated as errors |
| `git diff --check` | Passed |

The fix adds 20 passing regression cases without changing skip or
deselection counts. Public signatures, generated output, dependencies,
credential handling, and request routing remain unchanged. No additional
platform or live API coverage was run. The earlier platform limits still
apply. The checkpoint commit is local, and the remediation is uncommitted.
