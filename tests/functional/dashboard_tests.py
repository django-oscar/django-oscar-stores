from django.core.urlresolvers import reverse
from oscar.test.testcases import WebTestCase

from tests.factories import StoreFactory, StoreAddressFactory


class TestDashboardStoreSearchForm(WebTestCase):
    is_staff = True
    is_anonymous = False

    def setUp(self):
        super(TestDashboardStoreSearchForm, self).setUp()

        location = '{"type": "Point", "coordinates": [144.917908,-37.815751]}'
        location = 'POINT(144.917908 -37.815751)'

        self.store1 = StoreFactory(name='store1', location=location)
        self.store2 = StoreFactory(name='store2', location=location)

        StoreAddressFactory(
            store=self.store1, line1='Great Portland st., London')
        StoreAddressFactory(
            store=self.store2, line1='Sturt Street, Melbourne')

    def test_list_with_search(self):
        resp = self.get(reverse('stores-dashboard:store-list') + '?address=portland+london')
        self.assertIn('form', resp.context)
        self.assertEqual(resp.context['form'].cleaned_data, {'address': 'portland london',
                                                             'name': ''})
        self.assertEqual(list(resp.context['object_list']), [self.store1])
