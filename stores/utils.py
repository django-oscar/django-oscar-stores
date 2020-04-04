from django.conf import settings


def get_geographic_srid():
    return getattr(settings, 'STORES_GEOGRAPHIC_SRID', 3577)


def get_geodetic_srid():
    return getattr(settings, 'STORES_GEODETIC_SRID', 4326)
