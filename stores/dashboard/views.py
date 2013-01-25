from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from extra_views import (CreateWithInlinesView, UpdateWithInlinesView,
                         InlineFormSet)

from stores.dashboard import forms
from stores.utils import get_current_ip

Store = get_model('stores', 'Store')
StoreGroup = get_model('stores', 'StoreGroup')
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


class OpeningPeriodInline(InlineFormSet):
    extra = 7
    max_num = 7
    model = OpeningPeriod
    form_class = forms.OpeningPeriodForm


class StoreEditMixin(object):
    inlines = [OpeningPeriodInline, StoreAddressInline]

    def get_form_kwargs(self):
        kwargs = super(StoreEditMixin, self).get_form_kwargs()
        kwargs['current_ip'] = get_current_ip(self.request)
        return kwargs


class StoreCreateView(StoreEditMixin, CreateWithInlinesView):
    model = Store
    template_name = "stores/dashboard/store_update.html"
    form_class = forms.StoreForm
    success_url = reverse_lazy('stores-dashboard:store-list')

    def get_context_data(self, **kwargs):
        ctx = super(StoreCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Create new store")
        return ctx

    def forms_valid(self, form, inlines):
        msg = render_to_string('stores/dashboard/messages/store_saved.html',
                               {'store': self.object})
        messages.success(self.request, msg, extra_tags='safe')
        return super(StoreCreateView, self).forms_valid(form, inlines)


class StoreUpdateView(StoreEditMixin, UpdateWithInlinesView):
    model = Store
    template_name = "stores/dashboard/store_update.html"
    form_class = forms.StoreForm
    success_url = reverse_lazy('stores-dashboard:store-list')

    def get_context_data(self, **kwargs):
        ctx = super(StoreUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx

    def forms_valid(self, form, inlines):
        msg = render_to_string('stores/dashboard/messages/store_saved.html',
                               {'store': self.object})
        messages.success(self.request, msg, extra_tags='safe')
        return super(StoreUpdateView, self).form_valid(form)


class StoreDeleteView(generic.DeleteView):
    model = Store
    template_name = "stores/dashboard/store_delete.html"
    success_url = reverse_lazy('stores-dashboard:store-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        for time in self.object.opening_times.all():
            time.delete()
        return super(StoreDeleteView, self).delete(request, *args, **kwargs)


class StoreGroupListView(generic.ListView):
    model = StoreGroup
    context_object_name = 'group_list'
    template_name = "stores/dashboard/store_group_list.html"


class StoreGroupCreateView(generic.CreateView):
    model = StoreGroup
    template_name = "stores/dashboard/store_group_update.html"
    success_url = reverse_lazy('stores-dashboard:store-group-list')

    def get_context_data(self, **kwargs):
        ctx = super(StoreGroupCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Create new store group")
        return ctx


class StoreGroupUpdateView(generic.UpdateView):
    model = StoreGroup
    template_name = "stores/dashboard/store_group_update.html"
    success_url = reverse_lazy('stores-dashboard:store-group-list')

    def get_context_data(self, **kwargs):
        ctx = super(StoreGroupUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx


class StoreGroupDeleteView(generic.DeleteView):
    model = StoreGroup
    template_name = "stores/dashboard/store_group_delete.html"
    success_url = reverse_lazy('stores-dashboard:store-group-list')
