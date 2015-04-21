'''Wikimapia_ is an open-content collaborative map project. This library is a
Python (2.7, 3.3 and 3.4) implementation of wikimapia api_.

Documentation available in tutorial_.

.. _Wikimapia: http://wikimapia.org
.. _api: http://wikimapia.org/api
.. _tutorial: http://wikimapia-api-py.readthedocs.org/en/latest/tutorial.html
'''

from __future__ import absolute_import

__all__ = ['API', 'Config']

from wikimapia_api.api import API
from wikimapia_api.config import Config
import wikimapia_api.capabilities_api
import wikimapia_api.category_api
import wikimapia_api.place_api
import wikimapia_api.street_api
