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


class PylintCmd(distutils.cmd.Command):
    """Custom command to run Pylint"""

    description = 'run Pylint on src, tests and examples dir'
    user_options = [
        ('pylint-rcfile=', None, 'path to Pylint config file'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        self.pylint_rcfile = ''

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                'Pylint config file {} does not exist.'.format(self.pylint_rcfile))

    def run(self):
        """Run command."""
        cmd = ['pylint']
        paths = ['./src', './tests', './examples']
        if self.pylint_rcfile:
            cmd.append('--rcfile={}'.format(self.pylint_rcfile))
        for path in paths:
            cmd.append(path)
        self.announce(
            'Running command: %s' % str(cmd),
            level=distutils.log.INFO)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            pass

class MypyCmd(distutils.cmd.Command):
    """Custom command to run Mypy"""

    description = 'run Mypy on kentik_api directory'    
    user_options = [
        ('package=', None, 'Path to run mypy (default kentik_api)')
    ]

    def initialize_options(self):
        """Set default values for option package (default kentik_api)"""
        self.package = 'kentik_api'
    
    def finalize_options(self):
        """Post-process options."""
        if self.package:
            assert os.path.exists(self.package), (
                'Path {} does not exist.'.format(self.package))

    def run(self):
        """Run command"""
        cmd = ['mypy']
        if self.package:
            cmd.append('-p{}'.format(self.package))
        self.announce(
            'Run command: {}'.format(str(cmd)),
            level=distutils.log.INFO)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            pass


setup(
    name="kentik-api",
    version="0.0.1",
    description="API Library to help using Kenti API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kentik/community_sdk_python/tree/main/kentik_api_library",
    include_package_data=True,
    install_requires=[
        'python-http-client>=3.3.1',
        'requests>=2.25.0'
        ],
    setup_requires=['pytest-runner', 'pylint-runner'],
    tests_require=['pytest', 'pylint'],
    packages=[
        'kentik_api',
        'kentik_api.auth',
        'kentik_api.api_calls'
        ],
    package_dir={
        'kentik_api': 'kentik_api',
        'kentik_api.auth' : 'kentik_api/auth',
        'kentik_api.api_calls' : 'kentik_api/api_calls'
        },
    cmdclass={
        'pylint': PylintCmd,
        'mypy' : MypyCmd
    },
)
