# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import object
from past.builtins import basestring

from .api import WikimapiaAPI

LIST_KEYS = {
    'api.getlanguages': 'languages',
    'place.getbyarea': 'places',
    'place.search': 'places',
    'place.getnearest': 'places',
    'category.getall': 'categories'
}

class WikimapiaIterator(object):
    def __init__(self, api, function, opts={}):
        if not isinstance(api, WikimapiaApi):
            raise TypeError('Wrong WikimapiaApi')
        if not isinstance(function, basestring) or not function in LIST_KEYS:
            raise TypeError('Wrong function name')
        self.total = 0
        self.loaded = -1
        self.buffer = []

        self.api = api
        self.function = function
        self.key = LIST_KEYS[function]
        self.opts = opts

        self.max = self.opts.pop('max', None)
        self.page_specified = 'page' in self.opts
        self.page = self.opts.setdefault('page', 1)
        self.page_size = int(self.opts.setdefault('count', '100'))

    def __iter__(self):
        return self

    def __len__(self):
        if self.max is None:
            return self.api.count_array(self.function, self.opts)
        else:
            return min(self.max, self.api.count_array(self.function, self.opts))

    def __getitem__(self, key):
        if not isinstance(key, (int, long)):
            raise TypeError('Wrong key')
        length = self.__len__()
        if key < 0:
            key += length
        if key < 0 or key > length:
            raise TypeError('Key out of bounds')
        if key // self.page_size == self.page - 1:
            if not self.buffer:
                self.__next_page()
            if not self.buffer:
                return None
            return self.buffer[key]
        result = self.__load_page(key // self.page_size + 1)
        if result is None:
            return None
        return self.buffer[key % self.page_size]

    def __next__(self):
        if not self.buffer:
            self.__next_page()
        if not self.buffer:
            raise StopIteration
        return self.buffer.pop(0)

    def __load_page(self, page):
        self.opts['page'] = str(page)
        #self.opts['count'] = str(self.page_size)
        result = self.api.request(self.function, self.opts)
        if not isinstance(result, dict) or self.key not in result:
            return None
        return result

    def __next_page(self):
        if self.max is not None and self.loaded >= self.max:
            return
        self.buffer = []
        if self.loaded < self.total:
            result = self.__load_page(self.page)
            if result is None:
                return
            self.loaded += int(result['count'])
            if self.total == 0:
                self.total = int(result['found'])
            self.page += 1
            self.buffer += result[self.key]
        if self.page_specified:
            self.max = self.loaded
