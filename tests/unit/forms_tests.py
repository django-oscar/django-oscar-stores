from django.test import TestCase
from oscar.core.loading import get_model

from stores.dashboard.forms import DashboardStoreSearchForm

from tests.factories import StoreFactory, StoreAddressFactory


class TestDashboardStoreSearchForm(TestCase):

    def test_filters(self):
        f = DashboardStoreSearchForm()
        Store = get_model('stores', 'Store')

        location = '{"type": "Point", "coordinates": [144.917908,-37.815751]}'

        store1 = StoreFactory(name='store1', location=location)
        store2 = StoreFactory(name='store2', location=location)

        StoreAddressFactory(
            store=store1, line1='Great Portland st., London')

        StoreAddressFactory(
            store=store2, line1='Sturt Street, Melbourne')

        f.cleaned_data = {'address': 'portland st, london'}
        qs = f.apply_filters(Store.objects.all())
        self.assertEquals(list(qs), [store1])

        f.cleaned_data = {'name': 'store2'}
        qs = f.apply_filters(Store.objects.all())
        self.assertEquals(list(qs), [store2])

        f.cleaned_data = {'name': 'store2', 'address': 'london'}
        qs = f.apply_filters(Store.objects.all())
        self.assertEquals(list(qs), [])
