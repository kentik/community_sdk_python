# Feature Specification: Runtime Boundary Fixes

**Feature Branch**: `fix/008-runtime-boundaries`

**Created**: 2026-10-19

**Status**: Draft

**Input**: Specify fixes for the three confirmed review findings: mutable
timeout state, batch waits that exceed their deadline, and repeated cache
refreshes that fail when no new time range exists.

## Background

An offline review reproduced three failures twice, with control cases:

- Changing a supplied timeout object's read value to `None` changes the
  next REST request. That request has neither a read timeout nor a total
  deadline, despite the configuration's read-only contract.
- A batch wait with a one-second limit returns success after a status
  call takes 30 simulated seconds. Polls receive no remaining time budget.
  Another poll can start when that budget is already exhausted.
- Two cache refreshes within the same minute produce equal start and end
  times. The second refresh raises `ValueError`. Reading the cached data
  and refreshing in the next minute both succeed.

The existing mocked suite passes: 3,555 passed, 149 skipped, and 487
deselected. Lint and type checks also pass. These results establish a
baseline, not proof that the three cases work.

This specification covers observable behavior, not a new class design.
The shared runtimes and generated operations remain the request path.

## Clarifications

### Planning Decisions 2026-10-19

The user delegated unresolved planning choices for later review.
These defaults keep the work within the existing synchronous transport:

- Deadlines are cooperative. The SDK caps request limits and rejects
  late results at its next execution point. It does not guarantee forced
  interruption at an exact wall-clock time.
- A request timeout observed at or after the wait deadline becomes
  `BatchWaitTimeout`, with the original error as its cause. Observation
  time is the policy, not proof of which underlying limit expired first.
- A timeout observed before the deadline, or any non-timeout request
  error, propagates unchanged. No cancellation engine is added.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Keep timeout settings stable (Priority: P1)

A caller constructs a configuration from a timeout object and reuses that
object elsewhere. Later changes to that object do not change active SDK
settings. Reading the SDK's timeout settings also gives no way to change
active settings by accident.

**Why this priority**: A shared configuration affects every REST
operation. A changed timeout can turn a bounded request into an
indefinite wait.

**Independent Test**: Change each timeout phase through the supplied
object and through a value read from the configuration. Make sure that
the next mocked REST request retains its validated settings.

**Acceptance Scenarios**:

1. **Given** a configuration constructed with four finite timeout
   values, **When** the caller changes any phase on the supplied object,
   **Then** the configuration and subsequent requests retain those values.
2. **Given** a timeout value read from a configuration, **When** the caller
   changes any phase on that value, **Then** active settings stay unchanged.
3. **Given** a timeout-only copy of a configuration, **When** the caller
   changes an exposed timeout object, **Then** neither configuration changes.
4. **Given** a timeout-only copy, **When** it makes a request, **Then** it
   uses its own timeout settings and shares the original connection pool
   and quota tracking. Its host, credentials, and TLS settings stay unchanged.
5. **Given** a configuration with a total timeout, **When** a request
   starts, **Then** the existing total-deadline behavior stays unchanged.

---

### User Story 2 - Bound the whole batch wait (Priority: P1)

A caller sets a time limit for waiting for a batch. The limit covers
status requests and the gaps between them. A batch that reports completion
at or after the deadline does not return success.

A deadline is the instant at which the wait budget expires. Remaining
budget is the positive time before that deadline.

**Why this priority**: Callers use the wait limit to bound their work.
A request that ignores it can block the caller beyond that limit.

**Independent Test**: Use a controllable clock and status responses with
known durations. Make sure that requests receive bounded timeouts and
that no request starts after the budget expires.

**Acceptance Scenarios**:

1. **Given** a pending batch with time left, **When** the helper polls,
   **Then** the request uses no more than the remaining wait budget and
   does not relax a tighter client timeout.
2. **Given** a status that reports completion before the deadline,
   **When** the helper receives it, **Then** it returns that status.
3. **Given** a one-second wait budget, **When** a status call reports
   completion at one second or later, **Then** the helper raises
   `BatchWaitTimeout` instead of returning success.
