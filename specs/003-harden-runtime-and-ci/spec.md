# Feature Specification: Harden the Shared Runtime, Retire Dead Code, Enforce CI

**Feature Branch**: `FA-2-Update-the-python-SDK-from-V5-to-V6`

**Created**: 2026-09-21

**Status**: Draft

**Input**: User description: "Spec out the items from the 2026-09-21 stability
review: the gRPC deadline and error-handling defects, the untested gRPC path,
the CI gates that only run locally, the three confirmed dead-code items, HTTP
connection reuse, generator phase-module coverage, and an examples import
check. For gRPC specifically, also produce a hands-on REST-vs-gRPC learning
exercise (not tracked in git) and, once the learning has happened, a published
guide covering the differences, use cases, and trade-offs."

## Context

A stability review on 2026-09-21 found the project in a healthy baseline state:
`make test` green (2016 passed, 43 skipped), `make typecheck` clean, `ruff
check` clean, Sphinx building clean under `-W`, all 56 tasks across features 001
and 002 complete, and `make generate local` producing a **zero-line diff**
against committed output. Generation is already deterministic.

The remaining gaps are not broken behavior. They are unguarded behavior: real
reliability defects in the gRPC runtime, a shared runtime path with no test
coverage at all, correctness properties that hold today but nothing enforces,
and code that exists but is never reached. Investigating those defects surfaced
a further one, recorded as User Story 2: the two transports raise **different
exception types for the same failure**, so a caller's `except` clauses are not
portable across the protocol switch the client offers.

Item 7 from the review (untracked `reports/` artifacts) is already resolved by a
`reports/.gitignore` and is out of scope here.

### Resolved scoping decisions

Four questions were settled before this spec was finalized. They are recorded
here because each one changes what the requirements below demand.

1. **V6 is a clean break.** Tags `v1.0.0` through `v1.0.7` (2022-08 to 2023-05)
   are the V5 SDK. No user of that SDK is being carried forward. Backward
   compatibility with V5 exception types is therefore **not** a constraint, and
   the workarounds it would have forced are dropped.
2. **Callers must be able to override client-wide defaults per call.** A
   long-running or paginating operation legitimately needs a longer timeout than
   a cheap read. This requires a generated-output change and is scoped as its own
   story (User Story 10) so the generated diff is reviewed on its own.
3. **Error mapping is corrected properly, not patched.** Where REST and gRPC
   need different handling to raise the semantically correct exception, they get
   different handling. Forcing every gRPC failure through an HTTP status code is
   a shortcut and is abandoned (User Story 2).
4. **Rate-limit handling is evidence-led.** The investigation ran against the
   live API on 2026-09-21 and is complete for four of its five questions. Kentik
   follows the IETF `draft-polli-ratelimit-headers` scheme: 60 requests per
   60-second window, **per endpoint**, shared between REST and gRPC. The SDK
   surfaces that data; automatic retry of a completed request stays gated on the
   one open question (User Story 8).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A gRPC call never hangs forever, and its failures are diagnosable (Priority: P1)

As an SDK caller using `protocol="grpc"`, I want a call against an unresponsive
Kentik endpoint to fail within a bounded time. Today `call_grpc()` invokes the
stub with no deadline, so an unresponsive server blocks the calling thread
indefinitely. The REST path already bounds itself at 60 seconds, so the two
transports behave differently for the same failure.

**Why this priority**: This is the only defect in scope that can hang a
caller's process. It is a reliability regression relative to the REST transport
that the same client object can select, and it affects every one of the 35
mounted services.

Two secondary defects live in the same function and are fixed together, because
each one degrades the diagnosis of the failure this story is about:

- The `except Exception` fallback wraps *any* non-`RpcError` exception as
  `TransportError`. A `TypeError` from a malformed proto request (a caller bug,
  or a generator bug) is reported as a network failure, sending the reader to
  the wrong place.
- The path used to label the error, `getattr(stub_method, "_method",
  b"unknown").decode(...)`, runs *inside* the `except grpc.RpcError` handler. If
  `_method` is ever absent as bytes, that raises `AttributeError` from inside
  the handler and the original `RpcError` is lost.

**Independent Test**: Point a gRPC wrapper method at a stub that never returns
and confirm the call raises a bounded transport failure instead of blocking.
Separately, raise a non-`RpcError` from a stub and confirm the resulting error
distinguishes a caller/programming fault from a transport fault.

**Acceptance Scenarios**:

1. **Given** a gRPC stub method that does not respond, **When** a wrapper method
   calls it, **Then** the call raises rather than blocking indefinitely, and the
   raised error is part of the SDK exception hierarchy.
2. **Given** a caller who wants a different deadline, **When** they configure
   one, **Then** gRPC calls use that deadline, and the configuration mechanism
   is the same one that sets the REST timeout.
3. **Given** a gRPC stub method that raises a non-transport error, **When** a
   wrapper method calls it, **Then** the resulting error distinguishes that
   cause from a transport failure.
4. **Given** a gRPC stub whose method label cannot be read, **When** the call
   fails with an `RpcError`, **Then** the original `RpcError` is still the cause
   of the raised SDK error.
5. **Given** the deadline change, **When** `make generate local` runs, **Then**
   the diff against committed output stays empty.

---

### User Story 2 - The same failure raises the same exception type on both transports (Priority: P1)

As an SDK caller, I want my `except` clauses to keep working when I flip
`protocol` between `"rest"` and `"grpc"`. Today they do not, and the SDK's own
example says otherwise.

**The three confirmed asymmetries:**

| Failure | REST raises | gRPC raises |
| --- | --- | --- |
| Authentication rejected | `<Op>UnexpectedError` (an `HTTPException`) | `AuthenticationError` |
| Client-side timeout | `TransportError` | `HTTPException` with status `500` |
| Server unreachable | `TransportError` | `HTTPException` with status `503` |

- **Authentication.** No file under `src/kentik_api/gen/` references
  `AuthenticationError`. REST never raises it. `map_grpc_error()` does.
  `examples/common/error_handling.py` opens with *"works identically for REST and
  gRPC"* and catches `AuthenticationError` first, so that branch is dead on REST
  and the example's central claim is false.
