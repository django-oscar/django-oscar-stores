from django.contrib import admin

from stores.models import Store, StoreGroup, OpeningTime


admin.site.register(Store)
admin.site.register(StoreGroup)
admin.site.register(OpeningTime)
