import logging
from typing import Any, Optional


class DebugOut:
    def __init__(self, logger: logging.Logger, output: str) -> None:
        self.logger = logger
        self.output = output
        self.orig_handler: Optional[logging.Handler] = None
        self.orig_level: Optional[int] = None

    def __enter__(self) -> None:
        self.logger.debug("Switching log output to: %s", self.output)
        self.orig_handler = self.logger.handlers[0]
        self.orig_level = self.logger.getEffectiveLevel()
        self.logger.removeHandler(self.logger.handlers[0])
        if type(self.output) == str:
            self.logger.addHandler(logging.FileHandler(self.output))
        else:
            self.logger.addHandler(logging.StreamHandler(self.output))
        self.logger.setLevel(logging.DEBUG)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.logger.debug("Restoring logger settings: handler: %s, level: %s", self.orig_handler, self.orig_level)
        self.logger.removeHandler(self.logger.handlers[0])
        self.logger.addHandler(self.orig_handler)
        self.logger.setLevel(self.orig_level)
