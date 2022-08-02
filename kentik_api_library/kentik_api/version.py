# noinspection PyProtectedMember
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("kentik_api")
except PackageNotFoundError:
    __version__ = "dev-unknown"


def get_user_agent() -> str:
    return f"kentik_community_sdk_python/{__version__}"
