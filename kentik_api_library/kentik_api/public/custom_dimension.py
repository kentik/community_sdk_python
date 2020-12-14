from typing import Optional, List, Any


class CustomDimension:
    def __init__(
        self,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        type: Optional[str] = None,
        populators: Optional[List[Any]] = None,
        id: Optional[int] = None,
        company_id: Optional[str] = None,
    ) -> None:
        # read-write
        self.name = name  # must start with c_ and be unique even against deleted dimensions (deleted names are retained for 1 year)
        self.display_name = display_name
        self.type = type
        self.populators = populators

        # read-only
        self._id = id
        self._company_id = company_id

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    @property
    def company_id(self) -> Optional[str]:
        return self._company_id
