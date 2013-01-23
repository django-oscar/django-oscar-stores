from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext as _

StoreGroup = get_model('stores', 'StoreGroup')


class StoreSearchForm(forms.Form):
    location = forms.CharField(widget=forms.HiddenInput)
    store_search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': _("Enter your postcode or address..."),
                'class': 'search-query',
            }))
    group = forms.ModelChoiceField(
        queryset=StoreGroup.objects.none(),
        widget=forms.Select(attrs={'data-behaviours': 'filter-group'}),
    )

    def __init__(self, *args, **kwargs):
        super(StoreSearchForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = StoreGroup.objects.all()
