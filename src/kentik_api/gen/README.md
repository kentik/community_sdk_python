<!-- AUTO-GENERATED: scripts/generation/docs_rendering.py, _generate_gen_root_readme() -->
<!-- Rebuilt on every `uv run poe generate`. Do not edit by hand. -->
# Generated Services (`kentik_api.gen`)

The generator builds every file in this folder. Each
[`uv run poe generate`](../../../pyproject.toml) run deletes each subdirectory here,
builds it again, and writes this README again.

> [!WARNING]
> Do not edit any file in this folder, this README included. The next run deletes the edit.
> If the output is wrong, fix the generator ([`scripts/generate_sdk.py`](../../../scripts/generate_sdk.py)),
> a phase module in [`scripts/generation/`](../../../scripts/generation/README.md), or a template in
> [`scripts/openapi_templates/`](../../../scripts/openapi_templates/README.md). Then run the generator again.

## Layout

Each subdirectory is one Kentik API service (`device`, `alerting`, `user`, and others).
The generator builds it from the OpenAPI v3 schema files of that service.
Each service directory has the same shape:

```text
gen/device/
├── models/      Pydantic v2 request and response models
├── services/    one REST function per operation, and the DeviceServiceWrapper class
├── error/       one error class per operation, picked by the response status code
├── pb/          gRPC stubs (*_pb2.py, *_pb2_grpc.py) for the gRPC transport
└── README.md    a link to the Sphinx reference page of the service
```

## Where a call runs

No service directory here has its own HTTP, auth, or retry code.

- On a REST transport, each generated REST function calls `request_json()` in
  [`kentik_api.core`](../core/README.md). That one function sends the REST traffic of every service.
- On a gRPC transport, a wrapper method calls `call_grpc()` in [`kentik_api.core`](../core/README.md).
  The generator writes that call when an RPC has the same HTTP rule as the REST operation: the same
  proto service, verb, and path.

A wrapper method raises `NotImplementedError` on a `GrpcTransport` in two cases only:

1. The proto companions of the service did not import.
2. No RPC has the same HTTP rule as the operation.

[SDK Runtime Architecture](../../../docs/sphinx/sdk_runtime_architecture.md) shows the full call path.

## Full reference

The page `docs/sphinx/services/<service>.md` gives the parameters, the response shapes, and a usage
example for each operation of a service. The built Sphinx docs show the same pages.
