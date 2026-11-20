<!-- HAND-WRITTEN prose, except the `kentik-gen` marker blocks, which [`uv run poe generate`](../../../pyproject.toml) rewrites. Fix those in scripts/generation/docs_rendering.py. -->

# Quick Start

Install the SDK and make your first API call in under five minutes.

## Prerequisites

- Python 3.12 or later
- [uv](https://github.com/astral-sh/uv) package manager

## Install

```bash
pip install -U "kentik-api>=2"
```

In a uv project, use this command instead:

```bash
uv add kentik-api
```

From a source checkout, `requirements.txt` pins every runtime dependency by version and hash.
Install the dependencies first. Then install the SDK without dependencies:

```bash
pip install --require-hashes -r requirements.txt
pip install --no-deps .
```

## Configure credentials

Create `.env` at your project root:

```bash
KENTIK_EMAIL=you@example.com
KENTIK_API_TOKEN=your_api_token
```

The SDK reads these values when you create the client. You can also pass them
as arguments:

```python
from kentik_api.client import KentikAPI

client = KentikAPI(
    email="you@example.com",
    api_token="your_api_token",
    protocol="rest",
)
```

To keep credentials encrypted instead of in a plaintext `.env`, see
[Authentication](../authentication.md).

## Make your first call

<!-- kentik-gen:first-call-example -->
```python
from kentik_api.client import KentikAPI

client = KentikAPI(protocol="rest")
response = client.as_group.list()
print(response)  # ListASGroupsResponse
```
<!-- /kentik-gen:first-call-example -->

## Switch to gRPC

To use gRPC, change one argument:

<!-- kentik-gen:grpc-call-example -->
```python
client = KentikAPI(protocol="grpc")
response = client.as_group.list()  # same API, same response models
```
<!-- /kentik-gen:grpc-call-example -->

For more, see the [gRPC transport guide](grpc.md).

## Set a timeout

Every call uses a timeout: 60 seconds by default, on both transports.
To set it for the whole client, pass `timeout`:

```python
client = KentikAPI(timeout=10)
```

To give one slow call more time without a second client, use `with_timeout()`:

```python
slow = client.api_config.with_timeout(300)
response = client.device.list(api_config_override=slow)
```

`with_timeout()` copies the configuration of the client and can change only
the timeouts. It shares the connection and the credentials of the client. A
configuration that you pass as `api_config_override` replaces the
configuration of the client for that one call. An override that you build any
other way must therefore carry its own credentials.

Timeout settings are read-only. The SDK copies any supplied
`httpx.Timeout`, and `client.api_config.rest_timeout` returns a detached
snapshot. A change to either object does not change the active settings.
To change a timeout, use `with_timeout()`, not the returned timeout object.

A number is a total deadline for the call. To bound each REST phase
separately, as httpx does, pass `rest_timeout=httpx.Timeout(...)`. A slow body
then keeps the call open while each read arrives in time. A REST total
deadline is cooperative: the SDK checks it after the response headers and each
chunk arrive. A blocking operation can finish after the deadline. It does not
stop at an exact wall-clock instant.

## Next steps

- [REST transport guide](rest.md)
- [gRPC transport guide](grpc.md)
- [Error handling guide](error_handling.md)
- [Runnable examples](https://github.com/kentik/community_sdk_python/blob/main/examples/README.md)

> [!NOTE]
> Run each example with `python -m` from the project root, for example
> `uv run python -m examples.device.rest`. This prevents conflicts between
> module names.
