from typing import Optional

# pylint: disable=too-many-instance-attributes


class CustomApplication:
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        ip_range: Optional[str] = None,
        protocol: Optional[str] = None,
        port: Optional[str] = None,
        asn: Optional[str] = None,
        id: Optional[int] = None,
        company_id: Optional[str] = None,
        user_id: Optional[str] = None,
        cdate: Optional[str] = None,
        edate: Optional[str] = None,
    ) -> None:
        # read-write
        self.name = name
        self.description = description
        self.ip_range = ip_range
        self.protocol = protocol
        self.port = port
        self.asn = asn

        # read-only
        self._id = id
        self._company_id = company_id
        self._user_id = user_id
        self._cdate = cdate
        self._edate = edate

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    @property
    def company_id(self) -> Optional[str]:
        return self._company_id

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @property
    def cdate(self) -> Optional[str]:
        return self._cdate

    @property
    def edate(self) -> Optional[str]:
        return self._edate


# pylint: enable=too-many-instance-attributes
