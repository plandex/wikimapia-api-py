import unittest
import httpretty
from sure import expect

from wikimapia_api.list_result import ListResult
from wikimapia_api.category_api import CategoryAPI
from .helpers import mock_list_request, without_resource_warnings

class TestListResult(unittest.TestCase):
    def setUp(self):
        self.api = CategoryAPI(compression=False, delay=1)
        self.list = ListResult(self.api, 'category.getall')

    @httpretty.activate
    @without_resource_warnings
    def test_len(self):
        mock_list_request('category.getall')
        expect(len(self.list)).to.equal(200)
        query = httpretty.last_request().querystring
        expect(query['count'][0]).to.equal('5')

    @httpretty.activate
    @without_resource_warnings
    def test_index_access(self):
        mock_list_request('category.getall')
        expect(self.list[0]['id']).to.equal(46535)
        expect(self.list[1]['id']).to.equal(46534)
        expect(self.list[2]['id']).to.equal(46532)
        expect(self.list[100]['id']).to.equal(44733)