4. **Given** a pending status and a sleep that exhausts the budget,
   **When** the sleep ends, **Then** the helper raises `BatchWaitTimeout`
   without another status request.
5. **Given** a request timeout observed at or after the wait deadline,
   **When** the helper reports the failure, **Then** it raises
   `BatchWaitTimeout` with the batch ID and the last received status.
   The original request error remains the exception cause.
6. **Given** a timeout observed before the deadline or any non-timeout error,
   **When** the helper receives the error, **Then** it propagates the
   original error without retrying the request or resending the batch.
7. **Given** a non-positive or non-finite wait timeout or poll interval,
   **When** the caller starts a wait, **Then** it raises `ValueError`
   before making a request or sleeping.

---

### User Story 3 - Refresh a current cache without failure (Priority: P2)

A caller refreshes a cache more than once within the same minute.
The second refresh has no new interval to fetch and returns `None`.
The existing cached data remains available through the normal read call.

**Why this priority**: Repeated refreshes are normal in scheduled jobs
and interactive use. No new interval is not an invalid caller request.

**Independent Test**: Hold the current time fixed, refresh twice, and
count query calls. Advance the clock one minute and refresh again.

**Acceptance Scenarios**:

1. **Given** an empty cache, **When** the caller refreshes it, **Then**
   the existing initial range is fetched and returned.
2. **Given** a successful refresh, **When** the caller refreshes again
   within the same minute, **Then** it gets `None` without another query.
   Cached files stay unchanged and remain readable.
3. **Given** a cache current through the previous minute, **When** time
   advances by one minute, **Then** the helper fetches only the new range
   and returns its data.
4. **Given** a cache whose newest time is later than the current minute,
   **When** the caller refreshes it, **Then** it gets `None` without a
   reversed-range query or changes to cached files.
5. **Given** an explicit invalid range passed to `fetch()` or `get()`,
   **When** the caller requests data, **Then** the existing range
   validation remains in force.

### Edge Cases

- Each timeout phase needs isolation: connect, read, write, and pool.
  Changing a phase to `None`, zero, a negative value, or a non-finite value
  on an external object cannot change validated active settings.
- Two configurations can start from the same supplied timeout object.
  Neither gains an indirect mutation path into the other.
- A timeout-only copy can change one transport's limit without changing
  the other transport. Closing the copy does not close the shared pool.
- A status call can consume all the remaining budget before the first
  status arrives. The timeout then carries `last_status=None`.
- A late status can report completion. The deadline takes precedence,
  and that received status is available as `last_status` on the timeout.
- A client timeout observed before the wait deadline propagates unchanged.
  A timeout observed at or after the deadline raises `BatchWaitTimeout`,
  even if its underlying limit expired earlier.
- The poll interval can exceed the remaining budget. The helper sleeps
  only for the remaining budget and starts no poll afterward.
- The clock can move backward between cache refreshes. A future cached
  end time produces a no-op refresh, not deletion or refetching.
- A valid query can return no data. Existing handling of that result
  stays unchanged. It is distinct from having no interval to query.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Changing any phase on a supplied timeout object MUST NOT
  change settings that a configuration already accepted.
- **FR-002**: Changing any phase on a timeout object read from a
  configuration MUST NOT change its active settings.
- **FR-003**: Timeout-only copies MUST keep independent effective timeout
  values. They MUST preserve the existing shared connection ownership,
  quota tracking, host, credentials, and TLS settings.
- **FR-004**: The fix MUST preserve scalar total-deadline behavior,
  per-phase timeout behavior, timeout validation, and read-only assignment.
- **FR-005**: Batch waits MUST reject non-positive or non-finite timeout
  and interval values with `ValueError` before any request or sleep.
- **FR-006**: One deadline MUST govern the whole batch wait, including
  status requests, result handling, and sleeps. Enforcement is cooperative,
  not a guarantee of forced interruption during blocking operations.
- **FR-007**: A batch wait MUST start no poll or sleep without a positive
  remaining budget. A sleep MUST NOT exceed that budget.
