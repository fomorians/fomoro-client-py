import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fomoro'))

from version import version

with open('README.md') as f:
    long_description = f.read()

setup(name='fomoro',
    version=version,
    description='Fomoro client library.',
    long_description=long_description,
    url='https://github.com/fomorians/fomoro-client-py',
    author='Jim Fleming',
    author_email='jim@fomoro.com',
    packages=['fomoro'],
    install_requires=[
        'pytz==2016.4',
        'tzlocal==1.2.2',
        'requests==2.10.0',
        'six==1.10.0'
    ],
)
