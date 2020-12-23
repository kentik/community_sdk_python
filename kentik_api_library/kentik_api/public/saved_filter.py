from dataclasses import dataclass
from typing import Optional, List


@dataclass()
class Filter:
    filterField: str
    filterValue: str
    operator: str
    id: Optional[str] = None


class FilterGroups:
    def __init__(
        self,
        connector: str,
        filters: List[Filter],
        not_: bool,
        filterString: Optional[str] = None,
        id: Optional[str] = None,
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


class SavedFilter:
    # pylint: disable=too-many-arguments
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

    # pylint: enable=too-many-arguments
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


# pylint: enable=too-many-instance-attributes
