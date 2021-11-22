# pylint: skip-file
import sys
import importlib


def test_import(library=""):

    library_found = False
    error = None
    try:
        imported_library = importlib.import_module(library)
    except ImportError as err:
        error = err
    else:
        library_found = True

    assert library_found, "Can't import '" + library + "': " + str(error)


if __name__ == "__main__":
    test_import(sys.argv[1])
