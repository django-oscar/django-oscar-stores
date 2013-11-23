from django.conf.urls import patterns, url

from oscar.core.application import Application

from stores.dashboard import views


class StoresDashboardApplication(Application):
    name = 'stores-dashboard'
    default_permissions = ['is_staff',]
    permissions_map = {
        'store-list': (['is_staff'], ['partner.dashboard_access']),
        'store-create': (['is_staff'], ['partner.dashboard_access']),
        'store-update': (['is_staff'], ['partner.dashboard_access']),
    }
    
    
    store_list_view = views.StoreListView
    store_create_view = views.StoreCreateView
    store_update_view = views.StoreUpdateView
    store_delete_view = views.StoreDeleteView

    store_group_list_view = views.StoreGroupListView
    store_group_create_view = views.StoreGroupCreateView
    store_group_update_view = views.StoreGroupUpdateView
    store_group_delete_view = views.StoreGroupDeleteView

    def get_urls(self):
        urlpatterns = patterns('',
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
        )
        return self.post_process_urls(urlpatterns)


application = StoresDashboardApplication()
