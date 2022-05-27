from typing import List, Tuple

from .synth_tests import SynTest


def dict_compare(left: dict, right: dict, path: str = "") -> List[Tuple[str, str, str]]:
    def _make_path(p: str, k: str) -> str:
        if not p:
            return k
        return ".".join([p, k])

    diffs = []
    if path is None:
        path = []
    a_keys = set(left.keys())
    b_keys = set(right.keys())
    for k in a_keys.difference(b_keys):
        if left[k]:
            diffs.append((_make_path(path, k), left[k], ""))
    for k in b_keys.difference(a_keys):
        if right[k]:
            diffs.append((_make_path(path, k), "", right[k]))
    for k, vl, vr in [(_k, _v, right[_k]) for _k, _v in left.items() if _k in right]:
        if not isinstance(vl, type(vr)) and not isinstance(vr, type(vl)):
            diffs.append((_make_path(path, k), f"not comparable {type(vl)}", f"{type(vr)}"))
        else:
            if isinstance(vl, dict):
                diffs.extend(dict_compare(vl, vr, _make_path(path, k)))
            else:
                if vl != vr:
                    diffs.append((_make_path(path, k), f"{vl}", f"{vr}"))
    return diffs


def compare_tests(left: SynTest, right: SynTest) -> List[Tuple[str, str, str]]:
    return dict_compare(left.to_dict(), right.to_dict())
