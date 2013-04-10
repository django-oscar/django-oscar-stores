import requests
from django.contrib.gis.geos import Point


class GeoCode(object):
    class ResponseError(Exception):
        pass

    class ZeroResultsError(ResponseError):
        pass

    error_codes = {
        'ZERO_RESULTS': ZeroResultsError,
        'OVER_QUERY_LIMIT': ResponseError,
        'REQUEST_DENIED': ResponseError,
        'INVALID_REQUEST': ResponseError,
        'UNKNOWN_ERROR': ResponseError,
    }

    get = staticmethod(requests.get)

    @classmethod
    def run_query(cls, query):
        payload = {
            'address': query,
            'sensor': 'false',
        }
        response = cls.get(
            'http://maps.googleapis.com/maps/api/geocode/json', params=payload)

        if response.status_code != 200:
            raise cls.ResponseError(response.status_code, response.content)

        data = response.json()

        return data

    @classmethod
    def geocode(cls, query):
        """
        Geocode a search query using Google's API
        """
        data = cls.run_query(query)

        if not data['status'] == 'OK':
            errorcls = cls.error_codes.get(data['status'], cls.ResponseError)
            raise errorcls(data['status'])

        location = data['results'][0]['geometry']['location']
        return Point(location['lng'], location['lat'])
