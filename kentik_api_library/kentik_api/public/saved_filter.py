from dataclasses import dataclass
from typing import Optional, List

from kentik_api.public.types import ID


@dataclass()
class Filter:
    filterField: str
    filterValue: str
    operator: str
    id: Optional[ID] = None


@dataclass()
class FilterGroups:
    def __init__(
        self,
        connector: str,
        filters: List[Filter],
        not_: bool,
        filterString: Optional[str] = None,
        id: Optional[ID] = None,
        metric: Optional[str] = None,
    ) -> None:
        self.connector = connector
        self.filters = filters
        setattr(self, "not", not_)
        self.filterString = filterString
        self.id = id
        self.metric = metric

    @property
    def not_(self) -> bool:
        return getattr(self, "not")

    @not_.setter
    def not_(self, not_: bool) -> None:
        setattr(self, "not", not_)


@dataclass()
class Filters:
    connector: str
    filterGroups: List[FilterGroups]
    custom: Optional[bool] = None
    filterString: Optional[str] = None


# pylint: disable=too-many-instance-attributes


@dataclass()
class SavedFilter:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        company_id: Optional[ID] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        filter_description: Optional[str] = None,
        filter_level: Optional[str] = None,
        filter_name: Optional[str] = None,
        filters: Optional[Filters] = None,
        id: Optional[ID] = None,
    ) -> None:
        self.filter_description = filter_description
        self.filter_level = filter_level
        self.filter_name = filter_name
        self.filters = filters

        self._created_date = created_date
        self._updated_date = updated_date
        self._id = id
        self._company_id = company_id

    # pylint: enable=too-many-arguments
    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date

    @property
    def id(self) -> ID:
        assert self._id is not None
        return self._id

    @property
    def company_id(self) -> ID:
        assert self._company_id is not None
        return self._company_id


# pylint: enable=too-many-instance-attributes
