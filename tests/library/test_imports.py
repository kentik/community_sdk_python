import importlib
import sys


def try_import_library(library: str) -> None:
    error = None
    try:
        _ = importlib.import_module(library)
    except ImportError as err:
        error = err

    assert error is None, f"Can't import '{library}': {error}"


if __name__ == "__main__":
    try_import_library(sys.argv[1])
