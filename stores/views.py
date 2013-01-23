from django.views import generic
from django.db.models import get_model
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from django import http

from stores.forms import StoreSearchForm
from stores.utils import get_geographic_srid, get_geodetic_srid
from stores.services import geocode

Store = get_model('stores', 'store')


class StoreListView(generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'
    point = None

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)

        group = self.request.POST.get('group', None)
        if group:
            queryset = queryset.filter(group=group)

        if self.point:
            queryset = queryset.transform(
                get_geographic_srid()
            ).distance(
                self.point
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
        self.point = self.get_geocoordinates(request)
        if not self.point:
            messages.error(request, "Unable to find the searched for location")
            return http.HttpResponseRedirect('.')
        return self.get(request, *args, **kwargs)

    def get_geocoordinates(self, request):
        location = request.POST.get('location', None)
        query = request.POST.get('store_search', None)
        point = None
        if location:
            # There is a lat/lng submitted as part of the form (populated from
            # the Google Maps Autocomplete API).  We use this to filter out
            # search results.
            point = GEOSGeometry(location)
        elif query:
            # We geocode a raw query
            point = geocode(query)
        return point


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'stores/detail.html'
    context_object_name = 'store'
