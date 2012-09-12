from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import get_model


class StoreAddressForm(forms.ModelForm):

    class Meta:
        model = get_model('stores', 'storeaddress')
        exclude = ('title', 'first_name', 'last_name', 'search_text')


class StoreForm(forms.ModelForm):

    class Meta:
        model = get_model('stores', 'store')
        exclude = ('slug',)
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 15}),
        }

class OpeningPeriodForm(forms.ModelForm):

    class Meta:
        model = get_model('stores', 'openingperiod')
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': _("e.g. Christmas")}
            ),
        }
