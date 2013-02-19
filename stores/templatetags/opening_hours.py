from django.template import Library, defaultfilters
from django.utils.translation import ugettext as _

register = Library()


@register.filter
def printable_period(period, arg=None):
    if not period.start and not period.end:
        return _("Closed")
    start = defaultfilters.time(period.start, arg)
    end = defaultfilters.time(period.end, arg)
    return period.PERIOD_FORMAT % {'start': start, 'end': end}


@register.filter
def printable_weekday(period):
    return period.WEEK_DAYS.get(period.weekday, _("Unknown weekday"))
