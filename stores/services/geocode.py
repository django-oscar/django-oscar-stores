import requests
from django.contrib.gis.geos import Point


class ServiceError(Exception):
    pass

class InvalidResponse(ServiceError):
    pass

class ZeroResuls(ServiceError):
    pass

class OverQueryLimit(ServiceError):
    pass

class RequestDenied(ServiceError):
    pass

class InvalidRequest(ServiceError):
    pass

class UnknownError(ServiceError):
    pass


code_to_exception_map = {
    'ZERO_RESULTS': ZeroResuls,
    'OVER_QUERY_LIMIT': OverQueryLimit,
    'REQUEST_DENIED': RequestDenied,
    'INVALID_REQUEST': InvalidRequest,
    'UNKNOWN_ERROR': UnknownError,
}


def get_response_exception(status):
    return code_to_exception_map.get(status, UnknownError)


class BaseGeoCodeService(object):
    """
    Base class to geocode a search query.
    """
    get = staticmethod(requests.get)

    def geocode(self, query):
        return Point(0, 0)


class GeoCodeService(BaseGeoCodeService):
    """
    Geocode a search query using Google's API
    """
    def run_query(self, query):
        payload = {
            'address': query,
            'sensor': 'false',
        }
        response = self.get(
            'http://maps.googleapis.com/maps/api/geocode/json', params=payload)

        if response.status_code != 200:
            raise InvalidResponse(response.status_code, response.content)

        data = response.json()

        return data

    def geocode(self, query):
        data = self.run_query(query)

        if not data['status'] == 'OK':
            errorcls = get_response_exception(data['status'])
            raise errorcls(data['status'])

        location = data['results'][0]['geometry']['location']
        return Point(location['lng'], location['lat'])
