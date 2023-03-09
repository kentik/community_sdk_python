# pylint: disable=redefined-outer-name
"""
Example of using the My Kentik Portal API
"""

import logging

from examples.utils import pretty_print
from kentik_api import KentikAPI
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_tenants = client.my_kentik_portal.get_all()
    pretty_print(all_tenants)
    print()

    print("### CREATE")
    tenant_user_email = "user2@testtenant.com"
    created = client.my_kentik_portal.create_tenant_user(all_tenants[0].id, tenant_user_email)
    pretty_print(created)
    created_id = created.id
    print()

    print("### DELETE")
    deleted = client.my_kentik_portal.delete_tenant_user(all_tenants[0].id, created_id)
    print(deleted)
    print()

    print("### GET")
    got = client.my_kentik_portal.get(all_tenants[0].id)
    pretty_print(got)
    print()


if __name__ == "__main__":
    run_crud()
