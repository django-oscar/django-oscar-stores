from django.views import generic
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from stores.forms import StoreSearchForm
from stores.utils import get_geographic_srid, get_geodetic_srid

Store = get_model('stores', 'store')


class StoreListView(generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'
    form_class = StoreSearchForm
    title = _("All stores")

    def get(self, request, *args, **kwargs):
        if self.is_form_submitted(request):
            self.form = self.form_class(data=request.GET)
        else:
            self.form = self.form_class()
        return super(StoreListView, self).get(request, *args, **kwargs)

    def is_form_submitted(self, request):
        return 'query' in request.GET

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        group = data.get('group', None)
        if group:
            queryset = queryset.filter(group=group)

        latlng = self.form.point
        if latlng:
            queryset = queryset.transform(
                get_geographic_srid()
            ).distance(
                latlng
            ).transform(
                get_geodetic_srid()
            ).order_by('distance')

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(StoreListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form_class()
        ctx['all_stores'] = self.model.objects.all()

        query = None
        title = _("All stores")
        if self.form.is_valid():
            query = self.form.cleaned_data.get('query', None)
            if query:
                title = _('Stores nearest to %(query)s') % {'query': query}
            elif self.form.point:
                title = _('Stores nearest my location')
                query = _('Nearest to me')
            coords = self.form.point.coords
            ctx['latitude'] = coords[1]
            ctx['longitude'] = coords[0]

        ctx['title'] = title
        ctx['query'] = query

        return ctx


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'stores/detail.html'
    context_object_name = 'store'
