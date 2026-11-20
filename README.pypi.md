# kentik-api

A type-safe Python client for the [Kentik](https://www.kentik.com) API v6.
A generator builds it from Kentik's public
[OpenAPI schema](https://github.com/kentik/api-schema-public), so it covers
every published endpoint. It calls the endpoints over REST or gRPC.

Version 2 is a rewrite. If you use kentik-api 1.x, read the
[migration guide](https://github.com/kentik/community_sdk_python/blob/main/docs/sphinx/guides/migrating-from-1x.md)
before you upgrade.

## Install

```bash
pip install -U "kentik-api>=2"
```

kentik-api requires Python 3.12 or later.

## Make a call

Put your credentials in a `.env` file in your project, or in the
`KENTIK_EMAIL` and `KENTIK_API_TOKEN` environment variables:

```bash
KENTIK_EMAIL=you@example.com
KENTIK_API_TOKEN=your_api_token
```

Then make the call:

```python
from kentik_api import KentikAPI

with KentikAPI() as client:
    devices = client.device.list()
    for device in devices.devices or []:
        print(device.id, device.deviceName)
```

The client does not write the `.env` file into the process environment. You
can also pass `email` and `api_token` as arguments, for example from a
secret store.

## Choose a transport

```python
client = KentikAPI(protocol="rest")  # the default
client = KentikAPI(protocol="grpc")
```

Both transports return the same Pydantic models and raise the same
exceptions, so you can switch without changing other code.

## Documentation

- [Quickstart](https://github.com/kentik/community_sdk_python/blob/main/docs/sphinx/guides/quickstart.md)
- [Authentication](https://github.com/kentik/community_sdk_python/blob/main/docs/sphinx/authentication.md)
- [Error handling](https://github.com/kentik/community_sdk_python/blob/main/docs/sphinx/guides/error_handling.md)
- [Rate limiting](https://github.com/kentik/community_sdk_python/blob/main/docs/sphinx/guides/rate_limiting.md)
- [REST or gRPC](https://github.com/kentik/community_sdk_python/blob/main/docs/sphinx/guides/rest-vs-grpc.md)
- [Examples for each service](https://github.com/kentik/community_sdk_python/tree/main/examples)
- [Changelog](https://github.com/kentik/community_sdk_python/blob/main/CHANGELOG.md)

## License

kentik-api uses the Apache-2.0 license. See
[LICENSE](https://github.com/kentik/community_sdk_python/blob/main/LICENSE).
