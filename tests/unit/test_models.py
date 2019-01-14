from datetime import time

import pytest
from django.core.exceptions import ValidationError

from stores.models import OpeningPeriod

from ..factories import StoreFactory


@pytest.mark.django_db
def test_opening_period_clean_empty_start_and_end():
    store = StoreFactory(location='POINT(144.917908 -37.815751)')
    period = OpeningPeriod(store=store, weekday=1, start=None, end=None)
    # This should not raise a validation error
    period.clean()


@pytest.mark.django_db
def test_opening_period_clean_start_after_end():
    store = StoreFactory(location='POINT(144.917908 -37.815751)')
    period = OpeningPeriod(store=store, weekday=1, start=time(10, 0), end=time(7, 0))
    with pytest.raises(ValidationError):
        period.clean()


@pytest.mark.django_db
def test_opening_period_clean_valid():
    store = StoreFactory(location='POINT(144.917908 -37.815751)')
    period = OpeningPeriod(store=store, weekday=1, start=time(7, 0), end=time(10, 0))
    # This should not raise a validation error
    period.clean()
