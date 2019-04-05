from django.utils.http import urlencode
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_add_param(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
