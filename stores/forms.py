from django import forms
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import get_model
from django.utils.translation import ugettext as _

from stores.services import geocode

StoreGroup = get_model('stores', 'StoreGroup')


class StoreSearchForm(forms.Form):
    latitude = forms.CharField(widget=forms.HiddenInput, required=False)
    longitude = forms.CharField(widget=forms.HiddenInput, required=False)
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _("Enter your postcode or address..."),
                'class': 'search-query',
            }))
    group = forms.ModelChoiceField(
        required=False,
        queryset=StoreGroup.objects.none(),
        widget=forms.Select(attrs={'data-behaviours': 'filter-group'}),
    )

    def __init__(self, *args, **kwargs):
        super(StoreSearchForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = StoreGroup.objects.all()

    def clean(self):
        cleaned_data = super(StoreSearchForm, self).clean()
        self.point = self.geocoordinates(cleaned_data)
        return cleaned_data

    def geocoordinates(self, data):
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        if latitude and longitude:
            return GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

        query = data.get('query', None)
        if query is not None:
            return geocode(query)
