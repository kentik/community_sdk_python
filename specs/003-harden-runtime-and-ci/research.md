# Phase 0: Research and Design Decisions

Feature: [003-harden-runtime-and-ci](spec.md). Every decision below was checked
against the real code or the live API rather than assumed. Where an option was
rejected, the reason is recorded so it does not get re-litigated.

No `NEEDS CLARIFICATION` items remain.

---

## D1. How timeouts are modeled

**Decision**: `APIConfig(timeout=60.0)` sets one shared default. Two optional
fields refine it without letting the transports drift:

```python
APIConfig(
    timeout=60.0,  # shared default, both transports
    rest_timeout=None,  # httpx.Timeout | float | None
    grpc_deadline=None,  # float | None
)
```

When a refinement is `None` it derives from `timeout`, so the common case has a
single source of truth. Supplying one is explicit and visible at the call site.

**Rationale**: a REST timeout and a gRPC deadline are not the same concept, and
an earlier draft of this plan wrongly collapsed them into one scalar.

- `httpx` models **four independent phases**: connect, read, write, pool. They
  fail for different reasons and want different bounds.
- gRPC has **one end-to-end deadline** covering the whole call.

Collapsing them means a caller who raises the bound to tolerate a slow
paginating read also waits that long to discover an unreachable host, and the
resulting error cannot say which phase failed. That is the same defect class as
the gRPC status mapping in D3: discarding information the transport actually
has.

**Why a shared default anyway**: the defect being fixed is REST bounded at 60s
while gRPC was unbounded. Deriving both from one default makes that specific
drift impossible by construction, while keeping per-transport precision
available.

**Validation**: every phase bound and the deadline must be `> 0`, checked at
construction, naming the offending field and value (FR-017).

**Verified**: the wrapper always passes
`api_config_override=rest_transport.api_config`, so one long-lived `APIConfig`
per `KentikAPI` already serves every call.

**Alternatives rejected**:

- *One scalar for both* (the earlier draft): loses phase granularity and
  misreports which phase failed.
- *Two independent fields with no shared default*: reintroduces the exact drift
  being fixed.
- *A per-call `timeout=` kwarg on every wrapper method*: changes all 1198
  generated files. D6 achieves the same outcome through the parameter the
  generated functions already accept.

---

## D1a. How the deadline reaches a gRPC call without touching generated code

**Decision**: apply the deadline with a `grpc.UnaryUnaryClientInterceptor`
installed on the channel in `GrpcTransport.__init__`, via
`grpc.intercept_channel`. The interceptor fills in `timeout` only when the call
did not set one.

**The problem it solves**: generated wrappers call `call_grpc(stub_method,
proto_request)`. There is no parameter through which a deadline could arrive,
and adding one would change all 198 gRPC call sites, breaking FR-005 (User
Story 1 must not change any generated file). This tension surfaced while writing
tasks, not while writing the plan.

**Why the interceptor works**: every stub in a wrapper is constructed from
`self._transport.channel`. If that channel is already intercepted, every stub
inherits the deadline with no call-site change at all. The transport owns the
`APIConfig`, so the deadline is per-client, not global.

**Verified**, against a local black-hole socket that accepts connections and
never replies:

```text
WITHOUT interceptor:  still blocked after 3s
WITH interceptor:     DEADLINE_EXCEEDED after 2.0s
```

**Alternatives rejected**:

- *Add a parameter to `call_grpc`*: changes 198 generated call sites in the
  story that FR-005 says must change none. This becomes available anyway in
  User Story 10, where a generated diff is expected and reviewed.
- *Module-level default deadline*: global mutable state, wrong the moment two
  `KentikAPI` instances want different timeouts.
- *Construct a default `APIConfig()` inside `call_grpc`*: ignores whatever the
  caller configured, which defeats FR-002.

**Interaction with User Story 10**: the interceptor only fills a deadline when
the call did not specify one, so a per-call override set later takes precedence
without any further change here.

---

## D2. Where the persistent HTTP client lives

**Decision**: `APIConfig` lazily creates and owns one `httpx.Client`.
`RestTransport.close()` closes it. `request_json()` uses
`api_config.client` instead of constructing its own.

