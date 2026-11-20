# Contract: the public runtime surface that changes

Feature: [003-harden-runtime-and-ci](../spec.md). Rationale in
[research.md](../research.md), entities in [data-model.md](../data-model.md).

This is a library, so its contract is its importable API. Everything below is
caller-visible and therefore belongs in release notes (FR-058).

---

## 1. `APIConfig`

```python
class APIConfig:
    def __init__(
        self,
        base_path: str = "https://grpc.api.kentik.com",
        auth_email: str | None = None,
        auth_token: str | None = None,
        verify: bool = True,
        timeout: float = 60.0,  # NEW, shared default
        rest_timeout: httpx.Timeout | float | None = None,  # NEW, per-phase
        grpc_deadline: float | None = None,  # NEW, end-to-end
    ) -> None: ...

    @property
    def client(self) -> httpx.Client: ...  # NEW, lazy, reused

    def with_timeout(self, seconds: float) -> "APIConfig": ...  # NEW
    def close(self) -> None: ...  # NEW
```

| Guarantee | |
| --- | --- |
| `rest_timeout` / `grpc_deadline` omitted | derive from `timeout`, so the two transports cannot drift |
| `rest_timeout` supplied | honors connect, read, write, and pool bounds independently |
| a scalar for `rest_timeout` | shorthand that sets all four phases |
| any bound `<= 0` | raises `ConfigurationError` at construction, naming the field and value |
| `client` | same instance on every access until `close()` |
| `with_timeout` | returns a **copy**; the original is untouched |
| `close()` | idempotent; safe to call twice |
| use after `close()` | raises `ConfigurationError` naming `close()` as the cause |

**Why three fields**: `httpx` has four independent timeout phases, gRPC has one
end-to-end deadline. Collapsing them loses the ability to say which phase
failed, and makes "tolerate a slow read" imply "wait a long time to discover an
unreachable host."

**Breaking**: none. All three are new keyword arguments, and `timeout` defaults
to the previously hardcoded value.

### 1a. `KentikAPI` (FR-015a)

```python
class KentikAPI:
    def __init__(
        self,
        email: str | None = None,
        api_token: str | None = None,
        protocol: str = "rest",
        region: str = "us",
        *,
        timeout: float = 60.0,  # NEW
        rest_timeout: httpx.Timeout | float | None = None,  # NEW
        grpc_deadline: float | None = None,  # NEW
    ) -> None: ...
```

The client builds one `APIConfig` from these and passes it to whichever
transport it constructs, so the guarantees in section 1 apply unchanged. The
arguments are keyword-only, so no existing positional call changes meaning.

---

## 2. Exception hierarchy

```python
KentikError
├── ConfigurationError
├── AuthenticationError
├── TransportError
└── HTTPException
        status_code: int
        message: str
        method: str | None
        path: str | None
        details: dict[str, Any]
        grpc_status_code: str | None    # NEW
```

All four gain:

```python
rate_limit: RateLimit | None  # NEW
```

### What raises what, by failure class

| Failure | REST before | gRPC before | Both, after |
| --- | --- | --- | --- |
| Auth rejected | `<Op>UnexpectedError` | `AuthenticationError` | `AuthenticationError` |
| Client-side timeout | `TransportError` | `HTTPException(500)` | `TransportError` |
| Server unreachable | `TransportError` | `HTTPException(503)` | `TransportError` |
| API responded with a fault | `<Op>...Error` | `HTTPException` | unchanged per transport |
| Missing credentials | `ValueError` | `ValueError` | `ConfigurationError` |
| Unknown region | `ValueError` | `ValueError` | `ConfigurationError` |

**Breaking, and intentional** (V6 is a clean break from V5):

- `except ValueError:` around `KentikAPI(...)` no longer catches. Use
  `except ConfigurationError:` or `except KentikError:`.
- `except HTTPException:` no longer catches a REST 401. Use
  `except AuthenticationError:`, which now works on **both** transports.
