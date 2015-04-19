# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API

class CapabilitiesAPI(API):
    def result_key(self, function):
        if function == u'api.getlanguages':
            return u'languages'

    def valid_params(self, function):
        return []

    @property
    def languages(self):
        if u'languages' in self._cache:
            return self._cache[u'languages']
        result = self.request(u'api.getlanguages')
        if result and u'languages' in result:
            self._cache[u'languages'] = result[u'languages']
        return self._cache[u'languages']

API.register(u'languages', CapabilitiesAPI, u'languages')
