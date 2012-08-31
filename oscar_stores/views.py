from django.db.models import get_model
from django.views import generic

Store = get_model('stores', 'store')


class StoreListView(generic.ListView):
    model = Store
    template_name = 'stores/index.html'
    context_object_name = 'store_list'

    def get_context_data(self, **kwargs):
        """
        Get context data with additional list of store groups inside.
        """
        context = super(StoreListView, self).get_context_data(**kwargs)
        context['store_group_list'] = get_model('stores', 'storegroup').objects.all()
        return context


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'stores/detail.html'
    context_object_name = 'store'
