from typing import Optional


class ManualMitigation:
    def __init__(
        self,
        ipCidr: str,
        platformID: str,
        methodId: str,
        minutesBeforeAutoStop: str,
        comment: Optional[str] = None
    ) -> None:
        self.ipCidr = ipCidr
        self.platformID = platformID
        self.methodId = methodId
        self.minutesBeforeAutoStop = minutesBeforeAutoStop
        self.comment = comment
