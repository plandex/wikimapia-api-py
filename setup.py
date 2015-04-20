#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup
from os import path
from io import open

install_requires = ['future>=0.14.3']
tests_require = ['sure>=1.2.10', 'httpretty<=0.8.6']

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION'), 'rt') as f:
    version = f.read().strip()

with open(path.join(here, 'DESCRIPTION.rst'), 'rt') as f:
    long_description = f.read()

setup(
    name='wikimapia_api',
    version=version,
    description='Wikimapia API Python Implementation',
    long_description=long_description,
    author='Alexey Ovchinnikov',
    author_email='alexey.ovchinnikov@yandex.ru',
    url='https://github.com/plandex/wikimapia-api-py/',
    license='MIT',
    keywords = 'wikimapia api geo map',
    packages=['wikimapia_api'],
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite = 'tests',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
