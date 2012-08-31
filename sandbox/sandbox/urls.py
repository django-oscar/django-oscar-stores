from django.contrib import admin
from django.conf.urls import patterns, include, url

from oscar.app import shop
from stores.app import application as stores_app
from stores.dashboard.app import application as dashboard_app

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(shop.urls)),
    url(r'^dashboard/stores/', include(dashboard_app.urls)),
    url(r'^stores/', include(stores_app.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
