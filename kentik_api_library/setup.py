import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="kentik-api",
    version="0.0.1",
    description="API Library to help using Kenti API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kentik/community_sdk_python/tree/main/kentik_api_library",
    licence="GPL-3.0",
    package_dir= {'':'src'},
    include_package_data=True
)
