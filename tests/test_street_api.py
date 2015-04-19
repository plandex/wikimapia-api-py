import unittest
import httpretty
from sure import expect

from wikimapia_api.api import API
import wikimapia_api.street_api
from .helpers import mock_request, without_resource_warnings

class TestStreetAPI(unittest.TestCase):
    def setUp(self):
        API.config = {'compression': False, 'delay': 1}
        API.clear_entire_cache()

    def tearDown(self):
        API.config.reset()

    @httpretty.activate
    @without_resource_warnings
    def test_getbyid(self):
        mock_request('street.getbyid.1.json')
        expect(API.streets[1]['object_type']).to.equal('2')
        expect(API.streets.get(1)['object_type']).to.equal('2')
