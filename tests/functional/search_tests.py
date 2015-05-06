from django.core.urlresolvers import reverse
from oscar.test.testcases import WebTestCase

from tests.factories import StoreFactory, StoreGroupFactory



class TestTheListOfStores(WebTestCase):
    anonymous = True

    def setUp(self):
        super(TestTheListOfStores, self).setUp()
        self.main_location = 'POINT(144.917908 -37.815751)'
        self.other_location = 'POINT(144.998401 -37.772895)'

        self.main_store = StoreFactory(
            name="Main store in Southbank",
            is_pickup_store=True,
            location=self.main_location,
        )
        self.other_store = StoreFactory(
            name="Other store in Northcote",
            is_pickup_store=True,
            location=self.other_location,
        )

    def test_displays_all_stores_unfiltered(self):
        page = self.get(reverse('stores:index'))
        self.assertContains(page, self.main_store.name)
        self.assertContains(page, self.other_store.name)

    def test_can_be_filtered_by_location(self):
        page = self.get(reverse('stores:index'))
        search_form = page.forms['store-search']
        search_form['latitude'] = '-37.7736132'
        search_form['longitude'] = '-144.9997396'
        page = search_form.submit()

        self.assertContains(page, self.main_store.name)
        self.assertContains(page, self.other_store.name)

        stores = page.context[0].get('object_list')
        self.assertSequenceEqual(stores, [self.other_store, self.main_store])

    def test_can_be_filtered_by_store_group(self):
        north_group = StoreGroupFactory(name="North")
        south_group = StoreGroupFactory(name="South")

        self.main_store.group = south_group
        self.main_store.save()
        self.other_store.group = north_group
        self.other_store.save()

        page = self.get(reverse('stores:index'))
        search_form = page.forms['store-search']
        search_form['group'] = south_group.id
        page = search_form.submit()

        self.assertContains(page, self.main_store.name)

        stores = page.context[0].get('object_list')
        self.assertSequenceEqual(stores, [self.main_store])
