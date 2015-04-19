# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API
from .collection_api import CollectionAPI

_LIST_FUNCTIONS = [u'place.getbyarea', u'place.getnearest', u'place.search']
_LIST_DATA_BLOCKS = [u'main', u'geometry', u'edit', u'location', u'photos',
                     u'comments', u'translate']
_NEAREST_DATA_BLOCKS = [u'geometry', u'location']

class PlaceAPI(CollectionAPI):
    def __getitem__(self, key):
        return self.get_single(u'place.getbyid', key)

    def result_key(self, function):
        if function == u'place.getbyid':
            return None
        elif function in _LIST_FUNCTIONS:
            return 'places'

    def valid_params(self, function):
        if function == u'place.getbyid':
            return [u'id', u'options', u'data_blocks']
        elif function == u'place.getbyarea':
            return [u'bbox', u'x', u'y', u'z', u'options', u'data_blocks',
                    u'count', u'page',
                    u'category', u'categories_or', u'categories_and']
        elif function == u'place.getnearest':
            return [u'lon', u'lat', u'options', u'data_blocks',
                    u'count', u'page', u'category']
        elif function == u'place.search':
            return [u'lon', u'lat', u'q', u'options', u'data_blocks',
                    u'count', u'page',
                    u'category', u'categories_or', u'categories_and']

    def get(self, id, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params)
        return self.get_single(u'place.getbyid', id, **params)

    def inside(self, lon_min, lat_min, lon_max, lat_max, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _LIST_DATA_BLOCKS)
        params[u'bbox'] = u'{0},{1},{2},{3}'.format(lon_min, lat_min,
                                                    lon_max, lat_max)
        return self.get_collection(u'place.getbyarea', **params)

    def in_tile(self, x, y, z, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _LIST_DATA_BLOCKS)
        params[u'x'] = x
        params[u'y'] = y
        params[u'z'] = z
        return self.get_collection(u'place.getbyarea', **params)

    def nearest(self, lon, lat, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _NEAREST_DATA_BLOCKS)
        params[u'lon'] = lon
        params[u'lat'] = lat
        return self.get_collection(u'place.getnearest', **params)

    def search(self, query, lon, lat, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _LIST_DATA_BLOCKS)
        self.sanitize_distance(params)
        params[u'q'] = query
        params[u'lon'] = lon
        params[u'lat'] = lat
        return self.get_collection(u'place.search', **params)

    def update(self):
        pass

    def sanitize_distance(self, params):
        if not u'distance' in params:
            return
        distance = params[u'distance']
        if not isinstance(distance, int):
            try:
                distance = int(distance)
            except ValueError:
                distance = None
        if distance is None:
            del params[u'distance']
        else:
            params[u'distance'] = str(distance)

API.register(u'places', PlaceAPI)
