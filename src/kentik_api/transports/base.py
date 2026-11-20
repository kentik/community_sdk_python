# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from abc import ABC, abstractmethod


class BaseTransport(ABC):
    @abstractmethod
    def close(self):
        pass
