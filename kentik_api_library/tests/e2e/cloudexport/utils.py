import os

from kentik_api import KentikAPI
from kentik_api.utils import get_credentials

credentials_missing_str = (
    "KTAPI_AUTH_EMAIL, KTAPI_AUTH_TOKEN and KTAPI_PLAN_ID env variables are required to run the test"
)
credentials_present = (
    "KTAPI_AUTH_EMAIL" in os.environ and "KTAPI_AUTH_TOKEN" in os.environ and "KTAPI_PLAN_ID" in os.environ
)


def client() -> KentikAPI:
    """Get KentikAPI client"""

    email, token = get_credentials()
    return KentikAPI(email, token)
