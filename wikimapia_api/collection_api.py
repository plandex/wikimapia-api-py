# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import int
from past.builtins import basestring

from .api import API
from .list_result import ListResult

_DATA_BLOCKS = [u'main', u'geometry', u'edit', u'location', u'attached',
                u'photos', u'comments', u'translate', u'similar_places',
                u'nearest_places', u'nearest_comments', u'nearest_streets',
                u'nearest_hotels']
_OPTIONS = [u'mercator']

class CollectionAPI(API):
    def clear_cache(self):
        self._cache = []

    def request(self, function, params={}):
        # make real request in parent class
        result = super(CollectionAPI, self).request(function, params)
        # update cache
        if isinstance(result, dict):
            key = self.result_key(function.lower())
            if key is None:
                data = result
            elif key in result:
                data = result[key]
            else:
                data = None
            if data:
                if isinstance(data, dict):
                    item = self._search_cache(data[u'id'])
                    item[1] = data
                else:
                    for data_item in data:
                        item = self._search_cache(data_item[u'id'])
                        item[1] = data_item
        return result

    def get_single(self, function, id, **params):
        if not isinstance(function, basestring):
            return None
        if not isinstance(id, int):
            if not isinstance(id, basestring):
                return None
            try:
                id = int(id)
            except ValueError:
                return None
        item = self._search_cache(id, append=False)
        if item[1] is None:
            params[u'id'] = id
            result = self.request(function, params)
            if isinstance(result, dict):
                key = self.result_key(function)
                if key is None:
                    item[1] = result
                    self._cache.append(item)
                elif key in result:
                    item[1] = result[key]
                    self._cache.append(item)
        return item[1]

    def get_collection(self, function, **opts):
        if not isinstance(function, basestring):
            return None
        return ListResult(self, function, **opts)

    def sanitize_list_param(self, params, name, values):
        if not name in params:
            return
        l = params[name]
        if isinstance(l, basestring):
            l = l.split(',')
        l = [x.strip().lower() for x in l]
        l = set([x for x in l if x in values])
        if not l:
            del params[name]
            return
        params[name] = ','.join(l)

    def sanitize_data_blocks(self, params, blocks=_DATA_BLOCKS):
        self.sanitize_list_param(params, u'data_blocks', blocks)
        if not u'data_blocks' in params:
            return
        if len(params[u'data_blocks']) == len(blocks):
            del params[u'data_blocks']
            return

    def sanitize_options(self, params):
        self.sanitize_list_param(params, u'options', _OPTIONS)
        if u'mercator' in params:
            if params[u'mercator']:
                if u'options' in params:
                    l = set(params[u'options'].split(','))
                    l.add(u'mercator')
                    params[u'options'] = ','.join(l)
                else:
                    params[u'options'] = u'mercator'
            del params[u'mercator']

    def _search_cache(self, id, append=True):
        try:
            return next(x for x in self._cache if x[0] == id)
        except StopIteration:
            item = [id, None]
            if append:
                self._cache.append(item)
            return item
