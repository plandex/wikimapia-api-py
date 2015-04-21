import unittest
import httpretty
from sure import expect

from wikimapia_api.api import API
import wikimapia_api.place_api
from wikimapia_api.list_result import ListResult, ListsResult
from .helpers import mock_request, mock_list_request, without_resource_warnings

class TestPlaceAPI(unittest.TestCase):
    def setUp(self):
        API.config = {'compression': False, 'delay': 1}
        API.clear_entire_cache()

    def tearDown(self):
        API.config.reset()

    @httpretty.activate
    @without_resource_warnings
    def test_getbyid(self):
        mock_request('place.getbyid.55.json')
        expect(API.places[55]['object_type']).to.equal(1)
        expect(API.places.get(55)['object_type']).to.equal(1)

    @httpretty.activate
    @without_resource_warnings
    def test_inside(self):
        # TODO: full testing here
        mock_list_request('place.getbyarea')
        l = API.places.inside(10, 20, 30, 40)
        expect(l).to.be.a(ListsResult)
        expect(len(l)).to.equal(810)

    @httpretty.activate
    @without_resource_warnings
    def test_in_tile(self):
        mock_list_request('place.getbyarea.tiles')
        l = API.places.in_tile(10, 20, 30)
        expect(l).to.be.a(ListResult)
        expect(len(l)).to.equal(27)
        expect(l[0]['id']).to.equal(55)

    @httpretty.activate
    @without_resource_warnings
    def test_nearest(self):
        mock_list_request('place.getnearest')
        l = API.places.nearest(10, 20)
        expect(l).to.be.a(ListResult)
        # strange, but real API returns found=0
        expect(len(l)).to.equal(0)
        expect(l[0]['id']).to.equal(12927832)

    @httpretty.activate
    @without_resource_warnings
    def test_search(self):
        mock_list_request('place.search')
        l = API.places.search('q', 10, 20)
        expect(l).to.be.a(ListResult)
        expect(len(l)).to.equal(445)
        expect(l[0]['id']).to.equal(55)
        expect(l[100]['id']).to.equal(385)
