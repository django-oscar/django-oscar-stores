from django.db import models
#from django.contrib.gis.geos.point import Point
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.gis.db.models import PointField

from oscar.apps.address.abstract_models import AbstractAddress

from stores.managers import StoreManager


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


class StoreContact(models.Model):
    manager_name = models.CharField(_('Manager name'), max_length=200,
                                    blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
    email = models.CharField(_('Email'), max_length=100, blank=True, null=True)

    store = models.OneToOneField('stores.Store', name=_("Store"),
                                 related_name="contact_details")

    def __unicode__(self):
        if self.store:
            return "Contact details for %s" % self.store.name
        return "Store contacts #%s" % self.id


class Store(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, null=True)

    reference = models.CharField(
        _("Reference"), max_length=32, unique=True, null=True, blank=True,
        help_text=_("A reference number that uniquely identifies this store"))

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

    location = PointField(_("Location"), null=True, blank=True)

    group = models.ForeignKey('stores.StoreGroup', related_name='stores',
                              name=_("Group"), null=True, blank=True)

    is_pickup_store = models.BooleanField(_("Is pickup store"), default=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    objects = StoreManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class OpeningPeriod(models.Model):
    PERIOD_FORMAT = _("%(start)s - %(end)s")
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(1, 8)
    WEEK_DAYS = {
        MONDAY: _("Monday"),
        TUESDAY: _("Tuesday"),
        WEDNESDAY: _("Wednesday"),
        THURSDAY: _("Thursday"),
        FRIDAY: _("Friday"),
        SATURDAY: _("Saturday"),
        SUNDAY: _("Sunday"),
    }
    store = models.ForeignKey('stores.Store', name=_("Store"),
                              related_name='opening_periods')

    weekday_choices = [(k, v) for k, v in WEEK_DAYS.items()]
    weekday = models.PositiveIntegerField(_("Weekday"),
                                          choices=weekday_choices)
    start = models.CharField(
        _("Start"), max_length=30, null=True, blank=True,
        help_text=_("Leaving start and end time empty is displayed as 'Closed'")
    )
    end = models.CharField(
        _("End"), max_length=30, null=True, blank=True,
        help_text=_("Leaving start and end time empty is displayed as 'Closed'")
    )

    @property
    def printable_weekday(self):
        return self.WEEK_DAYS.get(self.weekday, _("Unknown weekday"))

    @property
    def printable_period(self):
        if not self.start and not self.end:
            return _("Closed")
        return self.PERIOD_FORMAT % {'start': self.start, 'end': self.end}

    def __unicode__(self):
        return "%s: %s to %s" % (self.weekday, self.start, self.end)

    class Meta:
        ordering = ['weekday']
        verbose_name = _("Opening period")
        verbose_name_plural = _("Opening periods")
