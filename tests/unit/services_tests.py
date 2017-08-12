from unittest import TestCase

from mock import Mock, patch

from stores.services import geocode


class GeoCodeTest(TestCase):
    def patch(self, *args, **kwargs):
        return patch.object(geocode.GeoCodeService, *args, **kwargs)

    def test_geocode_servererror(self):
        response = Mock()
        response.status_code = 500
        get = Mock(return_value=response)

        with self.patch('get', get):
            func = geocode.GeoCodeService().geocode
            error = geocode.InvalidResponse
            self.assertRaises(error, func, 'query')

    def test_geocode_zeroresults(self):
        response = Mock()
        response.status_code = 200
        response.json = Mock(return_value={'results': [], 'status': 'ZERO_RESULTS'})
        get = Mock(return_value=response)

        with self.patch('get', get):
            func = geocode.GeoCodeService().geocode
            error = geocode.ZeroResuls
            self.assertRaises(error, func, 'query')
