<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../pyproject.toml). Edit directly. -->

# Kentik Community Python SDK Documentation

All documentation for the SDK is in or linked from this directory.

## Where to start

| Document | What it covers |
| --- | --- |
| [Quick start](sphinx/guides/quickstart.md) | Install, configure credentials, make your first call |
| [REST transport guide](sphinx/guides/rest.md) | HTTP/REST usage, pagination, and tips |
| [gRPC transport guide](sphinx/guides/grpc.md) | gRPC usage, sequence diagrams, and transport comparison |
| [Authentication](sphinx/authentication.md) | Credential sources, and keeping them encrypted |
| [Error handling guide](sphinx/guides/error_handling.md) | Exception hierarchy and how to catch each type |
| [Rate limiting guide](sphinx/guides/rate_limiting.md) | Quota headers and the limits no header shows |
| [REST vs gRPC](sphinx/guides/rest-vs-grpc.md) | How the transports differ, and how to choose one |
| [Migrating from 1.x](sphinx/guides/migrating-from-1x.md) | Moving from kentik-api 1.x |
| [SDK generation workflow](sphinx/guides/generation.md) | How to regenerate the SDK from the OpenAPI schema |

## Examples

Runnable scripts are in [examples/](../examples/README.md). Each V6 service has
a REST and a gRPC variant. The V5 endpoints are REST only:

```text
examples/
├── common/
│   └── error_handling.py
├── device/
│   ├── rest.py
│   └── grpc.py
├── user/
│   ├── rest.py
│   └── grpc.py
├── label/
│   ├── rest.py
│   └── grpc.py
├── site/
│   ├── rest.py
│   └── grpc.py
├── alerting/
│   ├── rest.py
│   └── grpc.py
├── synthetics/
│   ├── rest.py
│   └── grpc.py
└── v5/
    ├── analytics_topx.py
    ├── batch.py
    └── query.py
```

## Sphinx HTML documentation

Run [`uv run poe docs`](../pyproject.toml) to build the full HTML reference from
[docs/sphinx/](sphinx/README.md). The HTML output includes per-endpoint
parameter tables, response tables, model schemas, and interactive Mermaid
diagrams.

## Source code documentation

Each package directory has a README that explains its role:

- [src/kentik_api/](../src/kentik_api/README.md): package overview and request flow
- [src/kentik_api/auth/](../src/kentik_api/auth/README.md): credential loading
- [src/kentik_api/core/](../src/kentik_api/core/README.md): shared REST/gRPC runtime
- [src/kentik_api/errors/](../src/kentik_api/errors/README.md): exception hierarchy
- [src/kentik_api/transports/](../src/kentik_api/transports/README.md): transport layer
- [src/kentik_api/gen/](../src/kentik_api/gen/README.md): generated services
- [scripts/](../scripts/README.md): SDK generator and tooling
- [tests/](../tests/README.md): test suite structure
