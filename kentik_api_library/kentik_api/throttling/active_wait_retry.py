import time
import logging
from typing import Any

from kentik_api.public.errors import IntermittentError
from kentik_api.throttling.cmd import Cmd

logger = logging.getLogger(__name__)


def active_wait_retry(cmd: Cmd, num_attempts: int, retry_delay_seconds: float) -> Any:
    """active_wait_retry enables retrying command in an active-waiting manner (in main thread)"""

    last_error: Exception
    for num_retries_left in reversed(range(num_attempts)):
        try:
            result = cmd.execute()
            return result
        except IntermittentError as err:
            if num_retries_left > 0:
                logger.error('request failed with "%s". Retrying in %0.2f seconds...', err, retry_delay_seconds)
                last_error = err
                time.sleep(retry_delay_seconds)

    logger.error('request failed with "%s". Giving up after %d attempts', last_error, num_attempts)
    raise last_error
