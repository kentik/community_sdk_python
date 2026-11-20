# Quickstart: Validate Schema Checkout Before Generating

Validates end-to-end that a corrupted local schema checkout is caught
before generation, and that a healthy checkout is unaffected.

## Prerequisites

- Repo dependencies installed (`uv sync`, or just use `uv run`/`make`
  targets, which install on demand).
- A local `../api-schema-public/` checkout (only needed for the
  `make generate local` manual check below; the automated tests use
  `tmp_path` fixtures and need no real checkout).

## Automated checks (what CI/`make test` runs)

```sh
uv run pytest tests/generator/test_parity.py -v
```

Expected: all `test_validate_schema_files_*` cases pass, including a
regression case shaped like the 2026-08-26 incident (a swagger fixture
truncated to a single line/character).

## Manual end-to-end check (optional, exercises the real `make` target)

1. Truncate one swagger file in the schema checkout to confirm the gate
   fires. The glob matches more than one version, so pick one file first:
   in zsh, a redirect to a glob writes to every match.

   ```sh
   target=$(ls ../api-schema-public/gen/openapiv3/kentik/device/*/device.swagger.json | sort | tail -n 1)
   cp "$target" /tmp/device.swagger.json.bak
   printf x > "$target"
   make generate local
   ```

   Expected: the run stops with a non-zero exit code and a printed list
   naming the truncated file and the reason (invalid JSON), before
   anything under `src/kentik_api/gen/` changes.

2. Restore the file, from the same shell, and confirm a clean run proceeds
   normally:

   ```sh
   cp /tmp/device.swagger.json.bak "$target"
   make generate local
   ```

   Expected: generation completes exactly as before this feature (SC-002).

## Traceability

- SC-001 -> manual check step 1, and
  `test_validate_schema_files_reports_all_failures_before_raising`
- SC-002 -> manual check step 2, and
  `test_generate_modular_sdk_unaffected_by_valid_checkout` (existing
  generation tests continue passing unchanged)
- SC-003 -> `test_validate_schema_files_catches_truncated_file_like_2026_08_26_incident`
