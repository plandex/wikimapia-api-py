Wikimapia API for Python |build-status|
=======================================

`Wikimapia`_ is an open-content collaborative map project. This is a Python
(2.7, 3.3 and 3.4) implementation of wikimapia `api`_.

Installation
------------

.. code-block:: bash
    pip install wikimapia_api

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

.. _Wikimapia: http://wikimapia.org
.. _api: http://wikimapia.org/api

.. _https://speakerdeck.com/brettcannon/3-compatible
.. _http://pythonhosted.org/six/
.. _http://python-future.org/compatible_idioms.html
.. _https://github.com/pypa/sampleproject/blob/master/setup.py
.. _https://packaging.python.org/en/latest/single_source_version.html
.. _http://css.dzone.com/articles/tdd-python-5-minutes

.. |build-status| image:: https://travis-ci.org/samgiles/slumber.svg?branch=master
   :target: https://travis-ci.org/samgiles/slumber
   :alt: Build status
.. |coverage-status| image:: https://img.shields.io/coveralls/samgiles/slumber.svg
   :target: https://coveralls.io/r/samgiles/slumber
   :alt: Test coverage percentage
.. |docs| image:: https://readthedocs.org/projects/slumber/badge/?version=latest
   :target: http://slumber.readthedocs.org/
   :alt: Documentation
