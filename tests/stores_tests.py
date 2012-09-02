from django.test import TestCase

from django_dynamic_fixture import get as G

from stores.models import Store


class TestStore(TestCase):

    def test_getting_shipping_data(self):
        store = G(Store)
        self.assertItemsEqual(store.get_shipping_data(), [
            'line1', 'line2', 'line3', 'line4',
            'postcode', 'country', 'state'
        ])

    def test_querying_available_pickup_stores(self):
        store1 = G(Store, is_pickup_store=True)
        store2 = G(Store, is_pickup_store=True)
        G(Store, is_pickup_store=False)
        store4 = G(Store, is_pickup_store=True)

        stores = Store.objects.pickup_stores()
        self.assertItemsEqual(
            stores,
            [store1, store2, store4]
        )
