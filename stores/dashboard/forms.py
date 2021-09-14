from django import forms
from django.contrib.gis.forms import fields
from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from oscar.core.loading import get_class, get_model

OpeningPeriod = get_model('stores', 'OpeningPeriod')
Store = get_model('stores', 'Store')


class StoreAddressForm(forms.ModelForm):

    class Meta:
        model = get_model('stores', 'StoreAddress')
        fields = [
            'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country']


class StoreForm(forms.ModelForm):
    location = fields.GeometryField(widget=forms.HiddenInput())

    class Meta:
        model = Store
        fields = [
            'name', 'manager_name', 'phone', 'email', 'reference', 'image',
            'description', 'location', 'group', 'is_pickup_store', 'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure that we store the initial data as GeoJSON so that
        # it is easier for us to use it in Javascript.
        instance = kwargs.get('instance', None)
        if instance:
            self.initial['location'] = instance.location.geojson

    def clean_reference(self):
        ref = self.cleaned_data['reference']
        if ref == "":
            return None
        return ref


class OpeningPeriodForm(forms.ModelForm):

    class Meta:
        model = OpeningPeriod
        fields = ['start', 'end']
        widgets = {
            'start': forms.TimeInput(
                format='%H:%M',
                attrs={'placeholder': _("e.g. 9 AM, 11:30, etc.")}
            ),
            'end': forms.TimeInput(
                format='%H:%M',
                attrs={'placeholder': _("e.g. 5 PM, 18:30, etc.")}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.weekday = kwargs.pop('weekday')
        self.store = kwargs.pop('store')

        super().__init__(*args, **kwargs)
        time_input = ['%H:%M', '%H', '%I:%M%p', '%I%p', '%I:%M %p', '%I %p']
        self.fields['start'].input_formats = time_input
        self.fields['end'].input_formats = time_input

    def save(self, commit=True):
        self.instance.store = self.store
        self.instance.weekday = self.weekday
        return super().save(commit=commit)


class DashboardStoreSearchForm(forms.Form):
    name = forms.CharField(label=_('Store name'), required=False)
    address = forms.CharField(label=_('Address'), required=False)

    def is_empty(self):
        d = getattr(self, 'cleaned_data', {})
        empty = lambda key: not d.get(key, None)
        return empty('name') and empty('address')

    def apply_address_filter(self, qs, value):
        words = value.replace(',', ' ').split()
        q = [Q(address__search_text__icontains=word) for word in words]
        return qs.filter(*q)

    def apply_name_filter(self, qs, value):
        return qs.filter(name__icontains=value)

    def apply_filters(self, qs):
        for key, value in self.cleaned_data.items():
            if value:
                qs = getattr(self, 'apply_%s_filter' % key)(qs, value)
        return qs


class IsOpenForm(forms.Form):
    open = forms.BooleanField(label=_('Open'), required=False)

    def __nonzero__(self):
        self.is_valid()
        return self.cleaned_data['open']

    def __bool__(self):
        return self.__nonzero__()


BaseOpeningPeriodFormset = forms.inlineformset_factory(
    Store,
    OpeningPeriod,
    form=OpeningPeriodForm,
    extra=10,
    min_num=0,
    max_num=30,     # Reasonably safe number of maximum period intervals per day
    validate_min=True,
    validate_max=True
)


class OpeningPeriodFormset(BaseOpeningPeriodFormset):

    def __init__(self, weekday, data, instance=None):
        self.weekday = weekday
        if instance:
            queryset = instance.opening_periods.all().filter(weekday=weekday)
        else:
            queryset = OpeningPeriod.objects.none()
        prefix = 'day-%d' % weekday

        self.openform = IsOpenForm(data=data or None, prefix=prefix, initial={
            'open': len(queryset) > 0
        })

        self.open = self.openform['open']

        super().__init__(data=data, instance=instance, prefix=prefix, queryset=queryset)

    def get_weekday_display(self):
        return force_str(OpeningPeriod.WEEK_DAYS[self.weekday])

    def get_form_kwargs(self, index):
        return {
            'store': self.instance,
            'weekday': self.weekday,
        }

    def save(self, *args, **kwargs):
        if not self.openform:
            for form in self:
                if form.instance.pk:
                    form.instance.delete()
        else:
            return super().save(*args, **kwargs)


class OpeningHoursFormset:
    def __init__(self, data, instance):
        self.data = data or None
        self.instance = instance
        self.forms = [self.construct_sub_formset(weekday) for weekday in
                      OpeningPeriod.WEEK_DAYS]

    def __iter__(self):
        return iter(self.forms)

    def __getitem__(self, key):
        return self.forms[key]

    def construct_sub_formset(self, weekday):
        OpeningPeriodFormset = get_class('stores.dashboard.forms', 'OpeningPeriodFormset')
        return OpeningPeriodFormset(
            weekday,
            self.data or None,
            self.instance,
        )

    def is_valid(self):
        return all([form.is_valid() for form in self.forms])

    def save(self):
        for form in self:
            form.save()


class OpeningHoursInline:
    def __init__(self, model, request, instance, kwargs=None, view=None):
        self.data = request.POST
        self.instance = instance

    def construct_formset(self):
        OpeningHoursFormset = get_class('stores.dashboard.forms', 'OpeningHoursFormset')
        return OpeningHoursFormset(
            self.data or None,
            self.instance,
        )
