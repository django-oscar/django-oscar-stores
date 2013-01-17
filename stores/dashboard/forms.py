from django import forms
from django.db.models import get_model
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

    class Meta:
        model = get_model('stores', 'Store')
        exclude = ('slug',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }


class OpeningPeriodForm(forms.ModelForm):

    class Meta:
        model = get_model('stores', 'OpeningPeriod')
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': _("e.g. Christmas")}
            ),
            'start': forms.TextInput(
                attrs={'placeholder': _("e.g. 9am, noon, etc.")}
            ),
            'end': forms.TextInput(
                attrs={'placeholder': _("e.g. 5pm, late, etc.")}
            ),
        }
