import time
from typing import Any

from kentik_api.public.errors import IntermittentError
from kentik_api.throttling.cmd import Cmd


def active_wait_retry(cmd: Cmd, num_attempts: int, retry_delay_seconds: float) -> Any:
    """ active_wait_retry enables retrying command in an active-waiting manner """

    last_error: Exception
    for _ in range(num_attempts):
        try:
            result = cmd.execute()
            return result
        except IntermittentError as err:
            last_error = err
            time.sleep(retry_delay_seconds)

    raise last_error
