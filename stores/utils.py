from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_current_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geographic_srid():
    try:
        return settings.STORES_SRID
    except AttributeError:
        raise ImproperlyConfigured(
            "A geographic SRID is required for distance calculation in"
            "kilometers, miles, etc."
        )

