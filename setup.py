import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lab'))

from version import version

with open('README.md') as f:
    long_description = f.read()

setup(name='lab',
    version=version,
    description='An API helper for sending results to Fomoro.',
    long_description=long_description,
    url='https://github.com/fomorians/fomoro-lab',
    author='Fomoro',
    author_email='jim@fomoro.com',
    packages=['lab'],
    install_requires=['requests==2.10.0', 'six'],
)
