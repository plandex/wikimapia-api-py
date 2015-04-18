# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import with_metaclass
from future.moves.urllib.parse import urlparse, urlencode
from past.builtins import basestring
import http.client
import time
import json
import zlib

from .config import Config
from .errors import FunctionNameError, RequestError

# Workaround for python.future issue:
# https://github.com/PythonCharmers/python-future/issues/137
if not hasattr(http.client, 'OK'):
    http.client.OK = 200

_RESERVED = ['config']

class _APIMeta(type):
    @property
    def config(cls):
        return cls._config

    @config.setter
    def config(cls, value):
        if isinstance(value, Config):
            cls._config = config
        elif isinstance(value, dict):
            cls._config = Config(**value)

    def __getattribute__(cls, name):
        if name != '_api' and name in cls._api:
            (api_class, api) = cls._api[name]
            if not api:
                api = api_class()
                cls._api[name][1] = api
            return api
        return super(_APIMeta, cls).__getattribute__(name)

    def register(cls, name, api_class):
        if (not isinstance(name, basestring) or
                api_class == cls or
                not issubclass(api_class, API) or
                name in _RESERVED or
                name in cls._api and cls._api[name][0] == api_class):
            return
        cls._api[name] = [api_class, None]

class API(with_metaclass(_APIMeta, object)):
    _config = Config()
    _api = {}
    _last_call = None

    def __init__(self, **opts):
        self._config = self.__class__.config.merge(**opts)

    def config(self, **opts):
        return self._config.merge(**opts)

    def request(self, function, **opts):
        if not isinstance(function, basestring):
            return

        config = self.config(**opts)
        for k in set(dir(config)) & set(opts.keys()):
            del opts[k]

        opts['key'] = config.key
        opts['function'] = function.lower()
        opts['format'] = 'json'
        opts['language'] = config.language
        if config.compression:
            opts['pack'] = 'gzip'

        params = urlencode(opts)
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
                conn.request('GET', uri.path + '?' + params)
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
                result = json.loads(data.decode('utf-8'))
                conn.close()
            if isinstance(result, dict) and 'debug' in result:
                if result['debug']['code'] == 1004:
                    # API key limit expired
                    time.sleep(5)
                elif result['debug']['code'] == 1001:
                    # Function not found
                    raise FunctionNameError(result['debug']['message'], 1001)
                else:
                    # Other errors
                    raise RequestError(result['debug']['message'],
                                       result['debug']['code'])
            else:
                return result

    def count_array(self, req, **opts):
        opts['page'] = 1
        count = None
        if 'count' in opts:
            count = opts['count']
        opts['count'] = 5
        result = self.request(req, **opts)
        if count is not None:
            opts['count'] = count
        if isinstance(result, dict) and 'found' in result:
            return int(result['found'])
        else:
            return 0

    def load_array(self, req, key, **opts):
        total = 0
        loaded = -1
        page_specified = False
        if 'page' in opts:
            page = int(opts['page'])
            page_specified = True
        else:
            page = 1
        max = opts.pop('max', None)
        opts.setdefault('count', '100')
        arr = []
        while loaded < total:
            opts['page'] = str(page)
            result = self.request(req, **opts)
            if not isinstance(result, dict) or key not in result:
                return None
            loaded += int(result['count'])
            if total == 0:
                total = int(result['found'])
            page += 1
            arr.append(result[key])
            if page_specified or max is not None and loaded >= max:
                break
        return arr
