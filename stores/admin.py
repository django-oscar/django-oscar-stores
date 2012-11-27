from django.contrib import admin

from stores import models


admin.site.register(models.Store)
admin.site.register(models.StoreGroup)
admin.site.register(models.OpeningPeriod)
