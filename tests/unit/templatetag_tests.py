from django.test import TestCase
from django.db.models import get_model
from django.template import Template, Context

from django_dynamic_fixture import get as G

Product = get_model('catalogue', 'Product')
Store = get_model('stores', 'Store')
StoreStock = get_model('stores', 'StoreStock')


class StoreStockTest(TestCase):

    def setUp(self):
        self.product = G(Product)
        self.store1_location = '{"type": "Point", "coordinates": [87.39,12.02]}'
        self.store2_location = '{"type": "Point", "coordinates": [88.39,11.02]}'
        self.store1 = G(Store, is_pickup_store=True, location=self.store1_location)
        self.store2 = G(Store, is_pickup_store=True, location=self.store2_location)
        self.store_stock1 = G(StoreStock, store=self.store1, product=self.product)
        self.store_stock1 = G(StoreStock, store=self.store2, product=self.product)

    def test_store_stock_loads(self):
        Template(
            '{% load store_stock %}'
        ).render(Context())

    #def test_store_stock_for_product_returns_stock_lines(self):
    #    rendered = Template(
    #        """
    #        {% load store_stock %} {% store_stock_for_product product as store_stock %}
    #        {% for stock in store_stock %} {{ stock.store.name }} {% endfor %}
    #        """
    #    ).render(Context({
    #        'product': self.product
    #    }))
    #    self.assertTrue(self.store1.name in rendered)
    #    self.assertTrue(self.store2.name in rendered)

    #def test_store_stock_for_product_limits_when_asked(self):
    #    rendered = Template(
    #        """
    #        {% load store_stock %} {% store_stock_for_product product limit=1 as store_stock %}
    #        {% for stock in store_stock %} {{ stock.store.name }} {% endfor %}
    #        """
    #    ).render(Context({
    #        'product': self.product
    #    }))
    #    self.assertTrue(self.store1.name in rendered)

    #def test_store_stock_for_product_order_by_closed(self):
    #    rendered = Template(
    #        """
    #        {% load store_stock %} {% store_stock_for_product product location=loc as store_stock %}
    #        {% for stock in store_stock %}{{ stock.store.name }}{% endfor %}
    #        """
    #    ).render(Context({
    #        'product': self.product,
    #        'loc': '{"type": "Point", "coordinates": [88.39,11.02]}'
    #    }))
    #    self.assertTrue("%s%s" % (self.store2.name, self.store1.name) in rendered)
