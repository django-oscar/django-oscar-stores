from django.conf import settings
from django.conf.urls import url
from django.core.checks import Warning, register
from django.utils.translation import gettext_lazy as _

from oscar.core.application import OscarConfig
from oscar.core.loading import get_class


class StoresConfig(OscarConfig):

    name = 'stores'
    verbose_name = _('Stores')

    namespace = 'stores'

    def ready(self):
        self.list_view = get_class('stores.views', 'StoreListView')
        self.detail_view = get_class('stores.views', 'StoreDetailView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(),
                name='index'),
            url(r'^(?P<dummyslug>[\w-]+)/(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
        ]
        return self.post_process_urls(urls)


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