- **Timeout and unreachability.** `httpx.TimeoutException` and
  `httpx.ConnectError` both subclass `httpx.RequestError`, which `request_json`
  catches and converts to `TransportError`. The gRPC equivalents
  (`DEADLINE_EXCEEDED`, `UNAVAILABLE`) are forced through
  `_GRPC_STATUS_TO_HTTP` into an `HTTPException`, which claims a server sent a
  status when no response was ever received. `TransportError`'s own docstring,
  *"Raised when the transport layer fails before receiving a valid response,"*
  describes these cases exactly.

**The root cause** is that `map_grpc_error()` translates every gRPC status into
an HTTP status code. That translation is lossy: some gRPC conditions have no
honest HTTP equivalent, and an HTTP status implies a response that never
arrived. The fix is to classify by *what actually happened* rather than by what
HTTP code is nearest.

**Secondary gap**: `grpc.StatusCode` defines 17 members, of which 16 are error
codes (`OK` is the success case). `_GRPC_STATUS_TO_HTTP` covers 8 of those 16.
The other 8 silently fall through to `500`, confirmed by running the exercise
in User Story 9 against this codebase: `CANCELLED`, `UNKNOWN`,
`DEADLINE_EXCEEDED`, `FAILED_PRECONDITION`, `ABORTED`, `OUT_OF_RANGE`,
`INTERNAL`, and `DATA_LOSS`. A client-side deadline is currently reported to the
user as *"the server had an internal error."*

**Why this priority**: This is the correctness foundation User Story 1 depends
on. Adding deadlines without fixing the mapping would make the *expected*
timeout path report a fabricated server error. It also invalidates a shipped
example, which makes it user-visible today, before any change in this feature.

**Independent Test**: Run the same failing operation over both transports and
assert the same exception type is raised by each.

**Acceptance Scenarios**:

1. **Given** credentials the API rejects, **When** the same operation is called
   over REST and over gRPC, **Then** both raise the same exception type.
2. **Given** a failure in which no response is received (timeout, or server
   unreachable), **When** it occurs over either transport, **Then** both raise
   `TransportError`, and neither reports a fabricated HTTP status.
3. **Given** any of the 16 non-OK gRPC status codes, **When** a stub raises it,
   **Then** the SDK maps it explicitly, and no code reaches a catch-all default.
4. **Given** a failure in which the API did return a response, **When** it occurs
   over either transport, **Then** the raised error carries the status the API
   actually reported.
5. **Given** `examples/common/error_handling.py`, **When** it is run over each
   transport, **Then** either every `except` branch it declares is reachable on
   both, or the claim that it behaves identically has been removed.
6. **Given** the error-mapping change, **When** the mocked endpoint-coverage
   suite runs, **Then** it asserts the updated expectation for every declared
   status, including any status now handled before per-operation dispatch.

---

### User Story 3 - The gRPC transport is covered by tests, not just by claims (Priority: P1)

As an SDK maintainer, I want the mocked test suite to fail when the gRPC call
path breaks. Today `call_grpc()` itself is at **0% line coverage**; only the
pure helper beside it, `map_grpc_error()`, is tested. The gRPC auth plugin's
`__call__` (the code that actually emits `x-ch-auth-email` and
`x-ch-auth-api-token` metadata) and `GrpcTransport.__init__`/`close` are also
uncovered.

**Why this priority**: The documentation states that gRPC transport is fully
implemented, and `tests/generated/test_grpc_stub_wiring.py` checks that stubs
are wired. Neither fact is the same as proving a call executes, that auth
metadata is correct, or that errors map. The defects in User Stories 1 and 2
survived precisely because nothing exercises this code.

**Independent Test**: Run the mocked suite with coverage and confirm every line
of `core/grpc_runtime.py`, `auth/credentials.py`, and
`transports/grpc_client.py` is executed. Then deliberately break the auth
metadata tuple and confirm a test fails.

**Acceptance Scenarios**:

1. **Given** the mocked test suite, **When** it runs, **Then** every line of the
   shared gRPC call path is executed, with no live network call.
2. **Given** the gRPC auth metadata keys or values are deliberately changed,
   **When** the test suite runs, **Then** at least one test fails.
3. **Given** each of the 16 non-OK gRPC status codes, **When** a stub raises it,
   **Then** a test asserts the specific SDK exception the SDK produces for it.
4. **Given** a `GrpcTransport` is constructed and closed, **When** the test
   suite runs, **Then** both are exercised without opening a real channel.

---

### User Story 4 - CI enforces the properties that currently only hold by luck (Priority: P1)

As a maintainer reviewing a pull request, I want CI to fail on anything that
would break the guarantees this project depends on. Today CI runs pytest and
`make typecheck` only. Four things pass locally with nothing protecting them:

- **Formatting**: `ruff format --check` **fails right now** on
  `scripts/generate_sdk.py`. No CI job would have caught it.
- **Generation determinism**: the single most valuable property this repo has.
  `make generate local` produces a zero-line diff today, and nothing verifies
  that a generator change preserves it.
- **Docs build**: Sphinx builds clean under `-W`, unguarded.
- **Trigger configuration**: `push.branches` in both workflows hardcodes the
  in-flight feature branch name, which becomes wrong the moment it merges.

**Why this priority**: Without this, every other fix in this feature can silently
regress. It is also the cheapest item here: the properties already hold, so
adding the gates costs nothing but wiring.

**Independent Test**: Introduce a formatting violation, a generator change that
alters output, and a broken Sphinx reference, each on its own branch, and
confirm CI fails for each.

**Acceptance Scenarios**:

1. **Given** a change that violates the formatter, **When** CI runs, **Then** it
   fails with the formatting violation named.
2. **Given** a generator change whose output differs from committed `gen/`,
   **When** CI runs, **Then** it fails and shows the differing paths.
3. **Given** a documentation change that produces a Sphinx warning, **When** CI
   runs, **Then** it fails.
4. **Given** the current formatting violation in `scripts/generate_sdk.py`,
   **When** this feature is complete, **Then** it is fixed and the formatter gate
   passes.
