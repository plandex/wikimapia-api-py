# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import object, int
from past.builtins import basestring

from .api import API

class ListResult(object):
    def __init__(self, api, function, **opts):
        if not isinstance(api, API):
            raise TypeError(u'Wrong API')
        if not isinstance(function, basestring):
            raise TypeError(u'Wrong function name')
        self.length = None
        self.total = 0
        self.loaded = -1
        self.buffer = []

        self.api = api
        self.function = function
        self.key = api.result_key(function)
        self.opts = opts

        self.max = self.opts.pop(u'max', None)
        self.page_specified = u'page' in self.opts
        self.page = self.opts.setdefault(u'page', 0)
        self.page_size = int(self.opts.setdefault(u'count', u'100'))

    def __iter__(self):
        return self

    def __len__(self):
        if self.length is not None:
            return self.length
        if self.loaded < 0:
            length = self.api.count_array(self.function, self.opts)
        else:
            length = self.total
        if self.max is not None:
            length = min(self.max, length)
        self.length = length
        return length

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('Wrong key')
        length = self.__len__()
        if key < 0:
            key += length
        if key < 0 or key > length:
            raise TypeError('Key out of bounds')
        if self.page == 0 or key // self.page_size == self.page - 1:
            if not self.buffer:
                self.__next_page()
            if not self.buffer:
                return None
            return self.buffer[key]
        result = self.__load_page(key // self.page_size + 1)
        if result is None:
            return None
        self.buffer = result[self.key]
        return self.buffer[key % self.page_size]

    def __next__(self):
        if not self.buffer:
            self.__next_page()
        if not self.buffer:
            raise StopIteration
        return self.buffer.pop(0)

    def __load_page(self, page):
        if page <= 0:
            page = 1
        self.opts['page'] = str(page)
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
            if self.loaded < 0:
                self.loaded = 0
            self.loaded += int(result['count'])
            if self.total == 0:
                self.total = int(result['found'])
            self.page += 1
            self.buffer += result[self.key]
        if self.page_specified:
            self.max = self.loaded
