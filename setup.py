from setuptools import find_packages
from setuptools import setup

setup(
    name='pypi.trashfinder',
    namespace_packages=[
        'pypi',
        ],
    packages=find_packages(),
    version='0.0.1',
)
