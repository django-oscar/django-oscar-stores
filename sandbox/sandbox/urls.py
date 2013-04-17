from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from oscar.app import shop
from stores.app import application as stores_app
from stores.dashboard.app import application as dashboard_app

admin.autodiscover()

js_info_dict = {
    'packages': ('stores',),
}

urlpatterns = patterns('',
    url(r'^dashboard/stores/', include(dashboard_app.urls)),
    url(r'^stores/', include(stores_app.urls)),
    url(r'^', include(shop.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
