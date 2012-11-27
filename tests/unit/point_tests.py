from django.test import TestCase
from django.contrib.gis.geos.point import Point

from stores.models import Store


class TestALocation(TestCase):

    def test_can_be_set_for_a_store(self):
        store = Store(name='Test Store')
        store.location = Point(30.3333, 123.323)
        store.save()

        store = Store.objects.get(id=store.id)
        self.assertEquals(store.location.x, 30.3333)
        self.assertEquals(store.location.y, 123.323)