**Rationale**: `RestTransport` builds exactly one `APIConfig` in `__init__` and
every wrapper call passes that same instance, so an object stored on it is
naturally client-scoped. Putting the client on `RestTransport` instead would
leave `request_json`'s `APIConfig()` fallback path unable to reach it.

**Known limitation, accepted and documented**: a caller invoking a raw generated
REST function directly, with no `api_config_override`, still gets a fresh
`APIConfig` and therefore a fresh client per call. That path is not the SDK's
public surface (the mounted wrappers are), and closing that hole would mean
module-level global state, which is worse.

**Concurrency**: `httpx.Client` is thread-safe for concurrent requests, so
sharing one across threads is sound *on the client side*. The **API** is the
binding constraint: Kentik documents a maximum of **1 concurrent request** for
non-query APIs, where a request counts as concurrent if it arrives before the
previous one is answered. Concurrency is therefore capped by the service, not
the library. This must be documented (FR-036), and it is a further reason async
support (FR-061) buys less than it appears to.

**Use after close**: httpx raises on a closed client. The runtime wraps that in
`ConfigurationError` naming `close()` as the cause, rather than letting a raw
httpx error escape.

---

## D2a. Timeout defaults must absorb the documented soft-limit delay

**Decision**: keep the 60-second default rather than tightening it, and document
why.

**Rationale**: Kentik applies a **server-side response delay** past the
per-minute soft limit: 1.5s for non-query APIs, 1s for the query API, beginning
at 20 and 30 requests per minute respectively. A caller crossing the soft limit
sees *added latency, not an error*, and no response header announces it.

A timeout tuned aggressively on the assumption that a healthy call returns in
under a second would convert normal throttling into a spurious
`TransportError`, which is exactly the misdiagnosis this feature exists to
eliminate. FR-037 records the constraint.

**Observed baseline**: `x-envoy-upstream-service-time` of 534 to 642ms on
unthrottled `ListDevices` calls, so a throttled call lands near 2 seconds. The
default has ample headroom; the point is to not remove it later without knowing
this.

---

## D3. Classifying gRPC failures instead of translating them to HTTP

**Decision**: replace the partial `_GRPC_STATUS_TO_HTTP` translation with an
explicit classification of all 16 non-OK codes into three buckets:

| Bucket | Codes | Raises |
| --- | --- | --- |
| No response received | `DEADLINE_EXCEEDED`, `UNAVAILABLE`, `CANCELLED` | `TransportError` |
| Authentication | `UNAUTHENTICATED` | `AuthenticationError` |
| API responded with a fault | the remaining 12 | `HTTPException` |

**Rationale**: an HTTP status code asserts that a server sent a response. For a
client-side deadline or an unreachable host, none arrived, so any status is
fabricated. `TransportError`'s own docstring, *"Raised when the transport layer
fails before receiving a valid response,"* describes these exactly, and it is
already what REST produces for the identical conditions (verified:
`httpx.TimeoutException` and `httpx.ConnectError` both subclass
`httpx.RequestError`, which `request_json` converts).

**Measured gap this closes**: `_GRPC_STATUS_TO_HTTP` covers 8 of 16. The other 8
fall through to `500`, confirmed by running `learn/ex04_errors.py`:
`CANCELLED`, `UNKNOWN`, `DEADLINE_EXCEEDED`, `FAILED_PRECONDITION`, `ABORTED`,
`OUT_OF_RANGE`, `INTERNAL`, `DATA_LOSS`. A client-side deadline currently
reports itself as *"the server had an internal error."*

**Resolving an ambiguity in FR-010.** FR-010 forbids a "nearest-neighbor
approximation chosen for convenience," which could be read as forbidding any
HTTP status on a gRPC error. The resolution: for the 12 responded-fault codes
the SDK keeps the canonical `google.rpc.Code` to HTTP mapping (a published
standard, not a convenience choice) **and** additionally exposes the verbatim
gRPC code on the error, so nothing is lost. Nothing is invented for the codes
where no response arrived, because those no longer produce an `HTTPException`
at all.

