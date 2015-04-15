# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

class WikimapiaApi(object):
    def __init__(self, config=None):
        if isinstance(config, WikimapiaConfig):
            self.config = config
        else:
            self.config = WikimapiaConfig(config)
        self.last_call = None

    def get_place_by_id(self, id, opts={}):
        if 'data_blocks' not in opts:
            opts['data_blocks'] = 'main,geometry,location'
        return self.request('place.getbyid', {'id': id})

    def get_place_by_area(self, x1, y1, x2, y2, opts={}):
        opts['bbox'] = "{x1},{y1},{x2},{y2}".format(**locals())
        if 'data_blocks' not in opts:
            opts['data_blocks'] = 'main,geometry,location'
        return WikimapiaIterator(self, 'place.getbyarea', 'places', opts)

    def get_categories(self, name=None):
        opts = {}
        if isinstance(name, basestring):
            opts['name'] = name
        return WikimapiaIterator(self, 'category.getall', 'categories', opts)

    def get_category(self, id):
        if not isinstance(id, (int, long)) or id <= 0:
            return None
        result = self.request('category.getbyid', {'id': str(id)})
        if not isinstance(result, dict) or 'category' not in result:
            return None
        return result['category']

    def request(self, function, opts={}):
        if not isinstance(self.config, WikimapiaConfig): return None
        opts['key'] = self.config.api_key
        opts['function'] = function
        opts['format'] = 'json'
        opts['language'] = self.config.language
        params = urllib.urlencode(opts)
        uri = urlparse(self.config.api_url)
        conn = httplib.HTTPConnection(uri.netloc)
        while True:
            result = None
            now = int(round(time.time() * 1000))
            if self.last_call is not None:
                if now - self.last_call < self.config.api_delay:
                    time.sleep(
                        (self.config.api_delay - self.last_call + now) / 1000.0
                    )
            try:
                conn.request('GET', uri.path + '?' + params)
                response = conn.getresponse()
            except httplib.HTTPException:
                self.last_call = int(round(time.time() * 1000))
                return None
            else:
                self.last_call = int(round(time.time() * 1000))
                if response.status != httplib.OK:
                    return None
                result = json.loads(response.read())
                conn.close()
            if (isinstance(result, dict) and
                    'debug' in result and
                    result['debug']['code'] == 1004):
                time.sleep(110.0 / 1000.0)
            else:
                return result

    def count_array(self, req, opts={}):
        opts['page'] = 1
        count = None
        if 'count' in opts:
            count = opts['count']
        opts['count'] = 5
        result = self.request(req, opts)
        if count is not None:
            opts['count'] = count
        if isinstance(result, dict) and 'found' in result:
            return int(result['found'])
        else:
            return 0

    def load_array(self, req, key, opts={}):
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
            result = self.request(req, opts)
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
