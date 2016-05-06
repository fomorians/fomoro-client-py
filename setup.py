import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lab'))

from version import version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

packages = [package for package in find_packages() if package.startswith('lab')]

setup(name='fomoro-lab',
    version=version,
    description='An API helper for sending results to Fomoro.',
    long_description=read('README.md'),
    url='https://github.com/fomorians/fomoro-lab',
    author='Fomoro',
    author_email='jim@fomoro.com',
    packages=packages,
    install_requires=['requests==2.10.0', 'six'],
)
