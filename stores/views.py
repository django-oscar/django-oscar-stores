from django.views import generic
from django.db.models import get_model
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry


from stores.forms import StoreSearchForm

Store = get_model('stores', 'store')
STORES_SRID = getattr(settings, 'STORES_SRID', 4326)


class StoreListView(generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'

    def get_queryset(self):
        if self.request.POST and self.request.POST['location']:
            point = GEOSGeometry(self.request.POST['location'])
            # save to session
            self.request.session['request_location'] = point
            return self.model.objects.filter(
                is_active=True
            ).transform(STORES_SRID).distance(point).order_by('distance')

        return self.model.objects.filter(is_active=True)

    def get_search_form(self):
        if self.request.POST:
            return StoreSearchForm(self.request.POST)
        return StoreSearchForm

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
