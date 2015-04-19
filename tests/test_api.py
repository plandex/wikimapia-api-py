import unittest
import httpretty
from sure import expect
from os import path
from io import open

from wikimapia_api.api import API
from wikimapia_api.category_api import CategoryAPI
from wikimapia_api.errors import (FunctionNameError, RequestError,
                                  UnimplementedError)
from .helpers import mock_request, mock_list_request, without_resource_warnings

cwd = path.dirname(path.abspath(__file__))

class DummyAPI(API):
    def requst_key(self, function):
        return None

    def valid_params(self, function):
        return []

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = API(compression=False, delay=1)
        self.dummy = DummyAPI(compression=False, delay=1)

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

    def test_class_register(self):
        class TestAPI(API): pass
        class MyAPI(TestAPI):
            def test_method(self):
                return 'test_result'
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
        # creates attribute proxy
        TestAPI.register('test4', MyAPI, 'test_method')
        expect(TestAPI.test4()).to.equal('test_result')

    def test_class_clear_entire_cache(self):
        class TestAPI(API): pass
        class MyAPI(TestAPI): pass
        TestAPI.register('test1', MyAPI)
        TestAPI.test1._cache['test'] = 1
        TestAPI.clear_entire_cache()
        expect(TestAPI.test1._cache).to.be.empty

    def test_clear_cache(self):
        self.dummy._cache['test'] = 1
        self.dummy.clear_cache()
        expect(self.dummy._cache).to.be.empty

    def test_result_key(self):
        try:
            self.api.result_key('test')
            self.assertFail()
        except UnimplementedError as err:
            pass

    def test_valid_params(self):
        try:
            self.api.valid_params('test')
            self.assertFail()
        except UnimplementedError as err:
            pass

    @httpretty.activate
    @without_resource_warnings
    def test_request_with_wrong_function(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://api.wikimapia.org',
            body='{"debug":{"code":1001,"message":"Function not found"}}',
            content_type="application/json"
        )
        with self.assertRaises(FunctionNameError):
            self.dummy.request('test')

    @httpretty.activate
    @without_resource_warnings
    def test_request_with_error(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://api.wikimapia.org',
            body='{"debug":{"code":1010,"message":"Other error"}}',
            content_type="application/json"
        )
        try:
            self.dummy.request('test')
            self.assertFail()
        except RequestError as err:
            expect('{}'.format(err)).to.equal('Other error')
            expect(err.code).to.equal(1010)

    @httpretty.activate
    @without_resource_warnings
    def test_request_excludes_config_keys(self):
        mock_request('category.getbyid.203.json')
        self.dummy.request('test', {'delay': 5})
        query = httpretty.last_request().querystring
        expect(query).to_not.contain('delay')

    @httpretty.activate
    @without_resource_warnings
    def test_request_with_compression(self):
        mock_request('reply.gz')
        result = self.dummy.request('test', {'compression': True})
        expect(result['id']).to.equal(55)

    @httpretty.activate
    @without_resource_warnings
    def test_count_array(self):
        mock_list_request('category.getall')
        params = {'count': 100}
        expect(self.dummy.count_array('category.getall', params)).to.equal(200)
        expect(params['count']).to.equal(100)

    @httpretty.activate
    @without_resource_warnings
    def test_load_array(self):
        mock_list_request('category.getall')
        api = CategoryAPI(compression=False, delay=1)
        result = api.load_array('category.getall')
        expect(len(result)).to.equal(200)
