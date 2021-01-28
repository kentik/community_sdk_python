from unittest.mock import create_autospec, Mock

from kentik_api.public.errors import IntermittentError
from kentik_api.throttling.cmd import Cmd
from kentik_api.throttling.background_queue import BackgroundCmdQueue

FAIL = IntermittentError("fail, try again")
SUCCESS = "expected_cmd_call_result"


def test_queue_execute_cmd_success() -> None:
    # given
    queue = BackgroundCmdQueue()
    cmd = create_autospec(Cmd)
    cmd.execute.return_value = True

    # when
    queue.put(cmd=cmd)
    queue.join()

    # then
    assert cmd.execute.call_count == 1


def test_queue_execute_cmd_success_success() -> None:
    # given
    queue = BackgroundCmdQueue()
    cmd = create_autospec(Cmd)
    cmd.execute.return_value = SUCCESS
    success = Mock()

    # when
    queue.put(cmd=cmd, on_success=success)
    queue.join()

    # then
    assert cmd.execute.call_count == 1
    assert success.call_count == 1
    success.assert_called_with(SUCCESS)


def test_queue_execute_cmd_failure_abort() -> None:
    # given
    queue = BackgroundCmdQueue()
    cmd = create_autospec(Cmd)
    cmd.execute.side_effect = FAIL
    success = Mock()
    abort = Mock()

    # when
    queue.put(cmd=cmd, on_success=success, on_abort=abort)
    queue.join()

    # then
    assert cmd.execute.call_count == 1
    assert success.call_count == 0
    assert abort.call_count == 1
    abort.assert_called_with(FAIL)


def test_queue_execute_cmd_retry_success() -> None:
    # given
    queue = BackgroundCmdQueue(retry_delay_seconds=0.0)
    cmd = create_autospec(Cmd)
    cmd.execute.side_effect = [FAIL, FAIL, SUCCESS]
    success = Mock()
    abort = Mock()

    # when
    queue.put(cmd=cmd, num_attempts=3, on_success=success, on_abort=abort)
    queue.join()

    # then
    assert cmd.execute.call_count == 3
    assert success.call_count == 1
    success.assert_called_with(SUCCESS)
    assert abort.call_count == 0


def test_queue_execute_cmd_retry_abort() -> None:
    # given
    queue = BackgroundCmdQueue(retry_delay_seconds=0.0)
    cmd = create_autospec(Cmd)
    cmd.execute.side_effect = [FAIL, FAIL, FAIL]
    success = create_autospec(Cmd)
    success.execute.return_value = True
    abort = Mock()
    abort.return_value = True

    # when
    queue.put(cmd=cmd, num_attempts=3, on_success=success, on_abort=abort)
    queue.join()

    # then
    assert cmd.execute.call_count == 3
    assert success.call_count == 0
    assert abort.call_count == 1
    abort.assert_called_with(FAIL)
