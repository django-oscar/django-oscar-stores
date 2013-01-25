from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import GeoManager

from oscar.apps.address.abstract_models import AbstractAddress

from stores.managers import StoreManager
from stores.utils import get_geodetic_srid


# Re-use Oscar's address model
class StoreAddress(AbstractAddress):
    store = models.OneToOneField(
        'stores.Store',
        verbose_name=_("Store"),
        related_name="address")

    class Meta:
        abstract = True

    @property
    def street(self):
        """
        Summary of the 3 line fields
        """
        return "\n".join(filter(bool, [self.line1, self.line2, self.line3]))


class StoreGroup(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(StoreGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, null=True)

    # Contact details
    manager_name = models.CharField(
        _('Manager name'), max_length=200, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)
    email = models.CharField(_('Email'), max_length=100, blank=True, null=True)

    reference = models.CharField(
        _("Reference"),
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        help_text=_("A reference number that uniquely identifies this store"))

    image = models.ImageField(
        _("Image"),
        upload_to="uploads/store-images",
        blank=True, null=True)
    description = models.CharField(
        _("Description"),
        max_length=2000,
        blank=True, null=True)
    location = PointField(
        _("Location"),
        srid=get_geodetic_srid(),
    )

    group = models.ForeignKey(
        'stores.StoreGroup',
        related_name='stores',
        verbose_name=_("Group"),
        null=True,
        blank=True)

    is_pickup_store = models.BooleanField(_("Is pickup store"), default=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    objects = StoreManager()

    class Meta:
        abstract = True
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stores:detail', kwargs={'slug': self.slug})


class OpeningPeriod(models.Model):
    PERIOD_FORMAT = _("%(start)s - %(end)s")
    (MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
     FRIDAY, SATURDAY, SUNDAY) = range(1, 8)
    WEEK_DAYS = {
        MONDAY: _("Monday"),
        TUESDAY: _("Tuesday"),
        WEDNESDAY: _("Wednesday"),
        THURSDAY: _("Thursday"),
        FRIDAY: _("Friday"),
        SATURDAY: _("Saturday"),
        SUNDAY: _("Sunday"),
    }
    store = models.ForeignKey('stores.Store', verbose_name=_("Store"),
                              related_name='opening_periods')

    weekday_choices = [(k, v) for k, v in WEEK_DAYS.items()]
    weekday = models.PositiveIntegerField(
        _("Weekday"),
        choices=weekday_choices)
    start = models.CharField(
        _("Start"),
        max_length=30,
        null=True,
        blank=True,
        help_text=_("Leaving start and end time empty is displayed as 'Closed'"))
    end = models.CharField(
        _("End"),
        max_length=30,
        null=True,
        blank=True,
        help_text=_("Leaving start and end time empty is displayed as 'Closed'"))

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
        abstract = True
        ordering = ['weekday']
        verbose_name = _("Opening period")
        verbose_name_plural = _("Opening periods")


class StoreStock(models.Model):
    store = models.ForeignKey(
        'stores.Store',
        verbose_name=_("Store"),
        related_name='stock')
    product = models.ForeignKey(
        'catalogue.Product',
        verbose_name=_("Product"),
        related_name="store_stock")
    # Stock level information
    num_in_stock = models.PositiveIntegerField(
        _("Number in stock"),
        default=0,
        blank=True,
        null=True)

    # The amount of stock allocated in store but not fed back to the master
    num_allocated = models.IntegerField(
        _("Number allocated"),
        default=0,
        blank=True,
        null=True)

    location = models.CharField(
        _("In store location"),
        max_length=50,
        blank=True,
        null=True)

    # Date information
    date_created = models.DateTimeField(
        _("Date Created"),
        auto_now_add=True)
    date_updated = models.DateTimeField(
        _("Date Updated"),
        auto_now=True,
        db_index=True)

    class Meta:
        abstract = True
        verbose_name = _("Store Stock Record")
        verbose_name_plural = _("Store Stock Records")

    objects = GeoManager()

    def __unicode__(self):
        if self.store and self.product:
            return "%s @ %s" % (self.product.title, self.store.name)
        return "Store Stock"

    @property
    def is_available_to_buy(self):
        return self.num_in_stock > self.num_allocated
