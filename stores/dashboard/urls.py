from django.conf.urls import url

from oscar.core.loading import get_class

app_name = "stores_dashboard"

store_list_view = get_class("stores.dashboard.views", "StoreListView")
store_create_view = get_class("stores.dashboard.views", "StoreCreateView")
store_update_view = get_class("stores.dashboard.views", "StoreUpdateView")
store_delete_view = get_class("stores.dashboard.views", "StoreDeleteView")

store_group_list_view = get_class("stores.dashboard.views", "StoreGroupListView")
store_group_create_view = get_class("stores.dashboard.views", "StoreGroupCreateView")
store_group_update_view = get_class("stores.dashboard.views", "StoreGroupUpdateView")
store_group_delete_view = get_class("stores.dashboard.views", "StoreGroupDeleteView")

urlpatterns = [
    url(r"^$", store_list_view.as_view(), name="store-list"),
    url(r"^create/$", store_create_view.as_view(), name="store-create"),
    url(r"^update/(?P<pk>[\d]+)/$", store_update_view.as_view(), name="store-update"),
    url(r"^delete/(?P<pk>[\d]+)/$", store_delete_view.as_view(), name="store-delete"),
    url(r"^groups/$", store_group_list_view.as_view(), name="store-group-list"),
    url(
        r"^groups/create/$",
        store_group_create_view.as_view(),
        name="store-group-create",
    ),
    url(
        r"^groups/update/(?P<pk>[\d]+)/$",
        store_group_update_view.as_view(),
        name="store-group-update",
    ),
    url(
        r"^groups/delete/(?P<pk>[\d]+)/$",
        store_group_delete_view.as_view(),
        name="store-group-delete",
    ),
]
