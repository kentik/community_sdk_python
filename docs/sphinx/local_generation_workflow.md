<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# Local SDK Generation Workflow

You can regenerate the SDK from an updated
[`api-schema-public`](https://github.com/kentik/api-schema-public) checkout.
You do not change the upstream
[`openapi-python-generator`](https://github.com/MarcoMuellner/openapi-python-generator)
project to do it.

## Why This Is Local-Only

This repository holds the customization of generation:

- Custom templates live in [`scripts/openapi_templates/`](https://github.com/kentik/community_sdk_python/blob/main/scripts/openapi_templates/README.md).
- Shared runtime logic lives in [`src/kentik_api/core/rest_runtime.py`](https://github.com/kentik/community_sdk_python/blob/main/src/kentik_api/core/rest_runtime.py).
- The generator entrypoint is [`scripts/generate_sdk.py`](https://github.com/kentik/community_sdk_python/blob/main/scripts/generate_sdk.py).

Because this repository holds the customization, the project can take upstream
generator updates without a permanent fork.

For a runtime-level dependency map that shows how the client, mixin,
auth/core/errors, and generated services connect, see
[SDK Runtime Architecture](sdk_runtime_architecture.md).

## Default Regeneration (Local Schema Repo)

Run this command from the project root:

```bash
uv run poe generate --local
```

The command reads the sibling checkout at `../api-schema-public/`. The
`--local` option of the `generate` task in
[`pyproject.toml`](https://github.com/kentik/community_sdk_python/blob/main/pyproject.toml)
sets this path.

## Override Schema Location

To read the schema from another path, pass `--local-repo`:

```bash
uv run poe generate --local-repo /path/to/api-schema-public
```

## Optional: Test a Forked Generator Temporarily

To point generation at a fork without a code change, set an environment
variable:

```bash
OPENAPI_GENERATOR_FROM="git+https://github.com/<org>/openapi-python-generator.git@<branch>" \
uv run poe generate --local
```

If your fork exposes a different CLI name, also set `OPENAPI_GENERATOR_CMD`:

```bash
OPENAPI_GENERATOR_CMD="openapi-python-generator" uv run poe generate --local
```

## Update Cycle (Simple Repeatable Flow)

1. Pull the latest schema updates into your local `api-schema-public` clone.
2. Run `uv run poe generate --local`. It writes the commit of the checkout to
   [`schema.lock`](https://github.com/kentik/community_sdk_python/blob/main/schema.lock).
   Commit that file with the generated changes. A checkout with uncommitted
   changes to tracked files leaves `schema.lock` unchanged.
3. Review the generated changes in [`src/kentik_api/gen/`](https://github.com/kentik/community_sdk_python/blob/main/src/kentik_api/gen/README.md).
4. Run the tests and the linter as needed:
   [`uv run poe test`](https://github.com/kentik/community_sdk_python/blob/main/pyproject.toml) and
   [`uv run poe lint`](https://github.com/kentik/community_sdk_python/blob/main/pyproject.toml).
5. Read the message at the end of the `uv run poe generate` output. This step
   is required. If the message says `⚠️ API SURFACE CHANGED`, update
   [`CHANGELOG.md`](https://github.com/kentik/community_sdk_python/blob/main/CHANGELOG.md)
   before you commit. Then run `uv run poe check-changelog --since HEAD`. The
   [generation guide](guides/generation.md) gives the steps in "Update the
   release notes after every regeneration".
6. Optional: before you commit, run
   [`uv run poe impact-report`](https://github.com/kentik/community_sdk_python/blob/main/pyproject.toml).
   It writes `reports/regeneration-impact-<date>.html` with the schema commit,
   the changed files by kind, the API surface delta, the toolchain floors, and
   the test, lint, and type-check results. The report counts proto stubs that
   changed only their protoc version stamp apart from real schema changes. To
   compare against an earlier commit, add `--since <ref>`. To skip the checks,
   add `--no-checks`. The report leaves its Findings section for you to fill
   in.

## Notes

- To list the `generate` options, run `uv run poe -h generate`.
- To change the shape of a generated service, edit the templates in [`scripts/openapi_templates/`](https://github.com/kentik/community_sdk_python/blob/main/scripts/openapi_templates/README.md).
- Keep business and runtime behavior in [`src/kentik_api/core/`](https://github.com/kentik/community_sdk_python/blob/main/src/kentik_api/core/README.md) and
  [`src/kentik_api/transports/`](https://github.com/kentik/community_sdk_python/blob/main/src/kentik_api/transports/README.md).
  Do not edit generated files.
