from typing import Any, Callable


class Cmd:
    """Command design pattern - wrap method call into an object for easy queuing and retrying"""

    def __init__(self, method: Callable, **method_params) -> None:
        self._method = method
        self._params = method_params

    def execute(self) -> Any:
        return self._method(**self._params)