5. **Given** the feature branch merges, **When** CI runs on the default branch,
   **Then** the workflows trigger without needing a branch-name edit.
6. **Given** CI runs on any branch, **When** the job list is inspected, **Then**
   no end-to-end job appears, because those need real credentials and must stay
   opt-in.

---

### User Story 5 - A caller who catches `KentikError` catches every SDK error (Priority: P2)

As an SDK caller, I want one exception hierarchy to reason about. Today
`KentikAPI.__init__` raises a plain `ValueError` for missing credentials and for
an invalid region. Those are exactly the cases `ConfigurationError` was defined
for, and `ConfigurationError` is currently raised nowhere in the SDK. A caller
who writes `except KentikError:` silently misses both.

**Why this priority**: Real behavior gap for every caller, but it fails loudly
and early (at construction time), so it is less severe than a hang.

**Clean break, no compatibility shim**: because V6 does not carry V5 users
forward, `ConfigurationError` stays a plain `KentikError` subclass. No dual
inheritance from `ValueError`, and no deprecation period. A compatibility shim
here would be a permanent wart added to protect nobody.

**Independent Test**: Construct `KentikAPI` with no credentials and with a bad
region. Both must be catchable as `KentikError`.

**Acceptance Scenarios**:

1. **Given** no credentials are available, **When** `KentikAPI()` is
   constructed, **Then** the raised error is catchable as `KentikError`.
2. **Given** an unrecognized region, **When** `KentikAPI(region="xx")` is
   constructed, **Then** the raised error is catchable as `KentikError`.
3. **Given** each raised configuration error, **When** a caller reads its
   message, **Then** it names the invalid or missing value.
4. **Given** the SDK's error documentation, **When** a reader looks up
   `ConfigurationError`, **Then** it no longer describes the class as never
   raised.

---

### User Story 6 - The auth header scheme exists in exactly one place (Priority: P2)

As a maintainer, I want one definition of Kentik's auth headers.
`KentikCredentials.get_rest_headers()` builds the
`X-CH-Auth-Email`/`X-CH-Auth-API-Token` dict and is called by nothing.
`request_json()` rebuilds the same dict inline. The `auth/README.md` already
documents the method as unused. Two copies of an auth scheme is a divergence
defect waiting to be written: a future change to one copy leaves the other
stale, and the stale one is the one with no test.

**Why this priority**: No wrong behavior today. It is a latent correctness
hazard in security-relevant code, which is why it ranks above the pure coverage
items.

**Independent Test**: Grep for the header names. Exactly one definition must
exist. The REST auth tests must still pass.

**Acceptance Scenarios**:

1. **Given** the source tree, **When** the Kentik auth header names are searched
   for, **Then** exactly one place constructs them.
2. **Given** the surviving definition, **When** the test suite runs, **Then** it
   is exercised by the existing REST auth assertions.
3. **Given** `auth/README.md`, **When** a reader consults it, **Then** it
   matches the code after the change.

---

### User Story 7 - Repeat calls reuse one connection (Priority: P2)

As a caller making many REST calls, I want the SDK to reuse its HTTP connection.
`request_json()` opens and closes an `httpx.Client` per request, so every single
call pays a fresh TCP handshake plus a TLS handshake. `RestTransport.close()` is
a no-op for exactly this reason: there is nothing to close. The same change
gives the SDK a place to put a caller-configurable timeout, which User Story 1
also needs.

**Why this priority**: Correct but slow. It becomes user-visible in any
list-then-fetch-each-item loop, which is the SDK's most common usage shape.

**Constitutional constraint**: the fix MUST live in the shared runtime
(`core/rest_runtime.py`, `core/api_config.py`, `transports/rest_client.py`).
Per-endpoint connection or retry code is forbidden by Principle II.

**Independent Test**: Issue several calls through one client and assert one
underlying connection/client instance is used. Then close the client and assert
the underlying resource was released.

**Acceptance Scenarios**:

1. **Given** one `KentikAPI` instance, **When** several REST calls are made,
   **Then** they share one underlying HTTP client.
2. **Given** a caller calls `close()` (directly or via the context manager),
   **When** the call returns, **Then** the underlying HTTP resource is released.
3. **Given** a caller configures a timeout, **When** a REST call is made,
   **Then** that timeout is used instead of the built-in default.
4. **Given** the change, **When** `make generate local` runs, **Then** the diff
   against committed output stays empty, because generated call sites are
   unchanged.

---

### User Story 8 - Rate-limit information is surfaced, based on measured API behavior (Priority: P2)

As a caller, I want the SDK to tell me how much quota I have left, because the
API already sends it on every single response and the SDK currently throws it
away. As a maintainer, I want any retry policy grounded in what the API actually
does.

**The investigation is done.** It combines live measurement (2026-09-21,
read-only calls) with Kentik's published documentation at
`kb.kentik.com/docs/apis-overview#api-rate-limiting`. The hypothesis that Kentik
follows the IETF `draft-polli-ratelimit-headers` scheme is confirmed. All five
questions now have answers, and **the documentation and the measurements
disagree on one of them**.

| # | Question | Answer | Evidence |
| --- | --- | --- | --- |
| 1 | Does it return `429` / `RESOURCE_EXHAUSTED`? | **Yes.** Triggered by exceeding the per-minute hard limit or the hourly limit. | Documented |
| 2 | Does it return retry or quota information? | **Partly.** `x-ratelimit-limit`, `x-ratelimit-remaining`, `x-ratelimit-reset` on every response. **No** `Retry-After`. The headers advertise only the minute window; the hourly limit is invisible. | Measured |
| 3 | What are the limits, and at what granularity? | **Contested.** Docs say per **customer**; headers behave per **endpoint**. See below. | Both, conflicting |
| 4 | Do REST and gRPC share a budget? | **Yes**, the same budget the headers report. | Measured |
| 5 | Which operations are safe to retry? | **Answered, derived.** RFC 9110 idempotent verbs only: 161 of 233 operations are GET, PUT, or DELETE; the other 72 are POST or PATCH. See FR-032a. | Derived from the schema |

**What the documentation publishes** (framed around V5 Query vs V5 Admin APIs,
though V5 was discontinued in January 2025):

