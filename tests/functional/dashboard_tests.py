from django.db.models import get_model
from django.core.urlresolvers import reverse

from django_dynamic_fixture import G
from oscar_testsupport.testcases import WebTestCase


Store = get_model('stores', 'Store')
StoreAddress = get_model('stores', 'StoreAddress')


class TestDashboardStoreSearchForm(WebTestCase):
    is_staff = True
    is_anonymous = False

    def setUp(self):
        super(TestDashboardStoreSearchForm, self).setUp()

        location = '{"type": "Point", "coordinates": [144.917908,-37.815751]}'

        self.store1 = G(Store, name='store1', location=location)
        self.store2 = G(Store, name='store2', location=location)

        G(StoreAddress, store=self.store1,
                        line1='Great Portland st., London')
        G(StoreAddress, store=self.store2,
                        line1='Sturt Street, Melbourne')
        
    def test_list_with_search(self):
        resp = self.get(reverse('stores-dashboard:store-list') + '?address=portland+london')
        self.assertIn('form', resp.context)
        self.assertEqual(resp.context['form'].cleaned_data, {'address': 'portland london',
                                                             'name': ''})
        self.assertEqual(list(resp.context['object_list']), [self.store1])
