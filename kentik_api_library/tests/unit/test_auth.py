from kentik_api.auth.auth import KentikAuth

DUMMY_EMAIL = "dummy@email"
DUMMY_API_TOKEN = "dummy_api_tocen"


def test_auth__return_kentik_auth():
    # GIVEN
    # DUMMY_API_URL, DUMMY_EMAIL

    # WHEN
    auth = KentikAuth(DUMMY_EMAIL, DUMMY_API_TOKEN)

    # THEN
    assert isinstance(auth, KentikAuth)
    assert auth.auth_email == DUMMY_EMAIL
    assert auth.auth_token == DUMMY_API_TOKEN