| Per-customer limit | Non-query APIs | Query API |
| --- | --- | --- |
| Maximum concurrent requests | **1** | 4 |
| Soft limit (per minute) | 20 | 30 |
| Server response delay past soft limit | 1.5s | 1s |
| Hard limit (per minute) | **60** | 100 |
| Hourly limit | 3750 | 1500 |

**What was measured against V6**: `x-ratelimit-limit: 60, 60;w=60`. The value
`60` matches the documented non-query hard limit exactly, which is strong
evidence the same regime governs V6. But the counter behaves **per endpoint**,
not per customer:

```text
Alternating transports, same endpoint  ->  59, 58, 57, 56, 55, 54   (one budget)
Two endpoints in the same service      ->  sites: 58, 57, 56
                                           site_markets: 59         (separate)
```

**Three consequences the SDK must handle**, none of which were visible before
reading the documentation:

- **Concurrency is capped at 1 for non-query APIs.** A request counts as
  concurrent if it arrives before the previous one is answered. Sharing one
  client across threads is therefore limited by the API, not by the client
  library. This must be documented, and it makes an async client (already out of
  scope) less valuable than it appears.
- **There is a soft limit with a server-side delay.** Past 20 requests per
  minute the server delays responses by 1.5s rather than failing. A caller sees
  latency, not an error, and nothing in the headers announces it. Timeout
  defaults must tolerate it.
- **The hourly limit is enforced but never advertised.** The headers carry one
  window (`w=60`). A client that trusts them exclusively will be surprised by a
  `429` from the 3750/hour budget it cannot see.

**Why this priority**: the minute-window data arrives on every response and is
discarded today. Surfacing it is small and safe. The documented limits fill in
what the headers omit.

**Implementation scope.** Three things:

- **Surface** the quota data, from REST headers and gRPC initial metadata,
  tracked per endpoint.
- **Document** the concurrency cap, the soft-limit delay, and the unadvertised
  hourly limit, since no header reveals them.
- **Connection-establishment retries** (`httpx.HTTPTransport(retries=N)`), which
  retry only a failure to open a connection and never a request that reached the
  server. Idempotency-safe by construction.

Automatic retry of a *completed* request that returned `429` stays out of scope
until question 5 has a documented answer. A naive client-wide backoff would also
be wrong given the measured per-endpoint granularity.

**Independent Test**: Make a call and read remaining quota off the result,
without reaching for raw headers. Confirm the same field is populated on both
transports, and that the value tracks the endpoint called.

**Acceptance Scenarios**:

1. **Given** any successful call, **When** a caller inspects the result, **Then**
   the current limit, remaining count, and reset window are available without
   parsing raw headers or metadata.
2. **Given** a rate-limited call, **When** it fails, **Then** the same
   information is available on the raised error.
3. **Given** the same operation over REST and over gRPC, **When** quota data is
   read, **Then** it appears in the same place with the same field names.
4. **Given** calls to two different endpoints, **When** quota is inspected,
   **Then** each endpoint reports its own budget rather than one shared counter.
5. **Given** the recorded findings, **When** a maintainer reads them, **Then**
   each answer states whether it was measured, documented, or still open, and
   the documented-versus-measured conflict on granularity is stated plainly.
6. **Given** the SDK documentation, **When** a caller reads it, **Then** it
   states the concurrency cap, the soft-limit response delay, and the hourly
   limit, none of which any response header reveals.
7. **Given** a mutating operation fails, **When** any retry logic runs, **Then**
   the SDK does not retry it.
8. **Given** the per-endpoint granularity, **When** any throttling guidance is
   documented, **Then** it does not tell callers to back off globally.

---

### User Story 9 - I can explain REST vs gRPC, and so can the next reader (Priority: P2)

As the SDK's maintainer, I want to genuinely understand what differs between the
two transports this SDK exposes, by making the same calls both ways and
observing the difference myself. Then I want to publish what I learned, so a
reader choosing `protocol="rest"` or `protocol="grpc"` can make an informed
choice instead of guessing.

**Why this priority**: The SDK offers a protocol switch with no guidance on when
to flip it. That is a real documentation gap for users. It is also the story that
makes User Stories 1 and 2 reviewable by someone who understands *why* a deadline
matters more for a long-lived gRPC channel than for a per-request HTTP call, and
why a gRPC status code does not translate cleanly to an HTTP one.

**Two artifacts, deliberately separate:**

- **The exercise** is a personal, hands-on learning artifact. It is **not
  tracked in git** and is **not** a reviewable deliverable. It lives under a
  path ignored the same way `reports/` is (a directory-local `.gitignore`
  containing `*`). It may call the real API with real credentials, which is
  another reason it must never enter the repository or CI.
- **The guide** is the tracked deliverable, written *after* the exercise, and
  derived from what the exercise actually demonstrated rather than from general
  knowledge about the two protocols.

**Independent Test**: A reader unfamiliar with gRPC reads the guide and can
state, unprompted, which transport they should use for their workload and why.

**Acceptance Scenarios**:

1. **Given** the exercise, **When** it is run, **Then** it performs the same
   logical operation over both transports and shows the observable differences
   side by side, including what each one does on failure.
2. **Given** the exercise directory, **When** `git status` is run, **Then**
   nothing from it appears as tracked or untracked content.
3. **Given** the published guide, **When** a reader consults it, **Then** it
   states the trade-offs concretely enough to choose a transport, and grounds
   each claim in this SDK's actual behavior rather than generic protocol
   commentary.
4. **Given** the guide, **When** it describes a limitation, **Then** it names
   the SDK's real constraints, including the six services with no wrapper and
   the two distinct `NotImplementedError` cases, rather than implying full
   parity.
5. **Given** the guide, **When** it describes error handling, **Then** it
   reflects the corrected, symmetric behavior from User Story 2.
6. **Given** the guide, **When** the docs build runs, **Then** it is reachable
   from the documentation navigation and builds clean under `-W`.

---

### User Story 10 - A caller can override client-wide defaults for one call (Priority: P3)