**`CANCELLED` note**: normally client-initiated. It is grouped with "no
response received" because that is factually what happened. Flagged here so the
choice is visible rather than buried.

---

## D4. Making REST raise `AuthenticationError`

**Decision**: handle `401` in `request_json()` **before** dispatching to the
generated `error_cls`, raising `AuthenticationError`.

**Rationale**: Principle II puts shared behavior in the runtime, and this keeps
every generated per-service error package byte-identical, preserving the
zero-diff property. The alternative, teaching `error_package.py` to emit
auth-aware classes, would change output across all 35 services for a rule that
is not service-specific.

**Measured problem**: no file under `src/kentik_api/gen/` references
`AuthenticationError`. Confirmed live, a rejected credential produces:

```text
rest  raised ListDevicesUnexpectedError status_code=401
grpc  raised AuthenticationError
```

**Consequence, tracked as Constitution gate IV**:
`test_endpoint_schema_coverage.py` drives every declared status through the real
runtime. Its 401 expectation changes for every discovered endpoint. The suite
must be updated to assert the new behavior exhaustively, not narrowed to dodge
it.

**Contingency**: if `403` turns out to warrant the same treatment, it is a
one-line addition at the same place. Not assumed in scope without evidence.

---

## D5. Surfacing rate-limit data

**Decision**: a frozen `RateLimit` value object in a new `core/rate_limit.py`,
captured from REST response headers and gRPC **initial** metadata, exposed as
`transport.rate_limit` (most recent call) and as `error.rate_limit` on raised
SDK errors.

**Rationale, from measurements taken 2026-09-21 against the live API**: the
data already arrives on every single response and the SDK discards it.

```text
x-ratelimit-limit:     60, 60;w=60
x-ratelimit-remaining: 59
x-ratelimit-reset:     40
retry-after:           ABSENT
```

**Why not on the returned model**: wrapper methods return Pydantic models
generated from the schema. Adding a field means changing generated models, which
breaks the zero-diff constraint for a concern the schema does not describe. A
client-scoped attribute is the only option that keeps generated output untouched.

**Honest deviation from FR-029's wording**: the spec says a caller inspects "the
result." In practice they inspect `client.<service>.rate_limit` (or the
transport) immediately after the call, and `error.rate_limit` on failure. The
requirement's intent, no raw header parsing, is met. Recorded here so the gap
between wording and mechanism is deliberate, not overlooked.

**Semantics to document**: "most recent call on this transport." Under
concurrent use the value reflects whichever call completed last. Stated
explicitly rather than implied.

**SUPERSEDED.** Both claims above were wrong, and were corrected by testing
rather than reasoning. See D5a.

---

## D5a. Rate-limit data, corrected by measurement

**Decision**: expose `RateLimit` three ways.

1. **On the returned result**, via `kentik_api.rate_limit_of(result)`
2. **On any raised SDK error**, as `error.rate_limit`
3. **Per endpoint** on the transport, as `transport.rate_limits[endpoint]`

### Attaching to the result is feasible

D5 asserted it was impossible without changing generated models. Tested against
a real generated model:

| Mechanism | Result |
| --- | --- |
| `result.rate_limit = x` | **Fails.** Generated models set `validate_assignment=True`, so an undeclared field raises `ValidationError` |
| `object.__setattr__(result, "_kentik_rate_limit", x)` | **Works** |
| Leaks into `model_dump()`? | **No.** Keys stay `['devices', 'invalidCount']` |
| Breaks `==` between two models? | **No.** Pydantic v2 compares declared fields, not raw `__dict__`. Verified `a == b` still `True` after attaching |
| `weakref.WeakKeyDictionary` side table | **Fails.** Models are unhashable |

The value rides along on the instance, generated models stay untouched, and the
zero-diff property holds. A module-level `rate_limit_of(result)` accessor keeps
the private attribute an implementation detail rather than public surface.

### A single "last seen" value is the wrong model

