from django.contrib import admin

from chocolatebox.stores.models import Store, StoreGroup, OpeningTime


admin.site.register(Store)
admin.site.register(StoreGroup)
admin.site.register(OpeningTime)
