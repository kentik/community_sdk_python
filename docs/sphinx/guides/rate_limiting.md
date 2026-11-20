<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../../pyproject.toml). Edit directly. -->

# Rate Limiting Guide

Kentik limits how fast you can call its API. The SDK reports the quota that
the API advertises, but the API never advertises several other limits. This
guide covers both, so you can pace calls without guessing.

## Read the quota the API reports

Every response carries three headers, on REST and gRPC alike:

| Header | Example | Meaning |
| --- | --- | --- |
| `x-ratelimit-limit` | `60, 60;w=60` | 60 requests per 60-second window |
| `x-ratelimit-remaining` | `59` | Requests left in the current window |
| `x-ratelimit-reset` | `40` | Seconds until the window resets |

The API sends no `Retry-After` header. Use `reset_seconds` instead.

The SDK parses these headers into a `RateLimit` value with `limit`, `remaining`,
`reset_seconds`, `window_seconds`, and `raw`. Any field the server omits is
`None`. A missing or malformed header never fails a call.

### On a result

`rate_limit_of()` returns the quota that the API reported on the call that
produced a result:

```python
from kentik_api import rate_limit_of

devices = client.device.list()
quota = rate_limit_of(devices)
if quota is not None and quota.remaining == 0:
    print(f"Next call to this endpoint waits {quota.reset_seconds}s")
```

The returned model carries the quota, but the quota is not one of its fields.
So the quota does not change the result of `model_dump()` or `==`.
`rate_limit_of()` returns `None` when the response carried no quota headers,
and for results that are not a model (a list, or `None`).

### On an error

Every SDK exception has a `rate_limit` attribute that holds the quota as of the
call that failed:

```python
from kentik_api.errors import HTTPException

try:
    client.device.list()
except HTTPException as exc:
    if exc.status_code == 429 and exc.rate_limit is not None:
        print(f"Quota exhausted; resets in {exc.rate_limit.reset_seconds}s")
```

`rate_limit` is `None` when no response arrived, for example on a
`TransportError`.

### Per endpoint

The client keeps the latest quota for each endpoint that it called:

```python
client.device.get(deviceid="42")
quota = client.api_config.rate_limits["GET /device/v202504beta2/device/{device.id}"]
print(quota.remaining, quota.reset_seconds)
```

On the REST transport, a key is the HTTP method and the path template of the
schema, so calls with different IDs share one entry. On the gRPC transport, a
key is the gRPC method name, for example
`/kentik.device.v202504beta2.DeviceService/GetDevice`.

## Quota is per endpoint

Measurement shows that each endpoint has its own budget. In one test, `sites`
counted down 58, 57, 56 while `site_markets` stayed at 59. REST and gRPC share
the same budget for the same endpoint.

Back off only on the endpoint whose quota is exhausted. A `429` on one
endpoint does not mean that the others are exhausted. If you pause every call,
you waste the budget that you still have.

## Limits that no header reveals

Kentik documents three more limits. None of them appears in a response header,
so an SDK that reads headers cannot report them. Plan for them yourself.

| Limit | Non-query APIs | Query API | What you see |
| --- | --- | --- | --- |
| Concurrent requests | 1 | 4 | Parallel calls queue on the server. Threads do not add throughput |
| Soft limit per minute | 20 | 30 | Past it, the API delays each response |
| Delay past the soft limit | 1.5s | 1s | Added latency, not an error |
| Hourly limit | 3750 | 1500 | A `429` from a budget the headers never showed |

Source: the Kentik Knowledge Base,
[API rate limiting](https://kb.kentik.com/docs/apis-overview#api-rate-limiting),
read 2026-09-21.

The SDK's default timeout is 60 seconds because of the soft-limit delay. A
throttled call is slow, not failed. If you lower the timeout, keep it well
above the healthy latency (about 0.6s) plus the 1.5s delay. Otherwise normal
throttling shows up as a `TransportError`.

## Documented and measured limits disagree

| Question | Answer | Basis |
| --- | --- | --- |
| Per-minute limit for non-query APIs | 60 | Measured, and matches the documentation |
| Granularity of that limit | Per endpoint | Measured |
| Granularity the documentation states | Per customer | Documented |
| Why the two differ | Unknown | Open, reported to Kentik |

The two answers cannot describe the same counter. The SDK reports what it
observes, per endpoint, and does not choose between them. If the hourly or
per-customer limits apply across endpoints, you can exhaust them even while
each endpoint still shows quota.

## Retries

The SDK retries a request only when the connection attempt fails. Such a
request never reached the server, so a retry cannot repeat it. The SDK never
retries a request that got a response, including a `429`. You decide how to
pace calls and whether to retry after a response.

If you add your own retries, retry only idempotent operations (safe to send
twice): those that use GET, PUT, or DELETE. Do not retry POST or PATCH. A
repeated POST or PATCH can create or change something twice. Of the SDK's 240
operations, 163 are idempotent and 77 are not.

## V5 calls report no quota

`client.v5` calls the V5 API, which sends no `X-RateLimit-*` headers. The
quota of a V5 call is therefore always empty: `rate_limit_of(result)` and
`exc.rate_limit` are `None`, and no V5 endpoint appears in
`client.v5_api_config.rate_limits`. The "Query API" column above still
applies to the V5 queries.

The V5 queries (`top_x_data`, `top_x_chart`, `query_url`) are POST calls, but
they only read data, so a retry cannot change anything. V5 sends no quota
headers, so wait a fixed time before you retry a `429`. Never retry
`batch_tags` or `batch_populators`. A repeated part can change data twice.

```python
import time

from kentik_api.errors import HTTPException


def top_x_data_with_retry(client, request, attempts=3, wait_seconds=60):
    for attempt in range(attempts):
        try:
            return client.v5.top_x_data(data=request)
        except HTTPException as exc:
            if exc.status_code != 429 or attempt == attempts - 1:
                raise
            # The Query API allows 30 calls per minute before it slows down.
            time.sleep(wait_seconds)
```
