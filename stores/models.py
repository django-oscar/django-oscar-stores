from django.db import models
#from django.contrib.gis.geos.point import Point
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.gis.db.models import PointField, GeoManager

from oscar.apps.address.abstract_models import AbstractAddress


class StoreAddress(AbstractAddress):
    store = models.OneToOneField(
        'stores.Store',
        verbose_name=_("Store"),
        related_name="address"
    )


class StoreGroup(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(StoreGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, null=True)

    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
    location = PointField(null=True, blank=True)

    image = models.ImageField(
        _("Image"),
        upload_to="images/stores",
        blank=True, null=True
    )
    description = models.CharField(
        _("Description"),
        max_length=2000,
        blank=True, null=True
    )

    group = models.ForeignKey(StoreGroup, related_name='stores',
                              name=_("Group"), null=True, blank=True)

    is_pickup_store = models.BooleanField(_("Is pickup store"), default=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    objects = GeoManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class OpeningPeriod(models.Model):
    store = models.ForeignKey('stores.Store', name=_("Store"),
                              related_name='opening_periods')

    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(1, 8)
    weekday_choices = (
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
        (SATURDAY, _("Saturday")),
        (SUNDAY, _("Sunday")),
    )
    weekday = models.PositiveIntegerField(_("Weekday"),
                                          choices=weekday_choices)
    start = models.TimeField(_("Start"))
    end = models.TimeField(_("End"))

    def __unicode__(self):
        return "%s: %s to %s" % (self.weekday, self.start, self.end)

    class Meta:
        ordering = ['weekday']
        verbose_name = _("Opening period")
        verbose_name_plural = _("Opening periods")


class OpeningPeriodOverride(models.Model):
    """
    Override the opening hours for a given date
    """
    store = models.ForeignKey(
        'stores.Store',
        name=_("Store"),
        related_name='opening_period_overrides'
    )

    name = models.CharField(_("Name"), max_length=100)
    date = models.DateField(_("Date"))
    start = models.TimeField(_("Start"))
    end = models.TimeField(_("End"))

    # Explain why normal hours are being overridden
    description = models.TextField(_("Description"))

    def __unicode__(self):
        return "%s: %s: %s to %s" % (self.name, self.weekday, self.start,
                                     self.end)

    class Meta:
        verbose_name = _("Opening period override")
        verbose_name_plural = _("Opening period overrides")


# To determine normal opening hours:
# 1. fetch all WeekdayOpeningPeriods ordered by weekday
# 2. fetch any OpeningHoursOverrides that occurs in the next x weeks
# 3. render this information

# To determine is a store is open at a given datetime:
# 1. look for override for date in question that covers datetime
# 2. if nothing, look for weekday opening for today
