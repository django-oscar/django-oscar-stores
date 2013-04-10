from django import forms
from django.db.models import Q, get_model
from django.contrib.gis.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geoip import HAS_GEOIP


class StoreAddressForm(forms.ModelForm):

    class Meta:
        model = get_model('stores', 'StoreAddress')
        exclude = ('title', 'first_name', 'last_name', 'search_text')


class StoreForm(forms.ModelForm):
    location = fields.GeometryField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        current_ip = kwargs.pop('current_ip', None)
        super(StoreForm, self).__init__(*args, **kwargs)

        # Make sure that we store the initial data as GeoJSON so that
        # it is easier for us to use it in Javascript.
        instance = kwargs.get('instance', None)
        if instance:
            self.initial['location'] = instance.location.geojson
        elif HAS_GEOIP:
            from django.contrib.gis.geoip import GeoIP
            point = GeoIP().geos(current_ip)
            if point:
                self.initial['location'] = point.geojson

    def clean_reference(self):
        ref = self.cleaned_data['reference']
        if ref == "":
            return None
        return ref

    class Meta:
        model = get_model('stores', 'Store')
        exclude = ('slug',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }


class OpeningPeriodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OpeningPeriodForm, self).__init__(*args, **kwargs)
        time_input = ['%H:%M', '%H', '%I:%M%p', '%I%p', '%I:%M %p', '%I %p']
        self.fields['start'].input_formats = time_input
        self.fields['end'].input_formats = time_input

    class Meta:
        model = get_model('stores', 'OpeningPeriod')
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': _("e.g. Christmas")}
            ),
            'start': forms.TimeInput(
                format='%H:%M',
                attrs={'placeholder': _("e.g. 9 AM, 11:30, etc.")}
            ),
            'end': forms.TimeInput(
                format='%H:%M',
                attrs={'placeholder': _("e.g. 5 PM, 18:30, etc.")}
            ),
        }

 
class DashboardStoreSearchForm(forms.Form):
    name = forms.CharField(label=_('Store name'), required=False)
    address = forms.CharField(label=_('Address'), required=False)

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
