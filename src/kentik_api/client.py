# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
import os
from collections.abc import Sequence
from typing import Any

import httpx
from dotenv import dotenv_values, find_dotenv

from kentik_api.auth.credentials import KentikCredentials
from kentik_api.client_mixin import KentikClientMixin
from kentik_api.core.api_config import APIConfig
from kentik_api.errors import ConfigurationError
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport

_REGION_ENDPOINTS: dict[str, tuple[str, str]] = {
    "us": ("grpc.api.kentik.com:443", "https://grpc.api.kentik.com"),
    "eu": ("grpc.api.kentik.eu:443", "https://grpc.api.kentik.eu"),
}
# The V5 API has its own hosts; never derived from the V6 URL.
_V5_BASE_URLS: dict[str, str] = {
    "us": "https://api.kentik.com/api/v5",
    "eu": "https://api.kentik.eu/api/v5",
}


def _resolve_credentials(
    email: str | None,
    api_token: str | None,
    env_file: str | os.PathLike[str] | None,
) -> tuple[str, str]:
    # An explicit empty value is a caller bug; falling back would send the
    # environment's or the file's identity instead of failing.
    for name, value in (("email", email), ("api_token", api_token)):
        if value is not None and not value.strip():
            raise ConfigurationError(
                f"{name} is empty. Pass a value, or omit it to read "
                "credentials from the environment."
            )

    # The file is read into a dict, never into os.environ: callers that keep
    # secrets out of the environment (so subprocesses cannot inherit them)
    # stay that way, and the file is not opened when nothing is missing.
    email = email or os.getenv("KENTIK_EMAIL")
    api_token = api_token or os.getenv("KENTIK_API_TOKEN")

    if (not email or not api_token) and env_file is not None:
        # find_dotenv also accepts a FIFO, such as the one `sops exec-file` makes.
        path = find_dotenv(filename=os.fspath(env_file), usecwd=True)
        if path:
            values = dotenv_values(path)
            email = email or values.get("KENTIK_EMAIL")
            api_token = api_token or values.get("KENTIK_API_TOKEN")

    if not email or not api_token:
        source = "" if env_file is None else f", or in {os.fspath(env_file)!r}"
        raise ConfigurationError(
            "Missing Kentik credentials. Pass email and api_token, or set "
            f"KENTIK_EMAIL and KENTIK_API_TOKEN in the environment{source}."
        )
    return email, api_token


class KentikAPI(KentikClientMixin):
    def __init__(
        self,
        email: str | None = None,
        api_token: str | None = None,
        protocol: str = "rest",
        region: str = "us",
        *,
        v5_base_url: str | None = None,
        timeout: float = 60.0,
        rest_timeout: httpx.Timeout | float | None = None,
        grpc_deadline: float | None = None,
        grpc_options: Sequence[tuple[str, Any]] | None = None,
        env_file: str | os.PathLike[str] | None = ".env",
    ):
        """Connect to the Kentik API over REST or gRPC.

        Credentials come from `email`/`api_token` first, then the
        `KENTIK_EMAIL`/`KENTIK_API_TOKEN` environment variables, then
        `env_file`, searched for from the working directory upward. Pass
        `env_file=None` to never read a file.

        `timeout` bounds every call on either transport. `rest_timeout` (a
        scalar or per-phase `httpx.Timeout`) and `grpc_deadline` override it
        for one transport; see `APIConfig`.

        `client.v5` calls the V5 API, which exists only on REST, at the
        region's V5 host, or at `v5_base_url` (it must use https).
        """
        email, api_token = _resolve_credentials(email, api_token, env_file)

        self.credentials = KentikCredentials(email, api_token)

        try:
            grpc_target, rest_base_url = _REGION_ENDPOINTS[region.lower()]
        except (KeyError, AttributeError):
            valid = ", ".join(f"'{r}'" for r in _REGION_ENDPOINTS)
            raise ConfigurationError(
                f"Invalid region '{region}'. Must be one of: {valid}."
            ) from None

        v5_base_url = v5_base_url or _V5_BASE_URLS[region.lower()]
        if not v5_base_url.startswith("https://"):
            raise ConfigurationError(
                f"v5_base_url must start with https://, got '{v5_base_url}'."
            )

        api_config = APIConfig(
            base_path=rest_base_url,
            auth_email=email,
            auth_token=api_token,
            timeout=timeout,
            rest_timeout=rest_timeout,
            grpc_deadline=grpc_deadline,
        )

        if protocol.lower() == "grpc":
            self._transport = GrpcTransport(
                api_config, target=grpc_target, options=grpc_options
            )
        elif protocol.lower() == "rest":
            self._transport = RestTransport(api_config)
        else:
            raise ConfigurationError(
                f"Invalid protocol '{protocol}'. Must be 'grpc' or 'rest'."
            )

        self._v5_transport = RestTransport(
            APIConfig(
                base_path=v5_base_url,
                auth_email=email,
                auth_token=api_token,
                timeout=timeout,
                rest_timeout=rest_timeout,
            )
        )

        self._mount_generated_services()

    @property
    def api_config(self) -> APIConfig:
        """This client's configuration, the base for a per-call override.

        client.api_config.with_timeout(300) gives a copy with a longer timeout
        that shares this client's connection and credentials.
        """
        return self._transport.api_config

    @property
    def v5_api_config(self) -> APIConfig:
        """The configuration of `client.v5` calls, the base for their per-call override."""
        return self._v5_transport.api_config

    def close(self):
        try:
            self._transport.close()
        finally:
            self._v5_transport.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
