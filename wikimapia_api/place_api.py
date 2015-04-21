# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from past.builtins import basestring
import collections
import math

from .api import API
from .collection_api import CollectionAPI
from .list_result import ListsResult

_LIST_FUNCTIONS = [u'place.getbyarea', u'place.getnearest', u'place.search']
_LIST_DATA_BLOCKS = [u'main', u'geometry', u'edit', u'location', u'photos',
                     u'comments', u'translate']
_NEAREST_DATA_BLOCKS = [u'geometry', u'location']

TILE_ZOOM = 8

def coo2tile(lon, lat, zoom):
    latr = math.radians(lat)
    n = 2.0 ** zoom
    tan = math.tan(latr)
    cos = math.cos(latr)
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(tan + (1 / cos)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def tile2coo(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon = xtile / n * 360.0 - 180.0
    latr = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat = math.degrees(latr)
    return (lat, lon)

def tile2lon(xtile, zoom):
    return xtile / (2.0 ** zoom) * 360.0 - 180.0

def tile2lat(ytile, zoom):
    latr = math.atan(math.sinh(math.pi * (1 - 2 * ytile / (2.0 ** zoom))))
    return math.degrees(latr)

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
                    u'count', u'page', u'category', u'category_or']
        elif function == u'place.getnearest':
            return [u'lon', u'lat', u'options', u'data_blocks',
                    u'count', u'page', u'category']
        elif function == u'place.search':
            return [u'lon', u'lat', u'q', u'options', u'data_blocks',
                    u'count', u'page', u'category', u'category_or']

    def get(self, id, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params)
        return self.get_single(u'place.getbyid', id, **params)

    def inside(self, lon_min, lat_min, lon_max, lat_max, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _LIST_DATA_BLOCKS)
        self.sanitize_category(params)
        self.sanitize_category_or(params)
        tiles = self.tiles(lon_min, lat_min, lon_max, lat_max)
        requests = []
        for tile in tiles:
            params[u'bbox'] = u'{0},{1},{2},{3}'.format(*tile)
            requests.append(self.get_collection(u'place.getbyarea', **params))
        if len(requests) == 1:
            return requests[0]
        return ListsResult(requests)

    def in_tile(self, x, y, z, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _LIST_DATA_BLOCKS)
        self.sanitize_category(params)
        self.sanitize_category_or(params)
        params[u'x'] = x
        params[u'y'] = y
        params[u'z'] = z
        return self.get_collection(u'place.getbyarea', **params)

    def nearest(self, lon, lat, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _NEAREST_DATA_BLOCKS)
        self.sanitize_category(params)
        params[u'lon'] = lon
        params[u'lat'] = lat
        return self.get_collection(u'place.getnearest', **params)

    def search(self, query, lon, lat, **params):
        self.sanitize_options(params)
        self.sanitize_data_blocks(params, _LIST_DATA_BLOCKS)
        self.sanitize_distance(params)
        self.sanitize_category(params)
        self.sanitize_category_or(params)
        params[u'q'] = query
        params[u'lon'] = lon
        params[u'lat'] = lat
        return self.get_collection(u'place.search', **params)

    def update(self):
        pass

    def tiles(self, x1, y1, x2, y2):
        (tx1, ty1) = coo2tile(x1, y1, TILE_ZOOM)
        (tx2, ty2) = coo2tile(x2, y2, TILE_ZOOM)
        if tx1 == tx2:
            if x1 > x2:
                x1, x2 = x2, x1
            xline = [(x1, x2)]
        else:
            if tx1 > tx2:
                tx1, tx2 = tx2, tx1
            xline = []
            for i in range(tx1, tx2+1):
                xx1 = x1 if i == tx1 else tile2lon(i, TILE_ZOOM)
                xx2 = x2 if i == tx2+1 else tile2lon(i+1, TILE_ZOOM)
                xline.append((xx1, xx2))
        if ty2 == ty1:
            if y1 > y2:
                y1, y2 = y2, y1
            yline = [(y1, y2)]
        else:
            if ty1 > ty2:
                ty1, ty2 = ty2, ty1
            yline = []
            for i in reversed(range(ty1, ty2+1)):
                yy1 = y1 if i == ty2+1 else tile2lat(i+1, TILE_ZOOM)
                yy2 = y2 if i == ty1 else tile2lat(i, TILE_ZOOM)
                yline.append((yy1, yy2))
        result = []
        for x in xline:
            for y in yline:
                result.append((x[0], y[0], x[1], y[1]))
        return result

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

    def sanitize_category(self, params):
        cats = None
        cats_and = None
        if u'category' in params:
            cats = params[u'category']
        elif u'categories' in params:
            cats = params[u'categories']
            del params[u'categories']
        if u'category_and' in params:
            cats_and = params[u'category_and']
            del params[u'category_and']
        elif u'categories_and' in params:
            cats_and = params[u'categories_and']
            del params[u'categories_and']
        if cats is None and cats_and is None:
            return
        if cats is None:
            cats = []
        if isinstance(cats, basestring):
            cats = cats.split(',')
        elif not isinstance(cats, collections.Iterable):
            cats = [cats]
        if isinstance(cats_and, basestring):
            cats += cats_and.split(',')
        elif isinstance(cats_and, collections.Iterable):
            cats += cats_and
        elif cats_and is not None:
            cats += [cats_and]
        cats = [str(x).strip() for x in cats]
        if cats:
            params[u'category'] = ','.join(cats)
        else:
            if u'category' in params:
                del params[u'category']

    def sanitize_category_or(self, params):
        if u'category_or' in params:
            cats = params[u'category_or']
        elif u'categories_or' in params:
            cats = params[u'categories_or']
            del params[u'categories_or']
        else:
            return
        if isinstance(cats, basestring):
            cats = cats.split(',')
        elif not isinstance(cats, collections.Iterable):
            cats = [cats]
        cats = [str(x).strip() for x in cats]
        if cats:
            params[u'category_or'] = ','.join(cats)
        else:
            if u'category_or' in params:
                del params[u'category_or']

API.register(u'places', PlaceAPI)
