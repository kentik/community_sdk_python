"""
Legacy fluent API client
"""

# Third party imports
from python_http_client import Client  # type: ignore

BASE_API_COM_URL = "https://api.kentik.com/api"
BASE_API_EU_URL = "https://api.kentik.eu/api"

GLOBAL_HEADERS_TEMPLATE = {
    "X-CH-Auth-Email": None,
    "X-CH-Auth-API-Token": None,
    "Content-Type": "application/json"
}


def get_kentik_client(base_url, auth_email, auth_api_token):
    global_headers = GLOBAL_HEADERS_TEMPLATE
    global_headers["X-CH-Auth-Email"] = auth_email
    global_headers["X-CH-Auth-API-Token"] = auth_api_token
    return Client(host=base_url, request_headers=global_headers)


def get_kentik_com_client(auth_email, auth_api_token):
    return get_kentik_client(BASE_API_COM_URL, auth_email, auth_api_token)


def get_kentik_eu_client(auth_email, auth_api_token):
    return get_kentik_client(BASE_API_EU_URL, auth_email, auth_api_token)
