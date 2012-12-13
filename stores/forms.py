from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext as _

StoreAddress = get_model('stores', 'StoreAddress')


class StoreSearchForm(forms.Form):

    STATE_CHOICES = (
        (_('VIC'), _('Victoria')),
        (_('NSW'), _('New South Wales')),
        (_('SA'), _('South Australia')),
        (_('TAS'), _('Tasmania')),
        (_('QLD'), _('Queensland')),
        (_('NT'), _('Northern Territory')),
    )

    location = forms.CharField(widget=forms.HiddenInput)
    store_search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _("Enter your postcode or suburb..."),
                'class': 'search-query'
            }
        )
    )
    #state = forms.ChoiceField(choices=STATE_CHOICES)