D5 also proposed one client-wide `transport.rate_limit`. Quota is enforced **per
endpoint** (measured: two endpoints in one service hold separate budgets), so a
lone value would report one endpoint's remaining count while the caller reasons
about another. `transport.rate_limits` is a mapping keyed by endpoint. FR-031
requires this.

### Lesson

Both errors came from reasoning about the framework instead of running it. The
probe that settled the question took five lines and less time than the paragraph
written to justify the workaround.

---

## D5b. What the headers do not tell you

**Source**: `kb.kentik.com/docs/apis-overview#api-rate-limiting`, read
2026-09-21. Consulted *after* the measurements, which is why D5 and D5a were
built on headers alone.

**Published limits**, framed around V5 Query vs V5 Admin APIs even though V5 was
discontinued in January 2025:

| Per-customer limit | Non-query | Query |
| --- | --- | --- |
| Maximum concurrent requests | **1** | 4 |
| Soft limit per minute | 20 | 30 |
| Response delay past soft limit | 1.5s | 1s |
| Hard limit per minute | **60** | 100 |
| Hourly limit | 3750 | 1500 |

The documented non-query hard limit of **60** matches the measured
`x-ratelimit-limit: 60, 60;w=60` exactly, which is strong evidence the same
regime governs V6.

**Three enforcement mechanisms exist that no response header reveals:**

1. **Concurrency cap of 1** for non-query APIs. Nothing in any header hints at
   it. See D2.
2. **A soft limit with a server-side delay.** Past 20 requests per minute the
   server slows responses by 1.5s instead of failing. The caller sees latency,
   not an error. See D2a.
3. **An hourly limit of 3750.** The headers advertise one window (`w=60`). A
   client trusting them exclusively gets a `429` from a budget it could not see.

**Unresolved conflict, deliberately left unresolved**: the documentation says
these are **per-customer** limits. Measurement says the advertised counter moves
**per endpoint**. Both cannot be describing the same thing. Possibilities
include an Envoy per-route counter layered under a per-customer one, or
documentation that predates the V6 gateway. The SDK reports what it observes and
records the conflict (FR-035), rather than picking a side. Resolving it is an
upstream question, filed as
`reports/upstream/upstream-ratelimit-scope-undocumented.html`.

**Consequence for the design**: `RateLimit` models the minute window the headers
actually carry. It MUST NOT synthesize an hourly figure, because nothing
transmits one. The hourly limit, the concurrency cap, and the soft-limit delay
belong in documentation (FR-036), not in a data structure pretending to have
measured them.

