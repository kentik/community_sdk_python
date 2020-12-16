from dataclasses import dataclass
import json
from typing import Optional, Dict, List, Any

from kentik_api.public.saved_filter import SavedFilter, Filters, FilterGroups, Filter


@dataclass()
class GetResponse:
    id: Optional[int] = None
    company_id: Optional[int] = None
    filters: Optional[Dict] = None
    filter_name: Optional[str] = None
    filter_description: Optional[str] = None
    cdate: Optional[str] = None
    edate: Optional[str] = None
    filter_level: Optional[str] = None

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_saved_filter(self) -> SavedFilter:
        filters_obj = self._to_filters(self.filters)
        return SavedFilter(
            cdate=self.cdate,
            company_id=self.company_id,
            edate=self.edate,
            filter_description=self.filter_description,
            filter_level=self.filter_level,
            filter_name=self.filter_name,
            filters=filters_obj,
            id=self.id,
        )

    def _to_filters(self, dic) -> Filters:
        filter_groups = [self._to_filtergroups(group) for group in dic["filterGroups"]]
        return Filters(
            connector=dic["connector"],
            custom=dic.get("custom"),
            filterGroups=filter_groups,
            filterString=dic.get("filterString"),
        )

    def _to_filtergroups(self, dic) -> FilterGroups:
        filters = [self._to_filter(ftr) for ftr in dic["filters"]]
        return FilterGroups(
            connector=dic["connector"],
            filterString=dic.get("filterString"),
            filters=filters,
            id=dic.get("id"),
            metric=dic.get("metric"),
            not_=dic["not"],
        )

    def _to_filter(self, dic) -> Filter:
        return Filter(
            filterField=dic["filterField"],
            filterValue=dic["filterValue"],
            operator=dic["operator"],
            id=dic.get("id"),
        )


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        saved_filters = cls()
        for item in dic:
            saved_filter = GetResponse(**item)
            saved_filters.append(saved_filter)
        return saved_filters

    def to_saved_filters(self) -> List[SavedFilter]:
        return [ftr.to_saved_filter() for ftr in self]


class CreateRequest:
    def __init__(
            self,
            saved_filter: SavedFilter,
    ) -> None:
        self.filter_name = saved_filter.filter_name
        self.filter_description = saved_filter.filter_description
        self.filters = {
                "connector": saved_filter.filters.connector,
                "filterGroups": CreateRequest.get_filter_groups(saved_filter.filters.filterGroups)
            } if saved_filter.filters is not None else None

    @staticmethod
    def get_filter_groups(filter_groups: List[FilterGroups]) -> List[Dict[str, Any]]:
        return [{
            "connector": i.connector,
            "filters": [{
                "filterField": j.filterField,
                "filterValue": j.filterValue,
                "operator": j.operator
            } for j in i.filters],
            "not": i.not_
        } for i in filter_groups]


CreateResponse = GetResponse

UpdateRequest = CreateRequest
UpdateResponse = GetResponse
