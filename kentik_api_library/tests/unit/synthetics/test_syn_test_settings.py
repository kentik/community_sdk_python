import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.synth_tests.base import SynTestSettings
from kentik_api.synthetics.types import TaskType


def test_skip_ignored_tasks() -> None:
    IGNORED_TASK = "bgp-monitor"

    # given
    pb_settings = pb.TestSettings()
    pb_settings.tasks.append(IGNORED_TASK)

    # when
    settings = SynTestSettings.from_pb(pb_settings)

    # then
    assert len(settings.tasks) == 0


def test_replace_legacy_tasks() -> None:
    LEGACY_TASK = "knock"
    REPLACEMENT_TASK = TaskType.PING

    # given
    pb_settings = pb.TestSettings()
    pb_settings.tasks.append(LEGACY_TASK)

    # when
    settings = SynTestSettings.from_pb(pb_settings)

    # then
    assert REPLACEMENT_TASK in settings.tasks
