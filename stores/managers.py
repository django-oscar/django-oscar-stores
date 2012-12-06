from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.db.models.query import GeoQuerySet


class StoreQuerySet(GeoQuerySet):

    def pickup_stores(self):
        return self.filter(is_pickup_store=True, is_active=True)


class StoreManager(GeoManager):

    def get_query_set(self):
        return StoreQuerySet(self.model)

    def pickup_stores(self):
        return self.get_query_set().pickup_stores()
