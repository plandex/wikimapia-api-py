# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API

class StreetAPI(API):
    def get_by_id():
        pass

API.register('street', StreetAPI)
