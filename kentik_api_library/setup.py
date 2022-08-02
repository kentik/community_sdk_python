# mypy: ignore-errors
import os
import pathlib
import shutil
import subprocess
from distutils import log
from pathlib import Path
from tempfile import TemporaryDirectory

from setuptools import Command, find_namespace_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Generate list of packages (will be replaced by pyproject.toml [tool.setuptools.packages.find] once support stabilizes)
PACKAGES = find_namespace_packages(HERE.as_posix(), exclude=("build*", "dist*", "tests*", "examples*"))


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


# noinspection PyAttributeOutsideInit
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


# noinspection PyAttributeOutsideInit
class Format(Command):
    """Custom command to run black + isort"""

    description = "run black and isort on all relevant code; read configuration from pyproject.toml"
    user_options = [
        ("dirs=", None, "Directories to check"),
        ("check", None, "Run in check mode"),
    ]

    def initialize_options(self) -> None:
        self.dirs = ["kentik_api", "tests", "examples", "setup.py"]
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


# noinspection PyAttributeOutsideInit
class GenerateGRPCStubs(Command):
    """Generate Python gRPC stubs from proto files in the source repo."""

    description = "Generate Python stubs from proto files in the source repo"
    user_options = [
        ("repo=", None, "Source repository"),
    ]

    def initialize_options(self):
        self.repo = "https://github.com/kentik/api-schema-public.git"

    def finalize_options(self):
        pass

    def run(self):
        import git

        def _make_python_pkg(directory):
            directory.joinpath("__init__.py").write_text("")
            for entry in directory.glob("*"):
                if entry.is_dir():
                    _make_python_pkg(entry)

        dst_path = HERE.joinpath("kentik_api").joinpath("generated").as_posix()
        apis = [
            dict(name="core", version="v202012alpha1"),
            dict(name="synthetics", version="v202202"),
            dict(name="cloud_export", version="v202101beta1"),
        ]
        print(f"Building gRPC stubs from proto files in {self.repo}")
        print("for following Kentik APIs:")
        for a in apis:
            print(f"\t{a['name']}/{a['version']}")

        deps = ["protovendor/github.com/googleapis/googleapis", "protovendor/github.com/grpc-ecosystem/grpc-gateway"]
        # cleanup destination directory
        shutil.rmtree(dst_path, ignore_errors=True)  # ignore "No such file or directory"
        # create destination directory, if it does not exist
        dst = Path(dst_path)
        dst.mkdir(parents=True)
        # checkout source repo and copy stubs
        with TemporaryDirectory() as tmp:
            git.Repo.clone_from(self.repo, tmp)
            cmd = [
                "python",
                "-m",
                "grpc_tools.protoc",
                f"--python_out={dst.as_posix()}",
                f"--grpc_python_out={dst.as_posix()}",
                f"-I{tmp}/proto/",
            ]
            for d in deps:
                cmd.append(
                    f"-I{tmp}/{d}/",
                )
            for d in deps:
                for f in Path(f"{tmp}").joinpath(d).glob("**/*.proto"):
                    cmd.append(f.as_posix())
            for a in apis:
                for f in Path(f"{tmp}/proto/kentik/").joinpath(a["name"]).joinpath(a["version"]).glob("*.proto"):
                    cmd.append(f.as_posix())
            run_cmd(cmd, self.announce)
            # _make_python_pkg(dst)


class PrintPackages(Command):
    """Print list of packages included in the build"""

    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self):
        print(*sorted(PACKAGES), sep="\n")


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
        "protobuf==3.20.1",
        "grpcio>=1.47.0",
    ],
    tests_require=["httpretty", "pytest", "pylint"],
    extras_require={"analytics": ["pandas>=1.2.4", "pyyaml>=5.4.1", "fastparquet>=0.6.3"]},
    # packages=PACKAGES,
    cmdclass={
        "mypy": Mypy,
        "pylint": Pylint,
        "pytest": Pytest,
        "format": Format,
        "grpc_stubs": GenerateGRPCStubs,
        "packages": PrintPackages,
    },
    classifiers=["License :: OSI Approved :: Apache Software License"],
)
