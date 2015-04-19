import unittest
import httpretty
from sure import expect

from wikimapia_api.api import API
from wikimapia_api.list_result import ListResult
import wikimapia_api.category_api
from .helpers import mock_request, mock_list_request, without_resource_warnings

class TestCategoryAPI(unittest.TestCase):
    def setUp(self):
        API.config = {'compression': False, 'delay': 1}
        API.clear_entire_cache()

    def tearDown(self):
        API.config.reset()

    @httpretty.activate
    @without_resource_warnings
    def test_getbyid(self):
        mock_request('category.getbyid.203.json')
        expect(API.categories[203]['amount']).to.equal(750827)
        expect(API.categories.get(203)['amount']).to.equal(750827)

    @httpretty.activate
    @without_resource_warnings
    def test_getall(self):
        mock_list_request('category.getall')
        l = API.categories.all()
        expect(l).to.be.a(ListResult)
        expect(len(l)).to.equal(200)
        expect(l[0]['id']).to.equal(46535)
        expect(l[1]['id']).to.equal(46534)
        expect(l[100]['id']).to.equal(44733)
