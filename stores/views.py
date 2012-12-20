from django.views import generic
from django.db.models import get_model
from django.contrib.gis.geos import GEOSGeometry

from stores.forms import StoreSearchForm
from stores.utils import get_geographic_srid, get_geodetic_srid


Store = get_model('stores', 'store')


class StoreListView(generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)

        group = self.request.POST.get('group', None)
        if group:
            queryset = queryset.filter(group=group)

        location = self.request.POST.get('location', None)
        if location:
            point = GEOSGeometry(location)
            queryset = queryset.transform(
                get_geographic_srid()
            ).distance(
                point
            ).transform(
                get_geodetic_srid()
            ).order_by('distance')
        return queryset

    def get_search_form(self):
        if self.request.POST:
            return StoreSearchForm(self.request.POST)
        return StoreSearchForm()

    def get_context_data(self, **kwargs):
        ctx = super(StoreListView, self).get_context_data(**kwargs)
        ctx['form'] = self.get_search_form()
        return ctx

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'stores/detail.html'
    context_object_name = 'store'
