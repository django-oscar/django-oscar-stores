import unittest
from django_dynamic_fixture import G
from django.db.models import get_model

from stores.dashboard.forms import DashboardStoreSearchForm


Store = get_model('stores', 'Store')
StoreAddress = get_model('stores', 'StoreAddress')


class TestDashboardStoreSearchForm(unittest.TestCase):
    def test_filters(self):
        f = DashboardStoreSearchForm()

        location = '{"type": "Point", "coordinates": [144.917908,-37.815751]}'

        store1 = G(Store, name='store1', location=location)
        store2 = G(Store, name='store2', location=location)

        G(StoreAddress, store=store1,
                        line1='Great Portland st., London')
        G(StoreAddress, store=store2,
                        line1='Sturt Street, Melbourne')
        
        f.cleaned_data = {'address': 'portland st, london'}
        qs = f.apply_filters(Store.objects.all())
        self.assertEquals(list(qs), [store1])

        f.cleaned_data = {'name': 'store2'}
        qs = f.apply_filters(Store.objects.all())
        self.assertEquals(list(qs), [store2])

        f.cleaned_data = {'name': 'store2', 'address': 'london'}
        qs = f.apply_filters(Store.objects.all())
        self.assertEquals(list(qs), [])
