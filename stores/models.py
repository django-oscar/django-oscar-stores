from django.db import models
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from model_utils.managers import PassThroughManager


class StoreGroup(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(StoreGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class StoreQuerySet(models.query.QuerySet):

    def pickup_stores(self):
        return self.filter(is_pickup_store=True, is_active=True)


class Store(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True, null=True)

    line1 = models.CharField(_("First line of address"), max_length=255)
    line2 = models.CharField(
        _("Second line of address"),
        max_length=255,
        blank=True,
        null=True
    )
    city = models.CharField(_('City'), max_length=255)
    postcode = models.CharField(_('Post Code'), max_length=4)
    country = models.ForeignKey('address.Country', verbose_name=_("Country"))
    state = models.CharField(_("State/County"), max_length=255)

    phone = models.CharField(_('Phone'), max_length=20, blank=True, null=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

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

    group = models.ForeignKey(StoreGroup, related_name='stores', null=True, blank=True)

    is_pickup_store = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = PassThroughManager.for_queryset_class(StoreQuerySet)()

    def get_shipping_data(self):
        return {
            'line1': self.name,
            'line2': self.line1,
            'line3': self.line2,
            'line4': self.city,
            'postcode': self.postcode,
            'country': self.country,
            'state': self.state,
        }

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class OpeningTime(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Description"))
    time = models.CharField(max_length=100)

    # Use display_order to determine the order of times
    display_order = models.PositiveIntegerField(_("Display Order"), default=0,
            help_text=_("""An image with a display order of
                        zero will be the primary image for a product"""))

    store = models.ForeignKey('stores.Store', related_name='opening_times')

    def __unicode__(self):
        return _("%s opened %s: %s") % (self.store.name, self.title, self.time)

    class Meta:
        ordering = ["display_order"]
