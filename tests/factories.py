import factory
from oscar.core.loading import get_model
from oscar.test.factories import CountryFactory


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_model('stores', 'Store')


class StoreAddressFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = get_model('stores', 'StoreAddress')


class StoreGroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_model('stores', 'StoreGroup')


class StoreStockFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_model('stores', 'StoreStock')
