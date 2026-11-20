<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../../pyproject.toml). Edit directly. -->

# Transports (`kentik_api.transports`)

This folder is hand-written. [`uv run poe generate`](../../../pyproject.toml) does not touch it.
It holds thin transport-selection code, not per-endpoint logic. Each transport takes one
[`APIConfig`](../core/api_config.py), the single source of the host,
credentials, timeouts, and quota record. [`KentikAPI`](../client.py) builds it.

## Classes

| Class | File | Role |
| --- | --- | --- |
| `BaseTransport` | [`base.py`](base.py) | Abstract base. Declares `close()`. |
| `RestTransport` | [`rest_client.py`](rest_client.py) | `RestTransport(api_config)`. Generated wrappers read `api_config` off this object. |
| `GrpcTransport` | [`grpc_client.py`](grpc_client.py) | `GrpcTransport(api_config, target, options)`. Opens a `grpc.secure_channel` with an auth plugin built from the config's credentials, and raises `ConfigurationError` when they are missing. Every call gets the `grpc_deadline` default, and the receive limit is 40 MiB. It records quota per gRPC method in `api_config.rate_limits`. |

```mermaid
%%{init: {"theme": "redux", "look": "neo", "layout": "elk", "fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "themeVariables": {"fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "primaryColor": "#f8f9fa", "primaryBorderColor": "#495057", "primaryTextColor": "#212529", "textColor": "#212529", "lineColor": "#77818c", "edgeLabelBackground": "#ffffff", "actorBkg": "#f8f9fa", "actorBorder": "#495057", "actorTextColor": "#212529", "actorLineColor": "#a9b3be", "signalColor": "#57616d", "signalTextColor": "#212529", "labelBoxBkgColor": "#f8f9fa", "labelBoxBorderColor": "#495057", "labelTextColor": "#212529", "loopTextColor": "#57616d", "noteBkgColor": "#fff9db", "noteBorderColor": "#f08c00", "noteTextColor": "#a35a00"}, "flowchart": {"curve": "basis", "nodeSpacing": 30, "rankSpacing": 70, "wrappingWidth": 400}}}%%
classDiagram
    class BaseTransport {
        <<abstract>>
        +close()
    }
    class RestTransport {
        +APIConfig api_config
    }
    class GrpcTransport {
        +grpc.Channel channel
        +APIConfig api_config
    }
    BaseTransport <|-- RestTransport
    BaseTransport <|-- GrpcTransport
    link BaseTransport "base.py"
    link RestTransport "rest_client.py"
    link GrpcTransport "grpc_client.py"
```

## gRPC

`GrpcTransport` opens a TLS channel to a per-region gRPC endpoint:
`grpc.api.kentik.com:443` for `region="us"` (the default), or
`grpc.api.kentik.eu:443` for `region="eu"`. Each service wrapper
sends calls through the compiled proto stubs in `gen/<service>/pb/`.
The [`gen/pb_companions/`](../gen/pb_companions/) registry loads all shared proto descriptors
before the wrapper imports the stubs. `call_grpc()` in
[`core/grpc_runtime.py`](../core/grpc_runtime.py) normalizes gRPC errors to the same exception
hierarchy as REST.

```python
client = KentikAPI(protocol="grpc")
response = client.device.list()  # works the same as REST
```

## Adding a transport

Add a new `BaseTransport` subclass here, and wire its selection logic
into [`KentikAPI`](../client.py). Keep per-endpoint request logic out
of this folder. That logic belongs in
[`core/rest_runtime.py`](../core/rest_runtime.py) and
[`core/grpc_runtime.py`](../core/grpc_runtime.py).
