# pylint: disable=redefined-outer-name
"""
Examples of using the typed custom applications API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, CustomApplication

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud():
    """
    Expected response is like:

    ### CREATE
    {'name': 'apitest-customapp-1', 'description': 'Testing custom application api', 'ip_range': '192.168.0.1,192.168.0.2', 'protocol': '6,17', 'port': '9001,9002,9003', 'asn': 'asn1,asn2,asn3', '_id': 211, '_company_id': '74333', '_user_id': '144319', '_cdate': None, '_edate': None}

    ### UPDATE
    {'name': 'apitest-customapp-ONE', 'description': 'Updated description', 'ip_range': '192.168.0.1,192.168.0.2', 'protocol': '6,17', 'port': '1023', 'asn': 'asn1,asn2,asn3', '_id': 211, '_company_id': '74333', '_user_id': '144319', '_cdate': '2020-12-11T12:10:12.853Z', '_edate': '2020-12-11T12:10:12.853Z'}

    ### DELETE
    True
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE")
    app = CustomApplication(
        name="apitest-customapp-1",
        description="Testing custom application api",
        ip_range="192.168.0.1,192.168.0.2",
        protocol="6,17",
        port="9001,9002,9003",
        asn="asn1,asn2,asn3",
    )
    created = client.custom_applications.create(app)
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.name = "apitest-customapp-ONE"
    created.description = "Updated description"
    created.port = "1023"
    updated = client.custom_applications.update(created)
    print(updated.__dict__)
    print()

    # GET for single custom application item is not available in custom applications api
    # print("### GET")

    print("### DELETE")
    deleted = client.custom_applications.delete(updated.id)
    print(deleted)


def run_list():
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)
    apps = client.custom_applications.get_all()
    for a in apps:
        print(a.__dict__)


if __name__ == "__main__":
    run_crud()
    # run_list()
