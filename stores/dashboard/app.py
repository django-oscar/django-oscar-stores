from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

from oscar.core.application import Application
from oscar.views.decorators import staff_member_required
from oscar.apps.dashboard.nav import register, Node

from stores.dashboard import views

node = Node(_('Store manager'))
node.add_child(Node(_('Stores'), 'stores-dashboard:store-list'))
node.add_child(Node(_('Store groups'), 'stores-dashboard:store-group-list'))
register(node, 100)


class StoresDashboardApplication(Application):
    name = 'stores-dashboard'

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

    def get_url_decorator(self, url_name):
        return staff_member_required

application = StoresDashboardApplication()
