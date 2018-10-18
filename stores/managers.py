from django.contrib.gis.db.models import Manager


class StoreManager(Manager):

    def pickup_stores(self):
        return self.get_queryset().filter(is_pickup_store=True, is_active=True)
