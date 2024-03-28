from django import template
from urllib.parse import urlparse
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils import timezone

register = template.Library()


@register.filter
def url_domain(value):
    parsed_url = urlparse(value)
    return parsed_url.netloc


@register.filter
def humanize_time_difference(value):
    print(now())
    return timesince(value, timezone.now()).split(", ")[0]


@register.filter
def calculate_time_difference(pub_date):
    time_difference = timezone.now() - pub_date
    return time_difference.total_seconds()
