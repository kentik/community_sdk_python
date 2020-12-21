# pylint: disable=redefined-outer-name
"""
Example of using the My Kentik Portal API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, Tenant, TenantUser

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_tenants = client.my_kentik_portal.get_all()
    for i in all_tenants:
        print(i.__dict__)
    print()

    print("### CREATE")
    tenant_user_email = "user2@testtenant.com"
    created = client.my_kentik_portal.create_tenant_user(all_tenants[0].id, tenant_user_email)
    print(created.__dict__)
    created_id = created.id
    print()

    print("### DELETE")
    deleted = client.my_kentik_portal.delete_tenant_user(all_tenants[0].id, created_id)
    print(deleted)

    print("### GET")
    got = client.my_kentik_portal.get(all_tenants[0].id)
    print(got.__dict__)
    print()


if __name__ == "__main__":
    run_crud()