As a caller with one slow operation among many fast ones, I want to raise the
timeout for that call alone. A long-running query or a paginating read can
legitimately need minutes, while a `list_*` call should fail fast. With only a
client-wide setting, I must either set every call's timeout to the worst case or
construct a second `KentikAPI`.

**The escape hatch exists but is hidden.** The raw generated REST functions
already accept `api_config_override`. The wrapper generator strips it from the
public method signature:

```python
def list_devices(self, *, querynoCustomColumns: ... = None, view: ... = None) -> ...
```

So `client.device.list_devices()` cannot reach it, even though the plumbing
beneath it is complete.

**Why this priority**: A workaround exists (a second client), so nothing is
blocked. It is sequenced last among the runtime stories because it is the only
one that **intentionally changes generated output**, and that diff deserves to
be reviewed on its own rather than mixed into a runtime fix.

**Independent Test**: Call one operation with an overridden timeout and another
without, on the same client, and confirm each used its own value.

**Acceptance Scenarios**:

1. **Given** a mounted service method, **When** a caller inspects its signature,
   **Then** a per-call configuration override is available.
2. **Given** a caller passes an override to one call, **When** other calls run on
   the same client, **Then** they keep using the client-wide defaults.
3. **Given** a caller passes no override, **When** the call runs, **Then**
   behavior is identical to before this story.
4. **Given** the override is available, **When** a caller uses it on a gRPC call,
   **Then** it applies there too, not only on REST.
5. **Given** this story's generated diff, **When** it is committed, **Then** it
   contains only the signature change and its call-site plumbing, and
   `api_surface.json` is regenerated in the same commit.
6. **Given** the change, **When** the auto-discovering wrapper contract tests
   run, **Then** they account for the new parameter rather than being weakened to
   ignore it.

---

### User Story 11 - The generator's own phase modules are tested (Priority: P3)

As a maintainer changing the generator, I want its unit tests to catch my
mistake. Coverage of the three phase modules that write the most output is low:
`docs_rendering.py` at **18%**, `endpoint_docs.py` at **26%**, and
`wrapper_generation.py` at **54%**. Between them they produce 1198 generated
files.

**Why this priority**: The determinism gate from User Story 4 partially
compensates, because it catches any *change* in output. It cannot catch a defect
that is present in both the generator and the committed output it produced,
which is exactly the class of defect feature 002 had to fix by hand.

**Independent Test**: Measure coverage of `scripts/generation/` from
`tests/generator/` alone and confirm each module clears the agreed threshold.

**Acceptance Scenarios**:

1. **Given** the generator unit tests, **When** coverage is measured over
   `scripts/generation/`, **Then** each phase module meets or exceeds the agreed
   threshold.
2. **Given** a new generator test, **When** it runs, **Then** it uses `tmp_path`
   fixtures and needs no schema checkout and no network.
3. **Given** a deliberate defect in a covered phase module, **When**
   `make test-generator` runs, **Then** it fails.

---

### User Story 12 - Examples cannot silently rot (Priority: P3)

As a new SDK user, I want the code in `examples/` to still work. Nothing imports
or executes any example, so a regeneration that renames a wrapper method breaks
them silently. Separately, `examples/common/` is advertised in
`examples/README.md` as "Shared helpers", and neither file in it is one:
`utils.py` exposes `pretty_print`, which **zero** examples import, and
`error_handling.py` is a standalone runnable example with its own `main()` and
`__main__` block, mis-filed alongside it.

**Why this priority**: User-facing, but the damage is confusion rather than
incorrect results, and it is caught the moment anyone actually runs an example.

**Independent Test**: Run a suite that imports every example module. It must
pass without network access and must fail if a referenced wrapper method
disappears.

**Acceptance Scenarios**:

1. **Given** the mocked test suite, **When** it runs, **Then** every module under
   `examples/` is imported successfully, with no network call and no credentials.
2. **Given** an example that references a wrapper method that no longer exists,
   **When** the suite runs, **Then** it fails.
3. **Given** `examples/common/`, **When** a reader consults `examples/README.md`,
   **Then** each file listed there is described as what it actually is, and any
   helper it claims is shared is genuinely imported by at least one example.

---

### Edge Cases

- **A caller sets a timeout of zero or a negative number.** The configuration
  layer must reject it at configuration time rather than producing an immediate
  unexplained transport failure on every call. This applies to a per-call
  override as much as to the client-wide default.
- **A caller shares one `KentikAPI` across threads.** Introducing a persistent
  HTTP client changes the object's concurrency characteristics. The chosen
  behavior must be decided and documented, not left implicit.
- **A caller uses a `KentikAPI` after calling `close()`.** With a persistent
  client this now fails where it previously worked by accident, since each call
  built its own client. The resulting error must name the cause.
- **A per-call override supplies only some settings.** Whether an override
  replaces the client-wide configuration wholesale or merges into it must be
  decided explicitly. A partial override that silently resets the base URL or
  credentials would be a security-relevant surprise.
- **A gRPC status arrives that the SDK does not recognize.** Even after the map
  is made exhaustive, a future grpcio release could add a code. The fallback
  must be explicit and must not claim a status the server never sent.
- **A 401 is handled before per-operation error dispatch.** Routing
  authentication failures to `AuthenticationError` in the shared runtime means
  generated per-operation error classes never see a 401. The endpoint-coverage
  suite drives every declared status, so its expectations change with it.
- **The rate-limit investigation finds no documented limits.** Absence of
  evidence must be recorded as such, and must not be read as permission to
  retry freely.
- **The exercise directory is created outside a gitignored path.** Real
  credentials could be committed. The ignore rule must exist before the first
  exercise file does.
- **The determinism gate runs where the schema repository is absent.** CI has no
  sibling `../api-schema-public/` checkout, so the gate must obtain the schema
  the same way the generator's fallback already does.

## Requirements *(mandatory)*

### Functional Requirements

**Shared gRPC runtime**

- **FR-001**: `call_grpc()` MUST apply a bounded deadline to every gRPC call.
- **FR-002**: The gRPC deadline MUST derive from a shared configuration default,
  so the two transports cannot silently drift apart, and MUST also be
  independently overridable for callers who need a different value on gRPC than
  on REST. A single conflated value is NOT acceptable: a gRPC deadline is one
  end-to-end bound, while a REST timeout is a set of per-phase bounds, and
  collapsing them would misreport which phase failed.
