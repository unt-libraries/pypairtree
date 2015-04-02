#!/usr/bin/env python

"""setup.py for pypairtree"""

import os

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pypairtree',
    version='1.0.0',
    author='University of North Texas Libraries',
    author_email='lauren.ko@unt.edu',
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/unt-libraries/pypairtree',
    keywords='python pairtree',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    license='LICENSE',
    description=('Python implementation of Pairtree for storing '
                 'objects in a filesystem hierarchy that maps object'
                 ' identifiers to two character directory paths'),
    long_description=README,
)
