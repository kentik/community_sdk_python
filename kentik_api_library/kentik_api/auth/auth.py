# Third party imports
from requests.auth import AuthBase

AUTH_EMAIL_KEY: str = "X-CH-Auth-Email"
AUTH_API_TOKEN_KEY: str = "X-CH-Auth-API-Token"


class KentikAuth(AuthBase):
    """Attaches HTTP Kentik Authentication to the given Request object."""

    def __init__(self, auth_email: str, auth_token: str):
        self.auth_email = auth_email
        self.auth_token = auth_token

    def __call__(self, r):
        # modify and return the request
        r.headers[AUTH_EMAIL_KEY] = self.auth_email
        r.headers[AUTH_API_TOKEN_KEY] = self.auth_token
        return r
