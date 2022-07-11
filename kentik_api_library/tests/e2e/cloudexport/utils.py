import os

from kentik_api import KentikAPI
from kentik_api.utils import get_credentials

credentials_missing_str = (
    "KTAPI_AUTH_EMAIL, KTAPI_AUTH_TOKEN and KTAPI_PLAN_ID env variables are required to run the test"
)
credentials_present = all(v in os.environ for v in ("KTAPI_AUTH_EMAIL", "KTAPI_AUTH_TOKEN", "KTAPI_PLAN_ID"))


def client() -> KentikAPI:
    """Get KentikAPI client"""

    email, token = get_credentials()
    return KentikAPI(email, token)
