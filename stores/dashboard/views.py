from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse

from extra_views import (CreateWithInlinesView, UpdateWithInlinesView,
                         InlineFormSet)

from stores.dashboard import forms
from stores.utils import get_current_ip

Store = get_model('stores', 'Store')
StoreGroup = get_model('stores', 'StoreGroup')
StoreContact = get_model('stores', 'StoreContact')
OpeningPeriod = get_model('stores', 'OpeningPeriod')
StoreAddress = get_model('stores', 'StoreAddress')


class StoreListView(generic.ListView):
    model = Store
    template_name = "stores/dashboard/store_list.html"
    context_object_name = "store_list"


class StoreAddressInline(InlineFormSet):
    extra = 1
    max_num = 1
    can_delete = False
    model = StoreAddress
    form_class = forms.StoreAddressForm


class StoreContactInline(InlineFormSet):
    extra = 1
    max_num = 1
    can_delete = False
    model = StoreContact


class OpeningPeriodInline(InlineFormSet):
    extra = 7
    max_num = 7
    model = OpeningPeriod
    form_class = forms.OpeningPeriodForm


class StoreEditMixin(object):
    inlines = [OpeningPeriodInline, StoreAddressInline, StoreContactInline]

    def get_form_kwargs(self):
        kwargs = super(StoreEditMixin, self).get_form_kwargs()
        kwargs['current_ip'] = get_current_ip(self.request)
        return kwargs


class StoreCreateView(StoreEditMixin, CreateWithInlinesView):
    model = Store
    template_name = "stores/dashboard/store_update.html"
    form_class = forms.StoreForm

    def get_success_url(self):
        return reverse('stores-dashboard:store-list')


class StoreUpdateView(StoreEditMixin, UpdateWithInlinesView):
    model = Store
    template_name = "stores/dashboard/store_update.html"
    form_class = forms.StoreForm

    def get_success_url(self):
        return reverse('stores-dashboard:store-list')


class StoreDeleteView(generic.DeleteView):
    model = Store
    template_name = "stores/dashboard/store_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for time in self.object.opening_times.all():
            time.delete()
        return super(StoreDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('stores-dashboard:store-list')


class StoreGroupListView(generic.ListView):
    model = StoreGroup
    context_object_name = 'group_list'
    template_name = "stores/dashboard/store_group_list.html"


class StoreGroupCreateView(generic.CreateView):
    model = StoreGroup
    template_name = "stores/dashboard/store_group_update.html"

    def get_success_url(self):
        return reverse('stores-dashboard:store-group-list')


class StoreGroupUpdateView(generic.UpdateView):
    model = StoreGroup
    template_name = "stores/dashboard/store_group_update.html"

    def get_success_url(self):
        return reverse('stores-dashboard:store-group-list')


class StoreGroupDeleteView(generic.DeleteView):
    model = StoreGroup
    template_name = "stores/dashboard/store_group_delete.html"

    def get_success_url(self):
        return reverse('stores-dashboard:store-group-list')
