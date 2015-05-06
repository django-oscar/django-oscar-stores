from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from oscar.test.factories import CountryFactory

from stores.models import Store

from tests.factories import StoreFactory


class TestStore(TestCase):

    def test_querying_available_pickup_stores(self):
        sample_location = '{"type": "Point", "coordinates": [88.39,11.02]}'
        store1 = StoreFactory(is_pickup_store=True, location=sample_location)
        store2 = StoreFactory(is_pickup_store=True, location=sample_location)
        StoreFactory(is_pickup_store=False, location=sample_location)
        store4 = StoreFactory(is_pickup_store=True, location=sample_location)

        stores = list(Store.objects.pickup_stores())

        self.assertEqual(len(stores), 3)
        self.assertIn(store1, stores)
        self.assertIn(store2, stores)
        self.assertIn(store4, stores)


def repr_opening_hours(store):
    r = {}
    for period in store.opening_periods.all().order_by('start'):
        if period.weekday not in r:
            r[period.weekday] = ''
        else:
            r[period.weekday] += ', '
        r[period.weekday] += '%s - %s' % (period.start.strftime('%H:%M'),
                                          period.end  .strftime('%H:%M'))
    return r


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
        self.country = CountryFactory(
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
        create_form['address-0-line4'] = 'Awesometown'
        create_form['address-0-state'] = 'Victoria'
        create_form['address-0-postcode'] = '3456'
        create_form['address-0-country'] = 'AU'
        create_form['location'] = '{"type": "Point", "coordinates": [30.203332,44.33333] }'

        create_form['description'] = 'A short description of the store'
        create_form['is_pickup_store'] = False
        create_form['is_active'] = True

        page = create_form.submit()

        self.assertRedirects(page, reverse('stores-dashboard:store-list'))

        self.assertEquals(Store.objects.count(), 1)

        store = Store.objects.all()[0]
        self.assertEquals(store.name, 'Sample Store')
        self.assertEquals(store.location.x, 30.203332)
        self.assertEquals(store.location.y, 44.33333)
        self.assertEquals(
            store.description,
            'A short description of the store'
        )
        self.assertEquals(store.is_pickup_store, False)
        self.assertEquals(store.is_active, True)

        self.assertEquals(store.address.line1, '123 Invisible Street')
        self.assertEquals(store.address.line4, 'Awesometown')
        self.assertEquals(store.address.state, 'Victoria')
        self.assertEquals(store.address.postcode, '3456')
        self.assertEquals(store.address.country, self.country)

        self.assertEquals(store.opening_periods.count(), 0)

    def test_workinghours_form(self):
        url = reverse('stores-dashboard:store-create')
        page = self.get(url)
        form = page.form

        form['name'] = 'WorkingHoursTest'
        form['location'] = '{"type": "Point", "coordinates": [88.39,11.02]}'

        form['day-1-open'] = True

        form['day-1-0-start'] = '10'
        form['day-1-0-end'] = '11'

        form['day-1-1-start'] = '12'
        form['day-1-1-end'] = '13'

        form['day-2-open'] = True

        form['day-2-0-start'] = '12'
        form['day-2-0-end'] = '13'

        form['day-3-0-start'] = '12'
        form['day-3-0-end'] = '13'

        resp = form.submit()

        if resp.context and 'form' in resp.context:
            assert False, repr(resp.context['form'].errors)

        store = Store.objects.get(name='WorkingHoursTest')
        assert store.opening_periods.count() == 3

        self.assertEquals(repr_opening_hours(store), {
            1: '10:00 - 11:00, 12:00 - 13:00',
            2: '12:00 - 13:00',
        })
