from distutils.cmd import Command
from distutils import log
import os
import pathlib
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def run_cmd(cmd, reporter) -> None:
    """Run arbitrary command as subprocess"""
    reporter("Run command: {}".format(str(cmd)), level=log.DEBUG)
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as ex:
        reporter(str(ex), level=log.ERROR)
        exit(1)


class Pylint(Command):
    """Custom command to run Pylint"""

    description = "run Pylint on kentik_api, tests and examples directories; read configuration from pyproject.toml"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        cmd = ["pylint"]
        paths = ["kentik_api", "tests", "examples"]
        for path in paths:
            cmd.append(path)
        run_cmd(cmd, self.announce)


class Mypy(Command):
    """Custom command to run Mypy"""

    description = "run Mypy on kentik_api, tests and examples directories; read configuration from pyproject.toml"
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
        run_cmd(cmd, self.announce)


class Pytest(Command):
    """Custom command to run pytest"""

    description = "run pytest on all relevant code; read configuration from pyproject.toml"
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command"""
        cmd = ["pytest"]
        run_cmd(cmd, self.announce)


class Format(Command):
    """Custom command to run black + isort"""

    description = "run black and isort on all relevant code; read configuration from pyproject.toml"
    user_options = [("dirs=", None, "Directories to check"), ("check", None, "Run in check mode")]

    def initialize_options(self) -> None:
        self.dirs = ["kentik_api", "tests", "examples"]
        self.check = False

    def finalize_options(self):
        """Post-process options."""
        for d in self.dirs:
            assert os.path.exists(d), "Path {} does not exist.".format(d)

    def run(self):
        """Run command"""
        self._black()
        self._isort()

    def _black(self) -> None:
        print("Tool: black")
        cmd = ["black"]
        if self.check:
            cmd.append("--check")
        for d in self.dirs:
            cmd.append(d)
        run_cmd(cmd, self.announce)

    def _isort(self) -> None:
        print("Tool: isort")
        cmd = ["isort"]
        if self.check:
            cmd.append("--check")
        for d in self.dirs:
            cmd.append(d)
        run_cmd(cmd, self.announce)


class FetchGRPCCode(Command):
    """Command copying generate Python gRPC code from source repo."""

    description = "Copy generated Python stubs from source repo"
    user_options = [
        ("repo=", None, "Source repository"),
        ("src-path=", None, "Path to generated Python code within the source repo"),
        ("dst-path=", None, "Destination path in the local source tree"),
    ]

    def initialize_options(self):
        self.repo = "https://github.com/kentik/api-schema-public.git"
        self.src_path = "gen/python"
        self.dst_path = HERE.joinpath("kentik_api").joinpath("generated").as_posix()

    def finalize_options(self):
        pass

    def run(self):
        print("Fetching gRPC generated code")

        import git

        # cleanup destination directory
        shutil.rmtree(self.dst_path, ignore_errors=True)  # ignore "No such file or directory"
        # create destination directory, if it does not exist
        dst = Path(self.dst_path)
        dst.mkdir(parents=True)
        # checkout source repo and copy stubs
        with TemporaryDirectory() as tmp:
            git.Repo.clone_from(self.repo, tmp)
            Path(tmp).joinpath(self.src_path).rename(dst)


def list_packages(root: str) -> List[str]:
    print("Listing packages")

    all_paths = [x[0] for x in os.walk(root)]
    src_paths = [p for p in all_paths if "__" not in p]  # skip __pycache__ and similar
    packages = [".".join(p.split(os.path.sep)) for p in src_paths]
    print(*packages, sep="\n")
    return packages


setup(
    name="kentik-api",
    description="SDK library for Kentik API",
    maintainer="Martin Machacek",
    maintainer_email="martin.machacek@kentik.com",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kentik/community_sdk_python/tree/main/kentik_api_library",
    license="Apache-2.0",
    include_package_data=True,
    python_requires=">=3.8, <4",
    install_requires=[
        "dacite>=1.6.0",
        "requests[socks]>=2.25.0",
        "typing-extensions>=3.7.4.3",
        "urllib3>=1.26.0",
        "protobuf>=3.19.1",
        "grpcio>=1.38.1",
    ],
    tests_require=["httpretty", "pytest", "pylint"],
    extras_require={"analytics": ["pandas>=1.2.4", "pyyaml>=5.4.1", "fastparquet>=0.6.3"]},
    packages=list_packages("kentik_api/"),
    cmdclass={"mypy": Mypy, "pylint": Pylint, "pytest": Pytest, "format": Format, "grpc_stubs": FetchGRPCCode},
    classifiers=["License :: OSI Approved :: Apache Software License"],
)
