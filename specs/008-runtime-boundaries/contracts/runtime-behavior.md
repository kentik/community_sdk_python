# Runtime Behavior Contract

This contract refines existing library behavior from
[the specification](../spec.md). It adds no HTTP operation, public method,
argument, response model, exception class, or dependency.

## Timeout Configuration

The public entry points remain `APIConfig(...)`, `rest_timeout`, and
`with_timeout(...)`, defined in
[api_config.py](../../../src/kentik_api/core/api_config.py).
Constructor and method parameter names, defaults, and types stay unchanged.

The following values keep their meanings:

| Input Or Read | Contract |
| --- | --- |
| Omitted REST timeout | Derive phase limits and total duration from `timeout` |
| Scalar REST timeout | Apply that total duration and corresponding phases |
| `httpx.Timeout` input | Keep its four finite phase limits, without a total duration |
| `rest_timeout` read | Return an equal, independent `httpx.Timeout` snapshot |
| Scalar `with_timeout()` | Reset both transport limits as before |
| REST-only refinement | Keep the gRPC limit and other configuration unchanged |
| gRPC-only refinement | Keep REST phase values and deadline meaning unchanged |

Changing supplied or returned timeout objects cannot change active
settings. This applies to the original, children, siblings, and further
copies. Tests must cover connect, read, write, and pool separately.
Object identity is not a supported contract.

Invalid constructor or refinement values retain their existing
`ConfigurationError`. Assigning a read-only public setting retains the
existing `AttributeError`. Connection and quota identity remain shared.
Host, credentials, TLS verification, and close ownership stay unchanged.

## Batch Wait Interface

The existing interface in
[v5_tools.py](../../../src/kentik_api/v5_tools.py) stays unchanged:

```python
def wait_for_batch(
    client: KentikAPI,
    guid: str,
    *,
    timeout: float = 600.0,
    interval: float = 5.0,
) -> BatchStatus: ...
```

The helper accepts only finite, positive timeout and interval values.
Other values raise `ValueError` before a request or sleep. This applies
to zero, negative values, NaN, and positive or negative infinity.

One absolute monotonic deadline covers the wait. Every status request
uses a per-call override derived from `client.v5_api_config`.
That override keeps the same host, credentials, pool, and quota map.
No persistent configuration changes.

The final request limits must preserve all tighter client limits.
The same absolute wait deadline reaches the shared runtime's request
extension. Time spent in lazy client setup cannot restart the budget.
If setup exhausts the budget, HTTP dispatch never occurs.

The public outcomes are:

| Observation | Outcome |
| --- | --- |
| Completion accepted before deadline | Return that `BatchStatus` |
| Status received at or after deadline | Raise `BatchWaitTimeout`, retain that status |
| Sleep exhausts the budget | Raise `BatchWaitTimeout`, no further poll |
| Request timeout observed at expiry | Raise `BatchWaitTimeout` from the request error |
| Request timeout observed earlier | Propagate the original error |
| Non-timeout error at any time | Propagate the original error |

Every `BatchWaitTimeout` retains its existing `guid` and `last_status`
attributes. `last_status` is `None` if no status arrived.
When translating a timeout, preserve the complete cause chain.
A native timeout delivered late follows observation time even when its
true underlying expiry order is unknown.

There is no helper-level retry after a failed status call and no resend
of batch parts. Existing transport connection-attempt retries remain
unchanged. A successful pending status can lead to another poll only
while positive budget remains.

The deadline is cooperative. The transport does not promise forced
cancellation of blocking operations, parsing, cleanup, or scheduler delay.
It must not accept a late successful status as completion.

## Cache Refresh Interface

The existing interface in
[cache.py](../../../src/kentik_api/analytics/cache.py) stays unchanged:

```python
def fetch_latest(
    self,
    query_fn: MappedQueryFn,
    step: timedelta | None = None,
    dedup_columns: list[str] | None = None,
    **kwargs: Any,
) -> pd.DataFrame | None: ...
```

If the newest cached timestamp equals or exceeds the rounded current
UTC time, return `None`. Do not query, sleep, rewrite, remove, or create
cache files. Existing cached data remains readable through `get()`.

An empty cache retains its existing initial range. A later refresh
queries only the new range. Existing stepping, deduplication, query
keyword forwarding, Parquet encoding, and timestamp naming stay unchanged.
Explicit invalid ranges in `fetch()` and `get()` retain their errors.

## Compatibility And Evidence

The intentional corrections are detached timeout state, rejected late
batch completion, invalid polling values, and no-op cache refreshes.
They require release notes but no public signature or generated record
change. New tests must fail on the original code before each fix.

Proof must include the actual generated status operation and shared REST
runtime. Helper-only mocks cannot prove timeout forwarding. Tests must
also retain credential isolation, pool ownership, all four phase limits,
error identity, cause chains, and cache file contents.

## Signature Baseline

Inspected on Python 3.14.2 before the batch and cache fixes.
The configuration ownership fix changes no public signature:

- `APIConfig` keeps `base_path`, `auth_email`, `auth_token`, `verify`,
  `timeout`, `rest_timeout`, and `grpc_deadline`, with the existing types.
  The base URL and 60-second timeout defaults stay unchanged.
- `with_timeout` keeps its optional positional `timeout` and keyword-only
  `rest_timeout` and `grpc_deadline`, all defaulting to `None`.
- `wait_for_batch` keeps `client`, `guid`, and keyword-only `timeout=600.0`
  and `interval=5.0`. Its return remains `BatchStatus`.
- `fetch_latest` keeps `query_fn`, `step=None`, `dedup_columns=None`, and
  query keywords. Its return remains `pd.DataFrame | None`.
- `BatchWaitTimeout` keeps its `guid` and `last_status` constructor values.
  Timeout settings still read as `httpx.Timeout`.

The helper import guard prohibits HTTPX, `request_json`, and the REST
runtime in hand-written helpers. The implementation preserves that guard.
