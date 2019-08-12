from django.contrib import admin

from oscar.core.loading import get_model

Store = get_model('stores', 'Store')
StoreGroup = get_model('stores', 'StoreGroup')
OpeningPeriod = get_model('stores', 'OpeningPeriod')
StoreStock = get_model('stores', 'StoreStock')


class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Store, StoreAdmin)
admin.site.register(StoreGroup)
admin.site.register(OpeningPeriod)
admin.site.register(StoreStock)
