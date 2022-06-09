# pylint: disable=redefined-outer-name
"""
Examples of using the typed sites API
"""

import logging

from examples.utils import pretty_print
from kentik_api import KentikAPI, Site
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE")
    site = Site(site_name="apitest-site-1", latitude=None, longitude=12)
    created = client.sites.create(site)
    pretty_print(created)
    print()

    print("### UPDATE")
    created.site_name = "apitest-site-one"
    created.latitude = 49
    updated = client.sites.update(created)
    pretty_print(updated)
    print()

    print("### GET")
    got = client.sites.get(updated.id)
    pretty_print(got)
    print()

    print("### DELETE")
    deleted = client.sites.delete(updated.id)
    print(deleted)
    print()


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET ALL")
    sites = client.sites.get_all()
    pretty_print(sites)
    print()


if __name__ == "__main__":
    run_crud()
    run_list()
