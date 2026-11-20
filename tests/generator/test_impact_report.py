# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The impact report's classification: it decides what a reviewer looks at first."""

from __future__ import annotations

import pytest

from scripts.impact_report import classify, floor_check, is_toolchain_only

TOOLCHAIN_DIFF = """\
--- a/src/kentik_api/gen/device/pb/device_pb2.py
+++ b/src/kentik_api/gen/device/pb/device_pb2.py
@@ -2 +2 @@
-# Protobuf Python Version: 6.33.5
+# Protobuf Python Version: 7.35.1
@@ -15,3 +15,3 @@
-    6,
-    33,
-    5,
+    7,
+    35,
+    1,
"""

CONTENT_DIFF = TOOLCHAIN_DIFF + "+_globals['_DEVICE']._serialized_start=123\n"


def test_version_stamp_only_diff_is_toolchain_churn():
    assert is_toolchain_only(TOOLCHAIN_DIFF)
    assert is_toolchain_only(
        '-GRPC_GENERATED_VERSION = "1.81.1"\n+GRPC_GENERATED_VERSION = "1.84.0"\n'
    )


def test_any_other_changed_line_is_content():
    assert not is_toolchain_only(CONTENT_DIFF)


def test_empty_diff_is_not_toolchain_churn():
    assert not is_toolchain_only("")


@pytest.mark.parametrize(
    ("path", "kind"),
    [
        ("src/kentik_api/gen/alerting/models/Suppression.py", "models"),
        ("src/kentik_api/gen/alerting/services/alerting.py", "services"),
        ("src/kentik_api/gen/alerting/error/__init__.py", "errors"),
        ("src/kentik_api/gen/alerting/README.md", "docs"),
        ("src/kentik_api/client_mixin.py", "mount"),
        ("docs/sphinx/services/alerting.md", "docs"),
        ("api_surface.json", "surface"),
        ("src/kentik_api/core/rest_runtime.py", "other"),
        ("CHANGELOG.md", "other"),
    ],
)
def test_classify(path, kind):
    assert classify(path) == kind


def test_classify_pb_by_its_diff():
    path = "src/kentik_api/gen/device/pb/device_pb2.py"
    assert classify(path, TOOLCHAIN_DIFF) == "pb-toolchain"
    assert classify(path, CONTENT_DIFF) == "pb"


def test_floor_check_flags_a_floor_below_gencode():
    surface = {
        "gencode": {"grpcio": "1.84.0", "protobuf": "7.35.1"},
        "requirements": {"grpcio": "grpcio>=1.78.0", "protobuf": "protobuf>=7.35.1,<8"},
    }
    grpcio, protobuf = floor_check(surface)
    assert "NOT covered" in grpcio
    assert "covered" in protobuf and "NOT" not in protobuf


def test_floor_check_flags_an_undeclared_package():
    (line,) = floor_check({"gencode": {"protobuf": "7.35.1"}, "requirements": {}})
    assert "not declared" in line and "NOT covered" in line
