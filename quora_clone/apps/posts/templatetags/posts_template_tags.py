from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_add_param(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return mark_safe(urlencode(query))
