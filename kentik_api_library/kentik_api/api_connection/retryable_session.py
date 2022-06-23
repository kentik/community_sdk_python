import logging
from typing import Optional

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from kentik_api.auth.auth import KentikAuth

log = logging.getLogger(__name__)


# mypy: ignore-errors
class RetryableSession(Session):
    DEFAULT_RETRY_STRATEGY = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 502, 503, 504],
        allowed_methods=["DELETE", "HEAD", "GET", "PUT", "OPTIONS", "PATCH", "POST"],
    )

    def __init__(self, retry_strategy: Optional[Retry] = None) -> None:
        super().__init__()
        if retry_strategy is None:
            retry_strategy = self.DEFAULT_RETRY_STRATEGY
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.mount("https://", adapter)
        self.mount("http://", adapter)
        log.debug("%s: retry_strategy: %s", self.__class__, retry_strategy)


def prepare_kentik_api_http_session(
    auth_email: str,
    auth_token: str,
    retry_strategy: Optional[Retry],
    proxy: Optional[str],
) -> RetryableSession:
    session = RetryableSession(retry_strategy)
    session.auth = KentikAuth(auth_email, auth_token)
    session.headers.update({"Content-Type": "application/json"})
    if proxy:
        session.proxies = dict(http=proxy, https=proxy)
    return session
