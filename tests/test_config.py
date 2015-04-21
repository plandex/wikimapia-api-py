import unittest
from sure import expect
from decimal import Decimal

from wikimapia_api.config import Config
from .helpers import without_resource_warnings

class TestConfig(unittest.TestCase):
    # TODO: test log and log_level

    def setUp(self):
        self.config = Config()

    def test_init(self):
        config = Config(key='0123', url='http://test',
                        language='ru', delay=5000)
        expect(config.key).to.equal('0123')
        expect(config.url).to.equal('http://test/')
        expect(config.language).to.equal('ru')
        expect(config.delay).to.equal(Decimal(5000))

    def test_dir(self):
        properties = ['key', 'url', 'language', 'delay', 'compression',
                      'log', 'log_level']
        expect(all(x in properties for x in dir(self.config))).to.be.ok

    def test_key(self):
        expect(self.config.key).to.equal('example')
        self.config.key = 1000
        expect(self.config.key).to.equal('example')
        self.config.key = 'test'
        expect(self.config.key).to.equal('example')
        self.config.key = '012-3456789-aBcD-eF012'
        expect(self.config.key).to.equal('01234567-89ABCDEF-012')
        self.config.key = 'exAMple'
        expect(self.config.key).to.equal('example')

    def test_url(self):
        expect(self.config.url).to.equal('http://api.wikimapia.org/')
        self.config.url = 1000
        expect(self.config.url).to.equal('http://api.wikimapia.org/')
        self.config.url = 'http://test'
        expect(self.config.url).to.equal('http://test/')
        self.config.url = 'http://test//'
        expect(self.config.url).to.equal('http://test/')

    @without_resource_warnings
    def test_language(self):
        expect(self.config.language).to.equal('en')
        self.config.language = 1000
        expect(self.config.language).to.equal('en')
        self.config.language = 'RU'
        expect(self.config.language).to.equal('ru')

    def test_delay(self):
        expect(self.config.delay).to.equal(Decimal(3000))
        self.config.delay = False
        expect(self.config.delay).to.equal(Decimal(3000))
        self.config.delay = '300.5'
        expect(self.config.delay).to.equal(Decimal(300.5))
        self.config.delay = 100
        expect(self.config.delay).to.equal(Decimal(100))
        self.config.delay = 200.3
        expect(self.config.delay).to.equal(Decimal(200.3))

    def test_compression(self):
        expect(self.config.compression).to.be(True)
        self.config.compression = 20
        expect(self.config.compression).to.be(True)
        self.config.compression = False
        expect(self.config.compression).to.be(False)

    def test_merge(self):
        config = self.config.merge(delay=5000, language='ru')
        expect(config).to.be.a(Config)
        expect(config).to_not.be(self.config)
        expect(config.key).to.equal(self.config.key)
        expect(config.url).to.equal(self.config.url)
        expect(config.language).to.equal('ru')
        expect(config.delay).to.equal(Decimal(5000))