- **FR-003**: `call_grpc()` MUST distinguish a transport failure from a
  non-transport exception raised by the stub, and MUST NOT report the latter as
  `TransportError`.
- **FR-004**: An `RpcError` MUST remain the `__cause__` of the raised SDK error
  even when the method label cannot be determined.
- **FR-005**: User Stories 1 and 3 MUST NOT change any generated file.

**Cross-transport error symmetry**

- **FR-006**: A given class of failure MUST raise the same SDK exception type
  regardless of whether it occurred over REST or gRPC.
- **FR-007**: An authentication failure MUST raise `AuthenticationError` on both
  transports. REST MUST raise it where it currently raises a per-operation
  `HTTPException` subclass.
- **FR-008**: A failure in which no response was received (client-side deadline
  expiry, or the server being unreachable) MUST raise `TransportError` on both
  transports, and MUST NOT be assigned a fabricated HTTP status code.
- **FR-009**: The SDK MUST handle all 16 non-OK gRPC status codes explicitly. No
  status may reach an unlabeled catch-all.
- **FR-010**: A gRPC failure in which the API did return a status MUST carry
  that status, not a nearest-neighbor approximation chosen for convenience.
- **FR-011**: REST-side changes for FR-007 MUST live in the shared runtime, per
  Principle II, so that generated per-service error packages are unchanged.
- **FR-012**: The "works identically for REST and gRPC" claim in
  `examples/common/error_handling.py` MUST be removed unless a test proves it.
  Removal is the default. The claim may only remain if FR-040's symmetry test
  covers every `except` branch the example uses, on both transports. An
  unverified claim MUST NOT survive on the grounds that it is expected to become
  true.

**Shared REST runtime**

- **FR-013**: One HTTP client instance MUST serve every REST call made through
  a single `KentikAPI`.
- **FR-014**: `RestTransport.close()` MUST release the underlying HTTP resource.
- **FR-015**: The REST timeout MUST be caller-configurable, replacing the
  hardcoded 60-second value.
- **FR-015a**: `KentikAPI` MUST accept `timeout`, `rest_timeout`, and
  `grpc_deadline` as keyword-only arguments with the same meaning and
  validation as the `APIConfig` fields, and MUST apply them to whichever
  transport it constructs. A timeout that can only be set by building a
  transport by hand is not caller-configurable in any practical sense.
- **FR-016**: The REST timeout MUST support distinct connect, read, write, and
  pool bounds, not one scalar applied to all four. A slow paginating read and an
  unreachable host are different failures, and a caller who raises the read
  bound to tolerate the former MUST NOT thereby wait minutes to discover the
  latter. A scalar MUST remain accepted as shorthand that sets all four.
- **FR-017**: A non-positive timeout MUST be rejected at configuration time with
  an SDK error that names the invalid value. This applies to every phase bound
  and to the gRPC deadline, not only to the shorthand scalar.

**Per-call configuration override**

- **FR-018**: Every mounted wrapper method MUST accept a per-call configuration
  override.
- **FR-018a**: The SDK MUST expose the client's `APIConfig` through a public
  accessor. Obtaining an override MUST NOT require reading a private attribute
  such as `client._transport.api_config`, because a documented feature reached
  only through an undocumented door is not actually supported.
- **FR-019**: The override MUST work on both transports.
- **FR-020**: Omitting the override MUST leave behavior unchanged from the
  client-wide defaults.
- **FR-021**: A per-call override MUST **replace** the client-wide
  configuration wholesale. It MUST NOT merge field-by-field, because a merging
  override that inherited credentials while the caller changed `base_path` would
  send live credentials to a host the caller never authenticated against.
- **FR-022**: `APIConfig` MUST offer a derivation helper that produces a copy
  differing only in timeout-related fields. The helper MUST accept a scalar as
  shorthand for all four REST phases and MUST also accept each phase bound and
  the gRPC deadline independently, so a caller can set a custom timeout on any
  call at the same granularity FR-016 gives the client-wide default. That
  helper MUST NOT be able to
  change `base_path`, `auth_email`, `auth_token`, or `verify`. Changing any of
  those four MUST require constructing an `APIConfig` explicitly, so that
  redirecting credentials to a different host or disabling TLS verification is
  always visible at the point it happens.
- **FR-023**: A per-call override that carries no credentials MUST fail with
  `ConfigurationError` before any request is sent, rather than issuing an
  unauthenticated request. Replacement semantics fail closed.
- **FR-024**: Tests MUST be able to supply an override without weakening
  transport security. Pointing the SDK at a mock MUST NOT require
  `verify=False`, and no test fixture may set it.
- **FR-025**: The generated diff for this change MUST be committed together with
  a regenerated `api_surface.json`, in its own commit, separate from any
  hand-written runtime change.

**Error hierarchy**

- **FR-026**: `KentikAPI.__init__` MUST raise `ConfigurationError` for missing
  credentials and for an unrecognized region.
- **FR-027**: `ConfigurationError` MUST remain a plain `KentikError` subclass.
  No compatibility base class and no deprecation shim, because V6 is a clean
  break from V5.
- **FR-028**: `KentikCredentials.get_rest_headers()` MUST either become the one
  source of the REST auth headers or be removed. The repository MUST NOT contain
  two independent definitions of the Kentik auth header scheme.

**Rate limiting**

- **FR-029**: The SDK MUST expose the current limit, remaining count, and reset
  window from `x-ratelimit-limit`, `x-ratelimit-remaining`, and
  `x-ratelimit-reset` on successful results and on raised errors, so a caller
  never has to parse raw headers or gRPC metadata.
- **FR-030**: Quota data MUST be read from REST response headers and from gRPC
  **initial** metadata, and MUST surface under the same names in the same place
  for both transports.
- **FR-031**: Quota state MUST be tracked per endpoint, because that is the
  granularity the API enforces. A single client-wide "last seen" value MUST NOT
  be the only thing offered, since it would report one endpoint's budget while a
  caller reasons about another.
