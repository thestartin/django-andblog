import os

from django import template
from django.conf import settings


register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.field.initial.name)


@register.filter
def get_media_url(value):
    data = value.replace(settings.MEDIA_ROOT, '')
    return settings.MEDIA_URL + data


@register.filter
def is_more(value):
    return len(value) > settings.MAX_DESCRIPTION_LIST_SIZE

