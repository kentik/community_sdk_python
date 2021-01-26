from kentik_api.throttling.cmd import Cmd


class _TestCalculator:
    def __init__(self, val: int) -> None:
        self._val = val

    def mul(self, multiplier) -> int:
        return self._val * multiplier


def test_cmd_execute_success() -> None:
    # given
    obj = _TestCalculator(val=7)
    cmd = Cmd(method=obj.mul, multiplier=3)

    # when
    result = cmd.execute()
    result = cmd.execute()
    result = cmd.execute()

    # then
    assert result == 21
