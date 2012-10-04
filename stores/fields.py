from decimal import Decimal as D

from django.db import models
from django.conf import settings
from django.core import exceptions


class Point(object):

    def __init__(self, x, y=None):
        """
        The Point object may be initialized with either a tuple, or individual
        parameters.

        For Example:
        >>> p = Point((5, 23)) # 2D point, passed in as a tuple
        """
        if isinstance(x, (tuple, list)):
            # Here a tuple or list was passed in under the `x` parameter.
            ndim = len(x)
            coords = x
        elif isinstance(x, (int, long, float, D)) and isinstance(y, (int, long, float, D)):
            # Here X, Y, and (optionally) Z were passed in individually, as parameters.
            ndim = 2
            coords = [x, y]
        else:
            raise TypeError('Invalid parameters given for Point initialization.')

        if ndim != 2:
            raise TypeError('Invalid point dimension: %s' % str(ndim))

        self.x = self._validate_geo_range(coords[0], 90)  # this is latitude
        self.y = self._validate_geo_range(coords[1], 180)  # this is longitude
        self.ndim = ndim

    def _validate_geo_range(self, geo_part, range_val):
        try:
            geo_part = D(geo_part)
            if abs(geo_part) > range_val:
                raise exceptions.ValidationError(
                'Must be between -%s and %s; received %s' % (range_val, range_val, geo_part)
            )
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                'Expected float, received %s (a %s).' % (geo_part, typename(geo_part))
            )
        return geo_part

    def __iter__(self):
        """
        Allows iteration over coordinates of this Point.
        """
        for coord in self.coords:
            yield coord

    def __len__(self):
        """
        Returns the number of dimensions for this Point.
        """
        return self.ndim

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):
        return "Point(%s, %s)" % self.coords

    @property
    def coords(self):
        """
        Returns a tuple of the point.
        """
        return (self.x, self.y)

    @coords.setter
    def coords(self, value):
        """
        Sets the coordinates of the point with the given tuple.
        """
        self.x, self.y = D(value[0]), D(value[1])


class PointField(models.CharField):
    description = "A field representing a geographical point in latitude and longitude."
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.delimiter = u','
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 150
        super(PointField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, Point):
            return value
        return Point(value.split(self.delimiter))

    def get_prep_lookup(self, lookup_type, value):
        # We only handle 'exact' and 'in'. All others are errors.
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def get_prep_value(self, value):
        if not value:
            return
        assert(isinstance(value, Point))
        return self.delimiter.join([unicode(v) for v in value.coords])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


# TODO: Is this the best way of doing this or should it be 
# handled with either a setting such as 'STORES_USE_GEODJANGO' which
# is more explicit, or should we check for the database engine that
# is used. The latter, however, has the problem that it might be tricky
# to work out which engine is actually used when complex routing is in 
# place and when third-party DB backends are used.
if "django.contrib.gis" in getattr(settings, 'INSTALLED_APPS', []):
    from django.contrib.gis.db.models import PointField
    from django.contrib.gis.geos.point import Point

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^stores\.fields\.PointField"])
except ImportError:
    pass
