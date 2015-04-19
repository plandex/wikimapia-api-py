# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import int
from past.builtins import basestring

from .api import API
from .collection_api import CollectionAPI
from .list_result import ListResult

class CategoryAPI(CollectionAPI):
    def __getitem__(self, key):
        return self.get_single(u'category.getbyid', key)

    def result_key(self, function):
        if function == u'category.getall':
            return u'categories'
        if function == u'category.getbyid':
            return u'category'

    def valid_params(self, function):
        if function == u'category.getall':
            return [u'name', u'page', u'count']
        if function == u'category.getbyid':
            return [u'id']

    def get(self, id, **params):
        return self.get_single(u'category.getbyid', id, **params)

    def all(self, **opts):
        if u'name' in opts and not isinstance(opts[u'name'], basestring):
            del opts[u'name']
        return self.get_collection(u'category.getall', **opts)

API.register(u'categories', CategoryAPI)
