from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def url_domain(value):
    parsed_url = urlparse(value)
    return parsed_url.netloc