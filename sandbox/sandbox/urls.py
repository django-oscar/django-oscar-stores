from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.i18n import javascript_catalog
from oscar.app import application

from stores.app import application as stores_app
from stores.dashboard.app import application as dashboard_app

admin.autodiscover()

js_info_dict = {
    'packages': ('stores',),
}

urlpatterns = [
    url(r'^dashboard/stores/', dashboard_app.urls),
    url(r'^stores/', stores_app.urls),
    url(r'^', application.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name="javascript-catalogue"),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
