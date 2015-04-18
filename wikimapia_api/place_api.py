# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .api import API

class PlaceAPI(API):
    def get_by_id(id, **opts):
        if 'data_blocks' not in opts:
            opts['data_blocks'] = 'main,geometry,location'
        return self.request('place.getbyid', {'id': id})

    def get_by_area(x1, y1, x2, y2, **opts):
        opts['bbox'] = "{x1},{y1},{x2},{y2}".format(**locals())
        if 'data_blocks' not in opts:
            opts['data_blocks'] = 'main,geometry,location'
        return WikimapiaIterator(self, 'place.getbyarea', 'places', opts)

    def get_nearest():
        pass

    def search():
        pass

    def update():
        pass

API.register('place', PlaceAPI)
