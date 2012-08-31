from django.test import TestCase

from django_dynamic_fixture import get

from chocolatebox.stores.models import Store


class StoreTests(TestCase):

    def test_getting_shipping_data(self):
        store = get(Store)
        self.assertItemsEqual(store.get_shipping_data(), [
            'line1', 'line2', 'line3', 'line4',
            'postcode', 'country', 'state'
        ])

    def test_pickup_stores_query(self):
        store1 = get(Store, is_pickup_store=True)
        store2 = get(Store, is_pickup_store=True)
        get(Store, is_pickup_store=False)
        store4 = get(Store, is_pickup_store=True)

        stores = Store.objects.pickup_stores()
        self.assertItemsEqual(
            stores,
            [store1, store2, store4]
        )
