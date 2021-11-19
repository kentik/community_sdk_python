# pylint: skip-file
import sys
import importlib


def test_import(library=""):
    error = None
    try:
        _ = importlib.import_module(library)
    except ImportError as err:
        error = err

    assert error is None, f'Can\'t import "{library}": {error}'


if __name__ == "__main__":
    test_import(sys.argv[1])
