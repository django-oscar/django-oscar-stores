from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Warning, register
from django.utils.translation import gettext_lazy as _


class StoresConfig(AppConfig):
    label = 'stores'
    name = 'stores'
    verbose_name = _('Stores')


@register()
def settings_check(app_configs, **kwargs):
    errors = []
    if not getattr(settings, 'GOOGLE_MAPS_API_KEY', False):
        errors.append(
            Warning(
                'Missing GOOGLE_MAPS_API_KEY setting',
                hint='The stores app should have a Google Maps API key to use Google Maps APIs',
                id='stores.E001',
            )
        )
    return errors