- `except HTTPException:` no longer catches a gRPC timeout or unreachable host.
  Use `except TransportError:`, which matches what REST already did.

**Invariant**: `except KentikError:` catches everything the SDK raises. That is
true after this feature and was not true before.

---

## 3. gRPC status classification

Complete and exhaustive. No code reaches an unlabeled default.

| gRPC status | Raises | HTTP equivalent |
| --- | --- | --- |
| `CANCELLED` | `TransportError` | none, no response arrived |
| `DEADLINE_EXCEEDED` | `TransportError` | none, no response arrived |
| `UNAVAILABLE` | `TransportError` | none, no response arrived |
| `UNAUTHENTICATED` | `AuthenticationError` | 401 |
| `INVALID_ARGUMENT` | `HTTPException` | 400 |
| `FAILED_PRECONDITION` | `HTTPException` | 400 |
| `OUT_OF_RANGE` | `HTTPException` | 400 |
| `PERMISSION_DENIED` | `HTTPException` | 403 |
| `NOT_FOUND` | `HTTPException` | 404 |
| `ALREADY_EXISTS` | `HTTPException` | 409 |
| `ABORTED` | `HTTPException` | 409 |
| `RESOURCE_EXHAUSTED` | `HTTPException` | 429 |
| `UNKNOWN` | `HTTPException` | 500 |
| `INTERNAL` | `HTTPException` | 500 |
| `DATA_LOSS` | `HTTPException` | 500 |
| `UNIMPLEMENTED` | `HTTPException` | 501 |
| *unrecognized* | `TransportError` | none, names the code |

`HTTPException.grpc_status_code` always carries the verbatim gRPC code name, so
the canonical HTTP mapping never loses information.

The three `TransportError` codes are the ones where **no response was
received**, which is exactly what REST already produces for the same conditions
via `httpx.RequestError`.

---

## 4. `RateLimit`

```python
@dataclass(frozen=True)
class RateLimit:
    limit: int | None
    remaining: int | None
    reset_seconds: int | None
    window_seconds: int | None
    raw: str | None

    @classmethod
    def from_headers(cls, headers) -> "RateLimit | None": ...
    @classmethod
    def from_metadata(cls, metadata) -> "RateLimit | None": ...
```

**Access**:

```python
from kentik_api import rate_limit_of

result = client.device.list_devices()
rl = rate_limit_of(result)  # quota as of THIS call
print(rl.remaining, rl.reset_seconds)

client._transport.rate_limits["/device/v202504beta2/device"]  # per endpoint

try:
    client.device.list_devices()
except KentikError as exc:
    print(exc.rate_limit.reset_seconds)  # quota as of the failure
```

| Guarantee | |
| --- | --- |
| Absent or malformed headers | returns `None`, never raises |
| Header forms accepted | `60, 60;w=60` and `100;window=60` |
| `rate_limit_of(result)` | the quota reported by the call that produced that result |
| `transport.rate_limits` | keyed by endpoint, because that is the enforced granularity |
| Scope | **per endpoint**, shared by REST and gRPC (measured) |
| Transport parity | same fields, same accessors, both transports |
| Effect on `model_dump()` | none, verified |
| Effect on model `==` | none, verified |

**Attachment mechanism**: `object.__setattr__(result, "_kentik_rate_limit", rl)`.
Generated models set `validate_assignment=True`, so plain assignment of an
undeclared field raises `ValidationError`. `rate_limit_of()` is the supported
accessor; the underscore attribute is not public API.

**Measured, not assumed** (live API, 2026-09-21): 60 requests per 60-second
window, per endpoint. No `Retry-After`; `reset_seconds` serves that purpose.

### What `RateLimit` deliberately does not model

Three enforcement mechanisms exist that **no response header transmits**
(source: `kb.kentik.com/docs/apis-overview#api-rate-limiting`). `RateLimit` must
not synthesize values for them, because nothing measured them:

