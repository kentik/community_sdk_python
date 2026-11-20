# Phase 1: Data Model

Feature: [003-harden-runtime-and-ci](spec.md). Design rationale in
[research.md](research.md).

This feature adds **one** new entity and modifies four existing ones. No
generated model changes.

---

## New: `RateLimit`

**Module**: `src/kentik_api/core/rate_limit.py` (new)

A frozen value object holding the quota state the API reports on every response.
Immutable, so a caller cannot corrupt the transport's view by mutating what they
read.

| Field | Type | Source | Meaning |
| --- | --- | --- | --- |
| `limit` | `int \| None` | first value of `x-ratelimit-limit` | Requests allowed in the window the caller is closest to exhausting |
| `remaining` | `int \| None` | `x-ratelimit-remaining` | Requests left in that window |
| `reset_seconds` | `int \| None` | `x-ratelimit-reset` | Seconds until the window resets |
| `window_seconds` | `int \| None` | `w=` parameter of `x-ratelimit-limit` | Length of that window |
| `raw` | `str \| None` | verbatim `x-ratelimit-limit` | Preserved so a caller can parse multiple windows the SDK does not model |

**Measured shape** (live API, 2026-09-21):
`x-ratelimit-limit: 60, 60;w=60` parses to `limit=60, window_seconds=60`.

**Construction**: two classmethods, one per transport, both returning `None`
when the headers are absent or malformed.

- `RateLimit.from_headers(headers)` for REST response headers
- `RateLimit.from_metadata(metadata)` for gRPC **initial** metadata (trailing
  metadata was measured empty)

**Validation rules**:

- A missing, empty, or unparseable header yields `None`, never an exception.
  Quota reporting must never be able to fail a call that otherwise succeeded.