- **FR-032**: The SDK MUST NOT automatically retry any request that reached the
  server within this feature. Connection-establishment retries, which never
  replay a request the server received, are permitted.
- **FR-032a**: Retry eligibility MUST be derived from the operation's HTTP
  verb, not from a hand-maintained list. Only RFC 9110 idempotent verbs are
  eligible: GET, PUT, and DELETE, which are 161 of the 233 wrapper operations.
  POST and PATCH, the remaining 72, MUST NOT be retried. This answers question 5
  in User Story 8 statically, with no probing of the live API. The rule MUST be
  recorded even though this feature implements no post-response retry, so a
  later feature does not have to re-litigate it.
- **FR-033**: The SDK MUST NOT retry a mutating operation under any
  circumstances introduced by this feature. FR-032a's verb rule is what makes
  this testable rather than aspirational.
- **FR-034**: Any throttling guidance the SDK documents MUST reflect that quota
  is per endpoint. It MUST NOT tell callers to back off globally when one
  endpoint is exhausted.
- **FR-035**: The rate-limit findings MUST be recorded in the repository, each
  answer labeled measured, documented, or open, and the conflict between the
  documented per-customer granularity and the measured per-endpoint behavior
  MUST be stated rather than silently resolved in favor of either.
- **FR-036**: The SDK documentation MUST state the three limits that no
  response header reveals: the concurrency cap of 1 for non-query APIs, the
  per-minute soft limit that triggers a 1.5-second server-side response delay,
  and the hourly limit. A caller who trusts `x-ratelimit-*` alone will be
  surprised by all three.
- **FR-037**: Default timeouts MUST tolerate the documented soft-limit response
  delay. A caller crossing the soft limit sees added latency, not an error, and
  the SDK MUST NOT convert that into a spurious `TransportError`.

**Test coverage**

- **FR-038**: The mocked suite MUST cover every line of `core/grpc_runtime.py`,
  `auth/credentials.py`, and `transports/grpc_client.py`.
- **FR-039**: A test MUST assert the exact gRPC auth metadata keys and values.
- **FR-040**: A test MUST assert cross-transport symmetry directly, by driving
  the same failure over both transports and comparing the exception type, and
  MUST assert the resulting SDK exception for each of the 16 non-OK gRPC status
  codes plus the unrecognized-code fallback.
- **FR-041**: `tests/generated/test_endpoint_schema_coverage.py` MUST be updated
  so that **every** discovered endpoint asserts the new authentication
  expectation from FR-007. Routing 401 to `AuthenticationError` in the shared
  runtime means generated per-operation error classes never see a 401, which
  changes this suite's expectation everywhere at once. The suite MUST NOT be
  narrowed, skipped, or made status-agnostic to accommodate the change:
  Constitution Principle IV requires exhaustive coverage, and weakening a suite
  to make a change pass is the precise failure mode that principle exists to
  prevent.
- **FR-042**: After the FR-007 change, deliberately reverting the shared-runtime
  401 path MUST cause `test_endpoint_schema_coverage.py` to fail. A suite that
  stays green either way has been narrowed and does not satisfy FR-041. This
  check MUST be performed and its result recorded, not assumed.
- **FR-043**: Each phase module in `scripts/generation/` MUST reach at least
  85% line coverage from `tests/generator/` alone. The six modules already at
  91% to 97% MUST NOT regress below their current figure to meet a lower bar.
- **FR-044**: A mocked test MUST import every module under `examples/`.
- **FR-045**: No new test may require network access, real credentials, or a
  schema checkout. None may run under the default `make test` if it does.

**Continuous integration**

- **FR-046**: CI MUST fail on a `ruff check` or `ruff format --check` violation.
- **FR-047**: CI MUST regenerate the SDK and fail if the result differs from
  committed output, reporting the differing paths.
- **FR-048**: CI MUST build the documentation and fail on any Sphinx warning.
- **FR-048a**: The docs gate MUST NOT be weakened by suppression.
  `suppress_warnings` in `docs/sphinx/conf.py` MUST be empty, and every warning
  it currently masks MUST be fixed at the source. Today it hides
  `myst.xref_missing` and `toc.not_included`, which are the two categories a
  broken documentation link actually produces, so the gate as specified would
  pass on exactly the defect it exists to catch.
- **FR-049**: CI workflow triggers MUST NOT hardcode a feature branch name.
- **FR-050**: CI MUST NOT run any `e2e` or `e2e_grpc` test.

**Documentation and learning artifacts**

- **FR-051**: A hands-on exercise MUST let the maintainer perform the same
  logical operation over both transports and observe the differences directly,
  including failure behavior.
- **FR-052**: The exercise MUST live under a path excluded from version control
  before any exercise file is created, and MUST NOT be referenced by any tracked
  file, test, or CI job.
- **FR-053**: A tracked guide MUST explain REST versus gRPC in this SDK:
  mechanism, when to choose each, and trade-offs.
- **FR-054**: Every claim in the guide MUST be grounded in this SDK's observed
  behavior. The guide MUST state the real coverage limits, measured rather than
  asserted: 35 services carry a wrapper, 6 carry none, and of 233 wrapper
  operations 198 have a gRPC translation while 35 are REST only. It MUST also
  name the two distinct `NotImplementedError` cases.
- **FR-055**: The guide MUST state that Kentik's REST API is an Envoy
  transcoding layer in front of the same gRPC services, evidenced by the
  `grpc-status`, `grpc-message`, and `server: envoy` headers on REST responses.
  A reader choosing a transport needs to know the two terminate in the same
  place, and that they draw on one shared 60-per-minute per-endpoint quota.
- **FR-056**: The guide MUST be reachable from the documentation navigation and
  MUST build clean under `-W`.
- **FR-056a**: The repository MUST have one documentation tree, not two. Every
  guide under `docs/guides/` MUST move inside the Sphinx source tree so that it
  is published. Today the five guides a user most needs, including the
  quickstart and both transport guides, are absent from the built site, so a
  new guide placed beside them would be equally invisible and FR-056 would be
  unsatisfiable where the plan puts it.
