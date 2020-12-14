from dataclasses import dataclass
from typing import Optional, List


@dataclass()
class Filter:
    filterField: str
    id: Optional[str]
    filterValue: str
    operator: str


@dataclass()
class FilterGroups:
    connector: str
    filterString: Optional[str]
    filters: List[Filter]
    id: Optional[str]
    metric: str
    _not: bool


@dataclass()
class Filters:
    connector: str
    custom: bool
    filterGroups: List[FilterGroups]
    filterString: Optional[str]


class SavedFilter:
    def __init__(
            self,
            cdate: Optional[str] = None,
            company_id: Optional[int] = None,
            edate: Optional[str] = None,
            filter_description: Optional[str] = None,
            filter_level: Optional[str] = None,
            filter_name: Optional[str] = None,
            filters: Optional[Filters] = None,
            id: Optional[int] = None,
    ) -> None:
        self.filter_description = filter_description
        self.filter_level = filter_level
        self.filter_name = filter_name
        self.filters = filters

        self._cdate = cdate
        self._edate = edate
        self._id = id
        self._company_id = company_id

    @property
    def cdate(self) -> Optional[str]:
        return self._cdate

    @property
    def edate(self) -> Optional[str]:
        return self._edate

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    @property
    def company_id(self) -> int:
        assert self._company_id is not None
        return self._company_id
