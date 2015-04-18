# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API

class CategoryAPI(API):
    def get_by_id(id):
        if not isinstance(id, (int, long)) or id <= 0:
            return None
        result = self.request('category.getbyid', {'id': str(id)})
        if not isinstance(result, dict) or 'category' not in result:
            return None
        return result['category']

    def get_all(name=None):
        opts = {}
        if isinstance(name, basestring):
            opts['name'] = name
        return WikimapiaIterator(self, 'category.getall', 'categories', opts)

API.register('category', CategoryAPI)
