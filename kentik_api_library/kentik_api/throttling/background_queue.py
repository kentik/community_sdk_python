import time
import logging
from queue import Queue
from threading import Thread
from typing import Callable, Any
from dataclasses import dataclass

from kentik_api.public.errors import IntermittentError
from kentik_api.throttling.cmd import Cmd


SuccessFunc = Callable[[Any, Any], None]  # input: successful cmd execution result, output: none
AbortFunc = Callable[[Any, Exception], None]  # input: exception thrown by cmd, output: none


def nop(*_) -> None:
    """no-operation"""


@dataclass
class BackgroundCmd:
    cmd: Cmd
    num_attempts_total: int
    num_attempts_left: int  # if 3, then this cmd will be attempted 3x execution before throwing it away
    success: SuccessFunc
    abort: AbortFunc


class BackgroundCmdQueue:
    """BackgroundCmdQueue enables retrying of commands in a background-processing manner (in background thread)"""

    def __init__(self, retry_delay_seconds: float = 5.0) -> None:
        self._queue: "Queue[BackgroundCmd]" = Queue()
        self._retry_delay_seconds = retry_delay_seconds
        self._logger = logging.getLogger(__name__)
        Thread(target=self._worker, daemon=True).start()

    def put(self, cmd: Cmd, num_attempts: int = 1, on_success: SuccessFunc = nop, on_abort: AbortFunc = nop) -> None:
        bcmd = BackgroundCmd(
            cmd=cmd,
            num_attempts_total=num_attempts,
            num_attempts_left=num_attempts,
            success=on_success,
            abort=on_abort,
        )
        self._queue.put(bcmd)

    def join(self) -> None:
        self._queue.join()

    def _worker(self) -> None:
        while True:
            self._process_next_item()

    def _process_next_item(self) -> None:
        try:
            item = self._queue.get()
            result = item.cmd.execute()
            item.success(result)
        except IntermittentError as err:
            item.num_attempts_left -= 1
            if item.num_attempts_left > 0:
                self._log_retry(err)
                self._queue.put(item)
                time.sleep(self._retry_delay_seconds)
            else:
                self._log_abort(err, item)
                item.abort(err)
        finally:
            self._queue.task_done()

    def _log_retry(self, err: Exception) -> None:
        self._logger.error('request failed with "%s". Retrying in %0.2f seconds...', err, self._retry_delay_seconds)

    def _log_abort(self, err: Exception, item: BackgroundCmd) -> None:
        self._logger.error('request failed with "%s". Giving up after %d attempts', err, item.num_attempts_total)
