# pylint: disable=redefined-outer-name
"""
Example of using the saved filters API
"""

import logging

from examples.utils import pretty_print
from kentik_api import Filter, FilterGroups, Filters, KentikAPI, SavedFilter
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_saved_filters = client.saved_filters.get_all()
    pretty_print(all_saved_filters)
    print()

    print("### CREATE")
    filter_ = Filter(filterField="dst_as", filterValue="81", operator="=")
    filter_groups = [FilterGroups(connector="All", not_=False, filters=[filter_])]
    filters = Filters(connector="All", filterGroups=filter_groups)
    to_create = SavedFilter(
        filter_name="test_filter1",
        filters=filters,
        filter_description="This is test filter description",
    )
    created = client.saved_filters.create(to_create)
    created_id = created.id
    pretty_print(created)
    print()

    print("### UPDATE")
    to_update = created
    to_update.filter_description = "Updated Saved Filter description"
    got = client.saved_filters.update(to_update)
    pretty_print(got)
    print()

    print("### GET")
    got = client.saved_filters.get(created_id)
    pretty_print(got)
    print()

    print("### DELETE")
    deleted = client.saved_filters.delete(created_id)
    print(deleted)
    print()


if __name__ == "__main__":
    run_crud()
