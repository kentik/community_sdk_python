
def test_kentik_api_clinet_import():
    # Given
    kentik_api_library_found = False

    # When
    try:
        import kentik_api_library
    except ImportError:
        pass
    else:
        kentik_api_library_found = True
    assert kentik_api_library_found
