from dataclasses import dataclass
from typing import Dict, List, Optional, Type, TypeVar

from kentik_api.internal.dataclass import mandatory_dataclass_attributes
from kentik_api.public.types import ID

FilterGroupsType = TypeVar("FilterGroupsType", bound="FilterGroups")
FiltersType = TypeVar("FiltersType", bound="Filters")
SavedFilterType = TypeVar("SavedFilterType", bound="SavedFilter")


@dataclass()
class Filter:
    filterField: str
    filterValue: str
    operator: str
    id: Optional[ID] = None


# noinspection PyShadowingBuiltins
# noinspection PyPep8Naming
@dataclass()
class FilterGroups:
    @classmethod
    def from_dict(cls: Type[FilterGroupsType], data: Dict) -> FilterGroupsType:
        """
        Construct FilterGroup based on data in a dictionary
        :param data: dictionary
        :return: instance of FilterGroups
        """
        # check presence of mandatory attributes
        missing = [a for a in ("connector", "filters") if a not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        # construct list of Filters
        _d = dict()
        _d.update(data)
        if "not" in data:
            _d["not_"] = data["not"]
            del _d["not"]
        _d["filters"] = [Filter(**f) for f in data["filters"]]
        filter_groups = data.get("filterGroups")
        if filter_groups:
            _d["filterGroups"] = [cls.from_dict(f) for f in data["filterGroups"]]
        saved_filters = data.get("saved_filtes")
        if saved_filters:
            _d["saved_filters"] = [SavedFilter.from_dict(f) for f in data["saved_filters"]]
        return cls(**_d)

    def __init__(
        self,
        connector: str,
        filters: List[Filter],
        not_: bool = False,
        filterString: Optional[str] = None,
        id: Optional[ID] = None,
        metric: Optional[str] = None,
        name: Optional[str] = None,
        named: Optional[bool] = False,
        autoAdded: Optional[str] = None,
        filterGroups: Optional[FilterGroupsType] = None,
        saved_filters: Optional[SavedFilterType] = None,
    ) -> None:
        self.connector = connector
        self.filters = filters
        setattr(self, "not", not_)
        self.filterString = filterString
        self.id = id
        self.metric = metric
        self.name = name
        self.named = named
        self.autoAdded = autoAdded
        self.filterGroups = filterGroups
        self.saved_filters = saved_filters

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

    @classmethod
    def from_dict(cls: Type[FiltersType], data: Dict) -> FiltersType:
        """
        Construct Filters object based on data in a dictionary. The dictionary must provide values for all mandatory
        Filters fields
        :param data: dictionary
        :return: instance of Filters
        """
        # verify that values are provided for all mandatory fields
        missing = [field_name for field_name in mandatory_dataclass_attributes(cls) if field_name not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        # construct list of FilterGroups
        _d = dict()
        _d.update(data)
        _d["filterGroups"] = [FilterGroups.from_dict(f) for f in data["filterGroups"]]
        return cls(**_d)


# noinspection PyShadowingBuiltins
# pylint: disable=too-many-instance-attributes
@dataclass()
class SavedFilter:
    @classmethod
    def from_dict(cls: Type[SavedFilterType], data: Dict) -> SavedFilterType:
        """
        Construct SavedFilter object based on data in a dictionary. The dictionary must provide values for all mandatory
        SavedFilter fields
        :param data: dictionary
        :return: instance of SavedFilter
        """
        # verify that values are provided for all mandatory fields
        missing = [field_name for field_name in mandatory_dataclass_attributes(cls) if field_name not in data]
        if missing:
            raise RuntimeError(f"{cls.__name__}.from_dict: missing mandatory fields: {missing}")
        # construct list of Filters
        _d = dict()
        _d.update(data)
        if "filters" in data:
            _d["filters"] = [Filters.from_dict(f) for f in data["filters"]]
        return cls(**_d)

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
