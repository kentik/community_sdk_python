from typing import List, Tuple

from .synth_tests import SynTest


def dict_compare(left: dict, right: dict, path: str = "") -> List[Tuple[str, str]]:
    diffs = []
    if path is None:
        path = []
    a_keys = set(left.keys())
    b_keys = set(right.keys())
    for k in a_keys.difference(b_keys):
        diffs.append((f"{path}.{k}", "<missing in left>"))
    for k in b_keys.difference(a_keys):
        diffs.append((f"{path}.{k}", "<missing in right>"))
    for k, vl, vr in [(_k, _v, right[_k]) for _k, _v in left.items() if _k in right]:
        if not isinstance(vl, type(vr)) and not isinstance(vr, type(vl)):
            diffs.append((f"{path}.{k}", f"incompatible types (left: {type(vl)} right: {type(vr)})"))
        else:
            if isinstance(vl, dict):
                diffs.extend(dict_compare(vl, vr, f"{path}.{k}"))
            else:
                if vl != vr:
                    diffs.append((f"{path}.{k}", f"different value (left: {vl} right: {vr})"))
    return diffs


def compare_tests(left: SynTest, right: SynTest) -> List[Tuple[str, str]]:
    return dict_compare(left.to_dict(), right.to_dict())
