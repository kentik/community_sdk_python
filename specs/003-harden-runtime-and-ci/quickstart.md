# Quickstart: verifying feature 003

How to confirm each user story is done, and how to reproduce the defects it
fixes. Every check here is local. Only the optional probes at the end touch the
network.

Baseline to return to at any point:

```bash
make test && make typecheck && make lint
```

---

## Reproduce the defects first

Worth doing before any code changes, so the fixes are verifiable rather than
assumed. These use the gitignored exercise from User Story 9.

```bash
# US1: gRPC blocks forever with no deadline. Local socket, no credentials.
uv run python learn/ex06_timeouts.py
#   expect: "STILL BLOCKED after 3s, and would block forever"

# US2: the transports disagree. Uses deliberately invalid credentials.
uv run python learn/ex04_errors.py
#   expect: rest -> ListDevicesUnexpectedError status_code=401
#           grpc -> AuthenticationError
#           same exception type on both transports? False
#   expect: 8 of 16 gRPC status codes falling through to 500

# US4: formatting gate would fail today
uv run ruff format --check .
#   expect: "Would reformat: scripts/generate_sdk.py"

# US3 / US11: the coverage gaps
uv run --with pytest-cov pytest -q \
  --cov=src/kentik_api/core --cov=src/kentik_api/auth \
  --cov=src/kentik_api/transports --cov=scripts/generation \
  --cov-report=term-missing
#   expect: grpc_runtime 65%, credentials 44%, grpc_client 50%
#           docs_rendering 18%, endpoint_docs 26%, wrapper_generation 54%
```

---

## Per-story verification

### US1: gRPC calls are bounded

```bash
uv run pytest tests/runtime/test_grpc_runtime.py -q
uv run python learn/ex06_timeouts.py     # now terminates at the deadline
```

Done when a non-responding stub raises `TransportError` within the configured
timeout, a non-`RpcError` from the stub is **not** reported as a transport
failure, and an unreadable method label still leaves the original `RpcError` as
`__cause__`.

### US2: the transports agree

```bash
uv run pytest tests/runtime/test_transport_symmetry.py -q
uv run pytest tests/generated/test_endpoint_schema_coverage.py -q
uv run python learn/ex04_errors.py       # "same exception type ... ? True"
```

Done when auth failures raise `AuthenticationError` on both transports, timeouts
and unreachable hosts raise `TransportError` on both, and all 16 non-OK gRPC
codes are handled explicitly.

**Watch for**: `test_endpoint_schema_coverage.py` must be *updated*, never
narrowed. It drives every declared status on every discovered endpoint
(Constitution gate IV).

### US3: the gRPC path is covered

```bash
uv run --with pytest-cov pytest -q \
  --cov=src/kentik_api/core/grpc_runtime --cov=src/kentik_api/auth \
  --cov=src/kentik_api/transports/grpc_client --cov-report=term-missing
```

Done at 100% on all three. Then prove the tests bite: change a character in the
`x-ch-auth-email` metadata key and confirm a test fails.

### US4: CI enforces the invariants

```bash
uv run ruff check . && uv run ruff format --check .
make generate && git diff --exit-code          # determinism gate
uv run sphinx-build -b html docs/sphinx docs/build/html -q -W
grep -n "branches:" .github/workflows/*.yml    # no feature branch name
grep -rn "e2e" .github/workflows/              # expect no matches
```

All four must pass locally before the workflow lands. Then verify each gate
actually fails: push a formatting violation, a generator change, and a bad
Sphinx reference on throwaway branches.

### US5: one exception hierarchy

```bash
uv run pytest tests/smoke/ -q
uv run python -c "
from kentik_api.client import KentikAPI
from kentik_api.errors import KentikError
try:
    KentikAPI(email='x@y.z', api_token='t', region='xx')
except KentikError as e:
    print(type(e).__name__, '->', e)
"
```

Done when both failures are catchable as `KentikError` and each message names
the offending value. `ConfigurationError` must **not** inherit `ValueError`.

### US6: one auth-header definition

```bash
grep -rn "X-CH-Auth-Email" src/ | grep -v "/gen/"
#   expect exactly one line
uv run pytest tests/runtime/test_rest_runtime.py -q
```

### US7: connections are reused

```bash
uv run pytest tests/runtime/test_rest_runtime.py -q
```

Done when N calls on one client share one `httpx.Client`, `close()` releases it,
a configured timeout is honored, and a non-positive timeout raises
`ConfigurationError` at construction.

### US8: rate limits are surfaced

```bash
uv run pytest tests/runtime/test_rate_limit.py -q
```

Parser cases that must all pass: `60, 60;w=60`, `100;window=60`, multiple
windows, absent header, malformed header (returns `None`, never raises).

Optional live confirmation, read-only, needs `.env`:

```bash
uv run python learn/ex07_rate_limits.py
```

### US9: the guide

```bash
uv run sphinx-build -b html docs/sphinx docs/build/html -q -W
git status --short        # nothing from learn/ may appear
```

Done when the guide is reachable from the docs navigation, every claim traces to
a measured finding, and it states the real coverage numbers (35 services, 233
operations, 198 with gRPC) plus the shared per-endpoint quota.

### US10: per-call override

```bash
make generate local
git diff --stat           # expect ONLY the signature change and its plumbing
uv run pytest tests/generated/test_wrapper_contracts.py -q
```

Done when every wrapper method accepts `api_config_override`, omitting it
changes nothing, and it reaches the gRPC deadline too. Commit the generated diff
together with a regenerated `api_surface.json`, separate from any hand-written
change.

### US11: generator coverage

```bash
uv run --with pytest-cov pytest tests/generator/ -q \
  --cov=scripts/generation --cov-report=term-missing
```

New tests must use `tmp_path` and need no schema checkout and no network.

### US12: examples cannot rot

```bash
uv run pytest tests/smoke/test_examples_import.py -q
```

Then prove it bites: rename a wrapper method an example calls and confirm a
failure.

---

## Definition of done for the whole feature

```bash
make test          # mocked only, no network, no credentials
make typecheck
make lint
make docs
make generate local && git diff --exit-code    # zero-diff, except the US10 commit
```

Plus:

- `git status` has never shown anything under `learn/`
- Release notes name every caller-visible change: `ConfigurationError` replacing
  `ValueError`, REST raising `AuthenticationError`, gRPC timeouts becoming
  `TransportError`, connection reuse, timeouts, and the per-call override
- No `e2e` or `e2e_grpc` test runs in CI
