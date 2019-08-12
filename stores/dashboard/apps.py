from django.conf.urls import url

from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class StoresDashboardConfig(OscarDashboardConfig):

    name = 'stores.dashboard'
    label = 'stores_dashboard'

    namespace = 'stores-dashboard'

    default_permissions = ['is_staff']

    def ready(self):
        self.store_list_view = get_class('stores.dashboard.views', 'StoreListView')
        self.store_create_view = get_class('stores.dashboard.views', 'StoreCreateView')
        self.store_update_view = get_class('stores.dashboard.views', 'StoreUpdateView')
        self.store_delete_view = get_class('stores.dashboard.views', 'StoreDeleteView')

        self.store_group_list_view = get_class('stores.dashboard.views', 'StoreGroupListView')
        self.store_group_create_view = get_class('stores.dashboard.views', 'StoreGroupCreateView')
        self.store_group_update_view = get_class('stores.dashboard.views', 'StoreGroupUpdateView')
        self.store_group_delete_view = get_class('stores.dashboard.views', 'StoreGroupDeleteView')

    def get_urls(self):
        urls = [
            url(
                r'^$',
                self.store_list_view.as_view(),
                name='store-list'
            ),
            url(
                r'^create/$',
                self.store_create_view.as_view(),
                name='store-create'
            ),
            url(
                r'^update/(?P<pk>[\d]+)/$',
                self.store_update_view.as_view(),
                name='store-update'
            ),
            url(
                r'^delete/(?P<pk>[\d]+)/$',
                self.store_delete_view.as_view(),
                name='store-delete'
            ),
            url(
                r'^groups/$',
                self.store_group_list_view.as_view(),
                name='store-group-list'
            ),
            url(
                r'^groups/create/$',
                self.store_group_create_view.as_view(),
                name='store-group-create'
            ),
            url(
                r'^groups/update/(?P<pk>[\d]+)/$',
                self.store_group_update_view.as_view(),
                name='store-group-update'
            ),
            url(
                r'^groups/delete/(?P<pk>[\d]+)/$',
                self.store_group_delete_view.as_view(),
                name='store-group-delete'
            ),
        ]
        return self.post_process_urls(urls)
