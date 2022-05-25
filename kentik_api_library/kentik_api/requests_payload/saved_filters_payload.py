from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.saved_filter import Filter, FilterGroups, Filters, SavedFilter
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, convert_or_none, dict_from_json, from_dict, list_from_json

# pylint: disable=too-many-instance-attributes


@dataclass
class SavedFilterPayload:

    filter_description: Optional[str] = None
    filter_name: Optional[str] = None
    filters: Optional[Filters] = None

    @staticmethod
    def get_filter_groups(filter_groups: List[FilterGroups]) -> List[Dict[str, Any]]:
        return [
            {
                "connector": i.connector,
                "filters": [
                    {
                        "filterField": j.filterField,
                        "filterValue": j.filterValue,
                        "operator": j.operator,
                    }
                    for j in i.filters
                ],
                "not": i.not_,
            }
            for i in filter_groups
        ]

    @classmethod
    def from_saved_filter(cls, saved_filter: SavedFilter):
        filters = None
        if saved_filter.filters:
            filters_dict = {
                "connector": saved_filter.filters.connector,
                "filterGroups": SavedFilterPayload.get_filter_groups(saved_filter.filters.filterGroups),
            }
            filters = Filters.from_dict(filters_dict)
        return cls(
            filter_name=saved_filter.filter_name,
            filter_description=saved_filter.filter_description,
            filters=filters,
        )


@dataclass()
class GetResponse:
    id: int
    company_id: str
    filters: Optional[Dict] = None
    filter_name: Optional[str] = None
    filter_description: Optional[str] = None
    cdate: Optional[str] = None
    edate: Optional[str] = None
    filter_level: Optional[str] = None

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, dic)

    def to_saved_filter(self) -> SavedFilter:
        filters_obj = self._to_filters(deepcopy(self.filters))
        return SavedFilter(
            company_id=convert(self.company_id, ID),
            created_date=self.cdate,
            updated_date=self.edate,
            filter_description=self.filter_description,
            filter_level=self.filter_level,
            filter_name=self.filter_name,
            filters=filters_obj,
            id=convert(self.id, ID),
        )

    def _to_filters(self, dic) -> Filters:
        dic["filterGroups"] = [self._to_filtergroups(group) for group in dic["filterGroups"]]
        return from_dict(Filters, dic)

    def _to_filtergroups(self, dic) -> FilterGroups:
        filters = [self._to_filter(ftr) for ftr in dic["filters"]]
        return FilterGroups(
            connector=dic["connector"],
            filterString=dic.get("filterString"),
            filters=filters,
            id=convert_or_none(dic.get("id"), ID),
            metric=dic.get("metric"),
            not_=convert(dic["not"], bool),
        )

    def _to_filter(self, dic) -> Filter:
        dic["id"] = convert_or_none(dic.get("id"), ID)
        return from_dict(Filter, dic)


# pylint: enable=too-many-instance-attributes


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string)
        saved_filters = cls()
        for item in items:
            saved_filter = from_dict(GetResponse, item)
            saved_filters.append(saved_filter)
        return saved_filters

    def to_saved_filters(self) -> List[SavedFilter]:
        return [ftr.to_saved_filter() for ftr in self]


@dataclass
class CreateRequest:

    saved_filter: SavedFilterPayload

    @classmethod
    def from_custom_application(cls, saved_filter: SavedFilter):
        validate(saved_filter, "Create")
        return SavedFilterPayload.from_saved_filter(saved_filter)


CreateResponse = GetResponse


@dataclass
class UpdateRequest:

    saved_filter: SavedFilterPayload

    @classmethod
    def from_custom_application(cls, saved_filter: SavedFilter):
        validate(saved_filter, "Update")
        return SavedFilterPayload.from_saved_filter(saved_filter)


UpdateResponse = GetResponse


def validate(saved_filter: SavedFilter, operation: str):
    class_name = saved_filter.__class__.__name__
    if operation == "Update":
        if saved_filter.id is None:
            raise IncompleteObjectError(operation, class_name, "ID has to be provided")
    if saved_filter.filter_name is None:
        raise IncompleteObjectError(operation, class_name, "filter must have name")
    if saved_filter.filters is not None:
        if saved_filter.filters.connector is None:
            raise IncompleteObjectError(operation, class_name, "connector is required")
        if not all(i.connector is not None for i in saved_filter.filters.filterGroups):
            raise IncompleteObjectError(operation, class_name, "filterGroups connector is required")
        if not all(i.not_ is not None for i in saved_filter.filters.filterGroups):
            raise IncompleteObjectError(operation, class_name, "not_ is required")