- Tolerates both `w=60` (Kentik) and `window=60` (WHOOP's documented form).
- Tolerates multiple comma-separated windows, modeling the first and keeping the
  rest in `raw`.

**Scope semantics, measured**: quota is **per endpoint**, shared between REST
and gRPC. Not per account, not per service. A caller who assumes per-account
will throttle far too aggressively.

**Access, three ways** (FR-029 and FR-031):

| Access | Shape | Use |
| --- | --- | --- |
| `kentik_api.rate_limit_of(result)` | `RateLimit \| None` | Quota as of the call that produced this result |
| `error.rate_limit` | `RateLimit \| None` | Quota as of the call that failed |
| `transport.rate_limits[endpoint]` | `dict[str, RateLimit]` | Per-endpoint budget tracking |

**Attachment mechanism, tested not assumed**: `object.__setattr__(result,
"_kentik_rate_limit", value)`. Generated models set `validate_assignment=True`,
so plain assignment of an undeclared field raises `ValidationError`. The
`object.__setattr__` route was verified to leave `model_dump()` keys unchanged
and to leave `==` between two models unaffected, because Pydantic v2 compares
declared fields rather than raw `__dict__`. A module-level `rate_limit_of()`
accessor keeps the private attribute out of the public surface.

**Why per-endpoint and not one "last seen" value**: a single client-wide value
would report one endpoint's remaining count while the caller reasons about
another. Measured: `sites` ran 58, 57, 56 while `site_markets` held its own 59.

---

## Modified: `APIConfig`

**Module**: `src/kentik_api/core/api_config.py`

The one shared configuration object every generated call site receives. Gains
the timeout and the shared HTTP client.

| Field | Change | Notes |
| --- | --- | --- |
| `base_path` | unchanged | |
| `auth_email` | unchanged | |
| `auth_token` | unchanged | |
| `verify` | unchanged | Stays a `bool`; custom CA bundles are out of scope |
| `timeout` | **new**, `float = 60.0` | Shared default both transports derive from |
| `rest_timeout` | **new**, `httpx.Timeout \| float \| None` | Per-phase connect/read/write/pool bounds. `None` derives from `timeout` |
| `grpc_deadline` | **new**, `float \| None` | One end-to-end bound. `None` derives from `timeout` |
| `client` | **new**, lazy `httpx.Client` | Created on first access, reused for every call (research D2) |

**Why three fields and not one** (research D1): `httpx` models four independent
timeout phases; gRPC has a single end-to-end deadline. One scalar for both
cannot say which phase failed, and forces a caller tolerating a slow paginating
read to also wait that long to discover an unreachable host. The shared
`timeout` default still makes the REST/gRPC drift this feature fixes impossible
by construction.

**Validation**: every phase bound and the deadline must be `> 0`. A non-positive
value raises `ConfigurationError` at construction, naming the offending field
and value, rather than producing an unexplained immediate failure on every call.

**New behavior**:

- `close()` releases the underlying client if one was created.
- `with_timeout(seconds)` returns a copy with a different timeout, the
  documented way to build a per-call override without hand-copying credentials
  (research D6).

**Relationships**: `RestTransport` constructs exactly one and passes it to every
call. `RestTransport.close()` delegates to `APIConfig.close()`.

---

## Modified: the exception hierarchy

**Module**: `src/kentik_api/errors/__init__.py`

Classes are unchanged in shape. What changes is **when** they are raised and
what they carry.

```text
KentikError
├── ConfigurationError      gains real raise sites
├── AuthenticationError     gains the REST transport
├── TransportError          gains the gRPC no-response cases
└── HTTPException           gains grpc_status_code, narrows to responded faults
```

| Class | Change |
| --- | --- |
| `ConfigurationError` | Raised for missing credentials, unknown region, non-positive timeout, and use-after-close. Stays a plain `KentikError` subclass: **no** `ValueError` base (V6 is a clean break) |
| `AuthenticationError` | Now raised on REST 401 from `request_json`, not only from gRPC |
| `TransportError` | Now the answer for gRPC `DEADLINE_EXCEEDED`, `UNAVAILABLE`, and `CANCELLED`, matching what REST already does for the same conditions |
| `HTTPException` | Gains `grpc_status_code: str \| None`, so a gRPC fault keeps its verbatim code alongside the canonical HTTP equivalent |
| all of the above | Gain `rate_limit: RateLimit \| None` |

**Invariant this establishes**: for any failure class, the exception type is the
same on both transports. The three measured asymmetries go to zero.

---

## Modified: `KentikCredentials`

**Module**: `src/kentik_api/auth/credentials.py`

No field changes. `get_rest_headers()` stops being unreachable and becomes the
**single** definition of the Kentik auth header scheme, with `request_json()`
calling it instead of rebuilding the dict inline.

The repository must not contain two independent definitions of these headers.
That is the whole point of the change: the duplicate copy is the one with no
test, and auth is not where divergence should be allowed to accumulate.

---

## Modified: the gRPC status classification

**Module**: `src/kentik_api/core/grpc_runtime.py`

`_GRPC_STATUS_TO_HTTP` (8 of 16 codes, silent `500` fallback) is replaced by an
exhaustive classification. Full mapping in
[contracts/runtime-api.md](contracts/runtime-api.md).

| Bucket | Count | Raises |
| --- | --- | --- |
| No response received | 3 | `TransportError` |
| Authentication | 1 | `AuthenticationError` |
| API responded with a fault | 12 | `HTTPException` with `grpc_status_code` set |

**Unknown-code rule**: a code absent from the table (a future grpcio addition)
raises `TransportError` naming the unrecognized code. It must not silently claim
an HTTP status the server never sent.

---

## Unchanged, and deliberately so

- **All generated Pydantic models** under `src/kentik_api/gen/*/models/`. Rate
  limit data rides along on the returned instance via `object.__setattr__`,
  verified not to affect `model_dump()` or `==` (research D5a). No model class
  changes.
- **All generated per-service error packages**. Handling 401 in the shared
  runtime keeps them byte-identical (research D4).
- **`BaseTransport`** and `GrpcTransport` behavior. `GrpcTransport` gains test
  coverage, not new logic.
- **Wrapper method signatures**, until User Story 10, the feature's only
  generated-output change.
