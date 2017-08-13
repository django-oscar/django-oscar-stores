from django.template import Context, Template
from django.test import TestCase
from oscar.test.factories import ProductFactory

from tests.factories import StoreFactory, StoreStockFactory


class StoreStockTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()
        self.store1_location = '{"type": "Point", "coordinates": [87.39,12.02]}'
        self.store2_location = '{"type": "Point", "coordinates": [88.39,11.02]}'
        self.store1 = StoreFactory(
            is_pickup_store=True, location=self.store1_location)
        self.store2 = StoreFactory(
            is_pickup_store=True, location=self.store2_location)

        self.store_stock1 = StoreStockFactory(
            store=self.store1, product=self.product)
        self.store_stock1 = StoreStockFactory(
            store=self.store2, product=self.product)

    def test_store_stock_loads(self):
        Template(
            '{% load store_stock %}'
        ).render(Context())
