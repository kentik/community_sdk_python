# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Without the analytics extra, analytics fails clearly and the SDK still works (FR-022)."""

from __future__ import annotations

import subprocess
import sys

_SCRIPT = """
import sys

class _HidePandas:
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] in ("pandas", "pyarrow", "yaml"):
            raise ImportError(f"No module named {name!r}")
        return None

sys.meta_path.insert(0, _HidePandas())

import kentik_api
from kentik_api.client import KentikAPI
from kentik_api.v5_tools import split_batch
from kentik_api.devices import DeviceLookup

try:
    import kentik_api.analytics
except ImportError as exc:
    print(exc)
else:
    print("imported")
"""


def test_analytics_without_the_extra_names_the_extra_to_install():
    result = subprocess.run(
        [sys.executable, "-c", _SCRIPT], capture_output=True, text=True, check=True
    )

    assert 'pip install "kentik-api[analytics]"' in result.stdout
    assert "imported" not in result.stdout
