# Quickstart: validate V5 query and batch support

**Feature**: [spec.md](spec.md) | **Contracts**: [contracts/](contracts/)

Run these steps from the repository root after implementation. Steps 1 to 4
need no network. Steps 5 to 7 call the real API and are opt-in.

## 1. Regenerate and check the tree

```sh
make generate local
git status --short src/kentik_api/gen/v5 public_names.json api_surface.json
```

Expected: `src/kentik_api/gen/v5/` exists. `public_names.json` has a `v5`
service with the six methods in [contracts/v5-service.md](contracts/v5-service.md).
`api_surface.json` has `"rest_only": true` for `v5`, and the run ends with an
`API SURFACE CHANGED` alert that lists the new service.

## 2. Mocked tests

```sh
make test-generator
make test-generated
make test-runtime
make test
```

Expected: every suite passes. The schema coverage suite has cases for all six
`v5` operations and for every declared status.

## 3. Client wiring (no network)

```sh
uv run python - <<'EOF'
from kentik_api import KentikAPI
for region, protocol in (("us", "rest"), ("eu", "grpc")):
    c = KentikAPI("a@b.c", "t", protocol=protocol, region=region, env_file=None)
    print(region, protocol, c.v5_api_config.base_path, type(c.v5._transport).__name__)
    c.close()
EOF
```

Expected:

```text
us rest https://api.kentik.com/api/v5 RestTransport
eu grpc https://api.kentik.eu/api/v5 RestTransport
```

## 4. Quality gates

```sh
make lint && make typecheck && make check-specs
make check-changelog SINCE=HEAD
uv run sphinx-build -W --keep-going -b html docs/sphinx docs/build/html
```

Expected: all pass. `docs/sphinx/services/v5.md` exists and says "REST only".

## 5. Live read-only queries (opt-in)

```sh
uv run pytest -m e2e tests/e2e/test_v5_query_e2e.py -v
```

Expected: `top_x_data` and `query_url` pass. `top_x_chart` reports `XFAIL`
while the endpoint still does not answer, or `XPASS` once Kentik fixes it.

## 6. Manual chart test (FR-004a)

Follow the steps in the V5 bridge guide (`docs/sphinx/guides/v5.md`, section
"Test the chart call by hand"). Record the status, the time, and the
`errorxid`.

## 7. Batch round trip (opt-in, writes data)

Only against a disposable custom dimension or tag name, with cleanup:

```sh
uv run pytest -m e2e_mutating --run-live-e2e tests/e2e/test_v5_batch_e2e.py -v
```

Expected: one upsert is applied, then deleted in a second batch, and both
statuses report `is_complete: true`. This suite is listed in the pull request
as mutating coverage (Principle V).

## Results (2026-10-16)

| Step | Result |
| --- | --- |
| 1 | `gen/v5/` exists, with no `pb/`. `public_names.json` has the six `v5` methods. `api_surface.json` records `"rest_only": true`. A second `make generate local` gives no diff. |
| 2 | `make test`: 3504 passed, 149 skipped. The `v5` coverage cases run (42 passed, 3 skipped for no path parameters). |
| 3 | The output above, exactly. |
| 4 | Lint, format, type check, `check-specs`, `check-changelog` (since `HEAD` and since `feat/v6-sdk`), and the strict Sphinx build pass. |
| 5 | `top_x_data`, `query_url`, and `top_x_data` on a gRPC client pass. `top_x_chart` is `XFAIL` (no answer in 60 s). A run right after a hung chart call timed out on `query_url`: the hung call holds a Query API slot. The chart test now runs last, and the V5 guide warns about it. |
| 6 | Done by the maintainer: `curl` timed out (exit 28) for both request bodies, while `topXdata` answered the same body in 1.4 s. |
| 7 | Not run: it writes to the account. |
| Regression proof (T053) | With the US V5 URL changed to `/api/v4` in `client.py`, `make test` failed 11 tests (client, smoke, examples, analytics). Restored, all pass. |
