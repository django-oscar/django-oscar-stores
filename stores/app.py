from django.conf.urls import patterns, url

from oscar.core.application import Application

from stores import views


class StoresApplication(Application):
    name = 'stores'
    list_view = views.StoreListView
    detail_view = views.StoreDetailView

    def get_urls(self):
        urlpatterns = super(StoresApplication, self).get_urls()
        urlpatterns += patterns('',
            url(r'^$', self.list_view.as_view(),
                name='index'),
            url(r'^(?P<dummyslug>[\w-]+)/(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
        )
        return self.post_process_urls(urlpatterns)


application = StoresApplication()
