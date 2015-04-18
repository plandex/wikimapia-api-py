# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API

class CapabilitiesAPI(API):
    def get_languages():
        pass

API.register('api', CapabilitiesAPI)
