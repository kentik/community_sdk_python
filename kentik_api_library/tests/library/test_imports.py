
def test_kentik_api_clinet_import():
    # Given
    kentik_api_library_found = False

    # When
    try:
        import kentik_api_library
        kentik_api_library_found = True
    except ImportError:
        pass
    assert kentik_api_library_found == True
