from django import template
from urllib.parse import urlparse
from django.utils.timesince import timesince
from django.utils.timezone import now

register = template.Library()

@register.filter
def url_domain(value):
    parsed_url = urlparse(value)
    return parsed_url.netloc

@register.filter
def humanize_time_difference(value):
    return timesince(value, now()).split(", ")[0]