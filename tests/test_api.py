import unittest
import httpretty
from sure import expect
from os import path
from io import open

from wikimapia_api.api import API
from wikimapia_api.errors import FunctionNameError, RequestError

cwd = path.dirname(path.abspath(__file__))

class TestSimple(unittest.TestCase):
    def setUp(self):
        self.api = API(compression=False, delay=1)

    def test_class_config(self):
        class TestAPI(API): pass
        expect(TestAPI.config.language).to.equal('en')
        TestAPI.config = {'key': '0123'}
        expect(TestAPI.config.key).to.equal('0123')

    def test_init(self):
        api = API(url='http://test')
        expect(api.config().url).to.equal('http://test/')

    def test_config(self):
        expect(self.api.config().language).to.equal('en')
        expect(self.api.config(language='ru').language).to.equal('ru')

    def test_register(self):
        class TestAPI(API): pass
        class MyAPI(TestAPI): pass
        # registers valid API
        TestAPI.register('test1', MyAPI)
        expect(TestAPI.test1).to.be.a(MyAPI)
        # avoids wrong API class
        TestAPI.register('test2', object)
        with self.assertRaises(AttributeError):
            TestAPI.test2
        TestAPI.register('test2', TestAPI)
        with self.assertRaises(AttributeError):
            TestAPI.test2
        # avoids wrong API name
        TestAPI.register('config', MyAPI)
        expect(TestAPI._api).to_not.contain('config')
        TestAPI.register(100, MyAPI)
        expect(TestAPI._api).to_not.contain(100)
        # doesn't create more that on instance for same API classes
        TestAPI.register('test3', MyAPI)
        api = TestAPI.test3
        TestAPI.register('test3', MyAPI)
        expect(api).to.be(TestAPI.test3)

    @httpretty.activate
    def test_request_with_wrong_function(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://api.wikimapia.org',
            body='{"debug":{"code":1001,"message":"Function not found"}}',
            content_type="application/json"
        )
        with self.assertRaises(FunctionNameError):
            self.api.request('test')

    @httpretty.activate
    def test_request_with_error(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://api.wikimapia.org',
            body='{"debug":{"code":1010,"message":"Other error"}}',
            content_type="application/json"
        )
        try:
            self.api.request('test')
            self.assertFail()
        except RequestError as err:
            expect('{}'.format(err)).to.equal('Other error')
            expect(err.code).to.equal(1010)

    @httpretty.activate
    def test_request_excludes_config_keys(self):
        httpretty.register_uri(httpretty.GET, 'http://api.wikimapia.org',
                               body='{"t":1}', content_type="application/json")
        self.api.request('test', delay=5000)
        expect(httpretty.last_request()).to_not.have.property('delay')

    @httpretty.activate
    def test_request_with_compression(self):
        with open(path.join(cwd, 'data/reply.gz'), 'rb') as f:
            data = f.read()
        httpretty.register_uri(httpretty.GET, 'http://api.wikimapia.org',
                               body=data, content_type="application/json")
        result = self.api.request('test', compression=True)
        expect(result['id']).to.equal(55)
