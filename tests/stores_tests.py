from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django_webtest import WebTest
from django_dynamic_fixture import get as G

from oscar.apps.address.models import Country

from stores.models import Store


class TestStore(TestCase):

    def test_querying_available_pickup_stores(self):
        store1 = G(Store, is_pickup_store=True)
        store2 = G(Store, is_pickup_store=True)
        G(Store, is_pickup_store=False)
        store4 = G(Store, is_pickup_store=True)

        stores = Store.objects.pickup_stores()
        self.assertItemsEqual(
            list(stores),
            [store1, store2, store4]
        )


class StoresWebTest(WebTest):
    is_staff = False
    is_anonymous = True
    username = 'testuser'
    email = 'testuser@buymore.com'
    password = 'somefancypassword'

    def setUp(self):
        self.user = None
        if not self.is_anonymous:
            self.user = User.objects.create(
                username=self.username,
                email=self.email,
                password=self.password,
                is_staff=self.is_staff
            )

    def get(self, url, **kwargs):
        kwargs.setdefault('user', self.user)
        return self.app.get(url, **kwargs)

    def post(self, url, **kwargs):
        kwargs.setdefault('user', self.user)
        return self.app.post(url, **kwargs)


class TestASignedInUser(StoresWebTest):
    is_staff = True
    is_anonymous = False

    def setUp(self):
        super(TestASignedInUser, self).setUp()
        self.country = G(
            Country,
            name="AUSTRALIA",
            printable_name="Australia",
            iso_3166_1_a2='AU',
            iso_3166_1_a3='AUS',
            iso_3166_1_numeric=36,
        )

    def test_can_create_a_new_store_without_opening_periods(self):
        url = reverse('stores-dashboard:store-create')
        page = self.get(url)
        create_form = page.form

        create_form['name'] = 'Sample Store'
        create_form['address-0-line1'] = '123 Invisible Street'
        #create_form['address-0-line2'] = '
        #create_form['address-0-line3
        create_form['address-0-line4'] = 'Awesometown'
        create_form['address-0-state'] = 'Victoria'
        create_form['address-0-postcode'] = '3456'
        create_form['address-0-country'] = 'AU'

        create_form['phone'] = '123456789'
        create_form['description'] = 'A short description of the store'
        create_form['is_pickup_store'] = False
        create_form['is_active'] = True
        page = create_form.submit()
        print page
