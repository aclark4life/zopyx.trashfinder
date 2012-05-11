from setuptools import find_packages
from setuptools import setup

setup(
    description='This is a fork of zopyx.trashfinder, with modifications made to make integration with pythonpackages.com easier. It is not intended to be used outside of pythonpackages.com. For a command line trash finder, please install zopyx.trashfinder.',
    install_requires=[
        'setuptools',
    ],
    name='pypi.trashfinder',
    namespace_packages=[
        'pypi',
        ],
    packages=find_packages(),
    version='0.0.3',
)