**Parsing**: `x-ratelimit-limit` uses the IETF `draft-polli-ratelimit-headers`
form `60, 60;w=60` (note `w=`, where WHOOP's documentation uses `window=`). The
parser must tolerate both, multiple windows, and a missing or malformed header
by yielding `None` rather than raising. Rate-limit metadata must never be able
to fail a call.

---

## D6. Restoring the per-call override

**Decision**: stop stripping `api_config_override` from wrapper signatures in
`wrapper_generation.py`, and thread an `APIConfig` through `call_grpc` so the
override reaches the gRPC deadline too.

**Verified**: the plumbing already exists and is complete on the REST side. The
generated raw function is
`def ListDevices(api_config_override: Optional[APIConfig] = None, *, ...)`, and
the wrapper already passes `api_config_override=rest_transport.api_config`. Only
the public signature hides it.

**Merge vs. replace** (FR-021 demands an explicit answer): **replace**, and the
supporting helper is deliberately restricted.

### Why replace

An override is a complete `APIConfig`. The decisive argument is security, and it
comes down to which way each option fails.

| Risk | Under merge | Under replace |
| --- | --- | --- |
| Caller overrides only `base_path` | Silently inherits live `auth_email` and `auth_token`, sending real credentials to a host they never authenticated against | No credentials, so the call fails closed |
| Caller sets `verify=False` for one local test | Propagates anywhere the merged config reaches | Confined to the single call that named it |
| Reviewing a call site | Cannot tell which credentials or host are in effect without tracing the base config and the merge rule | The override is the complete answer |

**Replace fails closed; merge fails open.** That asymmetry decides it.

### The helper is restricted, because a naive one reintroduces the risk

`with_timeout()` copies the existing config, which means it also copies
credentials. If it could also change `base_path`, it would be merge semantics
wearing a different name, with the identical credential-leak path. So:

```python
config.with_timeout(300)  # allowed
config.with_timeout(300, base_path="...")  # does not exist
```

The helper can only vary timeout-related fields (FR-022). Changing `base_path`,
`auth_email`, `auth_token`, or `verify` requires constructing an `APIConfig`
explicitly, so redirecting credentials to another host or disabling TLS
verification is always visible at the point it happens rather than inherited
from three frames away.

### Testing stays possible without weakening anything

This was checked rather than assumed, because a security rule that blocks
testing gets deleted.

- **Mocked layers** use `respx`, which intercepts at the httpx transport layer.
  `base_path` and `verify` never change, so no override is needed at all.
- **Timeout tests** use `with_timeout()`, which is exactly what it is for.
- **Tests that genuinely need a different host** construct an `APIConfig`
  explicitly with dummy credentials. One extra line, and the credentials in use
  are visible in the test.
- **`verify=False` is never required** for any of the above, and FR-024 forbids
  a fixture from setting it.

**Why sequenced last**: this is the only generated-output change in the feature.
Committed alone, with a regenerated `api_surface.json`, so its diff is
reviewable on its own terms.

---

## D7. How CI gets a schema for the determinism gate

**Decision**: rely on the generator's existing clone fallback. CI has no sibling
`../api-schema-public/`, so `make generate` (without `local`) clones the public
repository.

**Rationale**: no new credential, submodule, or cache. The fallback is already
exercised code.

**Gate shape**: `make generate` then `git diff --exit-code`, printing the
differing paths on failure.

**Accepted trade-off**: the gate pins against schema `HEAD`, so an upstream
schema change can fail an unrelated pull request. That is arguably a feature,
since it surfaces drift early, but it must be recognizable. The job name and
failure output should make "upstream schema moved" distinguishable from "your
generator change altered output."

---

## D8. Rejected outright

- **Automatic retry of completed requests.** Gated on User Story 8 question 5.
  A retried `Create*` that the server already committed duplicates a real
  resource. Connection-establishment retries
  (`httpx.HTTPTransport(retries=N)`) are permitted because they never replay a
  request the server received.
- **Global backoff on `429`.** Measured: quota is **per endpoint**
  (`sites` ran 58, 57, 56 while `site_markets` held its own 59). Throttling
  everything because one endpoint is exhausted would waste 59 other budgets.
- **Compatibility shim on `ConfigurationError`.** V6 is a clean break; a
  `ValueError` base would be a permanent wart protecting nobody.
- **Async client support.** FR-061, out of scope.
- **Proto-driven wrappers for the six wrapper-less services.** FR-060,
  unchanged upstream schema gap.

---

## Supporting evidence

| Claim | How it was established |
| --- | --- |
| Generation is deterministic today | `make generate local` then `git diff`, zero lines |
| `ruff format --check` fails now | `scripts/generate_sdk.py`, one hunk |
| `call_grpc` has 0% coverage | pytest-cov over the full suite |
| REST never raises `AuthenticationError` | no match under `src/kentik_api/gen/` |
| 8 of 16 gRPC codes unmapped | `learn/ex04_errors.py` |
| gRPC blocks forever without a deadline | `learn/ex06_timeouts.py`, local black-hole socket |
| 198/233 operations speak gRPC | `learn/ex05_coverage.py`, AST scan |
| Quota is 60/60s per endpoint | `learn/ex07_rate_limits.py` plus two interleaving probes |
| REST and gRPC share one budget | alternating calls: 59, 58, 57, 56, 55, 54 |
| REST is Envoy transcoding over gRPC | `grpc-status`, `grpc-message`, `server: envoy` on REST responses |
| Documented limits, concurrency cap, soft-limit delay, hourly limit | `kb.kentik.com/docs/apis-overview#api-rate-limiting` |
| Generated models accept attached metadata | probe against `ListDevicesResponse`: `model_dump()` and `==` both unaffected |
