from unittest import TestCase
from stores.services import GeoCode
from mock import patch, Mock


class GeoCodeTest(TestCase):
    def test_geocode_servererror(self):
        response = Mock()
        response.status_code = 500
        get = Mock(return_value=response)

        with patch.object(GeoCode, 'get', get):
            self.assertRaises(GeoCode.ResponseError, GeoCode.geocode, 'Address query')

    def test_geocode_zeroresults(self):
        response = Mock()
        response.status_code = 200
        response.json = Mock(return_value={'results': [], 'status': 'ZERO_RESULTS'})
        get = Mock(return_value=response)

        with patch.object(GeoCode, 'get', get):
            self.assertRaises(GeoCode.ZeroResultsError, GeoCode.geocode, 'Address query')
