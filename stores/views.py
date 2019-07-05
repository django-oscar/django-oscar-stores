from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from oscar.core.loading import get_class, get_model

StoreSearchForm = get_class('stores.forms', 'StoreSearchForm')
Store = get_model('stores', 'store')


class MapsContextMixin(object):

    def get_context_data(self, **kwargs):
        ctx = super(MapsContextMixin, self).get_context_data(**kwargs)
        ctx['maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return ctx


class StoreListView(MapsContextMixin, generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'
    form_class = StoreSearchForm
    title_template = "%(store_type)s %(filter)s"

    def get(self, request, *args, **kwargs):
        if self.is_form_submitted(request):
            self.form = self.form_class(data=request.GET)
        else:
            self.form = self.form_class()
        return super(StoreListView, self).get(request, *args, **kwargs)

    def is_form_submitted(self, request):
        return 'query' in request.GET

    def get_max_distance(self):
        """ Return max search distance when searching for stores """
        return getattr(settings, 'STORES_MAX_SEARCH_DISTANCE', None)

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
            queryset = queryset.annotate(distance=Distance('location', latlng))

            # Constrain by distance if set up
            max_distance = self.get_max_distance()
            if max_distance:
                queryset = queryset.filter(distance__lte=max_distance)

            # Order by distance
            queryset = queryset.order_by('distance')

        return queryset

    def get_title(self):
        title_kwargs = {
            'store_type': _('Stores'),
            'filter': '',
        }
        if self.form.is_valid():
            data = self.form.cleaned_data

            group = data.get('group', None)
            if group:
                title_kwargs['store_type'] = _('%(group)s stores') % {
                    'group': group.name,
                }

            latlng = self.form.point
            if latlng:
                if data['query']:
                    title_kwargs['filter'] = _('nearest to %(query)s') % {
                        'query': data['query']}
                else:
                    title_kwargs['filter'] = _('nearest to me')

        return _(self.title_template) % title_kwargs

    def get_context_data(self, **kwargs):
        ctx = super(StoreListView, self).get_context_data(**kwargs)

        ctx['form'] = self.form
        ctx['all_stores'] = self.model.objects.select_related('group', 'address').all()

        if hasattr(self.form, 'point') and self.form.point:
            coords = self.form.point.coords
            ctx['latitude'] = coords[1]
            ctx['longitude'] = coords[0]

        ctx['queryset_description'] = self.get_title()

        return ctx


class StoreDetailView(MapsContextMixin, generic.DetailView):
    model = Store
    template_name = 'stores/detail.html'
    context_object_name = 'store'