- **FR-057**: `auth/README.md`, `errors/README.md`,
  `docs/sphinx/guides/error_handling.md`, `docs/sphinx/guides/rest.md`,
  `docs/sphinx/guides/grpc.md`,
  and `examples/README.md` MUST be updated in lockstep with the code changes
  that make their current text wrong.
- **FR-058**: Release notes MUST call out every caller-visible behavior change:
  `ConfigurationError` replacing `ValueError`, REST now raising
  `AuthenticationError`, timeouts becoming `TransportError` on gRPC, connection
  reuse, the introduction of timeouts, and the new per-call override.

**Out of scope**

- **FR-059**: Automatic retry of requests that reached the server stays out of
  scope for this feature. FR-032a records the eligibility rule a later feature
  would implement against.
- **FR-060**: Proto-driven wrapper generation for the six wrapper-less services
  stays out of scope, per the existing decision recorded in CLAUDE.md. The guide
  documents the gap; it does not close it.
- **FR-061**: Async client support is NOT in scope.

### Key Entities

- **Shared runtime configuration (`APIConfig`)**: the one object holding base
  URL, credentials, TLS verification, and now the REST and gRPC timeouts. Every
  endpoint in every service reads it, and User Story 10 makes it overridable per
  call. It is where a cross-cutting setting belongs, per Principle II.
- **The SDK exception hierarchy**: `KentikError` and its four subclasses. This
  feature gives `ConfigurationError` real raise sites, extends
  `AuthenticationError` to the REST transport, and makes `TransportError` the
  answer on both transports whenever no response was received.
- **The gRPC status classification**: replaces `_GRPC_STATUS_TO_HTTP`'s partial
  status-code translation. Classifies all 16 non-OK codes by whether the API
  responded, rather than by nearest HTTP equivalent.
- **The rate-limit findings**: a recorded, evidence-marked answer to the five
  questions in User Story 8. It gates any future retry work.
- **The exercise workspace**: an untracked, gitignored directory holding
  throwaway comparison scripts and their captured output. Never referenced by
  tracked code.
- **The REST-vs-gRPC guide**: a tracked page under `docs/sphinx/guides/`, derived from
  the exercise, sitting alongside the existing `rest.md` and `grpc.md` rather
  than replacing them.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A gRPC call against a non-responding endpoint terminates within
  the configured deadline, instead of never terminating.
- **SC-002**: For every failure class the SDK can produce, REST and gRPC raise
  the same exception type. The count of failure classes where the two transports
  disagree goes from 3 to 0.
- **SC-003**: All 16 non-OK gRPC status codes are handled explicitly, up from 8,
  and each has a test asserting the SDK exception it produces.
- **SC-004**: Line coverage of `src/kentik_api/core/grpc_runtime.py`,
  `src/kentik_api/auth/credentials.py`, and
  `src/kentik_api/transports/grpc_client.py` reaches 100%, up from 65%, 44%, and
  50%.
- **SC-005**: A pull request that changes generator output without updating
  committed `gen/` fails CI, where today it merges clean.
- **SC-006**: A pull request with a formatting violation fails CI, where today it
  merges clean. `ruff format --check` passes on the whole repository, which it
  does not today.
- **SC-007**: `make generate local` produces a zero-line diff at the end of every
  story except User Story 10, whose generated diff is reviewed and committed
  deliberately, together with a regenerated `api_surface.json`.
- **SC-008**: `make test`, `make typecheck`, and `make docs` all stay green, and
  `make test` still needs no network and no credentials.
- **SC-009**: N REST calls through one client open one connection instead of N.
- **SC-010**: A caller can set a different timeout for one call without
  constructing a second client, which is impossible today.
- **SC-011**: Zero unreached functions remain in hand-written source. Both
  functions the review identified, `get_rest_headers` and `pretty_print`, are
  either called or gone, and dead-code detection at 60% confidence reports no
  unused function outside `src/kentik_api/gen/`.
- **SC-012**: Coverage of `docs_rendering.py`, `endpoint_docs.py`, and
  `wrapper_generation.py` each reaches the agreed threshold, up from 18%, 26%,
  and 54%.
- **SC-013**: Renaming any wrapper method referenced by an example causes a test
  failure, where today it causes none.
- **SC-014**: A caller can read remaining quota off any result or error without
  touching raw headers or gRPC metadata, where today the SDK discards it. Four
  of the five rate-limit questions carry a measured answer; the fifth is
  recorded as open.
- **SC-015**: A reader who has not used gRPC can choose a transport after
  reading the guide once, and can name at least two concrete trade-offs.
- **SC-016**: `git status` reports nothing from the exercise directory at any
  point during the feature.

## Assumptions

- The gRPC deadline default is chosen to match the REST default (60 seconds),
  so the two transports behave consistently unless a caller says otherwise.
  Changing the REST default itself is not intended.
- Routing REST 401s to `AuthenticationError` happens in `request_json` before
  per-operation error dispatch, keeping generated error packages unchanged. If
  planning finds this is not workable, the alternative is a generator change,
  which would move the work into a story of its own alongside User Story 10.
- The coverage threshold for generator phase modules is 85% per module, fixed
  in FR-043 after measuring the current figures. Six of the nine modules are
  already at 91% to 97%; the three that are not, `docs_rendering.py` at 18%,
  `endpoint_docs.py` at 26%, and `wrapper_generation.py` at 54%, are the ones
  this raises. 85% rather than 91% because part of `docs_rendering.py` is string
  templating a test would only restate.
- CI obtains the schema for the determinism gate by the generator's existing
  clone fallback. No new credential or submodule is introduced.
- The rate-limit investigation may use the opt-in e2e credentials for read-only
  probing. It must not deliberately exhaust a production quota to observe the
  limit.
- The exercise runs against a real account using the existing project-root
  `.env`, the same credentials the opt-in e2e suites use. It stays read-only,
  matching the e2e rule on non-mutating operations.
- `reports/.gitignore` already resolves review item 7. No further work there.
- The `verify` flag on `APIConfig` stays a boolean. Custom CA bundle support is
  a separate concern and is not assumed in scope.
- Only User Story 10 changes generated output. Every other story is confined to
  hand-written runtime, tests, CI, and documentation.
