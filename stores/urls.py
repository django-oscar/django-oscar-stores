from django.urls import path
from django.conf.urls import url

from oscar.core.loading import get_class

list_view = get_class("stores.views", "StoreListView")
detail_view = get_class("stores.views", "StoreDetailView")

app_name = "stores"

urlpatterns = [
    path("", list_view.as_view(), name="index"),
    url(r"^(?P<dummyslug>[\w-]+)/(?P<pk>\d+)/$", detail_view.as_view(), name="detail"),
]
