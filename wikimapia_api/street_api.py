# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API
from .collection_api import CollectionAPI

class StreetAPI(CollectionAPI):
    def __getitem__(self, key):
        return self.get_single(u'street.getbyid', key)

    def result_key(self, function):
        if function == u'street.getbyid':
            return None

    def valid_params(self, function):
        if function == u'street.getbyid':
            return [u'id', u'options', u'data_blocks']

    def get(self, id, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params)
        return self.get_single(u'street.getbyid', id, **params)

API.register(u'streets', StreetAPI)
