import importlib
import sys


def test_import(library: str) -> None:
    error = None
    try:
        _ = importlib.import_module(library)
    except ImportError as err:
        error = err

    assert error is None, f"Can't import '{library}': {error}"


if __name__ == "__main__":
    test_import(sys.argv[1])
