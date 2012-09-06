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

class OpeningTimeForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit', True)
        kwargs['commit'] = False
        obj = super(OpeningTimeForm, self).save(*args, **kwargs)
        obj.display_order = self.get_display_order()
        if commit:
            obj.save()
        return obj

    def get_display_order(self):
        return self.prefix.split('-').pop()

    class Meta:
        model = get_model('stores', 'openingtime')
        exclude = ('display_order',)
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': _("e.g. Friday or Monday - Friday")}
            ),
            'time': forms.TextInput(
                attrs={'placeholder': _("e.g. 9am - 8pm")}
            ),
        }
