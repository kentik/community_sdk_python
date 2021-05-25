import distutils.cmd
import distutils.log
import os
import pathlib
import subprocess

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PACKAGES = [
    "kentik_api",
    "kentik_api.auth",
    "kentik_api.api_calls",
    "kentik_api.api_connection",
    "kentik_api.api_resources",
    "kentik_api.requests_payload",
    "kentik_api.public",
]
PACKAGE_DIR = {
    "kentik_api": "kentik_api",
    "kentik_api.auth": "kentik_api/auth",
    "kentik_api.api_calls": "kentik_api/api_calls",
    "kentik_api.api_connection": "kentik_api/api_connection",
    "kentik_api.api_resources": "kentik_api/api_resources",
    "kentik_api.requests_payload": "kentik_api/requests_payload",
    "kentik_api.public": "kentik_api/public",
}


class PylintCmd(distutils.cmd.Command):
    """Custom command to run Pylint"""

    description = "run Pylint on src, tests and examples dir"
    user_options = [
        ("pylint-rcfile=", None, "path to Pylint config file"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        self.pylint_rcfile = ""

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), "Pylint config file {} does not exist.".format(
                self.pylint_rcfile
            )

    def run(self):
        """Run command."""
        cmd = ["pylint"]
        paths = ["./kentik_api", "./tests", "./examples"]
        if self.pylint_rcfile:
            cmd.append("--rcfile={}".format(self.pylint_rcfile))
        for path in paths:
            cmd.append(path)
        self.announce("Running command: %s" % str(cmd), level=distutils.log.INFO)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            pass


class MypyCmd(distutils.cmd.Command):
    """Custom command to run Mypy"""

    description = "run Mypy on kentik_api directory"
    user_options = [("packages=", None, "Packages to check with mypy")]

    def initialize_options(self):
        """Set default values for option packages"""
        self.packages = ["kentik_api", "tests", "examples"]

    def finalize_options(self):
        """Post-process options."""
        for package in self.packages:
            assert os.path.exists(package), "Path {} does not exist.".format(package)

    def run(self):
        """Run command"""
        cmd = ["mypy"]
        for package in self.packages:
            cmd.append(package)
        self.announce("Run command: {}".format(str(cmd)), level=distutils.log.INFO)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            self.announce(
                "Command: {} returned error. Check if tests are not failing.".format(str(cmd)), level=distutils.log.INFO
            )


setup(
    name="kentik-api",
    use_scm_version={
        "root": "..",
        "relative_to": __file__,
    },
    description="SDK library for Kentik API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kentik/community_sdk_python/tree/main/kentik_api_library",
    license="Apache-2.0",
    include_package_data=True,
    install_requires=["requests>=2.25.0", "typing-extensions>=3.7.4.3", "dacite>=1.6.0"],
    setup_requires=["pytest-runner", "pylint-runner", "setuptools_scm"],
    tests_require=["httpretty", "pytest", "pylint"],
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    cmdclass={"pylint": PylintCmd, "mypy": MypyCmd},
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
)
