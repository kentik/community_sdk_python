# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

import sys
from pathlib import Path

# Every test layer (generated/, e2e/, ...) shares tests/_discovery.py. Without
# this, pytest's default rootless import mode only puts each test file's own
# directory on sys.path, so `import _discovery` resolves when running
# tests/generated/ in isolation but not tests/e2e/ (or vice versa).
sys.path.insert(0, str(Path(__file__).resolve().parent))
