from django.views import generic
from django.db.models import get_model

Store = get_model('stores', 'store')


class StoreListView(generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'stores/detail.html'
    context_object_name = 'store'
