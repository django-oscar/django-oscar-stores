from django.conf import settings


def get_current_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geographic_srid():
    return getattr(settings, 'STORES_GEOGRAPHIC_SRID', 3577)


def get_geodetic_srid():
    return getattr(settings, 'STORES_GEODETIC_SRID', 4326)
