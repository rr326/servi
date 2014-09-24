import ez_setup
ez_setup.use_setuptools()
import servi.config as c
import os

from setuptools import setup, Command, find_packages


# For pytest
class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py', 'tests'])
        raise SystemExit(errno)

setup(
    name = "servi",
    version = "0.1",
    #packages = ['servi'],
    packages = find_packages(),
    include_package_data=True,
    # package_data={    }, # Not needed - should pick up ./templates from git
    exclude_package_data = {
        '' : ['.gitignore']
    },

    cmdclass={'test': PyTest},

    entry_points = {
      'console_scripts' :
            [ 'servi = main:main']
    },

    install_requires = ['PyYAML>=3.11', 'pytest>=2.6.2'],

    author = "Ross Rosen",
    author_email = "rrosen326@gmail.com",
    description = "Tools and templates for building a solid production "
                  "and development server",
    license = "MIT",
    keywords = "Vagrant ansible ubuntu server",
    url = "http://k2companhy.com",

)