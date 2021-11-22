import distutils.cmd
import distutils.log
import os
import pathlib
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from setuptools import setup
from setuptools.command.install import install

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PACKAGES = [
    "generated",
    "kentik_api",
    "kentik_api.analytics",
    "kentik_api.auth",
    "kentik_api.api_calls",
    "kentik_api.api_connection",
    "kentik_api.api_resources",
    "kentik_api.requests_payload",
    "kentik_api.public",
    "kentik_api.utils",
]


def rm_all(directory, remove_dir=False):
    """Remove all content in a directory"""
    for p in directory.iterdir():
        if p.is_dir():
            rm_all(p, remove_dir=True)
        else:
            p.unlink()
    if remove_dir:
        directory.rmdir()


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


class FetchGRPCCode(distutils.cmd.Command):
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
        self.dst_path = HERE.joinpath("generated").as_posix()

    def finalize_options(self):
        pass

    # noinspection Mypy
    def run(self):
        import git

        # create destination directory, if it does not exist
        dst = Path(self.dst_path)
        dst.mkdir(parents=True, exist_ok=True)
        # cleanup destination directory
        rm_all(dst)
        # checkout source repo and copy stubs
        with TemporaryDirectory() as tmp:
            git.Repo.clone_from(self.repo, tmp)
            Path(tmp).joinpath(self.src_path).rename(dst)


class Install(install):
    def run(self):
        print("### begin install")
        install.run(self)
        print("### end install")


setup(
    name="kentik-api",
    use_scm_version={
        "root": "..",
        "relative_to": __file__,
    },
    description="SDK library for Kentik API",
    maintainer="Martin Machacek",
    maintainer_email="martin.machacek@kentik.com",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kentik/community_sdk_python/tree/main/kentik_api_library",
    license="Apache-2.0",
    include_package_data=True,
    install_requires=[
        "dacite>=1.6.0",
        "requests[socks]>=2.25.0",
        "typing-extensions>=3.7.4.3",
        "urllib3>=1.26.0",
        "protobuf>=3.19.1",
        "grpcio>=1.38.1",
    ],
    setup_requires=["pytest-runner", "pylint-runner", "setuptools_scm", "wheel", "gitpython"],
    tests_require=["httpretty", "pytest", "pylint"],
    extras_require={
        "analytics": ["pandas>=1.2.4", "pyyaml>=5.4.1", "fastparquet>=0.6.3"],
    },
    packages=PACKAGES,
    package_dir={pkg: os.path.join(*pkg.split(".")) for pkg in PACKAGES},
    cmdclass={"install": Install, "pylint": PylintCmd, "mypy": MypyCmd, "grpc_stubs": FetchGRPCCode},
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
)