| Mechanism | Documented value | Visible in headers? |
| --- | --- | --- |
| Concurrency cap, non-query APIs | 1 request | No |
| Soft limit, then server delays responses | 20/min, then +1.5s | No |
| Hourly limit | 3750/hour | No, headers carry only `w=60` |

These belong in prose documentation, not in the data structure. A caller who
trusts `x-ratelimit-*` exclusively will be surprised by all three, which is why
documenting them is a requirement rather than a nicety.

**Documented granularity conflicts with measured granularity.** Kentik documents
these as **per-customer** limits; the advertised counter moves **per endpoint**.
The SDK reports what it observes and records the conflict rather than resolving
it. Filed upstream as `reports/upstream/upstream-ratelimit-scope-undocumented.html`.

---

## 5. Wrapper method signature (User Story 10 only)

```python
# before
def list_devices(
    self, *, querynoCustomColumns=None, view=None
) -> ListDevicesResponse: ...


# after
def list_devices(
    self,
    *,
    api_config_override: APIConfig | None = None,
    querynoCustomColumns=None,
    view=None,
) -> ListDevicesResponse: ...
```

| Guarantee | |
| --- | --- |
| Omitted | behavior identical to today |
| Supplied | **replaces** the client-wide config wholesale, never merges |
| Supplied without credentials | raises `ConfigurationError` before any request is sent |
| Transports | applies to gRPC (as the call deadline) as well as REST |

### Why replace, and why the helper is restricted

**Replace fails closed; merge fails open.**

| Risk | Under merge | Under replace |
| --- | --- | --- |
| Override changes only `base_path` | Inherits live credentials, sending them to a host the caller never authenticated against | No credentials, call fails closed |
| Override sets `verify=False` once | Propagates wherever the merged config reaches | Confined to that one call |
| Reviewing a call site | Cannot tell which credentials or host apply without tracing the base config | The override is the complete answer |

The derivation helper is deliberately narrow, because a general one would be
merge semantics under another name:

```python
config.with_timeout(300)  # allowed
config.with_timeout(300, base_path="...")  # does not exist
```

`base_path`, `auth_email`, `auth_token`, and `verify` can only be set by
constructing an `APIConfig` explicitly. Redirecting credentials to another host,
or disabling TLS verification, is therefore always visible at the point it
happens.

```python
slow = client.api_config.with_timeout(300)  # public accessor, FR-018a
client.query.data(api_config_override=slow, data=big_query)
```

### Testing under these rules

Checked rather than assumed, since a security rule that blocks testing gets
deleted:

| Test need | How | Needs `verify=False`? |
| --- | --- | --- |
| Mocked HTTP | `respx` intercepts at the httpx transport layer; `base_path` unchanged | No |
| Timeout behavior | `with_timeout()` | No |
| A genuinely different host | construct `APIConfig` explicitly with dummy credentials | No |

No fixture may set `verify=False`.

**Breaking**: none. New keyword-only argument with a default.

**Generated-output impact**: this is the feature's only change under
`src/kentik_api/gen/`. Committed on its own, with a regenerated
`api_surface.json`.

---

## 6. `KentikCredentials`

No signature change. `get_rest_headers()` goes from unreachable to being the
single source `request_json()` calls. The repository must not hold two
definitions of the Kentik auth header scheme.

---

## Contract test mapping

| Contract | Test |
| --- | --- |
| 1 | `tests/runtime/test_rest_runtime.py` (reuse, timeout validation, close) |
| 2 | `tests/runtime/test_transport_symmetry.py` (same failure, both transports) |
| 3 | `tests/runtime/test_grpc_runtime.py` (all 16 codes plus unrecognized) |
| 4 | `tests/runtime/test_rate_limit.py` (parsing, both sources, malformed input) |
| 5 | `tests/generated/test_wrapper_contracts.py` (auto-discovered, all methods) |
| 6 | `tests/runtime/test_rest_runtime.py` (auth header assertions) |

Every one is mocked. No network, no credentials, no schema checkout.
