# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rate_limit import RateLimit
from kentik_api.transports.base import BaseTransport


class RestTransport(BaseTransport):
    api_config: APIConfig

    def __init__(self, api_config: APIConfig):
        self.api_config = api_config

    @property
    def rate_limits(self) -> dict[str, RateLimit]:
        """Quota per REST method and path template, as of the last call to each."""
        return self.api_config.rate_limits

    def close(self):
        self.api_config.close()
