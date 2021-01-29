from unittest.mock import create_autospec
import pytest

from kentik_api.public.errors import IntermittentError
from kentik_api.throttling.cmd import Cmd
from kentik_api.throttling.active_wait_retry import active_wait_retry


FAIL = IntermittentError("fail, try again")
SUCCESS = "expected_cmd_call_result"


def test_retry_execute_cmd_success() -> None:
    # given
    cmd = create_autospec(Cmd)
    cmd.execute.return_value = SUCCESS

    # when
    result = active_wait_retry(cmd=cmd, num_attempts=1, retry_delay_seconds=0.0)

    # then
    assert cmd.execute.call_count == 1
    assert result == SUCCESS


def test_retry_execute_cmd_3x_retry_success() -> None:
    # given
    cmd = create_autospec(Cmd)
    cmd.execute.side_effect = [FAIL, FAIL, SUCCESS]

    # when
    result = active_wait_retry(cmd=cmd, num_attempts=3, retry_delay_seconds=0.0)

    # then
    assert cmd.execute.call_count == 3
    assert result == SUCCESS


def test_retry_execute_cmd_2x_retry_abort() -> None:
    # given
    cmd = create_autospec(Cmd)
    cmd.execute.side_effect = [FAIL, FAIL, SUCCESS]

    # when
    with pytest.raises(IntermittentError) as ctx:
        active_wait_retry(cmd=cmd, num_attempts=2, retry_delay_seconds=0.0)

    # then
    assert cmd.execute.call_count == 2
    assert ctx.value == FAIL


def test_retry_execute_cmd_3x_retry_abort() -> None:
    # given
    cmd = create_autospec(Cmd)
    cmd.execute.side_effect = [FAIL, FAIL, FAIL]

    # when
    with pytest.raises(IntermittentError) as ctx:
        active_wait_retry(cmd=cmd, num_attempts=3, retry_delay_seconds=0.0)

    # then
    assert cmd.execute.call_count == 3
    assert ctx.value == FAIL
