<!-- HAND-WRITTEN prose, except the `kentik-gen` marker blocks, which [`uv run poe generate`](../../pyproject.toml) rewrites. Fix those in scripts/generation/docs_rendering.py. -->

# Documentation Source

This directory holds the Sphinx source for the documentation of the Kentik
Community Python SDK. To build it, run [`uv run poe docs`](../../pyproject.toml).
The HTML output goes to `docs/build/html/`.

## Structure

```text
docs/sphinx/
├── index.md                      Sphinx root toctree
├── conf.py                       Sphinx configuration
├── authentication.md
├── dependencies.md
├── local_generation_workflow.md
├── sdk_runtime_architecture.md   generated
├── guides/                       task guides, one page per topic
└── services/                     generated, one page per service
```

## Pages

| File | Description |
| --- | --- |
| [index.md](index.md) | Sphinx root toctree |
| [authentication.md](authentication.md) | Credential sources (arguments, environment, `.env`), and keeping them encrypted |
| [dependencies.md](dependencies.md) | Each declared package, why the project needs it, and the audit decision |
| [sdk_runtime_architecture.md](sdk_runtime_architecture.md) | Module dependency graph and runtime flow. Generated |
| [local_generation_workflow.md](local_generation_workflow.md) | How to regenerate the SDK from the OpenAPI schema |
| [guides/](guides/) | Quick start, REST, gRPC, errors, rate limits, V5 calls, migration from 1.x, and generation |
| [services/](services/README.md) | One page per Kentik API service (<!-- kentik-gen:service-count -->43<!-- /kentik-gen:service-count --> total) |

## Building

```bash
uv run poe docs                # build Sphinx HTML → docs/build/html/
uv run poe generate            # regenerate service .md pages from the OpenAPI schema
uv run poe generate --local    # use the local ../api-schema-public/ checkout
```
