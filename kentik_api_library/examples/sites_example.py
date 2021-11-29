# pylint: disable=redefined-outer-name
"""
Examples of using the typed sites API
"""

import logging

from kentik_api import KentikAPI, Site
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Expected response is like:

    ### CREATE
    {'site_name': 'apitest-site-1', 'latitude': None, 'longitude': 12, '_id': 8420, '_company_id': '74333'}

    ### UPDATE
    {'site_name': 'apitest-site-one', 'latitude': 49, 'longitude': 12, '_id': '8420', '_company_id': '74333'}

    ### GET
    {'site_name': 'apitest-site-one', 'latitude': 49, 'longitude': 12, '_id': 8420, '_company_id': 74333}

    ### DELETE
    True
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE")
    site = Site(site_name="apitest-site-1", latitude=None, longitude=12)
    created = client.sites.create(site)
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.site_name = "apitest-site-one"
    created.latitude = 49
    updated = client.sites.update(created)
    print(updated.__dict__)
    print()

    print("### GET")
    got = client.sites.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.sites.delete(updated.id)
    print(deleted)


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)
    sites = client.sites.get_all()
    for s in sites:
        print(s.__dict__)


if __name__ == "__main__":
    run_crud()
    # run_list()
