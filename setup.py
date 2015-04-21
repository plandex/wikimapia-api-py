import os
import io

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

INSTALL_REQUIRES = []
TESTS_REQUIRE = ['sure>=1.2.10', 'httpretty<=0.8.6']

HERE = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(HERE, 'VERSION'), 'rt') as f:
    VERSION = f.read().strip()

with io.open(os.path.join(HERE, 'DESCRIPTION.rst'), 'rt') as f:
    LONG_DESCR = f.read()

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
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
]

setup(name='wikimapia_api',
      version=VERSION,
      description='Wikimapia API Python Implementation',
      long_description=LONG_DESCR,
      author='Alexey Ovchinnikov',
      author_email='alexey.ovchinnikov@yandex.ru',
      url='https://github.com/plandex/wikimapia-api-py/',
      license='MIT',
      keywords='wikimapia api geo map',
      packages=['wikimapia_api'],
      install_requires=INSTALL_REQUIRES,
      tests_require=TESTS_REQUIRE,
      test_suite='tests',
      classifiers=CLASSIFIERS)
