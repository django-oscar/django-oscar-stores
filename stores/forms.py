from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext as _

StoreGroup = get_model('stores', 'StoreGroup')


class StoreSearchForm(forms.Form):

    location = forms.CharField(widget=forms.HiddenInput)
    group = forms.ModelChoiceField(
        queryset=StoreGroup.objects.all(),
        widget=forms.Select(
            attrs={
                'data-behaviours': 'filter-group'
            }
        )
    )
    store_search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _("Enter your postcode or suburb..."),
                'class': 'search-query'
            }
        )
    )
