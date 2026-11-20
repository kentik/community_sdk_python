<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# Kentik Community SDK Documentation

The Kentik Community SDK is a type-safe Python client for the Kentik API. A
generator builds it from the Kentik OpenAPI schemas. It uses Pydantic v2 for
its models and HTTPX for REST calls.

To make your first call, start with the [Quick Start](guides/quickstart.md).

:::{toctree}
:maxdepth: 2
:caption: "Contents"

guides/quickstart
authentication
guides/rest
guides/grpc
guides/error_handling
guides/rate_limiting
guides/rest-vs-grpc
guides/migrating-from-1x
guides/v5
guides/generation
local_generation_workflow
sdk_runtime_architecture
dependencies
services/index
:::
