# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import with_metaclass
from future.moves.urllib.parse import urlparse, urlencode
from past.builtins import basestring
from builtins import dict
import http.client
import time
import json
import zlib

from .config import Config
from .errors import FunctionNameError, RequestError, UnimplementedError

# Workaround for python.future issue:
# https://github.com/PythonCharmers/python-future/issues/137
if not hasattr(http.client, u'OK'):
    http.client.OK = 200

_RESERVED = [u'config']

class _APIMeta(type):
    @property
    def config(cls):
        return cls._config

    @config.setter
    def config(cls, value):
        if isinstance(value, Config):
            cls._config = value
        elif isinstance(value, dict):
            cls._config = cls._config.merge(**value)

    def __getattribute__(cls, name):
        if name != u'_api' and name in cls._api:
            (api_class, api, attr) = cls._api[name]
            if not api:
                api = api_class()
                cls._api[name][1] = api
            if attr:
                return getattr(api, attr)
            return api
        return super(_APIMeta, cls).__getattribute__(name)

    def register(cls, name, api_class, attr=None):
        if (not isinstance(name, basestring) or
                api_class == cls or
                not issubclass(api_class, API) or
                name in _RESERVED or
                name in cls._api and cls._api[name][0] == api_class):
            return
        if not isinstance(attr, basestring):
            attr = None
        cls._api[name] = [api_class, None, attr]

    def clear_entire_cache(cls):
        for (api_class, api, method) in cls._api.values():
            if api:
                api.clear_cache()

_VALID_PARAMS = [u'key', u'function', u'format', u'language', u'pack']

class API(with_metaclass(_APIMeta, object)):
    _config = Config()
    _api = dict()
    _last_call = None

    def __init__(self, **opts):
        self._opts = opts
        self.clear_cache()

    def config(self, **opts):
        options = self._opts.copy()
        options.update(opts)
        return API.config.merge(**options)

    def clear_cache(self):
        self._cache = dict()

    def result_key(self, function):
        raise UnimplementedError('Illegal call to unimplemented result_key')

    def valid_params(self, function):
        raise UnimplementedError('Illegal call to unimplemented valid_params')

    def request(self, function, params={}):
        if not isinstance(function, basestring):
            return None
        # merge config
        config = self.config(**params)
        # setup general params
        params[u'key'] = config.key
        params[u'function'] = function.lower()
        params[u'format'] = u'json'
        params[u'language'] = config.language
        if config.compression:
            params[u'pack'] = u'gzip'
        # cleanup params
        valid_params = self.valid_params(function) + _VALID_PARAMS
        for k in list(params):
            if k not in valid_params:
                del params[k]
        # prepare request
        params = urlencode(params)
        uri = urlparse(config.url)
        conn = http.client.HTTPConnection(uri.netloc)
        while True:
            result = None
            now = int(round(time.time() * 1000))
            if API._last_call is not None:
                if now - API._last_call < config.delay:
                    delay = float(now - API._last_call + config.delay)
                    time.sleep(delay / 1000.0)
            try:
                conn.request(u'GET', uri.path + u'?' + params)
                response = conn.getresponse()
            except http.client.HTTPException:
                API._last_call = int(round(time.time() * 1000))
                return None
            else:
                API._last_call = int(round(time.time() * 1000))
                if response.status != http.client.OK:
                    return None
                data = response.read()
                if config.compression:
                    # http://stackoverflow.com/questions/2695152/in-python-how-do-i-decode-gzip-encoding/2695575#2695575
                    data = zlib.decompress(data, 16+zlib.MAX_WBITS)
                result = json.loads(data.decode(u'utf-8'))
                conn.close()
            if isinstance(result, dict) and u'debug' in result:
                if result[u'debug'][u'code'] == 1004:
                    # API key limit exceeded
                    time.sleep(5)
                elif result[u'debug'][u'code'] == 1001:
                    # Function not found
                    raise FunctionNameError(result[u'debug'][u'message'], 1001)
                else:
                    # Other errors
                    raise RequestError(result[u'debug'][u'message'],
                                       result[u'debug'][u'code'])
            else:
                return result

    def count_array(self, function, params={}):
        params[u'page'] = 1
        count = None
        if u'count' in params:
            count = params[u'count']
        params[u'count'] = 5
        result = self.request(function, params)
        if count is not None:
            params[u'count'] = count
        if isinstance(result, dict) and u'found' in result:
            return int(result[u'found'])
        else:
            return 0

    def load_array(self, function, params={}):
        total = 0
        loaded = -1
        page_specified = False
        if u'page' in params:
            page = int(params[u'page'])
            page_specified = True
        else:
            page = 1
        max = params.pop(u'max', None)
        params.setdefault(u'count', u'100')
        arr = []
        while loaded < total:
            params[u'page'] = str(page)
            result = self.request(function, params)
            key = self.result_key(function)
            if not isinstance(result, dict) or key not in result:
                return None
            if loaded < 0:
                loaded = 0
            loaded += int(result[u'count'])
            if total == 0:
                total = int(result[u'found'])
            page += 1
            arr += result[key]
            if page_specified or max is not None and loaded >= max:
                break
        return arr
