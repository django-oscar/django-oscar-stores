from django import template
from django.db.models import get_model

StoreStock = get_model('stores', 'StoreStock')

register = template.Library()


@register.assignment_tag
def store_stock_for_product(product, location=None, limit=20):
    query_set = StoreStock.objects.filter(product=product)
    if location:
        #FIXME: this query currently only works on PostGIS. This is described in
        # the geodjango docs. This restricts the use of the stores package to only
        # be used with that backend which should be changed.
        query_set = query_set.distance(
            location,
            field_name='store__location'
        ).order_by('distance')
    else:
        query_set = query_set.order_by('store__name')
    return query_set[0:limit]
