<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# Authentication

The SDK takes Kentik API credentials from constructor arguments, environment
variables, or a `.env` file.

For a runtime-level dependency map that shows how credentials and transports
connect to generated services, see
[SDK Runtime Architecture](sdk_runtime_architecture.md).

## .env Setup

Create `.env` at your project root:

```bash
KENTIK_EMAIL=you@example.com
KENTIK_API_TOKEN=your_api_token
```

## Transport selection

To choose between REST and gRPC, pass `protocol`. Both transports return the
same Pydantic response models.

```python
client = KentikAPI(protocol="rest", region="us")  # REST (default)
client = KentikAPI(protocol="grpc", region="us")  # gRPC
```

## How Credentials Are Resolved

`KentikAPI` takes each value from the first source that has it:

1. The `email` and `api_token` arguments.
2. The `KENTIK_EMAIL` and `KENTIK_API_TOKEN` environment variables.
3. The `env_file` argument, `.env` by default. The client searches for it
   from the current working directory upward.

The client reads the file only when a value is still missing after steps 1
and 2. It reads the file into memory and never writes its contents into
`os.environ`. Subprocesses that your program starts therefore do not inherit
the credentials.

An argument that is empty or only whitespace raises `ConfigurationError`. The
client does not fall back to another source, because a fallback can send the
credentials of another identity. To use the other sources, omit the argument
or pass `None`.

| `env_file` | Result |
| --- | --- |
| `".env"` (default) | Search for `.env` from the working directory upward. |
| A `str` or `Path`, such as `Path.home() / ".kentik.env"` | The client reads an absolute path as is. It searches for a relative path like the default. |
| `None` | Never read a file. |

## Keeping credentials out of plaintext files

To keep the credentials out of a plaintext file, decrypt them in your own code.
Then pass them as arguments. The client then reads no file and no environment
variable:

```python
import json
import subprocess

from kentik_api.client import KentikAPI

secrets = json.loads(
    subprocess.run(
        ["sops", "decrypt", "--output-type", "json", "kentik.sops.json"],
        capture_output=True,
        check=True,
    ).stdout
)
client = KentikAPI(email=secrets["email"], api_token=secrets["api_token"])
```

This works the same way for any secret store, for example a keyring, a
password manager CLI, or a cloud secret manager.

With no code change, `sops exec-file` gives the decrypted file to your program
as a named pipe. sops writes no plaintext file to disk:

```bash
sops exec-file kentik.sops.env 'python my_script.py --env-file {}'
```

In `my_script.py`, pass that path as `KentikAPI(env_file=args.env_file)`.

## Required Variables

- `KENTIK_EMAIL`
- `KENTIK_API_TOKEN`

If no source supplies both values, `KentikAPI` raises `ConfigurationError`.