- **FR-008**: Each status request MUST have timeout limits no greater
  than the remaining wait budget. It MUST NOT relax tighter existing
  client limits or change the client's persistent configuration.
  The remaining budget MUST bound the whole request, including when the
  client uses separate per-phase timeouts.
- **FR-009**: A batch wait MUST return a completed status only when it
  receives and accepts that status strictly before the deadline.
- **FR-010**: When the wait budget expires, the helper MUST raise
  `BatchWaitTimeout` with the batch ID and latest received status, or
  `None` if no status arrived. A request timeout observed at or after
  the deadline MUST become `BatchWaitTimeout` with the original error
  as its cause. Timeouts observed before the deadline and all non-timeout
  errors MUST propagate unchanged. Exception text MUST NOT determine
  hidden expiry times.
- **FR-011**: A batch wait MUST NOT retry failed status requests or resend
  batch parts. Successful polls for a pending batch remain permitted.
- **FR-012**: If the newest cached time equals or exceeds the current
  minute, `fetch_latest()` MUST return `None` without querying or changing
  cached files.
- **FR-013**: If a new cache interval exists, `fetch_latest()` MUST retain
  the existing initial range, fetch only the new interval, and preserve
  its data, stepping, and deduplication behavior.
- **FR-014**: The no-op refresh MUST NOT weaken explicit range validation
  in `fetch()` or `get()`, or change stored files and timestamp formats.
- **FR-015**: Public signatures, default values, supported timeout input
  types, response types, and exception attributes MUST remain unchanged.
  Timeout-object identity is not a supported contract.
- **FR-016**: All calls MUST use the existing generated operations and
  shared runtimes. The fix MUST NOT add direct HTTP, duplicate credential
  handling, change generated files, or add dependencies.
- **FR-017**: Regression tests MUST reproduce all three original failures
  before the fixes and pass afterward. They MUST use controlled time and
  offline responses, without live credentials or real sleeps.
- **FR-018**: Hand-written user documentation and release notes MUST state
  the corrected timeout and no-op behavior when the fixes ship.

### Key Entities

- **Timeout settings**: Accepted limits for connection, reading, writing,
  pool access, and the total call. Reading or supplying a mutable object
  does not grant ownership of active settings.
- **Batch wait budget**: The time available for one wait, its deadline,
  and the last received status. The budget does not extend on each poll.
- **Cache refresh interval**: The range from the newest cached time to
  the current minute. No positive range means no work and a `None` result.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Changes through supplied and returned timeout objects leave
  all four effective request-phase limits unchanged, including on copies.
- **SC-002**: No batch poll starts with an exhausted budget. Every poll
  respects the remaining budget and tighter client limits. Completion at
  or after the deadline never returns success.
- **SC-003**: Two refreshes in the same minute issue one query in total.
  The second returns `None` with unchanged files. A next-minute refresh
  queries exactly the new interval.
- **SC-004**: Deterministic regression tests detect each original failure
  and pass with its fix. Repeated runs give the same result without live
  API calls, real sleeps, or persistent debug artifacts.
- **SC-005**: The full mocked suite, lint, type, and specification-reference
  checks pass. Public signatures and generated output remain unchanged.

## Assumptions

- This feature fixes the three review findings as one bounded maintenance
  change. It does not redesign the generator or transport interfaces.
- The existing request layer can receive a shorter timeout for one call.
  This work does not introduce background threads or a cancellation engine.
- Deadline enforcement uses elapsed time, not calendar time. Tests model
  elapsed time directly and include exact deadline equality.
- No new interval means no new data result, so a no-op refresh returns
  `None`. Reading earlier data remains a separate cache operation.
- Finite, positive wait parameters define supported polling. Rejecting
  other values is part of enforcing that wait contract.
- The behavioral corrections are intentional: timeout objects cannot
  mutate active settings, late completion times out, and a current cache
  returns `None`. Callers must not depend on the old failure behavior.
- Implementation details and task ordering belong in the planning phase.
  No runtime fix or regression test is implemented by this specification.
