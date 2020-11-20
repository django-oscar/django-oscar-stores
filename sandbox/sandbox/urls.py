from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()

js_info_dict = {
    'packages': ('stores',),
}

urlpatterns = [
    path('dashboard/stores/', apps.get_app_config('stores_dashboard').urls),
    path('stores/', apps.get_app_config('stores').urls),
    path('', include(apps.get_app_config('oscar').urls[0])),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(**js_info_dict), name="javascript-catalog"),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
