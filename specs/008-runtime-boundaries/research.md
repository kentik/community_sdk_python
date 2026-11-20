# Research: Runtime Boundary Fixes

This research supports [the plan](plan.md) and [specification](spec.md).
Earlier offline probes reproduced all three failures twice.
Two read-only research agents reviewed timeout ownership and batch waits.
This document does not claim that implementation tests already pass.

## Timeout Ownership

Decision: Copy the input before validation. Store a private
`httpx.Timeout` snapshot and return a new snapshot from `rest_timeout`.

Rationale: The constructor directly stores the supplied object in
[api_config.py](../../src/kentik_api/core/api_config.py#L173).
HTTPX's copy constructor copies all four phase values. The getter must
also detach its result. Preserve the input's scalar-versus-object meaning
before copying, along with the existing assignment error and validation.

Alternatives considered: Input-only copying leaves the getter leak open.
Output-only copying leaves the input leak open. An immutable replacement
changes the public type. A timeout subclass adds unnecessary behavior.

Four identity assertions need value equality and isolation assertions:

- Constructor and derived values in
  [test_api_config.py](../../tests/runtime/test_api_config.py).
- Request forwarding in
  [test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py).
- Client construction in
  [test_client_mounts_and_calls.py](../../tests/smoke/test_client_mounts_and_calls.py).

## Absolute Wait Deadline

Decision: Attach a private absolute REST deadline to a timeout-only
configuration copy. Keep it separate from the scalar relative duration.
Use the V5 configuration as the origin, including for a gRPC client.

Rationale: Scalar overrides alone can relax tighter phases. Per-phase
overrides alone remove total deadlines. Restarting a relative budget in
the runtime loses request preparation time. One absolute instant must
remain unchanged across all polls and timeout-only copies.

Existing copies share the pool owner and quota map through
[with_timeout()](../../src/kentik_api/core/api_config.py#L192).
Use that ownership path without changing host, credentials, TLS, or gRPC.
No generated signature needs to change.

Alternatives considered: Helper-only guards leave requests unbounded.
A new public deadline argument expands the API without need. A new client
per poll loses pooling and makes resource ownership harder to preserve.

## Dispatch-Time Limits

Decision: Resolve the lazy pooled client and prepare request inputs first.
Then calculate effective limits inside the shared runtime's existing
request-error wrapping block, immediately before dispatch.

Let `S` be the request start captured at the runtime's existing deadline
point, before lazy client setup. Let `W` be the absolute wait deadline
and `R` the optional scalar client duration. Choose the earlier of `W`
and `S + R`, ignoring absent values. At dispatch, read fresh monotonic
time and cap each phase at the positive remaining duration. Preserve
each tighter phase. Calls without a wait override keep their existing
deadline start and per-phase behavior.

Pass the selected absolute deadline through the existing request
extension. If the wait budget is exhausted, raise a request-timeout error
before dispatch. Do not create a zero timeout or restart the deadline.

Rationale: [request_json()](../../src/kentik_api/core/rest_runtime.py#L251)
already owns per-request timeouts, deadline extensions, and error causes.
The final calculation must include time spent constructing the client.
No direct HTTP belongs in the batch helper.

Alternatives considered: Phase limits alone allow cumulative overrun.
Calculating once before lazy client creation loses part of the budget.
Adding a second request path violates the shared-runtime rule.

## Cooperative Timing

Decision: Keep cooperative enforcement. Reject a successful status
received at or after expiry instead of returning late success.

Rationale: The current transport checks after headers and response chunks
arrive. It cannot forcibly stop blocking work or scheduler delay at an
exact instant. The existing
[deadline test](../../tests/runtime/test_rest_deadline.py#L82)
allows this overrun. The spec records the limit explicitly.

Alternatives considered: Hard cancellation requires broader transport
changes, background execution, or a cancellation engine. Those changes
conflict with the scope. Making no late-result check leaves the defect.

## Timeout Classification

Decision: Translate a `TransportError` with an HTTPX timeout cause only
when observed at or after the wait deadline. Preserve the complete cause
chain. Earlier observed timeouts and all non-timeout errors propagate.

Rationale: The runtime retains the HTTPX exception as `__cause__`.
Native phase timeouts expose no exact expiry instant. A late timeout
cannot be attributed with certainty. Observation time is an explicit
policy, not proof of which clock expired first.

Keep HTTPX type inspection in a private core helper next to existing
HTTPX-dependent timeout handling. The batch helper must not import HTTPX
or the REST runtime. The existing
[helper boundary test](../../tests/smoke/test_helpers_no_direct_http.py)
protects this rule. Do not classify errors by message text.

Alternatives considered: Translating every transport error hides faults.
Translating only an explicit deadline marker leaves native timeouts
inconsistent with the agreed observation-time policy.

## Cache Refresh Interval

Decision: Return `None` when the newest cached time equals or exceeds
the existing rounded current time, before calling `fetch()`.

Rationale: [fetch_latest()](../../src/kentik_api/analytics/cache.py#L229)
owns this interval. No positive interval means no query, not an invalid
explicit range. Keep the existing initial range, file format, and contents.

Alternatives considered: Returning all cached data changes result meaning.
Relaxing `fetch()` or `get()` validation changes a wider contract.
Querying the previous minute again repeats work without new data.

## Validation Decisions

Decision: Extend existing test files with controlled clocks and offline
responses. Exercise the generated status operation and actual runtime,
not only a fake status method. Use temporary Parquet files for the cache.

Rationale: Helper-only mocks cannot establish final HTTP phase limits,
deadline extensions, or preserved pool ownership. Existing tests already
provide these boundaries and need no new framework.

Alternatives considered: Live tests add credentials and nondeterministic
network timing without isolating these failures. Real sleeps slow the
new regressions. Structural tests alone cannot prove behavior.

No unresolved design question remains under the delegated defaults.
Research did not change source code, dependencies, or Git history.
