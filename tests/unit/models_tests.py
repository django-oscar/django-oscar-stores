from django.test import TestCase
from django.core.exceptions import ValidationError
from oscar.core.loading import get_model
from tests.factories import OpeningPeriodFactory


OpeningPeriod = get_model('stores', 'OpeningPeriod')


class TestStoreModels(TestCase):

    def test_open_period_clean(self):
        period = OpeningPeriodFactory()
        self.assertEqual(period.end, None)
        self.assertEqual(period.start, None)
        # With null values can be cleaned
        period.clean()
        # End or start is Null raise ValidationError
        period.start = '08:00'
        with self.assertRaises(ValidationError):
            period.clean()
        # Both is not Null period is valid
        period.end = '13:00'
        period.clean()
        # start > end period is not valid
        period.start = '20:00'
        with self.assertRaises(ValidationError):
            period.clean()
