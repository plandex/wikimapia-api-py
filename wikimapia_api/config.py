# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import object
from past.builtins import basestring

import re
from decimal import Decimal


_KEY_RE = re.compile(u'[0-9A-F]*\Z')
_URL_RE = re.compile(u'\/+\Z')

class Config(object):
    def __init__(self, **opts):
        self.reset()
        for key in dir(self):
            if key in opts:
                setattr(self, key, opts[key])

    def reset(self):
        self._key = u'example'
        self._url = u'http://api.wikimapia.org/'
        self._language = u'en'
        self._delay = Decimal(3000)
        self._compression = True

    def __dir__(self):
        return [u'key', u'url', u'language', u'delay', u'compression']

    @property
    def key(self):
        return self._key
    @key.setter
    def key(self, value):
        if not isinstance(value, basestring):
            return
        if value.lower() == u'example':
            self._key = u'example'
            return
        value = value.replace(u'-', u'').upper()
        if not _KEY_RE.match(value):
            return
        parts = [value[i : i+8] for i in range(0, len(value), 8)]
        self._key = u'-'.join(parts)

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        if not isinstance(value, basestring):
            return
        self._url = _URL_RE.sub(u'', value) + u'/'
        return self._url

    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, value):
        if not isinstance(value, basestring):
            return
        self._language = value.lower()

    @property
    def delay(self):
        return self._delay
    @delay.setter
    def delay(self, value):
        value = Decimal(value)
        if value <= 0 or not value.is_finite():
            return
        self._delay = value

    @property
    def compression(self):
        return self._compression
    @compression.setter
    def compression(self, value):
        self._compression = value != False

    def merge(self, **opts):
        if not opts:
            return self
        config = Config()
        for key in dir(config):
            if key in opts:
                setattr(config, key, opts[key])
            else:
                setattr(config, key, getattr(self, key))
        return config

