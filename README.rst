Wikimapia API for Python |build-status| |coverage-status| |docs|
================================================================

Wikimapia_ is an open-content collaborative map project. This library is a
Python (2.7, 3.3 and 3.4) implementation of wikimapia api_.

Documentation available in tutorial_.

Installation
------------

Library is in prerelease stage, so use ``--pre`` option:

.. code-block:: bash

    pip install --pre wikimapia_api

Usage
-----

.. code-block:: python

    from wikimapia_api import API

    API.config.key = 'YOUR WIKIMAPIA API KEY'
    print(API.places[55])

Testing
-------

Firstly, clone git repository:

.. code-block:: bash

    git clone https://github.com/cybernetlab/wikimapia_api_py wikimapia_api

For developing and testing you should install additional packages:

.. code-block:: bash

    cd wikimapia_api
    python setup.py develop
    pip install -r requirements.txt

To run tests execute:

.. code-block:: bash

    python -m unittest discover

TODO
----

1. Logging (in progress)
2. Doc comments in sources
3. Enlage test coverage

.. _Wikimapia: http://wikimapia.org
.. _api: http://wikimapia.org/api
.. _tutorial: http://wikimapia-api-py.readthedocs.org/en/latest/tutorial.html

.. _https://speakerdeck.com/brettcannon/3-compatible
.. _http://pythonhosted.org/six/
.. _http://python-future.org/compatible_idioms.html
.. _https://github.com/pypa/sampleproject/blob/master/setup.py
.. _https://packaging.python.org/en/latest/single_source_version.html
.. _http://css.dzone.com/articles/tdd-python-5-minutes

.. |build-status| image:: https://travis-ci.org/plandex/wikimapia-api-py.svg?branch=master
   :target: https://travis-ci.org/plandex/wikimapia-api-py
   :alt: Build status
.. |coverage-status| image:: https://coveralls.io/repos/plandex/wikimapia-api-py/badge.svg?branch=master
   :target: https://coveralls.io/r/plandex/wikimapia-api-py?branch=master
   :alt: Test coverage percentage
.. |docs| image:: https://readthedocs.org/projects/wikimapia-api-py/badge/?version=latest
   :target: https://readthedocs.org/projects/wikimapia-api-py/?badge=latest
   :alt: Documentation status
