import anydbm
import os
import qgis

class WikimapiaConfig(object):
    @property
    def api_key(self):
        return self._api_key
    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def api_url(self):
        if not self._api_key: self._api_url = 'http://api.wikimapia.org/'
        return self._api_url
    @api_url.setter
    def api_url(self, value):
        self._api_url = value

    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, value):
        self._language = value

    @property
    def api_delay(self):
        if not self._api_delay: self._api_delay = 1
        return self._api_delay
    @api_delay.setter
    def api_delay(self, value):
        self._api_delay = int(value)
