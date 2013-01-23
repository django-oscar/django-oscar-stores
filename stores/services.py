import requests
from django.contrib.gis.geos import Point


def geocode(query):
    """
    Geocode a search query using Google's API
    """
    payload = {
        'address': query,
        'sensor': 'false',
    }
    response = requests.get(
        'http://maps.googleapis.com/maps/api/geocode/json', params=payload)
    if response.status_code != 200:
        return None
    data = response.json()
    if data and data['results']:
        location = data['results'][0]['geometry']['location']
        return Point(location['lng'], location['lat'])
    return None
