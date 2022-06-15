# pylint: disable=redefined-outer-name
"""
Examples of using the typed custom applications API
"""

import logging

from examples.utils import pretty_print
from kentik_api import CustomApplication, KentikAPI
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud():
    email, token = get_credentials()
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
    pretty_print(created)
    print()

    print("### UPDATE")
    created.name = "apitest-customapp-ONE"
    created.description = "Updated description"
    created.port = "1023"
    updated = client.custom_applications.update(created)
    pretty_print(updated)
    print()

    # GET for single custom application item is not available in custom applications api
    # print("### GET")

    print("### DELETE")
    deleted = client.custom_applications.delete(updated.id)
    print(deleted)
    print()


def run_list():
    print("### GET ALL")
    email, token = get_credentials()
    client = KentikAPI(email, token)
    apps = client.custom_applications.get_all()
    pretty_print(apps)
    print()


if __name__ == "__main__":
    run_crud()
    run_list()
