# templatetags/contenttypes.py
from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def content_type_id(obj):
    return ContentType.objects.get_for_model(obj).id


@register.filter(name="get_model")
def get_model(obj):
    return ContentType.objects.get_for_model(obj).model


@register.filter(name="get_model_name")
def get_model_name(obj):
    return obj._meta.model_name
